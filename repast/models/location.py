# coding: utf-8

"""
    province city country数据库表的定义，本模块定义了Province City Country类。
    Province: Province类，省份和直辖市。
    City: City类，省下面的事，直辖市的设置标记
    Country: Country类，市下面的区县或者是直辖市的区县
"""

from sqlalchemy import Column, Integer, String

from .database import Base

PROVINCE_TABLE = 'province'
CITY_TABLE = 'city'
COUNTRY_TABLE = 'country'


class Province(Base):
    """province表对应的类
    id
    name 省名
    code 标志位
    country 国家标志
    """

    __tablename__ = PROVINCE_TABLE

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    code = Column(String(4), nullable=False)
    country = Column(String(4), nullable=True, server_default=None)

    def __init__(self, name, code, country='zh'):
        self.name = name
        self.code = code
        self.country = country

    def __repr__(self):
        return '<Province(name: %s)>' % self.name


class City(Base):
    """city表对应的类
    id
    name 市名
    code 标志位
    province_id 上级省
    """

    __tablename__ = CITY_TABLE

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    code = Column(String(4), nullable=False)
    province_id = Column(Integer, nullable=False)

    def __init__(self, name, code, province_id):
        self.name = name
        self.code = code
        self.province_id = province_id

    def __repr__(self):
        return '<City(name: %s)>' % self.name


class Country(Base):
    """city表对应的类
    id
    name 市名
    code 标志位
    province_id 上级省
    """

    __tablename__ = COUNTRY_TABLE

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    code = Column(String(4), nullable=False)
    city_id = Column(Integer, nullable=False)

    def __init__(self, name, code, city_id):
        self.name = name
        self.code = code
        self.city_id = city_id

    def __repr__(self):
        return '<Country(name: %s)>' % self.name