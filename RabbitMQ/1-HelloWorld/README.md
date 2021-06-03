# Introduction

RabbitMQ is a message broker: it accepts and forwards messages.

- **Producing**: means nothing more than sending. A program that sends messages is a producer.
- **Queue**: Although messages flow through RabbitMQ and your applications, they can only be stored inside a queue. A queue is only bound by the host's memory & disk limits, it's essentially a large message buffer. Many producers can send messages that go to one queue, and many consumers can try to receive data from one queue. This is how we represent a queue.
- **Consuming** has a similar meaning to receiving. A **consumer** is a program that mostly waits to receive messages.

Producer, consumer, and broker do not have to reside on the same host; indeed in most applications they don't. An application can be both a producer and consumer, too.

RabbitMQ speaks multiple protocols. This tutorial uses **AMQP** (Async Messaging Queue Protocol)

## Sending

```python
# send.py

# Python client recommended by the RabbitMQ team
import pika

# The first thing we need to do is to establish a connection with RabbitMQ server.
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
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
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')

# print(" [x] Sent 'Hello World!'")

# Before exiting the program we need to make sure the network buffers were 
# flushed and our message was actually delivered to RabbitMQ. We can do it 
# by gently closing the connection
connection.close()
```

## Receiving

```python
# receive.py

import pika
import sys
import os


def main():
    # first we need to connect to RabbitMQ server.
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    # The next step, just like before, is to make sure that the queue exists.
    # Creating a queue using queue_declare is idempotent ‒ we can run the command
    # as many times as we like, and only one will be created.

    channel.queue_declare(queue="hello")

    # You may ask why we declare the queue again ‒ we have already declared it in
    # our previous code. We could avoid that if we were sure that the queue already
    # exists. For example if send.py program was run before. But we're not yet sure
    # which program to run first. In such cases it's a good practice to repeat
    # declaring the queue in both programs.

    # Receiving messages from the queue is more complex. It works by subscribing a
    # callback function to a queue. Whenever we receive a message, this callback
    # function is called by the Pika library. In our case this function will print
    # on the screen the contents of the message.

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    # Next, we need to tell RabbitMQ that this particular callback function should
    # receive messages from our hello queue

    channel.basic_consume(queue="hello", auto_ack=True, on_message_callback=callback)

    # For that command to succeed we must be sure that a queue which we want to subscribe
    # to exists. Fortunately we're confident about that ‒ we've created a queue above
    # ‒ using queue_declare.

    # And finally, we enter a never-ending loop that waits for data and runs callbacks
    # whenever necessary, and catch KeyboardInterrupt during program shutdown.

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
```

## Executing

First, let's start a consumer, which will run continuously waiting for deliveries:

```bash
# python receive.py

 => [*] Waiting for messages. To exit press CTRL+C
 => [x] Received 'Hello World!'
```

Now start the producer. The producer program will stop after every run:

```bash
# python send.py
 => [x] Sent 'Hello World!'
```
