# coding: UTF-8

from flask import flash
from repast.util.session_common import *
from flask.ext.admin.babel import gettext
import os
from werkzeug import secure_filename
from repast.models.queue import QueueSetting, Queue
from .common_service import *
from repast.util.ex_time import *
from repast.models.database import db
from .stores_service import get_stores_by_id
from .queue_service import get_queue_by_id


class QueueService():
    '''桌型'''
    @staticmethod
    def create_queue_setting(session, form_dict):
        '''创建桌型'''
        try:
            queue_setting = QueueService.get_queue_setting(form_dict)
            session.add(queue_setting)
            session.commit()
        except Exception, ex:
            flash(gettext('Failed to create model. %(error)s', error=str(ex)), 'error')
            session.rollback()
            return False
        return True

    @staticmethod
    def update_queue_setting(session, form_dict, model):
        '''更新'''
        try:
            group_name = GetName._get_group(form_dict)
            form_dict['group'] = group_name
            brand_name = GetName._get_brand(form_dict)
            form_dict['brand'] = brand_name
            stores_name = GetName._get_stores(form_dict)
            form_dict['stores'] = stores_name
            model.update(**form_dict)
            session.commit()
        except Exception, ex:
            flash(gettext('Failed to update model. %(error)s', error=str(ex)), 'error')
            session.rollback()
            return False
        return True

    @staticmethod
    def get_queue_setting(form_dict):
        group = GetName._get_group(form_dict)
        brand = GetName._get_brand(form_dict)
        stores = GetName._get_stores(form_dict)
        return QueueSetting(group_id=form_dict['group_id'],
                            group=group,
                            brand_id=form_dict['brand_id'],
                            brand=brand,
                            stores_id=form_dict['stores_id'],
                            stores=stores,
                            type=form_dict['type'],
                            number=form_dict['number'])


def check_queue_by_user_id_and_stores_id(user_id, stores_id, table_type_id):
    '''根据user_id,stores_id判断是否已经存在'''
    args_time = get_date_time_str()
    queue = Queue.query.filter(Queue.user_id == user_id, Queue.stores_id == stores_id, Queue.queue_time.like(args_time), Queue.status == 1).first()
    if queue:
        table_type = QueueSetting.query.filter(QueueSetting.id == queue.queue_setting_id).first()
        queue.table_type = ''
        if table_type:
            queue.table_type = table_type.type
        return queue
    return None




def create_queue(user_id, stores_id, table_type_id):
    '''根据当前时间得到队列'''
    args_time = get_date_time_str()
    queue_count = Queue.query.filter(Queue.queue_time.like(args_time), Queue.queue_setting_id == table_type_id).count()
    queue = None
    if queue_count == 1:
        queue = Queue.query.filter(Queue.queue_time.like(args_time), Queue.queue_setting_id == table_type_id).first() # 得到队列中最后一个
        next_number = queue.now_queue_number + 1 # 得到下一个队列号
        new_queue = get_queue(user_id,stores_id,table_type_id,next_number)
        create_new_queue(new_queue)
    elif queue_count > 1:
        queue = Queue.query.filter(Queue.queue_time.like(args_time), Queue.queue_setting_id == table_type_id).order_by(Queue.now_queue_number.desc()).first()# 得到已经存在的队列
        next_number = queue.now_queue_number + 1 # 得到下一个队列号
        new_queue = get_queue(user_id,stores_id,table_type_id,next_number)
        create_new_queue(new_queue)
    if queue_count == 0:
        new_queue = get_queue(user_id,stores_id,table_type_id, 1) # 如果当前没有队列，那么就创建一个新队列并为第一个
        create_new_queue(new_queue)
    return new_queue


def get_queue(user_id, stores_id, table_type_id, next_number):
    '''创建队列'''
    queue = Queue(queue_setting_id=table_type_id,
                  now_queue_number=next_number,
                  user_id=user_id,
                  stores_id=stores_id)
    return queue

def cancel(queue_id):
    '''取消排队'''
    queue = Queue.query.filter(Queue.id == queue_id).first()
    if queue:
        queue.status = 0
        try:
            db.commit()
        except:
            db.rollback()

def do_queue_format(table_type_id, request, user_id):
    '''用户排队'''
    stores_id = request.args.get('stores_id') # 用户排队的餐厅
    # queue = check_queue_by_user_id_and_stores_id(user_id, stores_id, table_type_id) # 判断是否已经存在队列当中
    queue_q, queue_count = get_queue_by_table_type_id(table_type_id)
    #if queue:
    #    message = '您已在队列中，当前桌型为%s,号码为%s,前面还有%s位' %(queue.table_type,queue.now_queue_number, queue_count) # 如果存在队列中，提示
    #    queue.queue_count = queue_count
    #    queue.message = message
    #    return queue
    #else:
    queue = create_queue(user_id, stores_id, table_type_id)
    table_type = QueueSetting.query.filter(QueueSetting.id == table_type_id).first()
    if queue and table_type:
        message = '排队成功，当前号码为%s,前面还有%s位' %(queue.now_queue_number, queue_count)
        queue.queue_count = queue_count
        queue.message = message
        queue.table_type = table_type.type
    return queue


def get_table_type_by_stores_id(stores_id):
    '''得到餐厅的所有桌型'''
    queue_setting_count = QueueSetting.query.filter(QueueSetting.stores_id == stores_id).order_by(QueueSetting.type).count() # 得到总共有多少个桌型
    if queue_setting_count > 1:
        queue_setting = QueueSetting.query.filter(QueueSetting.stores_id == stores_id).order_by(QueueSetting.type).all() #
    else:
        queue_setting = QueueSetting.query.filter(QueueSetting.stores_id == stores_id).order_by(QueueSetting.type).first()
    return queue_setting,queue_setting_count


def get_queue_by_stores_id(stores_id):
    '''得到一个餐厅的所有队列'''
    table_type, table_type_count = get_table_type_by_stores_id(stores_id)
    temp = []
    if table_type_count > 1:
        for t in table_type:
            queue, queue_count = get_queue_by_table_type_id(t.id)
            t.queue_number = queue_count
            temp.append(t)
    else:
        if table_type:
            queue, queue_count = get_queue_by_table_type_id(table_type.id)
            table_type.queue_number = queue_count
            temp.append(table_type)
    return temp


def get_now_queue_number_and_number_wait_by_stores_id(stores_id):
    '''根据餐厅id得到当前号码，等待号码'''
    table_type, table_type_count = get_table_type_by_stores_id(stores_id) # 得到餐厅桌型
    temp = []
    if table_type_count > 1:
        for t in table_type:
            now_number, wait_number, now_id = get_now_number_wait_number(t.id)
            t.now_number = now_number
            t.wait_number = wait_number
            t.now_id = now_id
            temp.append(t)
    else:
        if table_type:
            now_number, wait_number, now_id = get_now_number_wait_number(table_type.id)
            table_type.now_number = now_number
            table_type.wait_number = wait_number
            table_type.now_id = now_id
            temp.append(table_type)
    return temp

def get_now_number_wait_number(table_type_id):
    '''得到当前号码'''
    queue, queue_count = get_queue_by_table_type_id(table_type_id)
    now_number = 1
    wait_number = 1
    now_id = 1
    if queue_count > 1:
        now_number = queue[0].now_queue_number
        wait_number = queue[-1].now_queue_number + 1
        now_id = queue[0].id
    else:
        if queue:
            now_number = queue.now_queue_number
            wait_number = queue.now_queue_number + 1
            now_id = queue.id
        else:
            now_number = '当前没有人排队'
            wait_number = get_wait_number(table_type_id)
    return now_number, wait_number, now_id


def get_queue_by_table_type_id(table_type_id):
    """
    根据桌型得到队列,
    只获取当天有效的队列
    """
    args_time = get_date_time_str()
    queue_count = Queue.query.filter(Queue.queue_setting_id == table_type_id, Queue.queue_time.like(args_time), Queue.status == 1).count()
    if queue_count > 1:
        queue = Queue.query.filter(Queue.queue_setting_id == table_type_id, Queue.queue_time.like(args_time), Queue.status == 1).order_by(Queue.now_queue_number).all()
    else:
        queue = Queue.query.filter(Queue.queue_setting_id == table_type_id, Queue.queue_time.like(args_time), Queue.status == 1).first()
    return queue, queue_count


def get_wait_number(table_type_id):
    '''获取已经叫过号，并且没有人继续排队时候的等待号'''
    args_time = get_date_time_str()
    queue_count = Queue.query.filter(Queue.queue_setting_id == table_type_id, Queue.queue_time.like(args_time)).count()
    wait_number = queue_count + 1
    return wait_number


def get_schedule_by_user_id(user_id):
    '''获得用户的进展'''
    args_time = get_date_time_str()
    get_stores = Queue.query.filter(Queue.queue_time.like(args_time), Queue.user_id == user_id, Queue.status == 1).all()
    # 用户可以重复排队，提醒进度时候需要自己也算进去。？
    queue_count = Queue.query.filter(Queue.queue_time.like(args_time), Queue.user_id == user_id, Queue.status == 1).count()
    if get_stores:
        get_stores_info(get_stores, queue_count, user_id) # 格式化排队信息
        return get_stores
    return None

def get_stores_info(queue_info, queue_count, user_id):
    '''得到用户排队餐厅信息'''
    args_time = get_date_time_str()
    for queue in queue_info:
        queue.table_type = get_table_type(queue.queue_setting_id) # 得到桌型
        schedule_count = Queue.query.filter(Queue.queue_time.like(args_time), Queue.status == 1,Queue.user_id != user_id, Queue.stores_id == queue.stores_id).count()
        queue.schedule_count = schedule_count # 用户排队前面还有几人
        queue.table_type = get_table_type(queue.queue_setting_id) # 得到餐桌类型
        stores = Stores.query.filter(Stores.id == queue.stores_id).first() # 得到排队餐厅
        queue.stores_name = ''
        queue.address = ''
        if stores:
            queue.stores_name = stores.name
            queue.address = stores.address
        if queue_count > 1:
            queue.schedule_count = queue.schedule_count + (queue_count - 1) # 如果用户排了多个。前面几人自己也算一个

def get_table_type(table_type_id):
    table_type = get_queue_by_id(table_type_id)
    if table_type:
        return table_type.type
    return ''

def get_queue_info_by_user_id_and_stores_id(user_id, stores_id):
    temp = get_queue_by_stores_id(stores_id) # 前面还有几人


def create_new_queue(model):
    '''创建新model'''
    db.add(model)
    db.commit()