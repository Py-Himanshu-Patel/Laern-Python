# Rabbit MQ

RabbitMQ is a message broker: it accepts and forwards messages.

## Index

1. [Hello World](./1-HelloWorld/README.md)
2. [Work Queues](./2-WorkQueues/README.md)
3. [Publisher Subscriber](./3-PublisherSubscriber/README.md)

## Notes

Notes for installing, configuring and other details for RabbitMQ

### Install RabbitMQ and Pika client

```bash
sudo apt-get install rabbitmq-server
sudo systemctl start rabbitmq-server
sudo rabbitmq-plugins enable rabbitmq_management
# visit http://localhost:15672
# login: guest, password : guest
```

Install `pika` client for connecting python with `rabbitmq-server`

```bash
pipenv install pika
```

### Listing queues

You may wish to see what queues RabbitMQ has and how many messages are in them. You can do it (as a privileged user) using the `rabbitmqctl` tool:

```bash
sudo rabbitmqctl list_queues
```

On Windows, omit the sudo:

```bash
rabbitmqctl.bat list_queues
```

```bash
Timeout: 60.0 seconds ...
Listing queues for vhost / ...
name    messages
hello   3
```

Restart RabbitMQ server to free up the queues which are no longer used.

### Listing exchanges

To list the exchanges on the server you can run the ever useful `rabbitmqctl`:

```bash
sudo rabbitmqctl list_exchanges
```

```bash
Listing exchanges for vhost / ...
name  type
amq.match headers
amq.rabbitmq.trace  topic
amq.topic   topic
amq.fanout  fanout
amq.headers headers
amq.direct  direct
    direct
```

In this list there will be some amq.* exchanges and the default (unnamed) exchange. These are created by default, but it is unlikely you'll need to use them at the moment.

### Listing bindings

You can list existing bindings using, you guessed it,

```bash
sudo rabbitmqctl list_bindings
```

```bash
Listing bindings for vhost /...
source_name	source_kind	destination_name	destination_kind	routing_key	arguments
    exchange	task_queue	queue	task_queue	[]
```
