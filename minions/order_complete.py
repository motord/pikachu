# -*- coding: utf-8 -*-
__author__ = 'peter'


def process(data):
    message = dict(recipients=[], content=u'{0}')

    message['recipients'].append(data['mobile'])
    message['content']=message['content'].format(data['bar'])
    return message