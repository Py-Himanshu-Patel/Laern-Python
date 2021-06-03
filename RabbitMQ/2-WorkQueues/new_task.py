import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# channel.queue_declare(queue="hello")
channel.queue_declare(queue="task_queue", durable=True)

message = " ".join(sys.argv[1:]) or "Hello World!"
# channel.basic_publish(exchange="", routing_key="hello", body=message)
channel.basic_publish(
    exchange="",
    routing_key="task_queue",
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=2,  # make message persistent
    ),
)
print(f" [x] Sent {message}")

connection.close()
