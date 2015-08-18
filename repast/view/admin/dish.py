# coding: utf-8
from flask.ext.admin.contrib.sqla import ModelView
from flask import request
from wtforms.fields import FileField
from repast.util.others import form_to_dict
from repast.services.dish_service import DishService

from repast.models.dish import Dish

class DishView(ModelView):
    '''dish '''
    ARGS = ('group_id', 'brand_id', 'dish_sort_id', 'price', 'list_price', 'name', 'package_id')
    SPECIAL_ARGS = ('group','brand', 'dish_sort', 'package', 'base_path', 'rel_path', 'picture_name')
    dish_service = DishService()
    page_size = 20
    can_create = True
    can_edit = True

    column_exclude_list = ('group_id', 'brand_id', 'dish_sort_id','base_path', 'rel_path', 'picture_name', 'package_id',)
    column_filters = ('group', 'brand', 'dish_sort','package',)
    column_searchable_list = ('group','brand','dish_sort','name',)

    column_labels = dict(
        group_id = u'集团',
        group = u'集团',
        brand_id = u'品牌',
        brand = u'品牌',
        package = u'套餐',
        package_id = u'套餐',
        dish_sort_id = u'菜单类别',
        dish_sort = u'菜单类别',
        list_price = u'原价',
        price = u'现价',
        name = u'菜品名'
    )

    column_descriptions = dict(
        group_id = u'所属集团',
        group = u'所属集团',
        brand_id = u'所属品牌',
        brand = u'所属品牌',
        package = u'所属套餐',
        package_id = u'所属套餐',
        dish_sort_id = u'所属菜单类别',
        dish_sort = u'所属菜单类别',
        list_price = u'菜品原价',
        price = u'菜品现价',
        name = u'菜品名'
    )

    list_template = 'admin_page/dish_list.html'
    create_template = 'admin_page/dish_create.html'
    edit_template = 'admin_page/dish_edit.html'

    def __init__(self, db, **kwargs):
        super(DishView, self).__init__(Dish, db, **kwargs)

    def scaffold_form(self):
        form_class = super(DishView, self).scaffold_form()
        form_class.pictures = FileField(label=u'菜品图片', description=u'图片')
        delattr(form_class, 'group')
        delattr(form_class, 'brand')
        delattr(form_class, 'dish_sort')
        delattr(form_class, 'package')
        delattr(form_class, 'base_path')
        delattr(form_class, 'rel_path')
        delattr(form_class, 'picture_name')
        return form_class

    def create_model(self, form):
        form_dict = form_to_dict(form)
        success = self.dish_service.create_dish(self.session, form_dict, Dish, self.ARGS, request.files, self.SPECIAL_ARGS)
        return success

    def update_model(self, form, model):
        form_dict = form_to_dict(form)
        success = self.dish_service.update_dish(self.session, form_dict, model, self.ARGS, request.files, self.SPECIAL_ARGS)
        return success