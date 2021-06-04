import pika
import sys

connection = pika.BlockingConnection(
	pika.ConnectionParameters(host='localhost')
)
channel = connection.channel()

# declare fanout exchange for logger
# publishing to a non-existing exchange is forbidden
channel.exchange_declare(exchange='logs', exchange_type="fanout")

message = ''.join(sys.argv[1:]) or "Info: Hello World"

# publish the messsage to exchange without specifing any queue 
# publisher knows just about exchange and nothing about any queue
channel.basic_publish(exchange='logs', routing_key="", body=message)

print(" [x] Sent %r" % message)
connection.close()
