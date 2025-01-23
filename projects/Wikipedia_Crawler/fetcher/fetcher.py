import os
import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import pika 
import logging
from pymongo import MongoClient
from datetime import datetime

class Fetcher:
    
    def __init__(self, rabbitmq_uri, mongo_uri, storage_dir="./storage/html_files"):
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)    

        # Rabbitmq setup
        self.rabbitmq_uri = rabbitmq_uri
        self.rabbitmq_connection = pika.BlockingConnection(pika.URLParameters(self.rabbitmq_uri))
        self.channel = self.rabbitmq_connection.channel()
        self.channel.queue_declare(queue="fetcher_queue", durable=True)
        self.channel.queue_declare(queue="parser_queue", durable=True)

        #TODO: Maybe create a service that will add the first url and active all the message_queues
        self.channel.basic_publish(exchange='',  
            routing_key='fetcher_queue',  
            body="https://en.wikipedia.org/wiki/Distributed_systems",  
            properties=pika.BasicProperties(
                delivery_mode=2  # Make the message persistent
            ))
        
        # MongoDB setup 
        self.mongo_client = MongoClient(mongo_uri)
        self.db = self.mongo_client["wikipedia_crawler"]
        self.collection = self.db["urls_metadata"]
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("Fetcher initialized successfully.")
    
    
    
    def process_url(self, url):
        try:
            self.logger.info(f"Processing URL: {url}")
            response = self.fetch_page(url)
            if not response:
                self.logger.error(f"Failed to fetch page: {url}")
                return False
            
            file_path = self.save_page_local(url, response.text)
            
            last_edited = self.get_last_edited_time(response.text)
            self.save_to_db(url, file_path, last_edited)
            
            links = self.extract_links(response.text, url)
            self.logger.info(f"Extracted {len(links)} links from the page.")
            self.send_to_parser_queue(links)
        
            return True 
        
        except Exception as e:
            self.logger.error(f"Error processing URL {url}: {e}")
            return False  

    def fetch_page(self, url):
        try: 
            response = requests.get(url)
            response.raise_for_status()
            self.logger.info(f"Fetched page: {url}")
            return response
        
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching {url}: {e}")
            return None

    
    def save_page_local(self, url, html_content):
        file_name = f"{url.split('/')[-1]}.html"
        file_path = os.path.join(self.storage_dir, file_name)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(html_content)

        self.logger.info(f"Saved page to: {file_path}")
        return file_path
          
            
    def send_to_parser_queue(self, links):
        try:
            for link in links:
                self.channel.basic_publish(
                    exchange='',
                    routing_key='parser_queue',  
                    body=link,
                    properties=pika.BasicProperties(
                        delivery_mode=2  # Make the message persistent
                    )
                )
            self.logger.info(f"Sent {len(links)} links to the parser queue.")
        except Exception as e:
            self.logger.error(f"Error sending links to parser queue: {e}")
       
       
    # Extract the links from specific html page
    def extract_links(self, html_content, base_url):
        soup = bs(html_content, "html.parser")
        links = [urljoin(base_url, a["href"]) for a in soup.find_all("a", href=True)]
        return links

    
    # Get when was the last time a page was edited
    def get_last_edited_time(self, html_content):
        soup = bs(html_content, "html.parser")
        try:
            last_edited_element = soup.select_one("li#footer-info-lastmod")
            if last_edited_element:
                    text = last_edited_element.text.strip()
                    date_str = text.split("on ")[1].split(",")[0]  # Extract date part
                    date_obj = datetime.strptime(date_str, "%d %B %Y")
                    return date_obj
            else:
                return None
        except Exception as e:
            self.logger.error(f"Error extracting 'last edited' date: {e}")
            return None
        
        
    # save the url and metadata in the db
    def save_to_db(self, url, local_file_path, last_edited_time):
        try:
            existing_record = self.collection.find_one({"url": url})
            if existing_record:
                self.collection.update_one(
                        {"url": url},
                        {"$set": {
                            "local_path": local_file_path,
                            "metadata.last_edited": last_edited_time
                        }}
                    )
                self.logger.info(f"Updated metadata for URL: {url}")
                
            else:
                self.collection.insert_one({
                    "url": url,
                    "local_path": local_file_path,
                    "metadata": {
                        "last_edited": last_edited_time
                    }
                })
                self.logger.info(f"Inserted metadata for URL: {url}")
                
        except Exception as e:
            self.logger.error(f"Error saving metadata to MongoDB: {e}")


    def consume_url(self):
        def callback(ch, method, properties, body):
            url = body.decode().strip()
            self.logger.info(f"Received URL: {url}")
            try:
                success = self.process_url(url)
                if success:
                    ch.basic_ack(delivery_tag=method.delivery_tag)  
                else:
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
            except Exception as e:
                self.logger.error(f"Error processing URL: {e}")
            
        self.logger.info("Waiting for messages. To exit, press CTRL+C")
        self.channel.basic_consume(queue="fetcher_queue", on_message_callback=callback, auto_ack=False)
        self.channel.start_consuming()

    
    
    def cleanup(self):
        self.logger.info("Closing RabbitMQ connection.")
        self.rabbitmq_connection.close()
        self.logger.info("Closing MongoDB connection.")
        self.mongo_client.close()
    
    
    
if __name__ == "__main__":
    
    rabbitmq_uri = os.getenv("RABBITMQ_URI")
    mongodb_uri = os.getenv("MONGO_URI")
    
    try:
        fetcher = Fetcher(rabbitmq_uri, mongodb_uri)
        fetcher.consume_url()
    except KeyboardInterrupt:
        fetcher.logger.info("Interrupted by user.")
        fetcher.cleanup()
            
    #extracted_links = fetcher.fetch_and_save(initial_url)
        """   fetcher.consume_url()
        print("\nExtracted Links:")
        for link in extracted_links:
            print(link) """