import random
import pika
import datetime as datetime

def lambda_handler(event, context):
    try:
        # Generate random values
        current_value = round(random.uniform(-100.0, 100.0), 1)

        # Get current timestamp
        timestamp = datetime.datetime.now().isoformat()

        data_source = 'battery'

        # Connect to RabbitMQ on localstack
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='host.docker.internal', port=5672))
        channel = connection.channel()

        # Declare the queue 
        channel.queue_declare(queue='ess_queue')

        message = f'Timestamp: {timestamp}, DataSource: {data_source}, Value:{current_value}'

        channel.basic_publish(exchange='', routing_key='ess_queue', body=message)

        connection.close()

        return {
            'statusCode': 200,
            'body': 'Battery value sent to RabbitMQ'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }
