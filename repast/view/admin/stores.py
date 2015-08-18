# coding: UTF-8
import logging
import os
from flask.ext.admin.contrib.sqla import ModelView
from flask import request
from flask.ext import login


from wtforms.fields import TextAreaField, FileField
from repast.models.stores import Stores
from repast.services.stores_service import StoresService
from repast.services.stores_admin_service import StoresAdminService
from repast.util.others import form_to_dict

log = logging.getLogger("flask-admin.sqla")

class StoresView(ModelView):
    '''品牌'''
    ARGS = ('name','address', 'description','longitude','latitude','brand_id','manager',
        'tel','group_id','province_id','city_id','country_id','stars')
    SPECIAL_ARGS = ('brand','group')
    stores_admin_service = StoresAdminService()
    page_size = 20 # 每页条数
    column_display_pk = True # 显示外键
    can_create = True # 能否创建
    can_edit = True # 能否更改

    #column_display_all_relations = ('id','group_id', True)
    column_searchable_list = ('name','description','group',)
    column_exclude_list = ('group_id','brand_id','province_id','city_id','country_id','longitude','latitude','recommend','description','id','hours',)
    column_filters = ('group','brand',)

    create_template = 'admin_page/stores_create.html'
    edit_template = 'admin_page/stores_edit.html'
    list_template = 'admin_page/stores_list.html'

    column_labels = dict(
        name = u'餐厅名',
        address = u'餐厅地址',
        description = u'介绍',
        group_id = u'集团',
        group = u'集团',
        brand_id = u'品牌',
        brand = u'品牌',
        province_id = u'省份',
        city_id = u'市',
        country_id = u'区',
        manager = u'负责人',
        tel = u'电话',
        stars = u'星级'

    )

    column_descriptions = dict(
        name = u'餐厅名',
        address = u'详细地址',
        description = u'餐厅介绍',
        group_id = u'所属集团',
        group = u'所属集团',
        brand_id = u'所属品牌',
        brand = u'所属品牌',
        province_id = u'所属省份',
        city_id = u'所属市',
        country_id = u'所属区',
        manager = u'负责人',
        tel = u'电话电话',
        stars = u'餐厅级别(1-5)'
    )

    def __init__(self, db, **kwargs):
        super(StoresView, self).__init__(Stores, db, **kwargs)

    #def is_accessible(self):
    #    return login.current_user.is_superuser()

    # 描述字段为文本域
    form_overrides = dict(
        description = TextAreaField
    )

    def scaffold_form(self):
        form_class = super(StoresView, self).scaffold_form()
        form_class.pictures = FileField(label=u'餐厅图片', description=u'图片')
        delattr(form_class, 'group')
        delattr(form_class, 'brand')
        delattr(form_class, 'recommend')
        delattr(form_class, 'hours')
        return form_class

    def create_model(self, form):
        '''添加集团'''
        form_dict = form_to_dict(form)
        return self.stores_admin_service.create_stores(self.session, form_dict, Stores, self.ARGS, request.files, self.SPECIAL_ARGS)


    def update_model(self, form, model):
        '''修改餐厅'''
        form_dict = form_to_dict(form)
        return self.stores_admin_service.update_stores(self.session, form_dict, model, self.ARGS, request.files, self.SPECIAL_ARGS)