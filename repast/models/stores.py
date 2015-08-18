# coding: UTF-8

from .database import Base
from .base_class import InitUpdate
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DATETIME, FLOAT
from sqlalchemy.dialects.mysql import DOUBLE
from repast.util.ex_time import *
from .group import Group
from .brand import Brand
from .location import Province, City, Country

STORES = 'stores'
STORES_INFO = 'stores_info'

class Stores(Base, InitUpdate):
    '''餐厅'''
    __tablename__ = STORES
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=True)
    province_id = Column(Integer, nullable=False)
    city_id = Column(Integer, nullable=False)
    country_id = Column(Integer, nullable=False)
    address = Column(String(100), nullable=False)
    description = Column(String(200), nullable=True)
    group_id = Column(Integer, nullable=False)
    group = Column(String(50), nullable=False)
    brand_id = Column(Integer, nullable=False)
    brand = Column(String(50), nullable=False)
    recommend = Column(Boolean, nullable=False, server_default='0') # 0不推荐，1推荐
    manager = Column(String(20), nullable=False)
    tel = Column(String(20), nullable=False)
    stars = Column(Integer, nullable=False)
    hours = Column(DATETIME, nullable=True)
    longitude = Column(FLOAT, nullable=False)
    latitude = Column(FLOAT, nullable=False)

    def __init__(self, **kwargs):
        '''初始化'''
        args = ('name','address', 'description','longitude','latitude','brand_id','brand','manager',
        'tel','group_id','group','province_id','city_id','country_id','stars')
        self.init_value(args, kwargs)

    def update(self, **kwargs):
        args = ('name','address','description','longitude','latitude','brand_id','brand','recommend','manager',
        'tel','group_id','group','province_id','city_id','country_id', 'stars')
        self.update_value(args, kwargs)

class StoresInfo(Base,InitUpdate):
    '''详细信息'''
    __tablename__ = STORES_INFO
    id = Column(Integer, primary_key=True)
    stores_id = Column(Integer, ForeignKey(Stores.id, ondelete='cascade', onupdate='cascade'))
    base_path = Column(String(200), nullable=False)
    rel_path = Column(String(200), nullable=False)
    picture_name = Column(String(300), nullable=False)
    code_url = Column(String(500), nullable=True)

    def __init__(self, **kwargs):
        '''初始化'''
        args = ('stores_id','base_path','rel_path','picture_name')
        self.init_value(args, kwargs)

    def update(self, **kwargs):
        args = ('stores_id','base_path','rel_path','picture_name')
        self.update_value(args, kwargs)