# coding: UTF-8
import logging
import os
import Image
from flask.ext.admin.contrib.sqla import ModelView
from wtforms.fields import TextField, FileField, TextAreaField
from repast.services.group_admin_service import GroupAdminService
from repast.models.group import Group
from repast.util.others import form_to_dict

log = logging.getLogger("flask-admin.sqla")

class GroupView(ModelView):
    '''集团'''
    ARGS = ('name', 'description','address','group_person_in_charge','tel')
    SPECIAL_ARGS = None
    group_admin_service = GroupAdminService()
    page_size = 20 # 每页显示条数
    can_create = True # 能否创建
    can_edit = True # 能否修改

    column_searchable_list = ('name',)
    column_exclude_list = ('email','description',) # 过滤列名
    # 后台列表显示列名，以及修改，新增
    column_labels = dict(
        name = u'集团名',
        description = u'介绍',
        address = u'地址',
        group_person_in_charge = u'负责人',
        tel = u'电话'
    )
    # 列名的描述
    column_descriptions = dict(
        name = u'集团名',
        description = u'集团简单介绍',
        address = u'集团地址',
        group_person_in_charge = u'负责人',
        tel = u'手机号码'
    )

    create_template = 'admin_page/group_create.html'
    edit_template = 'admin_page/group_edit.html'
    list_template = 'admin_page/group_list.html'
    # 新增修改，描述为文本域
    form_overrides = dict(
        description = TextAreaField
    )

    def scaffold_form(self):
        form_class = super(GroupView, self).scaffold_form()
        delattr(form_class, 'email')
        return form_class

    def create_model(self, form):
        '''添加集团'''
        form_dict = form_to_dict(form)
        return self.group_admin_service.create_group(self.session, form_dict, Group, self.ARGS, self.SPECIAL_ARGS)

    def update_model(self, form, model):
        form_dict = form_to_dict(form)
        return self.group_admin_service.update_group(self.session, form_dict, model, self.ARGS, self.SPECIAL_ARGS)

    def __init__(self, db, **kwargs):
        super(GroupView, self).__init__(Group, db, **kwargs)