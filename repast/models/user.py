# coding: UTF-8
from .database import Base
from .base_class import InitUpdate
from sqlalchemy import Column, String, Integer, ForeignKey, FLOAT, DATETIME
from ..util.ex_time import get_date_time_str, todayfstr
from ..models.database import db

USER = 'user'
SHOP_ASSISTANT = 'shop_assistant'
USER_MENU = 'user_menu'
DISH_USER_MENU = 'dish_menu_number'

class User(Base, InitUpdate):
    '''用户'''
    __tablename__ = USER
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=True)
    nick_name = Column(String(20), nullable=True)
    password = Column(String(20), nullable=False, server_default='888888')
    openid = Column(String(200), nullable=False)
    picture_url = Column(String(500), nullable=True)
    longitude = Column(FLOAT, nullable=True)
    latitude = Column(FLOAT, nullable=True)
    description = Column(String(200), nullable=True)
    coupons_id = Column(String(50), nullable=True)

    def __init__(self, **kwargs):
        args = ('nick_name','openid','picture_url')
        self.init_value(args, kwargs)

    def update(self, **kwargs):
        args = ('longitude','latitude', 'description')
        self.update_value(args,kwargs)


class ShopAssistant(Base, InitUpdate):
    '''店员'''
    __tablename__ = SHOP_ASSISTANT
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, nullable=False)
    group = Column(String(50), nullable=False)
    brand_id = Column(Integer, nullable=False)
    brand = Column(String(50), nullable=False)
    stores_id = Column(Integer, nullable=False)
    stores = Column(String(50), nullable=False)
    name = Column(String(20), nullable=False)
    user_name = Column(String(20), nullable=False)
    password = Column(String(200), nullable=False)
    tel = Column(String(12), nullable=True)

    def __init__(self, **kwargs):
        args = ('group_id','group','brand_id','brand','stores_id','stores','name','tel','user_name','password')
        self.init_value(args, kwargs)


    def update(self, **kwargs):
        args = ('group_id','group','brand_id','brand','stores_id','stores','name','tel','user_name','password')
        self.update_value(args, kwargs)


class Menu(Base, InitUpdate):
    """用户菜单"""
    __tablename__ = USER_MENU
    id = Column(Integer, primary_key=True)
    dish_number_id = Column(String(50), nullable=False)
    user_id = Column(Integer, nullable=False)
    stores_id = Column(Integer, nullable=False)
    menu_time = Column(DATETIME, nullable=False, default='NOW()')

    def __init__(self, **kwargs):
        args = ('dish_number_id', 'user_id', 'stores_id')
        self.init_value(args, kwargs)

    def update(self, **kwargs):
        args = ()
        self.update_value(args, kwargs)

    @staticmethod
    def get_user_menu_by_user_id(user_id):
        today_time = get_date_time_str()
        user_menu = Menu.query.filter(Menu.user_id == user_id, Menu.menu_time.like(today_time)).all()
        return user_menu

    @staticmethod
    def add_user_menu(dish_id, user_id, stores_id):
        try:
            today_time = todayfstr()
            add_menu = Menu(dish_number_id=dish_id, user_id=user_id, stores_id=stores_id, menu_time=today_time)
            db.add(add_menu)
            db.commit()
        except Exception, e:
            print e


class DishUserMenu(Base, InitUpdate):
    """菜品，菜品个数"""
    __tablename__ = DISH_USER_MENU
    id = Column(Integer, primary_key=True)
    dish_id = Column(Integer, nullable=False)
    dish_number = Column(Integer, nullable=False)

    def __init__(self, **kwargs):
        args = ('dish_id', 'dish_number')
        self.init_value(args, kwargs)

    def update(self, **kwargs):
        args = ('dish_number',)
        self.update_value(args, kwargs)

    @staticmethod
    def get_dish_number_menu_by_id(dish_number_id):
        dish_number_menu = DishUserMenu.query.filter(DishUserMenu.id == dish_number_id).first()
        return dish_number_menu

    @staticmethod
    def add_dish_number_menu(dish_id, number):
        dish_user_menu = DishUserMenu.add_user_menu(dish_id, number)
        try:
            db.add(dish_user_menu)
            db.commit()
            return dish_user_menu
        except Exception, e:
            print e