# coding: utf-8

from flask.ext.admin.contrib.sqla import ModelView
from repast.util.others import form_to_dict
from repast.models.dish import DishSort
from repast.services.dish_sort_service import DishSortService

class DishSortView(ModelView):
    '''dish sort'''
    ARGS = ('group_id', 'brand_id', 'name')
    SPECIAL_ARGS = ('group', 'brand')
    dish_sort_service = DishSortService()
    page_size = 20
    can_edit = True
    can_create = True

    column_exclude_list = ('group_id', 'brand_id',)
    column_filters = ('group', 'brand',)
    column_searchable_list = ('group', 'brand', 'name',)

    column_labels = dict(
        group_id = u'集团',
        group = u'集团',
        brand = u'品牌',
        brand_id = u'品牌',
        name = u'菜单分类'
    )

    column_descriptions = dict(
        group_id = u'所属集团',
        group = u'所属集团',
        brand = u'所属品牌',
        brand_id = u'所属品牌',
        name = u'菜单分类名称'
    )

    create_template = 'admin_page/dish_sort_create.html'
    list_template = 'admin_page/dish_sort_list.html'
    edit_template = 'admin_page/dish_sort_edit.html'

    def __init__(self, db, **kwargs):
        super(DishSortView, self).__init__(DishSort, db, **kwargs)

    def scaffold_form(self):
        form_class = super(DishSortView, self).scaffold_form()
        delattr(form_class, 'group')
        delattr(form_class, 'brand')
        return form_class


    def create_model(self, form):
        form_dict = form_to_dict(form)
        success = self.dish_sort_service.create_dish_sort(self.session, form_dict, DishSort, self.ARGS, self.SPECIAL_ARGS)
        return success

    def update_model(self, form, model):
        form_dict = form_to_dict(form)
        success = self.dish_sort_service.update_dish_sort(self.session, form_dict, model, self.ARGS, self.SPECIAL_ARGS)
        return success