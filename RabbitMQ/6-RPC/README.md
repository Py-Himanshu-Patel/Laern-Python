# RPC (Remote Procedure Client)

If we need to run a function on a remote computer and wait for the result that is called RPC. We're going to use RabbitMQ to build an RPC system: a client and a scalable RPC server.

## Client interface

A simple client class going to expose a method named `call` which sends an RPC request and blocks until the answer is received:

```python
fibonacci_rpc = FibonacciRpcClient()
result = fibonacci_rpc.call(4)
print("fib(4) is %r" % result)
```

### A note on RPC

- Make sure it's obvious which function call is local and which is remote.
- Document your system. Make the dependencies between components clear.
- Handle error cases. How should the client react when the RPC server is down for a long time?

When in doubt avoid RPC. If you can, you should use an asynchronous pipeline - instead of RPC-like blocking, results are asynchronously pushed to a next computation stage.

## Callback queue

In general doing RPC over RabbitMQ is easy. A client sends a request message and a server replies with a response message. In order to receive a response the client needs to send a `callback` queue address with the request.

```python
result = channel.queue_declare(queue='', exclusive=True)
callback_queue = result.method.queue

channel.basic_publish(exchange='',
                      routing_key='rpc_queue',
                      properties=pika.BasicProperties(
                            reply_to = callback_queue,
                            ),
                      body=request)

# ... and some code to read a response message from the callback_queue ...
```

### Message properties

- `delivery_mode`: Marks a message as persistent (with a value of 2) or transient (any other value).
- `content_type`: Used to describe the mime-type of the encoding. For example for the often used JSON encoding it is a good practice to set this property to: application/json.
- `reply_to`: Commonly used to name a callback queue.
- `correlation_id`: Useful to correlate RPC responses with requests.

## Correlation id

In the method presented above we suggest creating a callback queue for every RPC request. That's pretty inefficient, but fortunately there is a better way - let's create a single callback queue per client.

That raises a new issue, having received a response in that queue it's not clear to which request the response belongs. That's when the `correlation_id` property is used. We're going to set it to a unique value for every request. Later, when we receive a message in the callback queue we'll look at this property, and based on that we'll be able to match a response with a request. If we see an unknown `correlation_id` value, we may safely discard the message - it doesn't belong to our requests.

You may ask, why should we ignore unknown messages in the callback queue, rather than failing with an error? It's due to a possibility of a race condition on the server side. Although unlikely, it is possible that the RPC server will die just after sending us the answer, but before sending an acknowledgment message for the request. If that happens, the restarted RPC server will process the request again. That's why on the client we must handle the duplicate responses gracefully, and the RPC should ideally be idempotent.

### Our RPC will work like this

- When the Client starts up, it creates an anonymous **exclusive callback queue** (An exclusive queue can only be used (consumed from, purged, deleted, etc) by its declaring connection. An attempt to use an exclusive queue from a different connection will result in a channel-level exception).
- For an RPC request, the Client sends a message with two properties: `reply_to`, which is set to the **callback queue** and  `correlation_id`, which is set to a **unique value for every request**.
- The request is sent to an `rpc_queue` queue.
- The RPC worker (aka: server) is waiting for requests on that queue. When a request appears, it does the job and sends a message with the result back to the Client, using the queue from the `reply_to` field.
The client waits for data on the callback queue. When a message appears, it checks the `correlation_id` property. If it matches the value from the request it returns the response to the application.

## Putting it all together

```python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

# declare RPC queue
channel.queue_declare(queue="rpc_queue")


def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


def on_request(ch, method, props, body):
    n = int(body)

    print(" [.] fib(%s)" % n)
    response = fib(n)

    ch.basic_publish(
        exchange="",
        routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id=props.correlation_id),
        body=str(response),
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()
```

- As usual we start by establishing the connection and declaring the queue `rpc_queue`.
- We declare a callback `on_request` for `basic_consume`, the core of the RPC server. It's executed when the request is received. It does the work and sends the response back.
- We might want to run more than one server process. In order to spread the load equally over multiple servers we need to set the `prefetch_count` setting.

```python
import pika
import uuid


class FibonacciRpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue="", exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True,
        )

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange="",
            routing_key="rpc_queue",
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n),
        )
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)


fibonacci_rpc = FibonacciRpcClient()

input_int = int(input())
print(f" [x] Requesting fib({input_int})")
response = fibonacci_rpc.call(input_int)
print(" [.] Got %r" % response)
```

The client code is slightly more involved

- We establish a connection, channel and declare an exclusive `callback_queue` for replies.
- We subscribe to the `callback_queue`, so that we can receive RPC responses.
- The `on_response` callback that got executed on every response is doing a very simple job, for every response message it checks if the `correlation_id` is the one we're looking for. If so, it saves the response in self.response and breaks the consuming loop.
- Next, we define our main `call` method - it does the actual RPC request.
- Also in `call` method, we publish the request message, with two properties: `reply_to` and `correlation_id`.
- At the end we wait until the proper response arrives and return the response back to the user.

## Execute

```bash
python rpc_server.py
=> [x] Awaiting RPC requests
```

To request a fibonacci number run the client:

```bash
python rpc_client.py
=> [x] Requesting fib(30)
```

## Summary

### What got solved

- If the RPC server is too slow, you can scale up by just running another one. Try running a second `rpc_server.py` in a new console.
- On the client side, the RPC requires sending and receiving only one message. No synchronous calls like `queue_declare` are required. As a result the RPC client needs only one network round trip for a single RPC request.

### Yet to solve

- How should the client react if there are no servers running?
- Should a client have some kind of timeout for the RPC?
- If the server malfunctions and raises an exception, should it be forwarded to the client?
- Protecting against invalid incoming messages (eg checking bounds) before processing.
