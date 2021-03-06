# -*- coding: utf-8 -*-
__author__ = 'peter'

import pika
import logging

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)

class Pikachu(object):
    
    def __init__(self, intelligence):
        self._channel = None
        self._intelligence=intelligence
        # Step #1: Connect to RabbitMQ using the default parameters
        credentials = pika.PlainCredentials(intelligence['username'], intelligence['password'])
        parameters = pika.ConnectionParameters(intelligence['host'],
                                               intelligence['port'],
                                               intelligence['virtualhost'],
                                               credentials)
        self._connection = pika.SelectConnection(parameters, self.on_connected)
    
    # Step #2
    def on_connected(self, connection):
        """Called when we are fully connected to RabbitMQ"""
        # Open a channel
        connection.channel(self.on_channel_open)
    
    # Step #3
    def on_channel_open(self, new_channel):
        """Called when our channel has opened"""
        self._channel = new_channel
        self._channel.queue_declare(queue=self._intelligence['queue'], durable=True, exclusive=False, auto_delete=False, callback=self.on_queue_declared)
    
    # Step #4
    def on_queue_declared(self, frame):
        """Called when RabbitMQ has told us our Queue has been declared, frame is the response from RabbitMQ"""
        self._channel.basic_consume(self.handle_delivery, queue=self._intelligence['queue'])
    
    # Step #5
    def handle_delivery(self, channel, method, header, body):
        """Called when we receive a message from RabbitMQ"""
        LOGGER.info('Received message # %s from %s: %s',
                    method.delivery_tag, header.app_id, body)
        self.acknowledge_message(method.delivery_tag)

    def acknowledge_message(self, delivery_tag):
        """Acknowledge the message delivery from RabbitMQ by sending a
        Basic.Ack RPC method for the delivery tag.

        :param int delivery_tag: The delivery tag from the Basic.Deliver frame

        """
        LOGGER.info('Acknowledging message %s', delivery_tag)
        self._channel.basic_ack(delivery_tag)

    def start(self):
        # Loop so we can communicate with RabbitMQ
        self._connection.ioloop.start()

    def stop(self):
        # Gracefully close the connection
        self._connection.close()
        # Loop until we're fully closed, will stop on its own
        self._connection.ioloop.start()
