import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

# declare the exchange
channel.exchange_declare(exchange="direct_logs", exchange_type="direct")

# get the message and severity from command line args
severity = sys.argv[1] if len(sys.argv) > 1 else "info"
message = " ".join(sys.argv[2:]) or "Hello World"

# specify the direct exchange which we delared now
# specify the routing key as per severity this will direct logs to specific queue
channel.basic_publish(exchange="direct_logs", routing_key=severity, body=message)

print(" [x] Sent %r:%r" % (severity, message))
connection.close()
