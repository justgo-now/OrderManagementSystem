# coding: UTF-8

from .database import Base
from .base_class import InitUpdate
from sqlalchemy import Column, String, Integer

GROUP = 'group'

class Group(Base, InitUpdate):
    '''集团'''
    __tablename__ = GROUP
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(200), nullable=True)
    address = Column(String(100), nullable=False)
    group_person_in_charge = Column(String(50), nullable=True)
    tel = Column(String(11), nullable=True)
    email = Column(String(50), nullable=True)

    def __init__(self, **kwargs):
        '''初始化'''
        args = ('name', 'description','address','group_person_in_charge','tel')
        self.init_value(args, kwargs)

    def update(self, **kwargs):
        '''更新'''
        args = ('name','description','address','group_person_in_charge','tel')
        self.update_value(args, kwargs)
