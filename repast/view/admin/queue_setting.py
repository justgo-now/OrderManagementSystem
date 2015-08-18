# coding: UTF-8
import logging
from flask.ext.admin.contrib.sqla import ModelView
from repast.util.others import form_to_dict
from repast.models.queue import *
from repast.services.table_type_admin_service import TableTypeService

log = logging.getLogger("flask-admin.sqla")


class QueueSettingView(ModelView):
    '''桌型'''
    ARGS = ('type','number','stores_id', 'group_id','brand_id')
    SPECIAL_ARGS = ('stores', 'group', 'brand')
    table_type_service = TableTypeService()
    page_size = 20 # 条数
    can_create = True # 能否创建
    can_edit = True # 能否编辑

    column_exclude_list = ('stores_id','group_id','brand_id','status','id',) # 过滤列
    column_filters = ('group','brand','stores',)

    create_template = 'admin_page/queue_setting_create.html'
    edit_template = 'admin_page/queue_setting_edit.html'
    list_template = 'admin_page/queue_setting_list.html'


    column_labels = dict(
        group_id = u'集团',
        group = u'集团',
        brand_id = u'品牌',
        brand = u'品牌',
        stores_id = '餐厅',
        stores = u'餐厅',
        type = u'桌位类型',
        number = u'桌位数'
    )

    column_descriptions = dict(
        group_id = u'所属集团',
        group = u'所属集团',
        brand_id = u'所属品牌',
        brand = u'所属品牌',
        stores_id = u'所属餐厅',
        stores = u'所属餐厅',
        type = u'桌位类型，(如: 2人桌)',
        number = u'桌位类型数'
    )

    def __init__(self, db, **kwargs):
        super(QueueSettingView, self).__init__(QueueSetting,db, **kwargs)

    def scaffold_form(self):
        form_class = super(QueueSettingView, self).scaffold_form()
        delattr(form_class, 'group')
        delattr(form_class, 'brand')
        delattr(form_class, 'stores')
        delattr(form_class, 'status')
        return form_class

    def create_model(self, form):
        '''覆盖创建model'''
        form_dict = form_to_dict(form)
        return self.table_type_service.create_table_type(self.session, form_dict, QueueSetting, self.ARGS, self.SPECIAL_ARGS)

    def update_model(self, form, model):
        '''覆盖更新model'''
        form_dict = form_to_dict(form)
        return self.table_type_service.update_table_type(self.session, form_dict, model, self.ARGS, self.SPECIAL_ARGS)