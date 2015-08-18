# coding: UTF-8

from .base_class import InitUpdate
from .database import Base
from sqlalchemy import Column, String, Integer, ForeignKey
from .group import Group

BRAND = 'brand'

class Brand(Base,InitUpdate):
    '''品牌'''
    __tablename__ = BRAND
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(200), nullable=True)
    group_id = Column(Integer, nullable=False)
    group = Column(String(50), nullable=False)
    manager = Column(String(20), nullable=False)
    tel = Column(String(11), nullable=False)
    email = Column(String(50), nullable=True)

    def __init__(self, **kwargs):
        '''初始化'''
        args = ('name','description','group_id','group','manager','tel','email')
        self.init_value(args,kwargs)

    def update(self, **kwargs):
        args = ('name','description','group_id','group','manager','tel','email')
        self.update_value(args, kwargs)
