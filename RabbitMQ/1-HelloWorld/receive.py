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
