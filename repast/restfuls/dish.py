# coding: utf-8
from flask.ext import restful
from flask.ext.restful import reqparse
from repast.util.session_common import set_session_dish, get_session_dish
from ..models.dish import Dish
from ..util.others import flatten


class AddDish(restful.Resource):
    """
    得到前台用户添加的菜品
    dish_number 菜品有几份
    dish_id 添加菜品的id
    """
    @staticmethod
    def get():
       # set_session_dish(None)

        parse = reqparse.RequestParser()
        parse.add_argument('dish_number', type=str, required=False)
        parse.add_argument('dish_id', type=int, required=True)
        parse.add_argument('package_id', type=str, required=False)
        parse.add_argument('dish_sort_id', type=str, required=False)
        parse.add_argument('operate', type=str, required=False)

        args = parse.parse_args()
        dish_number = args['dish_number']
        dish_id = args['dish_id']
        package_id = args['package_id']
        dish_sort_id = args['dish_sort_id']
        operate = args['operate']

        #用户点菜加减数量操作处理
        dishes = get_session_dish()
        has_dish = True # 判断用户添加的菜品是否在此套餐中
        if dishes:
            temp_bool = False
            for d in dishes:
                if dish_id == d['id']:
                    dish = None
                    has_dish = False
                    if operate == "add":
                        d['number'] = int(d['number']) + 1
                    if int(d['number']) < 1:
                        dishes.remove(d)
                    if operate == "reduce":
                        d['number'] = int(d['number']) - 1
                    temp_bool = False
                    break
                else:
                    temp_bool = True
            if temp_bool:
                dish = Dish.get_dish_by_id(dish_id)
                dish.number = 1
            if dish:
                dish_pic = flatten(dish)
                dishes.append(dish_pic)
        else:
            dishes = []
            if has_dish and operate == "add":
                dish = Dish.get_dish_by_id(dish_id)
                dish.number = 1
                d_pic = flatten(dish)
                dishes.append(d_pic)

        set_session_dish(dishes)


class ShowDish(restful.Resource):
    @staticmethod
    def get():
        dishes = get_session_dish()
        return dishes