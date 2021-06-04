import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

# make a topic exchange
channel.exchange_declare(exchange="topic_logs", exchange_type="topic")
# get the command line input
routing_key = sys.argv[1] if len(sys.argv) > 2 else "anonymous.info"
# get message from command line input
message = " ".join(sys.argv[2:]) or "Hello World!"

# publish the log on a particular topic and povide it in routing_key
channel.basic_publish(exchange="topic_logs", routing_key=routing_key, body=message)

print(" [x] Sent %r:%r" % (routing_key, message))
connection.close()
