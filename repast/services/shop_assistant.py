# coding: UTF-8
from flask import flash
from flask.ext.admin.babel import gettext
import hashlib

from repast.models.queue import *
from repast.models.user import *
from repast.models.database import db
from .queue_setting_service import get_table_type_by_stores_id
from .common_service import GetName


def get_shop_assistant_by_user(request):
    '''店员登录'''
    user_name = request.form.get('UserName')
    user_pass = request.form.get('Password')
    shop_assistant = ShopAssistant.query.filter(ShopAssistant.user_name == user_name, ShopAssistant.password == user_pass).first()
    return shop_assistant

def get_stores_id_by_shop_assistant_id(shop_assistant_id):
    '''根据员工id得到所属餐厅id'''
    shop_assistant = ShopAssistant.query.filter(ShopAssistant.id == shop_assistant_id).first()
    if shop_assistant:
        return shop_assistant.stores_id
    else:
        return 1


def call_number(queue_id):
    '''店员叫号'''
    queue = Queue.query.filter(Queue.id == queue_id).first()
    if queue:
        queue.status = 0 # 叫号修改状态值。说明已经叫过号
        try:
            db.commit()
        except:
            db.rollback()
            return False
    return True