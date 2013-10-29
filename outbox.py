# -*- coding: utf-8 -*-
__author__ = 'peter'

from suds.client import Client
from config import OUTBOX
import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)


client=Client(OUTBOX['url'])

def send(mobile, message):
    client.service.sendBatchMessage(OUTBOX['account'], OUTBOX['password'], mobile, message)

if __name__ == '__main__':
    print client

