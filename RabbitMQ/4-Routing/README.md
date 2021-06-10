# Routing (Receiving messages selectively)

We're going to modify previous Pub/Sub model to make it possible to subscribe only to a subset of the messages. For example, we will be able to direct only critical error messages to the log file (to save disk space), while still being able to print all of the log messages on the console.

## Bindings

In previous examples we were already creating bindings. You may recall code like:

```python
channel.queue_bind(exchange=exchange_name, queue=queue_name)
```

A binding is a relationship between an exchange and a queue. This can be simply read as: **the queue is interested in messages from this exchange**.

Bindings can take an extra `outing_key` parameter. To avoid the confusion with a `basic_publish` parameter we're going to call it a `binding key`. This is how we could create a binding with a key:

```python
channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key='black')
```

The **meaning of a binding key depends on the exchange type**. The `fanout` exchanges, which we used previously, simply ignored its value.

## Direct exchange

We were using a `fanout` exchange, which doesn't give us too much flexibility - it's only capable of mindless broadcasting.

We will use a `direct` exchange instead. The routing algorithm behind a `direct` exchange is simple - **a message goes to the queues whose binding key exactly matches the routing key of the message**.
It is perfectly legal to bind multiple queues with the same binding key. In that case, the direct exchange will behave like fanout and will broadcast the message to all the matching queues.

Each message send by emitter contains a `routing_key`, also each queue is binded to exchange via a `routing_key` (`binding key` here). Thus messsage get transferred to all those queues where `routing_key` of message meet is same as `routing_key` (`binding key`) of queue.

## Multiple bindings

It is perfectly legal to bind multiple queues with the same binding key. In that case, the direct exchange will behave like fanout and will broadcast the message to all the matching queues.

## Emitting logs

Instead of fanout we'll send messages to a direct exchange. We will supply the log severity as a routing key. That way the receiving script will be able to select the severity it wants to receive. Like always we need to create an exchange first and then the queue

```python
# exchange
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')
```

```python
# send message to respective routing key
channel.basic_publish(exchange='direct_logs', routing_key=severity, body=message)
```

## Subscribing

Receiving messages will work just like in pubsub, with one exception - we're going to create a new binding for each severity we're interested in.

```python
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

for severity in severities:
    channel.queue_bind(exchange='direct_logs', queue=queue_name, routing_key=severity)
```

`exclusive` - When set to true, your queue becomes private and can only be consumed by your app. This is useful when you need to limit a queue to only one consumer.
`auto-delete` - The queue is automatically deleted when the last consumer unsubscribes/disconnects.

## Putting it all together

```python
# emit_log_direct.py

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
```

```python
# receive_logs_direct.py

import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

severities = sys.argv[1:]
if not severities:
    sys.stderr.write['Usage: %s [info] [warning] [error]\n' % sys.args[0]]
    sys.exit(1)     # exit with error

for severity in severities:
    channel.queue_bind(exchange='direct_logs', queue=queue_name, routing_key=severity)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))

# consume the messages from the queue
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()
```

If you want to save only 'warning' and 'error' (and not 'info') log messages to a file, just open a console and type:

```bash
python receive_logs_direct.py warning error > logs_from_rabbit.log
```

If you'd like to see all the log messages on your screen, open a new terminal and do:

```bash
python receive_logs_direct.py info warning error
=> [*] Waiting for logs. To exit press CTRL+C
```

And, for example, to emit an error log message just type:

```bash
python emit_log_direct.py error "Run. Run. Or it will explode."
=> [x] Sent 'error':'Run. Run. Or it will explode.'
python emit_log_direct.py warning "It maight explode."
=> [x] Sent 'warning':'It maight explode.'
python emit_log_direct.py info "It explode once in production"
=> [x] Sent 'info':'It explode once in production'
```
