# coding: UTF-8
from flask import request, render_template
from repast.services.queue_setting_service import *
from repast.services.shop_assistant import *

from repast.util.session_common import *

def do_queue(table_type_id):
    '''用户排队'''
    #user_id = get_session('user_id') # 得到当前用户id
    user_id = 4
    #stores_id = request.args.get('stores_id') # 用户排队的餐厅
    stores_id = 6
    #queue = check_queue_by_user_id_and_stores_id(user_id, stores_id, table_type_id) # 判断是否已经存在队列当中
    #if queue:
    #    message = '您已在队列中，当前号码为%s' %(queue.now_queue_number) # 如果存在队列中，提示
    #    print message
    #else:
    queue = create_queue(user_id, stores_id, table_type_id)
    print queue.now_queue_number


def cancel_queue(queue_id):
    '''取消队列'''
    cancel(queue_id)


def shop_assistant_call_number(queue_id):
    '''店员叫号'''
    success_call_number = call_number(queue_id)


def queue_page(stores_id):
    '''排队页面'''
    temp = get_queue_by_stores_id(stores_id)
    for t in temp:
        print t.type +' '+ str(t.queue_number)


def call_number_page(stores_id):
    '''叫号'''
    json = get_now_queue_number_and_number_wait_by_stores_id(stores_id)
    for j in json:
        print str(j.now_number) + ' ' + str(j.wait_number)

if __name__ == '__main__':
    #do_queue(5)
    queue_info = get_schedule_by_user_id(4)
    for queue in queue_info:
        print '前面还有'+str(queue.schedule_count)
        print queue.stores_name
        print '当前号码'+str(queue.now_queue_number)
    #cancel(1)
    #shop_assistant_call_number(6)
    #queue_page(6)
    #call_number_page(6)




