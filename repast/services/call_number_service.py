# coding: utf-8
from ..setting.config import *
from ..weixin.webchat import WebChat
from ..services.queue_service import *
from ..services.user_service import *

class PushMessage():
    '''叫号时候推送消息给后面3个人'''
    def push_message(self, queue_id):
        queue = get_q_by_id(queue_id)
        open_id = ''
        if queue:
            now_number = queue.now_queue_number
            prompt_number = now_number + 3
            while True:
                prompt_queue = get_queue_by_now_number(prompt_number, queue.stores_id, queue.queue_setting_id) # 得到当前号码后3位
                if prompt_queue:
                    user_id = prompt_queue.user_id
                    user = get_user_by_id(user_id)
                    if user:
                        open_id = user.openid
                    break
                else:
                    prompt_number = prompt_number - 1
                if prompt_number < 1:
                    break
        webChat = WebChat('1234', APPID, SECRET)
        webChat.send_text_message(open_id, "快到您呢")