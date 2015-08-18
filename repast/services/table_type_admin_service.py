# coding: utf-8
from base_service import *

class TableTypeService(BaseService):
    '''table type admin service'''
    def create_table_type(self, session, form_dict, Object, args, special_args=None):
        if (self.check_table_type_is_exist(form_dict, Object)):
            return False
        return self.create_model(session, form_dict, Object, args, special_args)

    def update_table_type(self, session, form_dict, model, args, special_args=None):
        return self.update_model(session, form_dict, model, args, special_args)


    def check_table_type_is_exist(self, form_dict, Object):
        stores_id = form_dict['stores_id']
        type = form_dict['type']
        table_type = Object.query.filter(Object.stores_id == stores_id, Object.type == type).first()
        if table_type:
            flash(gettext('创建桌型失败. %(error)s', error='此餐厅已有此桌型'), 'error')
            return True
        return False