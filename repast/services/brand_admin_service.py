# coding: utf-8
from base_service import *

class BrandAdminService(BaseService):
    '''brand admin'''
    def create_brand(self, session, form_dict, object, args, special_args=None):
        return self.create_model(session, form_dict, object, args, special_args)

    def update_brand(self, session, form_dict, model, args, special_args=None):
        return self.update_model(session, form_dict, model, args, special_args)
