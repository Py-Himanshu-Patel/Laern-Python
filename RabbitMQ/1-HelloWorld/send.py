# Python client recommended by the RabbitMQ team
import pika

# The first thing we need to do is to establish a connection with RabbitMQ server.
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# We're connected now, to a broker on the local machine - hence the localhost.
# If we wanted to connect to a broker on a different machine we'd simply
# specify its name or IP address here.

# If we send a message to non-existing location, RabbitMQ will just drop the
# message. Let's create a hello queue to which the message will be delivered
channel.queue_declare(queue="hello")

# All we need to know now is how to use a default exchange identified by an
# empty string. This exchange is special ‒ it allows us to specify exactly
# to which queue the message should go. The queue name needs to be specified
# in the routing_key parameter
channel.basic_publish(exchange="", routing_key="hello", body="Hello World!")

print(" [x] Sent 'Hello World!'")

# Before exiting the program we need to make sure the network buffers were
# flushed and our message was actually delivered to RabbitMQ. We can do it
# by gently closing the connection
connection.close()
