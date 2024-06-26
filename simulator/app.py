import os
import datetime as datetime
import pika
import random
import time
import json
from dotenv import load_dotenv
from multiprocessing import Process

load_dotenv()
HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))  # Ensure that the port is an integer

try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST, port=PORT))
    channel = connection.channel()

    # Declare the queue 
    channel.queue_declare(queue='ess_queue')

    def simulate_meter(min_val, max_val, data_source, delay):
        while True:
            value = round(random.uniform(min_val, max_val), 1)
            message = {"value": value, "timestamp": datetime.datetime.now().isoformat(), "data_source": data_source}
            channel.basic_publish(exchange='', routing_key='ess_queue', body=json.dumps(message))
            print(f" [x] Sent {data_source}, {message}")
            time.sleep(delay)

    process1 = Process(target=simulate_meter, args=(-100.0, 100.0, "battery", 1))
    process2 = Process(target=simulate_meter, args=(-250.0, -150.0, 'site', 10))

    process1.start()
    process2.start()

    process1.join()
    process2.join()

    connection.close()
except Exception as e:
    print(f"An error occurred: {str(e)}")

    