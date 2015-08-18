#coding:utf-8
from repast.models.dish import *
from flask.ext import restful
from repast.util.others import flatten
from flask import request, render_template, redirect, url_for
from ..util.session_common import get_session_dish, get_session_value, set_session_value


class GetDishes(restful.Resource):
    """ 根据菜的种类获取菜单列表 """
    @staticmethod
    def get(dish_sort_id):
        package_id = request.args.get('package_id')
        #if package_id:
        #    dishes = Dish.get_dish_by_kind_and_package(dish_sort_id)
        #else:
        dishes = Dish.get_dish_by_kind_and_brand(dish_sort_id)
        json = append_json(dishes)
        return json


def append_json(model):
    json = {}
    json['dish'] = []
    json['dish_by_package'] = []
    json['total'] = 0
    dish_id = {}
    dish = get_session_dish()
    yes = get_session_value('yes')
    if yes is None:
        dish_format(dish, json, dish_id)
        set_session_value('yes', None)
    if model:
        dish_format(dish, json, dish_id)
        for i in range(len(model)):
            if dish_id.has_key(str(model[i].id)):
                model[i].number = dish_id.get(str(model[i].id))
            else:
                model[i].number = 0
            model_pic = flatten(model[i])
            json['dish'].append(model_pic)
    else:
        pass
    return json


def dish_format(dish, json, dish_id):
    if dish:
        temp_total = 0
        for d in dish:
            temp_total += int(d['price']) * int(d['number'])
            json['dish_by_package'].append(d['id'])
            dish_id[str(d['id'])] = d['number']
        json['total'] = temp_total

