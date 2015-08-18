# coding: utf-8
from repast.models.package import Package
from repast.models.dish import DishSort, Dish
from repast.util.session_common import set_session_dish, get_session_dish
from ..util.others import flatten

class PackageServiceView():
    '''套餐前台业务逻辑'''
    @staticmethod
    def get_package_by_brand_id(brand_id):
        package = Package.get_package_by_brand(brand_id) # 得到品牌下套餐
        return package

    @staticmethod
    def get_user_add_dish(number):
        '''用户可以在套餐基础上添加菜品'''
        pass

    @staticmethod
    def get_dish_sort_by_package(package_id):
        '''获取套餐所有分类'''
        package = Package.get_package_by_id(package_id)
        dish_sort_array = PackageServiceView.get_dish_sort_array(package)
        dish_sort = PackageServiceView.get_dish_sort(dish_sort_array)

        temp = []
        dish = PackageServiceView.get_dish_by_brand_id(package)
        if dish:
            for d in dish:
                try:
                    if d.package_id == int(package_id):
                        d.number = 1
                    else:
                        d.number = 0
                except:
                    if int(d['package_id']) == int(package_id):
                        d['number'] = 1
                    else:
                        d['numbre'] = 0
                d_pic = flatten(d)
                temp.append(d_pic)
            set_session_dish(temp)
        return dish_sort, dish

    @staticmethod
    def get_dish_price(dish_sort, dish):
        '''获取此套餐总价格'''
        price = 0
        for ds in dish_sort:
            for d in dish:
                if d.dish_sort_id == ds.id:
                    price = price + d.price
        return price

    @staticmethod
    def get_dish_sort(dish_sort_array):
        '''得到分类'''
        temp = []
        if dish_sort_array:
            for dsa in dish_sort_array:
                dish_sort = DishSort.get_dish_sort_by_id(dsa)
                temp.append(dish_sort)
        return temp

    @staticmethod
    def get_dish_by_brand_id(package):
        '''根据分类获取菜品'''
        if package:
            dish = Dish.get_dish_by_package(package)
            return dish
        return None

    @staticmethod
    def get_dish_sort_array(package):
        '''得到每个套餐下的所有分类id'''
        dish_sort_id_array = []
        if package:
            try:
                dish_sort = package.dish_sort_id.split(',') # 如果有多个根据，号分割
                for ds in dish_sort:
                    dish_sort_id_array.append(ds)
            except:
                dish_sort = package.dish_sort_id # 如果没有多个分割会抱异常
                dish_sort_id_array.append(dish_sort)
        return dish_sort_id_array