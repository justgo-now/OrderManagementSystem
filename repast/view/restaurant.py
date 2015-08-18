#coding:UTF-8
from flask import render_template,request
from repast.util.session_common import *
from repast.services.queue_service import *

def toRestaurant():
    store_id = request.args.get('id')
    name = request.args.get('name')
    openId = request.args.get('openid')
    set_session_user('openid',openId)
    count = get_queue_count(store_id)
    restaurant = find_queue_by_store_id(store_id)
    return render_template('restaurant.html',
                           count=count,
                           restaurant=restaurant,
                           name=name)


def toRestaurantList():
    return