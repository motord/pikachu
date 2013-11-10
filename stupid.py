# -*- coding: utf-8 -*-
__author__ = 'peter'

from pikachu import Pikachu
from suds.client import Client
from config import STUPID, OUTBOX, DATABASE
import logging
import json

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from datetime import datetime
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import ARRAY

DeclarativeBase = declarative_base()


def db_connect():
    """Performs database connection using database settings from settings.py.

    Returns sqlalchemy engine instance.

    """
    return create_engine(URL(**DATABASE))


class Message(DeclarativeBase):
    """Sqlalchemy messages model"""
    __tablename__ = "messages"
    __table_args__ = {'schema':DATABASE['username']}

    id = Column(Integer, primary_key=True)
    recipients = Column(ARRAY(String))
    headcount = Column(Integer)
    content = Column(String, nullable=True)
    delivered_at = Column(DateTime, nullable=True)


logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)

class Stupid(Pikachu):
    def __init__(self):
        Pikachu.__init__(self, STUPID)
        self._client=Client(OUTBOX['url'])
        """Initializes database connection and sessionmaker.

        Creates messages table.

        """
        engine = db_connect()
        self.Session = sessionmaker(bind=engine)

    # Step #5
    def handle_delivery(self, channel, method, header, body):
        """Called when we receive a message from RabbitMQ"""
        data=json.loads(body)
        recipients=data['recipients']
        headcount=len(recipients)
        content=data['content']

        session = self.Session()
        # session.execute('SET search_path TO {0}'.format(DATABASE['username']))

        message = Message(recipients=recipients, headcount=headcount, content=content, delivered_at=datetime.now())

        try:
            session.add(message)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        self.send(';'.join(recipients), data['content'])
        Pikachu.handle_delivery(self, channel, method, header, body)

    def send(self, mobile, message):
        self._client.service.sendBatchMessage(OUTBOX['account'], OUTBOX['password'], mobile, message)


stupid=Stupid()

if __name__ == '__main__':
    try:
        stupid.start()
    except KeyboardInterrupt:
        stupid.stop()
