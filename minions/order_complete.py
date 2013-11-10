# -*- coding: utf-8 -*-
__author__ = 'peter'

message = dict(recipients=[], content=u'{0}')

def process(data):
    message['recipients'].append(data['mobile'])
    message['content']=message['content'].format(data['bar'])
    return message