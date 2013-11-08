# -*- coding: utf-8 -*-
__author__ = 'peter'

from pikachu import Pikachu
from suds.client import Client
from config import STUPID, OUTBOX
import logging
import json

logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)

class Stupid(Pikachu):
    def __init__(self):
        Pikachu.__init__(self, STUPID)
        self._client=Client(OUTBOX['url'])

    # Step #5
    def handle_delivery(self, channel, method, header, body):
        """Called when we receive a message from RabbitMQ"""
        data=json.loads(body)
        self.send(data['mobile'], data['message'])

    def send(self, mobile, message):
        self._client.service.sendBatchMessage(OUTBOX['account'], OUTBOX['password'], mobile, message)


stupid=Stupid()

if __name__ == '__main__':
    try:
        stupid.start()
    except KeyboardInterrupt:
        stupid.stop()
