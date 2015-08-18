# coding: UTF-8
from flask import session
#session = Session()

def get_session_user():
    if session.has_key('user') and session['user']:
        #这里只能传递一个字符串，不然会报没有序列化的错
        return session['user']
    return None

def get_session_shop_user():
    if session.has_key('shop_user') and session['shop_user']:
        #这里只能传递一个字符串，不然会报没有序列化的错
        return session['shop_user']
    return None

def set_session_user(value_name):
    """
       登陆成功保存到session当中
    """
    session['user'] = value_name

def set_session_shop_user(value_name):
    session['shop_user'] = value_name


def set_session_mark_queue(value):
    session['mark_queue'] = value

def get_session_mark_queue():
    if session.has_key('mark_queue') and session['mark_queue']:
        return session['mark_queue']
    return None

def set_session_dish(dish):
    session['dish'] = dish

def get_session_dish():
    if session.has_key('dish') and session['dish']:
        dishes=session['dish']
        for d in dishes:
            if d['number'] == 0:
                return None

        return session['dish']
    return None

def set_session_value(key, value):
    session[str(key)] = value


def get_session_value(key):
    if session.has_key(str(key)) and session[str(key)]:
        return session[str(key)]
    return None