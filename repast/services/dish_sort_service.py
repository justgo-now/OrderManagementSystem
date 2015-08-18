# coding: utf-8
from base_service import *

class DishSortService(BaseService):
    '''菜单分类'''
    def create_dish_sort(self, session, form_dict, object, args, special_args=None):
        return self.create_model(session, form_dict, object, args, special_args)

    def update_dish_sort(self, session, form_dict, model, args, special_args=None):
        return self.update_model(session, form_dict, model, args, special_args)
