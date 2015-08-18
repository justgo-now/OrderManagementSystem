#coding:utf8

from repast.models.queue import Queue
from repast.models.user import *
from repast.services.queue_setting_service import *
from repast.weixin.webchat import WebChat
import time
from repast.services.user_service import *
from repast.services.queue_setting_service import get_schedule_by_user_id

def loop_message(openid,web_chat,content):
    user_service = UserService()
    user = user_service.get_user_by_openid(openid)
    schedule = get_schedule_by_user_id(user.id)
    if schedule:
            web_chat.send_text_message(openid,content)

def loop_time(web_chat):
    args_time = get_date_time_str()
    queue = Queue.query.filter(Queue.queue_time.like(args_time),Queue.user_id != '',Queue.status == 1).all()
    if queue:
            for q in queue:
                num = q.now_queue_number-1
                con = "You have "
                content=con+str(num)
                user = User.query.filter(User.id == q.user_id).first()
                loop_message(user.openid,web_chat,content)

if __name__ == '__main__':
    web_chat = WebChat('1234','wx55970915710ceae8','0a9fcd79087745628d8eb5dd5fb9c418')
    while True:
        time.sleep(180)
        loop_time(web_chat)
