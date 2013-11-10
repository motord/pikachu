# -*- coding: utf-8 -*-
__author__ = 'peter'

import order_complete, order_courier, user_register
import json

EXCHANGE_ORDER_COMPLETE = u'order.complete'
EXCHANGE_ORDER_COURIER = u'order.courier'
EXCHANGE_USER_REGISTER = u'user.register'

def process(method, header, body):
    data=json.loads(body)
    return {
    EXCHANGE_ORDER_COMPLETE: order_complete.process,
    EXCHANGE_ORDER_COURIER: order_courier.process,
    EXCHANGE_USER_REGISTER: user_register.process
    }[method.exchange](data)