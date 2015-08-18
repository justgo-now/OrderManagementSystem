# coding: utf-8
from ..models.user import Menu, DishUserMenu
from ..models.dish import *


class UserMenuService():
    """用户菜单"""
    @staticmethod
    def get_menu_by_user_id(user_id):
        user_menu = Menu.get_user_menu_by_user_id(user_id)
        temp_menu = {}
        temp_menu['stores'] = []
        total = 0
        for um in user_menu:
            dish_array = UserMenuService.fix_user_menu_dish_ids(um)
            temp_menu['stores'] = dish_array
            for dish in dish_array:
                temp_menu['stores'].append(dish)
                price = dish.price * dish.number
                total += price
            temp_menu[str(um.stores_id)] = total
        return user_menu

    @staticmethod
    def fix_user_menu_dish_ids(user_menu):
        """得到用选择的菜和菜的个数"""
        dish_id_array = []
        dish_array = []
        if user_menu:
            dish_id_array = user_menu.dish_nuber_id.split(',')  # 使用逗号分隔得到一个id数组
            for dish_id in dish_id_array:
                dish_center = DishUserMenu.get_dish_number_menu_by_id(dish_id)  # 得到菜品id和number
                dish = Dish.get_dish_by_id(dish_center.dish_id)  # 得到菜品
                dish.number = dish_center.dish_number
                dish_array.append(dish)
        return dish_array


    @staticmethod
    def add_menu(dish, user_id, stores_id):
        dish_id_array = []
        for d in dish:
            dish_user_menu = DishUserMenu.add_dish_number_menu(d['id'], d['number'])
            dish_id_array.append(dish_user_menu.id)
        dish_string = UserMenuService.fix_dish_id_array(dish_id_array)
        Menu.add_user_menu(dish_string, user_id, stores_id)


    @staticmethod
    def fix_dish_id_array(dish_id_array):
        dish_string = ''
        array_len = len(dish_id_array)
        temp_len = 0
        for dish_id in dish_id_array:
            temp_len += 1
            if temp_len == array_len:
                dish_string += str(dish_id)
            else:
                dish_string += str(dish_id) + ','
        return dish_string