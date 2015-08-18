# coding: utf-8
from flask import request, make_response
from xml.etree import ElementTree as ET
from repast.weixin.tools import parse_request
from repast.weixin.webchat import WebChat
from repast.setting.server import BASE_URL
#from repast.util.session_common import *
from repast.services.user_service import *
from repast.services.stores_service import get_stores_by_id
from repast.services.queue_setting_service import get_schedule_by_user_id

from repast.services.queue_setting_service import *

def weixin():
    web_chat = WebChat('1234','wx74cda484a2ba4fc2','613db0445596a3d5dd39b7f418979c1f')


    if request.method == "GET":
        if web_chat.validate(**parse_request(request.args, ("timestamp", "nonce", "signature"))):
            print make_response(request.args.get("echostr"))
            return make_response(request.args.get("echostr"))
        raise LookupError

    if request.method == "POST":
        # 这里需要验证 #todo
        xml_recv = ET.fromstring(request.data)
        MsgType = xml_recv.find("MsgType").text

        if MsgType == "event":
            return response_event(xml_recv, web_chat, request)
        if MsgType == "text":
            return response_text(xml_recv, web_chat)
        if MsgType == 'voice':
            return response_voice(xml_recv, web_chat)
        if MsgType == 'location':
            return response_location(xml_recv, web_chat)


def response_location(xml_recv, web_chat):
    '''用户手动发送地理位置'''

    FromUserName = xml_recv.find('FromUserName').text
    ToUserName = xml_recv.find('ToUserName').text
    latitude = xml_recv.find('Location_X').text
    longitude = xml_recv.find('Location_Y').text
    label = xml_recv.find('Label').text
    Content = str(label)
    user_service = UserService() #
    dictionary = web_chat.get_user_info(FromUserName)
    user = user_service.check_user_by_openid(FromUserName, dictionary['nickname'], dictionary['img_url'])
    user_service.get_location_and_save(FromUserName, longitude, latitude, label)
    reply_dict = response_event_message(FromUserName, ToUserName, Content)
    return response(web_chat,reply_dict, 'text')



def response_voice(xml_receive, web_chat):
    '''对于用户语音进行处理'''
    recognition = xml_receive.find("Recognition").text
    toUserName = xml_receive.find("ToUserName").text # 得到接受者
    fromUserName = xml_receive.find("FromUserName").text # 得到发送者
    reply_dict = {
        "ToUserName": fromUserName,
        "FromUserName": toUserName,
        "CreateTime": 12345,
        "Content": recognition
    }
    return response(web_chat, reply_dict, 'text')

def response_text(xml_receive, web_chat):
    '''回复'''
    Content = "总是这样"
    ToUserName = xml_receive.find("ToUserName").text
    FromUserName = xml_receive.find("FromUserName").text
    reply_dict = response_event_message(FromUserName, ToUserName, Content)
    return response(web_chat, reply_dict, 'text')

def response_event(xml_recv, web_chat, request):
    Event = xml_recv.find("Event").text
    EventKey = xml_recv.find("EventKey").text
    ToUserName = xml_recv.find("ToUserName").text
    FromUserName = xml_recv.find("FromUserName").text


    user_service = UserService() #
    dictionary = web_chat.get_user_info(FromUserName)
    user = user_service.check_user_by_openid(FromUserName, dictionary['nickname'], dictionary['img_url'])

    reply_dict = response_event_message(FromUserName, ToUserName, '感谢关注！')
    if (Event == 'CLICK' and EventKey == 'home'):
        reply_dict = event_click(FromUserName, ToUserName, user)
        return response(web_chat, reply_dict, "news")
    if (Event == 'CLICK' and EventKey == 'schedule'):
        reply_dict = event_schedule(FromUserName, ToUserName, user)
        return response(web_chat, reply_dict, 'text')
    if (Event == 'CLICK' and EventKey == 'my'):
        reply_dict = event_my(FromUserName,ToUserName, user)
        return response(web_chat, reply_dict, 'news')
    if (Event == 'subscribe'):
        reply_dict = event_subscribe(FromUserName, ToUserName, EventKey, user)
        return response(web_chat, reply_dict, "news")
    if (Event == 'SCAN'):
        reply_dict = event_scan(FromUserName, ToUserName, EventKey, user, request)
        return response(web_chat, reply_dict, "text")
    if (Event == 'LOCATION'):
        longitude = xml_recv.find("Latitude").text
        latitude = xml_recv.find("Longitude").text
        reply_dict = event_location(user_service, longitude, latitude, FromUserName, ToUserName)
        return response(web_chat, reply_dict, 'text')
    return response(web_chat, reply_dict, "text")


def event_my(FromUserName, ToUserName, user):
    '''我的排队，我的订单，我的账单，我的优惠'''
    reply_dict = {
            "ToUserName": FromUserName,
            "FromUserName": ToUserName,
            "ArticleCount": 4,
            "item": [{
                "Title": '我的账户',
                "Description": '微生活 | 微一切',
                "PicUrl": BASE_URL + '/static/images/image_queue.jpg',
                "Url": '%s/m/my_page/?user_id=%s' %(BASE_URL, user.id)
            },{
                "Title": '我的排队',
                "Description": '微生活 | 微一切',
                "PicUrl": BASE_URL + '/static/images/stores/Customized.jpg',
                "Url":  '%s/m/my_line_up?user_id=%s' %(BASE_URL, user.id)
            },{
               "Title": '我的优惠',
                "Description": '微生活 | 微一切',
                "PicUrl": BASE_URL + '/static/images/stores/preferential.png',
                "Url": '%s/m/my_coupons/?user_id=%s' %(BASE_URL, user.id)
            },{
                "Title": '我的菜单',
                "Description": '微生活 | 微一切',
                "PicUrl": BASE_URL + '/static/images/stores/bill.jpg',
                "Url": '%s/f/to_dish_selected' %(BASE_URL)
            }]
    }

    return reply_dict



def event_schedule(FromUserName, ToUserName, user):
    '''进度'''
    schedule = get_schedule_by_user_id(user.id)
    Content = ''
    if schedule:
        for s in schedule:
            Content = Content + '%s。%s。您的排队号数为%s号。前面有%s位等候者,请您耐心等候。(过号作废)' %(s.stores_name, s.table_type, s.now_queue_number, s.schedule_count)
            Content = Content + '\n'
    else:
        Content = '您还没任何排队信息！'
    reply_dict = response_event_message(FromUserName, ToUserName, Content)
    return reply_dict


def event_location(user_service, longitude, latitude, FromUserName, ToUserName):
    '''响应获取地理位置'''
    user_service.get_location_and_save(FromUserName, longitude, latitude)
    Content = "longitude" + str(longitude)
    reply_dict = response_event_message(FromUserName, ToUserName, Content)
    user_service=UserService()
    user_service.get_location_and_save(FromUserName, longitude, latitude,'')
    return reply_dict

def get_schedule(user):
    schedule = get_schedule_by_user_id(user.id)
    mark_queue = 0
    table_type_id = 0
    if schedule:
        for s in schedule:
            mark_queue = s.stores_id
            table_type_id = s.queue_setting_id
    return mark_queue, table_type_id


def event_click(FromUserName, ToUserName, user):
    '''响应click事件'''
    mark_queue, table_type_id = get_schedule(user)
    reply_dict = {
            "ToUserName": FromUserName,
            "FromUserName": ToUserName,
            "ArticleCount": 3,
            "item": [{
                "Title": '主页',
                "Description": '微生活 | 微一切',
                "PicUrl": BASE_URL + '/static/images/image_home.jpg',
                "Url": '%s/home_page/?user_id=%s&mark_queue=%s' %(BASE_URL, user.id, mark_queue)
            },{
                "Title": '去排队',
                "Description": '微生活 | 微一切',
                "PicUrl": BASE_URL + '/static/images/image_queue.jpg',
                "Url": '%s/q/search/?user_id=%s' %(BASE_URL, user.id)
            },{
               "Title": '去点餐',
                "Description": '微生活 | 微一切',
                "PicUrl": BASE_URL + '/static/images/image_meal.jpg',
                "Url": '%s/f/meal_restaurant?user_id=%s' %(BASE_URL, user.id)
            }
            ]
    }
    return reply_dict

def event_view(FromUserName, ToUserName):
    '''view事件'''
    Content = str(FromUserName)
    reply_dict = response_event_message(FromUserName, ToUserName, Content)
    return reply_dict

def event_subscribe(FromUserName, ToUserName, EventKey, user):
    '''用户扫二维码未关注，点击关注后的事件'''
    stores_id = EventKey.split('_')[1]
    title, description, pic_url = get_stores_(stores_id)
    mark_queue, table_type_id = get_schedule(user)
    reply_dict = {
            "ToUserName": FromUserName,
            "FromUserName": ToUserName,
            "ArticleCount": 1,
            "item": [{
                "Title": title,
                "Description": title +'\n'+ "去排队",
                "PicUrl": BASE_URL + pic_url,
                "Url": '%s/q/queue/%s?user_id=%s&mark_queue=%s' %(BASE_URL, stores_id, user.id, mark_queue)
            }]
    }
    return reply_dict


def get_stores_(stores_id):
    stores = get_stores_by_id(stores_id)
    title = '餐厅'
    description = '介绍'
    pic_url = '/static/images/stores/miaomiao.jpeg'
    if stores:
        title = stores.name
        description = stores.description
        pic_url = stores.image_url
    return title, description, pic_url


def event_scan(FromUserName, ToUserName, EventKey, user, request):
    '''用户扫二维码已关注'''
    stores_id = EventKey
    title, description, pic_url = get_stores_(stores_id)
    mark_queue, table_type_id = get_schedule(user)
    url = '%s/q/queue/%s?user_id=%s&mark_queue=%s' %(BASE_URL, stores_id, user.id, mark_queue)
    reply_dict = {
            "ToUserName": FromUserName,
            "FromUserName": ToUserName,
            "CreateTime": 1,
            "Content": request.args.get('ticket')
    }
    return reply_dict

def check_repast(stores_id):
    '''判断是那个餐厅'''
    name = ''
    if stores_id == '1':
        name = '喵喵餐厅'
    if stores_id == '2':
        name = '饭饭餐厅'
    return name


def response_event_message(FromUserName, ToUserName, Content):
    '''响应事件'''
    reply_dict = {
            "ToUserName": FromUserName,
            "FromUserName": ToUserName,
            "CreateTime": 1,
            "Content": Content
    }
    return reply_dict

def response(web_chat, reply_dict, reply_type):
    """通过返回的xml与类型，创建一个回复"""
    reply = web_chat.reply(reply_type, reply_dict)
    reply_response = make_response(reply)
    reply_response.content_type = 'application/xml'
    return reply_response


#def by_openId(openId):
#    '''得到openid获取用户'''
#    boolean = get_student_by_openId(openId)
#    return boolean


def get_type(Content):
    """返回用户输入的业务类型
    "jia" 或者 "gai" 值得是用户进行手机号码绑定与修改手机号码
    None 未知类型，不是相关的业务
    """
    if Content.startswith("jia"):
        return "jia"
    if Content.startswith("gai"):
        return "gai"
    if Content.startswith("授权"):
        return "授权"



HELP = "感谢关注客聚科技平台，输入'h'获取帮助信息"

