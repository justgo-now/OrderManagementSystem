# coding: utf-8
import os
from base_service import *
from repast.models.stores import StoresInfo
from repast.util.ex_file import *
from repast.setting.server import *
from werkzeug import secure_filename

class StoresAdminService(BaseService):
    '''stores'''
    def create_stores(self, session, form_dict, object, args, file, special_args=None):
        try:
            base_path = ''
            rel_path = ''
            pic_name = ''
            stores = self.get_model(object, args, form_dict, special_args)
            pictures = file.getlist('pictures')
            for picture in pictures:
                if not allowed_file_extension(picture.filename, STORES_PICTURE_ALLOWED_EXTENSION):
                    continue
                else:
                    upload_name = picture.filename
                    base_path = STORES_PICTURE_BASE_PATH
                    rel_path = STORES_PICTURE_REL_PATH
                    pic_name = time_file_name(secure_filename(upload_name), sign='_')
                    try:
                        picture.save(os.path.join(base_path+rel_path+'/', pic_name))
                    except Exception, e:
                        flash(gettext('创建餐厅失败，找不到路径. %(error)s', error=str(e)), 'error')
                        return False

            session.add(stores)
            session.commit()
            stores_info = StoresInfo(stores_id=stores.id,
                                     base_path=base_path,
                                     rel_path=rel_path,
                                     picture_name=pic_name)

            session.add(stores_info)
            session.commit()
        except Exception, e:
            flash(gettext('创建餐厅失败 %(error)s', error=str(e)), 'error')
            session.rollback()
            return False
        return True

    def update_stores(self, session, form_dict, model, args, file, special_args=None):
        try:
            model.update(**form_dict)
            pictures = file.getlist('pictures')
            is_true = self.update_stores_pictures(session, model, pictures)
            if is_true:
                pass
            else:
                return False
            session.commit()
        except Exception, ex:
            flash(gettext('Failed to update model. %(error)s', error=str(ex)), 'error')
            session.rollback()
            is_true = False
        return is_true


    def save_stores_pictures(slef, stores, pictures):
        for picture in pictures:
            if not allowed_file_extension(picture.filename, STORES_PICTURE_ALLOWED_EXTENSION):
                continue
            else:
                upload_name = picture.filename
                base_path = STORES_PICTURE_BASE_PATH
                rel_path = STORES_PICTURE_REL_PATH
                pic_name = time_file_name(secure_filename(upload_name), sign='_')
                try:
                    picture.save(os.path.join(base_path+rel_path+'/', pic_name))
                except Exception, e:
                    return None
                stores_info = StoresInfo(stores_id=stores.id,
                                         base_path=base_path,
                                         rel_path=rel_path,
                                         picture_name=pic_name)
                return stores_info

    def update_stores_pictures(self, session, stores, pictures):
        '''更新餐厅图片'''
        picture_length = len(pictures)
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
                    old_picture = stores_info.picture_name
                    stores_info.update(picture_name=pic_name)
                    if old_picture:
                        try:
                            picture.save(os.path.join(base_path+rel_path+'/', pic_name))
                            os.remove(os.path.join(base_path+rel_path+ '/', old_picture))
                        except:
                            pass
                    session.commit()
                    return True
                else:
                    try:
                        stores_info = StoresInfo(stores_id=stores.id,base_path=base_path, rel_path=rel_path,picture_name = pic_name)
                        session.add(stores_info)
                        session.commit()
                    except Exception, ex:
                        flash(gettext('更新餐厅失败. %(error)s', error=str(ex)), 'error')
                        session.rollback()
                        return False
                try:
                    picture.save(os.path.join(base_path+rel_path+'/', pic_name))
                except Exception, ex:
                    flash(gettext('更新餐厅失败.找不到路径 %(error)s', error=str(ex)), 'error')
                    return False
                return True
        return True