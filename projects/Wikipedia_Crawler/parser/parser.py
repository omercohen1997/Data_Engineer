import os
from urllib.parse import urlparse, urlunparse
import pika 
import logging


class Parser:
    
    def __init__(self, rabbitmq_uri):
        
        self.rabbitmq_connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_uri))
        self.channel = self.rabbitmq_connection.channel()
        self.channel.queue_declare(queue="parser_queue", durable=True)
        self.channel.queue_declare(queue="filter_queue", durable=True)

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("Parser initialized successfully.")


    def send_to_filter_queue(self, url):
        try:
            self.channel.basic_publish(
                exchange='', routing_key="filter_queue", 
                body=url,
                properties=pika.BasicProperties(delivery_mode=2)
            )
            self.logger.info(f"Sent link to filter queue: {url}")
        except Exception as e:
            self.logger.error(f"Error sending link to filter queue: {e}")
        
        
    def sanitize_link(self, url):
        parsed = urlparse(url)
        return urlunparse(parsed._replace(fragment=""))
    

    def is_valid_wikipedia_link(self, url):
        parsed = urlparse(url)
        return "en.wikipedia.org" in parsed.netloc and parsed.path.startswith("/wiki/")
    
        
    def process_url(self, ch, method, properties, body):
        try:
            url = body.decode()
            self.logger.info(f"Received URL: {url}")
            
            is_valid_link = self.is_valid_wikipedia_link(url)
            if is_valid_link:
                sanitized_link = self.sanitize_link(url)
                self.send_to_filter_queue(sanitized_link)
            else:
                self.logger.info(f"Ignored non-Wikipedia link: {url}")
                
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            self.logger.error(f"Error processing URL: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            
            
    def start_consuming(self):
        try:
            self.channel.basic_consume(
                queue="parser_queue",
                on_message_callback=self.process_url,
                auto_ack=False
            )
            self.logger.info("Started consuming from parser queue.")
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.logger.info("Interrupted by user.")
        except Exception as e:
            self.logger.error(f"Error during consuming: {e}")
        finally:
            self.cleanup()
        
    
    def cleanup(self):
        self.rabbitmq_connection.close()
        self.logger.info("Closing RabbitMQ connection.")
        
        
        
if __name__ == "__main__":
    rabbitmq_uri = os.getenv("RABBITMQ_URI", "amqp://guest:guest@localhost:5672/")
    parser = Parser(rabbitmq_uri)

    try:
        parser.start_consuming()
    except KeyboardInterrupt:
        parser.logger.info("Shutting down.")
        parser.cleanup()