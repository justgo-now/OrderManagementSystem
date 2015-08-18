# coding: utf-8
from base_service import BaseService
import hashlib

class ShopAssistantAdmin(BaseService):
    '''店员后台'''
    def create_shop_assistant(self, session, form_dict, object, args, special_args=None):
        form_dict = self.encryption_password(form_dict)
        return self.create_model(session, form_dict, object, args, special_args)

    def update_shop_assistant(self, session, form_dict, model, args, special_args=None):
        form_dict = self.encryption_password(form_dict)
        return self.update_model(session, form_dict, model, args, special_args)

    def encryption_password(self, form_dict):
        if form_dict.has_key('password') and form_dict['password']:
            password = form_dict['password']
            password = hashlib.new('md5', password).hexdigest()
            form_dict['password'] = password
        return form_dict