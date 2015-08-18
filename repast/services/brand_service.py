# coding: UTF-8
from .common_service import GetName
from repast.models.brand import Brand
from flask import flash
from flask.ext.admin.babel import gettext

class BrandService():
    '''品牌'''
    @staticmethod
    def insert_brand(session, form_dict):
        '''添加餐厅'''
        try:
            stores = BrandService.get_brand(form_dict)
            session.add(stores)
            session.commit()
            #pictures = files.getlist('pictures')
            #stores_info = StoresService.save_stores_pictures(stores,pictures)
            #session.add(stores_info)
            #session.commit()
        except Exception,ex:
            flash(gettext('Failed to create model. %(error)s', error=str(ex)), 'error')
            session.rollback()
            return False
        return True

    @staticmethod
    def get_brand(form_dict):
        group_name = GetName._get_group(form_dict)
        return Brand(name=form_dict['name'],
                     description=form_dict['description'],
                     group_id=form_dict['group_id'],
                     group=group_name,
                     manager=form_dict['manager'],
                     tel=form_dict['tel'],
                     email=form_dict['email'])