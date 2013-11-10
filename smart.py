# -*- coding: utf-8 -*-
__author__ = 'peter'

import pika
from pikachu import Pikachu
from config import SMART
import stupid
import json

import minions


class Smart(Pikachu):
    def __init__(self):
        self._forward_channel=None
        Pikachu.__init__(self, SMART)

    # Step #2
    def on_connected(self, connection):
        Pikachu.on_connected(self, connection)
        connection.channel(self.on_forward_channel_open)

    def on_forward_channel_open(self, new_channel):
        """Called when our channel has opened"""
        self._forward_channel = new_channel
        self._forward_channel.exchange_declare(exchange=self._intelligence['forward_exchange'],
                                               exchange_type='fanout',
                                               durable=True, auto_delete=False,
                                               callback=self.on_exchange_declared)

    def on_exchange_declared(self, frame):
        pass

    # Step #5
    def handle_delivery(self, channel, method, header, body):
        """Called when we receive a message from RabbitMQ"""
        try:
            data=json.loads(body)
            properties = pika.BasicProperties(content_type='application/json')
            body=json.dumps(minions.process(method, header, body))
            self._forward_channel.basic_publish(exchange=self._intelligence['forward_exchange'],
                                                routing_key='pikachu.stupid',
                                                body=body,
                                                properties=properties)
            Pikachu.handle_delivery(self, channel, method, header, body)
        except ValueError:
            pass

smart=Smart()

if __name__ == '__main__':
    try:
        smart.start()
    except KeyboardInterrupt:
        smart.stop()
