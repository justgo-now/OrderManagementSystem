#coding:UTF-8

from repast.models.queue import *
from repast.models.database import *

def get_queue_count(store_id):
    return QueueSetting.query.filter(QueueSetting.stores_id==store_id).count()

def find_queue_by_store_id(store_id):
    count = QueueSetting.query.filter(QueueSetting.stores_id==store_id).count()
    if count == 1:
        restaurant = QueueSetting.query.filter(QueueSetting.stores_id==store_id).first()
    elif count > 1:
        restaurant = QueueSetting.query.filter(QueueSetting.stores_id==store_id).all()
    else:
        restaurant = ''
    return restaurant

def get_queue_by_id(queue_id):
    '''根据id得到桌型'''
    table_type = QueueSetting.query.filter(QueueSetting.id == queue_id).first()
    return table_type

def get_q_by_id(queue_id):
    queue = Queue.query.filter(Queue.id == queue_id).first()
    return queue

def get_queue_by_now_number(now_number, stores_id, table_type_id):
    now_time = todayfstr()  # 当前时间
    str_time = str(now_time)[:10]  # 截取当前时间。去掉时分秒
    args_time = '%' + str_time + '%'
    queue = Queue.query.filter(Queue.now_queue_number == now_number,
                               Queue.queue_time.like(args_time),
                               Queue.status == 1,
                               Queue.stores_id == stores_id,
                               Queue.queue_setting_id == table_type_id).first()
    return queue

