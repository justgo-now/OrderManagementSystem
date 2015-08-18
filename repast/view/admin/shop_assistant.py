# coding: UTF-8

import logging
from flask.ext.admin.contrib.sqla import ModelView
from wtforms.fields import PasswordField
from flask import request
from repast.models.user import ShopAssistant
from repast.services.shop_assistant_admin_service import ShopAssistantAdmin
from repast.util.others import form_to_dict


log = logging.getLogger('flask-admin.sqla')

class ShopAssistantView(ModelView):
    '''员工管理'''
    ARGS = ('group_id', 'brand_id', 'stores_id', 'name', 'user_name', 'password', 'tel')
    SPECIAL_ARGS = ('group', 'brand', 'stores')
    page_size = 20 # 每页条数
    can_create = True # 创建
    can_edit = True # 更新

    column_exclude_list = ('group_id','brand_id','stores_id','password',)
    column_filters = ('group', 'brand', 'stores',)

    create_template = 'admin_page/shop_assistant_create.html'
    edit_template = 'admin_page/shop_assistant_edit.html'
    list_template = 'admin_page/shop_assistant_list.html'

    column_labels = dict(
        group_id = u'集团',
        group = u'集团',
        brand_id = u'品牌',
        brand = u'品牌',
        stores_id = u'餐厅',
        stores = u'餐厅',
        name = u'昵称',
        user_name = u'帐号',
        password = u'密码',
        tel = u'电话'
    )

    column_descriptions = dict(
        group_id = u'所属集团',
        group = u'所属集团',
        brand_id = u'所属品牌',
        brand = u'所属品牌',
        stores_id = u'所属餐厅',
        stores = u'所属餐厅',
        name = u'店员昵称',
        user_name = u'登录帐号',
        password = u'帐号密码',
        tel = u'手机号码'
    )

    def __init__(self, db, **kwargs):
        super(ShopAssistantView, self).__init__(ShopAssistant, db, **kwargs)

    form_overrides = dict(
        password = PasswordField
    )

    def scaffold_form(self):
        form_class = super(ShopAssistantView, self).scaffold_form()
        delattr(form_class, 'group')
        delattr(form_class, 'brand')
        delattr(form_class, 'stores')
        return form_class


    def create_model(self, form):
        form_dict = form_to_dict(form)
        shop_assistant_admin = ShopAssistantAdmin()
        create_success = shop_assistant_admin.create_shop_assistant(self.session, form_dict, ShopAssistant, self.ARGS, self.SPECIAL_ARGS)
        return create_success

    def update_model(self, form, model):
        form_dict = form_to_dict(form)
        shop_assistant_admin = ShopAssistantAdmin()
        success = shop_assistant_admin.update_shop_assistant(self.session, form_dict, model, self.ARGS, self.SPECIAL_ARGS)
        return success
