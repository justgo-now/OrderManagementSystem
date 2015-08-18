# coding: UTF-8
from flask.ext import restful
from flask.ext.restful import reqparse
from repast.services.queue_setting_service import *
from repast.services.shop_assistant import get_stores_id_by_shop_assistant_id


class AjaxCallNumber(restful.Resource):
    '''如果当前没人排队，必须要刷新页面'''
    @staticmethod
    def get(shop_assistant_id):
        stores_id = get_stores_id_by_shop_assistant_id(shop_assistant_id)
        stores_queue_info = get_now_queue_number_and_number_wait_by_stores_id(stores_id)
        json = []
        if stores_queue_info:
            for s in stores_queue_info:
                message = s.now_number
                type = s.type
                json.append([message, type])
        return json