# Rabbit MQ

RabbitMQ is a message broker: it accepts and forwards messages.

## Index

1. [Hello World](./1-HelloWorld/README.md)

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
