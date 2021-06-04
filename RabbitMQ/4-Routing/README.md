# Routing (Receiving messages selectively)

We're going to modify previous Pub/Sub model to make it possible to subscribe only to a subset of the messages. For example, we will be able to direct only critical error messages to the log file (to save disk space), while still being able to print all of the log messages on the console.

## Bindings

In previous examples we were already creating bindings. You may recall code like:

```python
channel.queue_bind(exchange=exchange_name, queue=queue_name)
```

A binding is a relationship between an exchange and a queue. This can be simply read as: **the queue is interested in messages from this exchange**.

Bindings can take an extra r`outing_key` parameter. To avoid the confusion with a `basic_publish` parameter we're going to call it a `binding key`. This is how we could create a binding with a key:

```python
channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key='black')
```

The **meaning of a binding key depends on the exchange type**. The `fanout` exchanges, which we used previously, simply ignored its value.

## Direct exchange

We were using a `fanout` exchange, which doesn't give us too much flexibility - it's only capable of mindless broadcasting.

We will use a `direct` exchange instead. The routing algorithm behind a `direct` exchange is simple - **a message goes to the queues whose binding key exactly matches the routing key of the message**.
It is perfectly legal to bind multiple queues with the same binding key. In that case, the direct exchange will behave like fanout and will broadcast the message to all the matching queues.

## Emitting logs

Instead of fanout we'll send messages to a direct exchange. We will supply the log severity as a routing key.

Like always we need to create an exchange first:

```bash
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')
```
