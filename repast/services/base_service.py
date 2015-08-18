# coding: UTF-8
from repast.services.common_service import GetName
from flask import flash
from flask.ext.admin.babel import gettext

class BaseService(object):
    def create_model(self, session, form_dict, object, args, special_args=None):
        '''创建实体'''
        try:
            model = self.get_model(object, args, form_dict, special_args)
            session.add(model)
            session.commit()
        except Exception, e:
            flash(gettext('创建失败. %(error)s', error=str(e)), 'error')
            session.rollback()
            return False
        return True

    def update_model(self, session, form_dict, model, args, special_args=None):
        '''更新实体'''
        try:
            dictionary = self.get_dictionary(form_dict, args, special_args)
            model.update(**dictionary)
            session.commit()
        except Exception, e:
            flash(gettext('修改失败. %(error)s', error=str(e)), 'error')
            session.rollback()
            return False
        return True

    def get_model(self, object, args, form_dict, special_args=None):
        '''得到一个新的实体'''
        dictionary = self.get_dictionary(form_dict, args, special_args)
        model = object(**dictionary)
        return model

    def get_dictionary(self, form_dict, args, special_args=None):
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
                    dictionary[str(arg)] = GetName._get_dish_sort(form_dict)
                if arg == 'dish_sort_id':
                    dictionary[str(arg)] = GetName._get_dish_sort_id(form_dict)
        return dictionary