# coding: utf-8
from flask.ext.admin.contrib.sqla import ModelView
from flask import request
from repast.util.others import form_to_dict
from repast.models.package import Package
from repast.services.package_service import PackageService

class PackageView(ModelView):
    ARGS = ('name', 'group_id','brand_id', 'suitable_number')
    SPECIAL_ARGS = ('group', 'brand', 'dish_sort_id', 'dish_sort')
    page_size = 20
    can_create = True

    column_exclude_list = ('group_id','brand_id', 'dish_sort_id',)
    column_filters = ('group', 'brand', 'dish_sort',)
    column_searchable_list = ('group', 'brand', 'dish_sort', 'name',)

    column_labels = dict(
        name = u'套餐',
        group_id = u'集团',
        group = u'集团',
        brand_id = u'品牌',
        brand = u'品牌',
        dish_sort_id = u'菜单类型',
        dish_sort = u'菜单类型',
        suitable_number = u'人数'
    )

    column_descriptions = dict(
        name = u'套餐名',
        group_id = u'所属集团',
        group = u'所属集团',
        brand_id = u'所属品牌',
        brand = u'所属品牌',
        dish_sort_id = u'菜单类型',
        dish_sort = u'菜单类型',
        suitable_number = u'适应人数'
    )

    def __init__(self, db, **kwargs):
        super(PackageView, self).__init__(Package, db, **kwargs)

    create_template = 'admin_page/package_create.html'
    edit_template = 'admin_page/package_edit.html'
    list_template = 'admin_page/package_list.html'

    def scaffold_form(self):
        form_class = super(PackageView, self).scaffold_form()
        delattr(form_class, 'group')
        delattr(form_class, 'brand')
        delattr(form_class, 'dish_sort')
        return form_class

    def create_model(self, form):
        form_dict = form_to_dict(form)
        package_service = PackageService()
        sort_list = request.form.getlist('dish_sort_id')
        success = package_service.create_package(self.session, form_dict, Package, self.ARGS, self.SPECIAL_ARGS, sort_list)
        return success

    def update_model(self, form, model):
        form_dict = form_to_dict(form)
        package_service = PackageService()
        package_service.update_package(self.session, form_dict, model, self.ARGS, self.SPECIAL_ARGS)