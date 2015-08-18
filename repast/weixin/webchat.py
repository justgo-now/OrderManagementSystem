# coding: utf-8

import hashlib
import urllib2
import urllib
import json

from repast.weixin.message import msg_format


class WebChat(object):
    """微信类"""

    def __init__(self, token, appid=None, secret=None, code=None):
        self.token = token
        self.appid = appid
        self.secret = secret
        self.code = code

    def update(self, appid, secret):
        self.appid = appid
        self.secret = secret

    def validate(self, timestamp, nonce, signature):
        """验证微信接入的参数，成功返回True 否则 False"""
        hash_string = ''.join(sorted([self.token, timestamp, nonce]))
        return signature == hashlib.sha1(hash_string).hexdigest()

    def create_menu(self, menu_string):
        menu_url = self.create_menu_url()
        urllib2.urlopen(menu_url, menu_string.encode('utf-8'))

    def delete_menu(self):
        '''删除菜单'''
        access_token = self.get_access_token()
        delete_menu_url = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=%s" %(access_token)
        urllib2.urlopen(delete_menu_url)

    def oauth_user_info(self):
        '''得到授权后的json字符串'''
        oauth_user_info_url = self.get_oauth_user_info_url()
        result = urllib2.urlopen(oauth_user_info_url)
        return result.read()

    def get_access_token(self):
        """得到access_token"""
        access_token_url = self.token_url()
        f = urllib2.urlopen(access_token_url)
        json_string = f.read()
        return json.loads(json_string)['access_token']

    def token_url(self):
        """返回获取access_token的链接"""
        return "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" \
               % (self.appid, self.secret)

    def oauth_token_url(self):
        '''返回得到授权的access_token链接'''
        return "https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code" \
                % (self.appid, self.secret, self.code)

    def get_oauth_user_info_url(self):
        '''根据得到授权access_token得到获取用户信息url'''
        access_token, oauth_openid = self.get_oauth_access_token()
        return "https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN" \
               % (access_token, oauth_openid)

    def get_oauth_access_token(self):
        '''获得授权的access_token'''
        access_token_url = self.oauth_token_url()
        result = urllib2.urlopen(access_token_url)
        json_string = result.read()
        return json.loads(json_string)['access_token'], json.loads(json_string)['openid']

    def create_menu_url(self):
        """返回创建菜单的url"""
        access_token = self.get_access_token()
        return "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=" + str(access_token)

    def get_ticket_url(self):
        '''获取ticket永久二维码的url'''
        access_token = self.get_access_token()
        url = "https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=%s" %(access_token)
        return url

    def get_ticket(self):
        '''获取ticket换取二维码的凭证'''
        body = {
                    "action_name": "QR_LIMIT_SCENE",
                    "action_info": {
                        "scene": {
                            "scene_id": 1
                        }
                    }
                }
        ticket_url = self.get_ticket_url()
        result_string = urllib2.urlopen(ticket_url, body)
        return json.loads(result_string)['ticket']

    def exchange_by_ticket(self):
        '''根据ticket换取二维码'''
        ticket = self.get_ticket()
        dic = {'key':str(ticket)}
        result = urllib.urlencode(dic)
        ticket = result.split('=')[1]
        exchange_by_ticket_url = "https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=%s" %(ticket)
        json_string = urllib2.urlopen(exchange_by_ticket_url)
        result = json.loads(json_string)['url']
        return result

    def get_user_info(self, openid):
        '''根据openid获取用户信息'''
        access_token = self.get_access_token()
        user_info_url = "https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN" %(access_token, openid)
        result = urllib2.urlopen(user_info_url)
        json_string = result.read()
        nickname = json.loads(json_string)['nickname']
        avatar_img_url = json.loads(json_string)['headimgurl']
        return {'nickname': nickname, 'img_url':avatar_img_url}

    def send_message_url(self):
        '''url路径'''
        access_token = self.get_access_token()
        message_url = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s" %(access_token)
        return message_url


    def send_text_message(self, openid, content):
        body = '{"touser": "'+openid+'","msgtype":"text","text":{"content":"'+content+'"}}'
        message_url = self.send_message_url()
        req = urllib2.Request(message_url) # 请求post请求
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        response = opener.open(req, body)
        json_string = response.read() # 得到请求后json string
        err_message = json.loads(json_string)['errmsg'] # 查看返回json string的error message
        print json.loads(json_string)['errcode']
        return err_message

    def transcoding(self, content):
        """转换编码utf-8 > ascii"""
        content = content.decode('utf-8')
        content = content.encode('ascii')
        return content


    @staticmethod
    def reply(msg_type, msg_dict):
        return msg_format(msg_type, msg_dict)
