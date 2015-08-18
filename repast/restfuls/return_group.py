# coding: UTF-8

from ..models.group import Group
from ..models.brand import Brand
from ..models.stores import Stores
from ..models.location import *
from ..models.dish import DishSort
from ..models.package import Package
from flask.ext import restful
from ..util.session_common import *

class GetGroup(restful.Resource):
    '''获取集团'''
    @staticmethod
    def get():
        group = Group.query.filter().all()
        json = append_json(group)
        return json


class GetBrand(restful.Resource):
    '''获取品牌'''
    @staticmethod
    def get(group_id):
        brand = Brand.query.filter(Brand.group_id == group_id).all()
        json = append_json(brand)
        return json


class GetProvince(restful.Resource):
    '''获取省'''
    @staticmethod
    def get():
        province = Province.query.filter().all()
        json = append_json(province)
        return json

class GetCity(restful.Resource):
    '''获取市'''
    @staticmethod
    def get(province_id):
        city = City.query.filter(City.province_id == province_id).all()
        json = append_json(city)
        return json

class GetCountry(restful.Resource):
    '''获取区'''
    @staticmethod
    def get(city_id):
        country = Country.query.filter(Country.city_id == city_id).all()
        json = append_json(country)
        return json


class GetStores(restful.Resource):
    '''获取餐厅'''
    @staticmethod
    def get(brand_id):
        stores = Stores.query.filter(Stores.brand_id == brand_id).all()
        json = append_json(stores)
        return json

class GetDishSort(restful.Resource):
    '''获取菜品分类'''
    @staticmethod
    def get(brand_id):
        dish_sort = DishSort.get_dish_sort_by_brand_id(brand_id)
        temp = []
        if dish_sort:
            for d in dish_sort:
                temp.append(d)
        json = append_json(temp)
        return json


class GetDishSortDish(restful.Resource):
    '''获取菜品分类'''
    @staticmethod
    def get(package_id):
        package = Package.get_package_by_id(package_id)
        array_sort = []
        temp = []
        if package and len(package.dish_sort_id) > 1:
            array_sort = package.dish_sort_id.split(',')
        else:
            array_sort = package.dish_sort_id
        for sort in array_sort:
            dish_sort = DishSort.get_dish_sort_by_id(sort)
            temp.append(dish_sort)
        json = append_json(temp)
        return json


class GetPackage(restful.Resource):
    '''获取套餐'''
    @staticmethod
    def get(brand_id):
        package = Package.query.filter(Package.brand_id == brand_id).all()
        json = append_json(package)
        return json


def append_json(model):
    json = []
    if model:
        for i in range(len(model)):
            json.append([model[i].id, model[i].name])
    return json