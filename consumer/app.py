import os
import pika
import json
from decimal import Decimal
from datetime import datetime
from dotenv import load_dotenv
import psycopg2

load_dotenv()
site_load = 0

HOST = os.getenv("HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT")
POSTGRES_DB_NAME = os.getenv("POSTGRES_DB_NAME")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")


def add_to_database(load_sum, battery_load, site_load):
    conn = psycopg2.connect(
        host=HOST,
        port=POSTGRES_PORT,
        dbname=POSTGRES_DB_NAME,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )
    cur = conn.cursor()

    timestamp = datetime.now().isoformat()
    insert_query = """
        INSERT INTO ess (timestamp, load_sum, battery_load, site_load)
        VALUES (%s, %s, %s, %s)
    """
    data = (timestamp, Decimal(str(load_sum)), Decimal(str(battery_load)), Decimal(str(site_load)))

    cur.execute(insert_query, data)
    conn.commit()

    cur.close()
    conn.close()


def callback(ch, method, properties, body):
    global site_load
    try:
        data = json.loads(body)
        data_source = data["data_source"]
        value = data["value"]
        if data_source == "site":
            site_load = value
        elif data_source == "battery":
            load_sum = value + site_load
            add_to_database(load_sum, value, site_load)
            print(f" [x] Added to DynamoDB")
            site_load = 0
    except Exception as e:
        print(f" [x] Error: {str(e)}")



connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST, port=RABBITMQ_PORT))
channel = connection.channel()

channel.queue_declare(queue='ess_queue')

channel.basic_consume(queue='ess_queue', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()