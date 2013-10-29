# -*- coding: utf-8 -*-
__author__ = 'peter'

import pika
from config import INBOX
import outbox
import json

# Create a global channel variable to hold our channel object in
channel = None

# Step #2
def on_connected(connection):
    """Called when we are fully connected to RabbitMQ"""
    # Open a channel
    connection.channel(on_channel_open)

# Step #3
def on_channel_open(new_channel):
    """Called when our channel has opened"""
    global channel
    channel = new_channel
    channel.queue_declare(queue=INBOX['queue'], durable=True, exclusive=False, auto_delete=False, callback=on_queue_declared)

# Step #4
def on_queue_declared(frame):
    """Called when RabbitMQ has told us our Queue has been declared, frame is the response from RabbitMQ"""
    channel.basic_consume(handle_delivery, queue=INBOX['queue'])

# Step #5
def handle_delivery(channel, method, header, body):
    """Called when we receive a message from RabbitMQ"""
    data=json.loads(body)
    outbox.send(data['mobile'], data['message'])

# Step #1: Connect to RabbitMQ using the default parameters
credentials = pika.PlainCredentials(INBOX['username'], INBOX['password'])
parameters = pika.ConnectionParameters(INBOX['host'],
                                       INBOX['port'],
                                       INBOX['virtualhost'],
                                       credentials)
connection = pika.SelectConnection(parameters, on_connected)


if __name__ == '__main__':
    try:
        # Loop so we can communicate with RabbitMQ
        connection.ioloop.start()
    except KeyboardInterrupt:
        # Gracefully close the connection
        connection.close()
        # Loop until we're fully closed, will stop on its own
        connection.ioloop.start()


