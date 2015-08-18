# coding: UTF-8
import logging
from flask.ext.admin.contrib.sqla import ModelView
from wtforms.fields import TextField, FileField, TextAreaField
from repast.util.others import form_to_dict
from repast.models.brand import Brand
from repast.util.others import form_to_dict
from repast.services.brand_admin_service import BrandAdminService

log = logging.getLogger("flask-admin.sqla")

class BrandView(ModelView):
    '''品牌'''
    ARGS = ('name','description','group_id','manager','tel','email')
    SPECIAL_ARGS = ('group',)
    brand_admin_service = BrandAdminService()
    page_size = 20 # 每页条数
    column_display_pk = True # 显示外键
    can_create = True # 能否创建
    can_edit = True # 能否更改

    #column_display_all_relations = ('id','group_id', True)
    column_searchable_list = ('name','description','group',)
    column_exclude_list = ('group_id','description','email','id')

    create_template = 'admin_page/brand_create.html'
    edit_template = 'admin_page/brand_edit.html'
    list_template = 'admin_page/brand_list.html'

    column_labels = dict(
        name = u'品牌名',
        description = u'介绍',
        manager = u'管理人',
        tel = u'电话',
        email = u'邮箱',
        group = u'集团',
        group_id = u'集团'
    )

    column_descriptions = dict(
        name = u'品牌名称',
        description = u'品牌简单介绍',
        manager = u'负责管理此品牌',
        tel = u'手机号码',
        email = u'电子邮箱',
        group = u'所属集团',
        group_id = u'所属集团'
    )

    def __init__(self, db, **kwargs):
        super(BrandView, self).__init__(Brand, db, **kwargs)

    # 描述字段为文本域
    form_overrides = dict(
        description = TextAreaField
    )

    def scaffold_form(self):
        form_class = super(BrandView, self).scaffold_form()
        delattr(form_class, 'group')
        return form_class

    def create_model(self, form):
        '''添加集团'''
        form_dict = form_to_dict(form)
        return self.brand_admin_service.create_brand(self.session, form_dict, Brand, self.ARGS, self.SPECIAL_ARGS)


    def update_model(self, form, model):
        '''添加集团'''
        form_dict = form_to_dict(form)
        return self.brand_admin_service.update_brand(self.session, form_dict, model, self.ARGS, self.SPECIAL_ARGS)