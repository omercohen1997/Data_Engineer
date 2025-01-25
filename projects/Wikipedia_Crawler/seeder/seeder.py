import os
import pika
import logging

def seed_queue(rabbitmq_uri, queue_name, initial_url):
    try:
        connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_uri))
        channel = connection.channel()

        channel.queue_declare(queue=queue_name, durable=True)

        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=initial_url,
            properties=pika.BasicProperties(
                delivery_mode=2 
            )
        )
        
        logging.info(f"Seeded {initial_url} into {queue_name} queue.")
        connection.close()

    except Exception as e:
        logging.error(f"Error seeding queue: {e}")


if __name__ == "__main__":

    RABBITMQ_URI = os.getenv("RABBITMQ_URI", "amqp://guest:guest@localhost:5672/")
    QUEUE_NAME = "fetcher_queue"
    INITIAL_URL = "https://en.wikipedia.org/wiki/Distributed_systems"  

    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    seed_queue(RABBITMQ_URI, QUEUE_NAME, INITIAL_URL)

