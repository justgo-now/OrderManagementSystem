# coding: UTF-8
from repast.models.stores import Stores, StoresInfo
from repast.services.common_service import GetName
from flask import flash
from flask.ext.admin.babel import gettext
import os
from werkzeug import secure_filename
from repast.util.ex_file import *
from repast.setting.server import *
from sqlalchemy import or_, and_
#from repast.setting.wbb import *

class StoresService():
    '''餐厅'''
    @staticmethod
    def insert_stores(session, form_dict, files):
        '''添加餐厅'''
        try:
            stores = StoresService.get_stores(form_dict)
            session.add(stores)
            session.commit()
            pictures = files.getlist('pictures')
            stores_info = StoresService.save_stores_pictures(stores,pictures)
            session.add(stores_info)
            session.commit()
        except Exception,ex:
            flash(gettext('Failed to create model. %(error)s', error=str(ex)), 'error')
            session.rollback()
            return False
        return True

    @staticmethod
    def update_stores(model, session, form_dict, files):
        '''更新stores'''
        is_true = True
        try:
            group_name = GetName._get_group(form_dict)
            form_dict['group'] = group_name
            brand_name = GetName._get_brand(form_dict)
            form_dict['brand'] = brand_name
            model.update(**form_dict)
            session.commit()
            pictures = files.getlist('pictures')
            is_true = StoresService.update_stores_pictures(session, model, pictures)
        except Exception, ex:
            flash(gettext('Failed to update model. %(error)s', error=str(ex)), 'error')
            session.rollback()
            is_true = False
        return is_true


    @staticmethod
    def get_stores(form_dict):
        group_name = GetName._get_group(form_dict)
        brand_name = GetName._get_brand(form_dict)
        stores = Stores(name=form_dict['name'],
                        address=form_dict['address'],
                        description=form_dict['description'],
                        longitude=form_dict['longitude'],
                        latitude=form_dict['latitude'],
                        brand_id=form_dict['brand_id'],
                        brand=brand_name,
                        manager=form_dict['manager'],
                        tel=form_dict['tel'],
                        group_id=form_dict['group_id'],
                        group=group_name,
                        province_id=form_dict['province_id'],
                        city_id=form_dict['city_id'],
                        country_id=form_dict['country_id'],
                        stars=form_dict['stars'])
        return stores
    @staticmethod
    def save_stores_pictures(stores, pictures):
        for picture in pictures:
            if not allowed_file_extension(picture.filename, STORES_PICTURE_ALLOWED_EXTENSION):
                continue
            else:
                upload_name = picture.filename
                base_path = STORES_PICTURE_BASE_PATH
                rel_path = STORES_PICTURE_REL_PATH
                pic_name = time_file_name(secure_filename(upload_name), sign='_')

                picture.save(os.path.join(base_path+rel_path+'/', pic_name))

                stores_info = StoresInfo(stores_id=stores.id,
                                         base_path=base_path,
                                         rel_path=rel_path,
                                         picture_name=pic_name)
                return stores_info

    @staticmethod
    def update_stores_pictures(session, stores, pictures):
        '''更新餐厅图片'''
        picture_length = len(pictures)
        if picture_length != 1:
            for picture in pictures:
                if not allowed_file_extension(picture.filename, STORES_PICTURE_ALLOWED_EXTENSION):
                    continue
                else:
                    stores_info = StoresInfo.query.filter(StoresInfo.stores_id == stores.id).first()
                    upload_name = picture.filename
                    base_path = STORES_PICTURE_BASE_PATH
                    rel_path = STORES_PICTURE_REL_PATH
                    pic_name = time_file_name(secure_filename(upload_name), sign='_')
                    di = {'picture_name':pic_name}
                    if stores_info:
                        stores_info.update(picture_name=pic_name)
                        old_picture = stores_info.picture_name
                        if old_picture:
                            try:
                                os.remove(os.path.join(base_path+rel_path+ '/', old_picture))
                            except:
                                pass
                        session.commit()
                    else:
                        try:
                            stores_info = StoresInfo(stores_id=stores.id,base_path=base_path, rel_path=rel_path,picture_name = pic_name)
                            session.add(stores_info)
                            session.commit()
                        except Exception, ex:
                            flash(gettext('Failed to update model. %(error)s', error=str(ex)), 'error')
                            session.rollback()
                            return False
                    picture.save(os.path.join(base_path+rel_path+'/', pic_name))
                    return True
        else:
            return True

def get_store_by_search(case):

    s = '%'+case+'%'
    stores_count = Stores.query.filter(or_(Stores.name.like(s),Stores.address.like(s))).count()
    if stores_count == 1:
        stores = Stores.query.filter(or_(Stores.name.like(s),Stores.address.like(s))).first()
    elif stores_count > 1:
        stores = Stores.query.filter(or_(Stores.name.like(s),Stores.address.like(s))).all()
    else:
        stores = None
    return stores

def get_store_by_search_count(case):
    s = '%'+case+'%'
    stores_count = Stores.query.filter(or_(Stores.name.like(s),Stores.address.like(s))).count()
    return stores_count

def get_store_by_position(province_id,city_id,country_id):
    if city_id==0 and country_id==0:
        stores_count = Stores.query.filter(Stores.province_id == province_id).count()
        if stores_count ==1:
            stores = Stores.query.filter(Stores.province_id == province_id).first()
        elif stores_count >1:
            stores = Stores.query.filter(Stores.province_id == province_id).all()
        else:
            stores = None
    elif city_id!=0 and country_id==0:
        stores_count = Stores.query.filter(and_(Stores.province_id==province_id,Stores.city_id==city_id)).count()
        if stores_count ==1:
            stores = Stores.query.filter(and_(Stores.province_id==province_id,Stores.city_id==city_id)).first()
        elif stores_count >1:
            stores = Stores.query.filter(and_(Stores.province_id==province_id,Stores.city_id==city_id)).all()
        else:
            stores = None
    else:
        stores_count = Stores.query.filter(and_(Stores.province_id==province_id,Stores.city_id==city_id,Stores.country_id==country_id)).count()
        if stores_count ==1:
            stores  = Stores.query.filter(and_(Stores.province_id==province_id,Stores.city_id==city_id,Stores.country_id==country_id)).first()
        elif stores_count >1:
            stores = Stores.query.filter(and_(Stores.province_id==province_id,Stores.city_id==city_id,Stores.country_id==country_id)).all()
        else:
            stores =None
    return stores

def get_store_by_position_count(province_id,city_id,country_id):
    if city_id==0 and country_id==0:
        stores_count = Stores.query.filter(Stores.province_id ==province_id).count()
    elif city_id!=0 and country_id==0:
        stores_count = Stores.query.filter(and_(Stores.province_id==province_id,Stores.city_id==city_id)).count()
    else:
        stores_count = Stores.query.filter(and_(Stores.province_id==province_id,Stores.city_id==city_id,Stores.country_id==country_id)).count()
    return stores_count

def get_stores_by_id(stores_id):
    stores = Stores.query.filter(Stores.id == stores_id).first()
    if stores:
        stores.image_url = ''
        stores_info = StoresInfo.query.filter(StoresInfo.stores_id == stores_id).first()
        if stores_info:
            stores.image_url = stores_info.rel_path + '/' +stores_info.picture_name
    return stores

def find_info_by_storeId(store_id):
    store_info = StoresInfo.query.filter(StoresInfo.stores_id == store_id).first()
    return store_info