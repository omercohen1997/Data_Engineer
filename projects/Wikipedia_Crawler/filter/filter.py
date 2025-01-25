import os
import pika 
import logging
import redis

class Filter:
    def __init__(self, rabbitmq_uri, redis_uri):
        self.rabbitmq_connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_uri))
        self.channel = self.rabbitmq_connection.channel()
        self.channel.queue_declare(queue="filter_queue", durable=True)
        self.channel.queue_declare(queue="fetcher_queue", durable=True)
        
        self.redis_client = redis.Redis.from_url(redis_uri, decode_responses=True)
        
        
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("Filter initialized successfully.")
        
        
    def is_url_visited(self, url):
        return self.redis_client.sismember("visited_urls", url)
        
        
    def mark_url_as_visited(self, url):    
        self.redis_client.sadd("visited_urls", url)
        self.logger.info(f"Added URL to redis: {url}")
        
    def send_to_fetcher_queue(self, url):
        try:
            self.channel.basic_publish(
                exchange='', routing_key="fetcher_queue",
                body=url,
                properties=pika.BasicProperties(delivery_mode=2)
            )
            self.logger.info(f"Sent link to fetcher queue: {url}")
        except Exception as e:
            self.logger.error(f"Error sending link to fetcher queue: {e}")

        
    def process_url(self, ch, method, properties, body):
        try:
            url = body.decode()
            self.logger.info(f"Received URL: {url}")

            if not self.is_url_visited(url):
                self.mark_url_as_visited(url)
                self.send_to_fetcher_queue(url)
            else:
                self.logger.info(f"URL already visited: {url}")

            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            self.logger.error(f"Error processing URL: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            
            
    def start_consuming(self):
        try:
            self.channel.basic_consume(
                queue="filter_queue",
                on_message_callback=self.process_url,
                auto_ack=False
            )
            self.logger.info("Started consuming from filter queue.")
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
        self.redis_client.close()
        self.logger.info("Closing Redis connection.")
        
        
        
if __name__ == "__main__":
    rabbitmq_uri = os.getenv("RABBITMQ_URI", "amqp://guest:guest@localhost:5672/")
    redis_uri = os.getenv("REDIS_URI", "redis://localhost:6379/0")

    filter = Filter(rabbitmq_uri, redis_uri)

    try:
        filter.start_consuming()
    except KeyboardInterrupt:
        filter.logger.info("Shutting down.")
        filter.cleanup()