# coding: utf-8
from .base_service import *

class PackageService(BaseService):
    """
    param:
         session: 事物session
         form_dict: 表单提交数据
         Object: 实体
         args: 实体所有属性（列）
         args2: 需要特殊处理属性
    """
    def create_package(self, session, form_dict, Object, args, args2, sort_list):
        '''创建实体'''
        try:
            model = self.get_sort_model(Object, args, form_dict, args2, sort_list)
            session.add(model)
            session.commit()
        except Exception, e:
            flash(gettext('创建失败. %(error)s', error=str(e)), 'error')
            session.rollback()
            return False
        return True

    def update_package(self, session, form_dict, model, args, special_args=None):
        return self.update_model(session, form_dict, model, args, special_args)

    def get_sort_model(self, object, args, form_dict, special_args=None, sort_list=None):
        dictionary = self.get_sort_dictionary(form_dict, args, sort_list, special_args)
        model = object(**dictionary)
        return model

    def get_sort_dictionary(self, form_dict, args, sort_list, special_args=None):
        '''获取所有实体的属性key和value'''
        dictionary = {}
        for arg in args:
            dictionary[str(arg)] = form_dict[str(arg)]
        if special_args != None:
            for arg in special_args:
                if arg == 'group':
                    dictionary[str(arg)] = GetName._get_group(form_dict)
                if arg == 'brand':
                    dictionary[str(arg)] = GetName._get_brand(form_dict)
                if arg == 'stores':
                    dictionary[str(arg)] = GetName._get_stores(form_dict)
                if arg == 'dish_sort':
                    dictionary[str(arg)] = GetName._get_dish_sort(sort_list)
                if arg == 'dish_sort_id':
                    dictionary[str(arg)] = GetName._get_dish_sort_id(sort_list)
        return dictionary
