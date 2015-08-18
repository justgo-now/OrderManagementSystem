# coding: UTF-8
from .database import Base
from .base_class import InitUpdate
from sqlalchemy import Column, Integer, String, ForeignKey, DATETIME,Boolean
from .stores import Stores
from .user import User
from repast.util.ex_time import *

QUEUE_SETTING = 'queue_setting'
QUEUE = 'queue'

class QueueSetting(Base, InitUpdate):
    '''队列，每个餐厅的座位种类，每个种类有多少个座位'''
    __tablename__ = QUEUE_SETTING
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, nullable=False)
    group = Column(String(50), nullable=False)
    brand_id = Column(Integer, nullable=False)
    brand = Column(String(50), nullable=False)
    stores_id = Column(Integer, nullable=False)
    stores = Column(String(50), nullable=False)
    status = Column(Integer, nullable=False, server_default='0')
    type = Column(String(20), nullable=False)
    number = Column(Integer, nullable=False)


    def __init__(self, **kwargs):
        args = ('type','number','stores_id','stores', 'group_id','group','brand_id','brand')
        self.init_value(args, kwargs)

    def update(self, **kwargs):
        args = ('type','number','stores_id','stores', 'group_id','group','brand_id','brand')
        self.update_value(args, kwargs)


class Queue(Base,InitUpdate):
    '''排队'''
    __tablename__ = QUEUE
    id = Column(Integer, primary_key=True)
    queue_setting_id = Column(Integer, ForeignKey(QueueSetting.id, ondelete='cascade', onupdate='cascade'))
    queue_time = Column(DATETIME, nullable=False)
    now_queue_number = Column(Integer, nullable=False)
    status = Column(Boolean, nullable=False, server_default='1')
    user_id = Column(Integer, ForeignKey(User.id, ondelete='cascade', onupdate='cascade'))
    stores_id = Column(Integer, ForeignKey(Stores.id, ondelete='cascade', onupdate='cascade'))

    def __init__(self, **kwargs):
        args = ('queue_setting_id','now_queue_number','user_id','stores_id')
        self.queue_time = todayfstr()
        self.init_value(args, kwargs)

    def update(self, **kwargs):
        args = ('status')
        self.update_value(args, kwargs)
