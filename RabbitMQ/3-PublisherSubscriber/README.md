# Publish / Subscribe (Sending messages to many consumers at once)

Now we'll deliver a message to multiple consumers. This pattern is known as "publish/subscribe".

To illustrate the pattern, we're going to build a simple logging system. It will consist of two programs -- the first will emit log messages and the second will receive and print them.

In our logging system every running copy of the receiver program will get the messages. That way we'll be able to run one receiver and direct the logs to disk; and at the same time we'll be able to run another receiver and see the logs on the screen.

Essentially, published log messages are going to be broadcast to all the receivers.

The core idea in the messaging model in RabbitMQ is that the producer never sends any messages directly to a queue. Actually, quite often the producer doesn't even know if a message will be delivered to any queue at all.

Instead, the producer can only send messages to an exchange. An exchange is a very simple thing. On one side it receives messages from producers and the other side it pushes them to queues. The exchange must know exactly what to do with a message it receives. Should it be appended to a particular queue? Should it be appended to many queues? Or should it get discarded. The rules for that are defined by the exchange type.

There are a few exchange types available: `direct`, `topic`, `headers` and `fanout`. We'll focus on the last one -- `the fanout`. Let's create an exchange of that type, and call it `logs`:

The `fanout` exchange is very simple. As you can probably guess from the name, it just broadcasts all the messages it receives to all the queues it knows. And that's exactly what we need for our logger.

```python
channel.exchange_declare(exchange='logs', exchange_type='fanout')
```

#### The default exchange

In previous parts of the tutorial we knew nothing about exchanges, but still were able to send messages to queues. That was possible because we were using a default exchange, which we identify by the empty string ("").

```python
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=message)
```

The `exchange` parameter is the name of the exchange. The empty string denotes the default or nameless exchange: messages are routed to the queue with the name specified by `routing_key`, if it exists. Now, we can publish to our named exchange instead:

```python
channel.basic_publish(exchange='logs',
                      routing_key='',
                      body=message)
```

## Temporary queues

Giving a queue a name is important when you want to share the queue between producers and consumers. But that's not the case for our logger. We want to hear about all log messages, not just a subset of them. We're also interested only in currently flowing messages not in the old ones. To solve that we need two things.

- Firstly, whenever we connect to Rabbit we need a fresh, empty queue. To do it we could create a queue with a random name, or, even better - let the server choose a random queue name for us. We can do this by supplying empty queue parameter to `queue_declare`:

```python
result = channel.queue_declare(queue='')
```

- Secondly, once the consumer connection is closed, the queue should be deleted. There's an `exclusive` flag for that:

```python
result = channel.queue_declare(queue='', exclusive=True)
```

At this point `result.method.queue` contains a random queue name. For example it may look like `amq.gen-JzTY20BRgKO-HjmUJj0wLg`.

## Bindings

We've already created a **fanout exchange** and a **queue**. Now we need to tell the exchange to send messages to our queue. That relationship between exchange and a queue is called a `binding`.

```python
channel.queue_bind(exchange='logs', queue=result.method.queue)
```

From now on the `logs` exchange will append messages to our queue.

## Putting it all together

The producer program, which emits log messages. The most important change is that we now want to publish messages to our `logs` exchange instead of the nameless one. We need to supply a `routing_key` when sending, but its value is ignored for `fanout` exchanges.

```python
import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)
channel = connection.channel()

# declare fanout exchange for logger
channel.exchange_declare(exachange='logs', exchange_type="fanout")

message = ''.join(sys.argv[1:]) or "Info: Hello World"

# publish the messsage to exchange without specifing any queue
channel.basic_publish(exchange='logs', routing_key="", body=message)

print(" [x] Sent %r" % message)
connection.close()
```

As you see, after establishing the connection we declared the exchange. This step is necessary as **publishing to a non-existing exchange is forbidden**. The messages will be lost if no queue is bound to the exchange yet, but that's okay for us; if no consumer is listening yet we can safely discard the message.

### Emitter

```python
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
```

### Receiver

```python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

# declare an fanout exchange
channel.exchange_declare(exchange="logs", exchange_type="fanout")
# declare queue
result = channel.queue_declare(queue="", exclusive=True)
queue_name = result.method.queue
# bind the queue to logs exchange
channel.queue_bind(exchange="logs", queue=queue_name)

print(" [*] Waiting for logs. To exit press CTRL+C")


def callback(ch, method, properties, body):
    print(" [x] %r" % body)

# bind consumer to queue
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()
```

If you want to save logs to a file, just open a console and type. Also data in logger appears after we close the shell/consumer.

```bash
python receive_logs.py > logs_from_rabbit.log
```

If you wish to see the logs on your screen, spawn a new terminal and run:

```bash
python receive_logs.py
```

And of course, to emit logs type:

```bash
python emit_log.py TextHere
```

Using `rabbitmqctl` list_bindings you can verify that the code actually creates bindings and queues as we want. With two `receive_logs.py` programs running you should see something like:

```bash
sudo rabbitmqctl list_bindings
=> Listing bindings ...
=> logs    exchange        amq.gen-JzTY20BRgKO-HjmUJj0wLg  queue           []
=> logs    exchange        amq.gen-vso0PVvyiRIL2WoV3i48Yg  queue           []
=> ...done.
```

The interpretation of the result is straightforward: data from exchange `logs` goes to two queues with server-assigned names. And that's exactly what we intended.
