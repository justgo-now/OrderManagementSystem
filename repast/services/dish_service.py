# coding: utf-8
import os
from base_service import *
from werkzeug import secure_filename
from repast.util.ex_file import *
from repast.setting.wbb import *
from repast.util.session_common import set_session_dish, get_session_dish

class DishService(BaseService):
    '''菜品'''
    def create_dish(self, session, form_dict, Object, args, files, special_args=None):
        try:
            base_path = ''
            rel_path = ''
            pic_name = ''
            pictures = files.getlist('pictures')
            for picture in pictures:
                if not allowed_file_extension(picture.filename, DISH_PICTURE_ALLOWED_EXTENSION):
                    continue
                else:
                    upload_name = picture.filename
                    base_path = DISH_PICTURE_BASE_PATH
                    rel_path = DISH_PICTURE_REL_PATH
                    pic_name = time_file_name(secure_filename(upload_name), sign='_')
                    try:
                        picture.save(os.path.join(base_path+rel_path+'/', pic_name))
                    except Exception, e:
                        flash(gettext('创建菜品失败，找不到路径. %(error)s', error=str(e)), 'error')
                        return False
            model = self.get_dish(Object, form_dict, args, special_args, base_path, rel_path, pic_name)
            session.add(model)
            session.commit()
        except Exception, e:
            flash(gettext('创建菜品失败 %(error)s', error=str(e)), 'error')
            return False
        return True


    def update_dish(self, session, form_dict, model, args, files, special_args=None):
        pictures = files.getlist('pictures')
        base_path, rel_path, pic_name = self.update_dish_picture(session, model, form_dict, args, special_args, pictures)
        if pic_name == "":
            pic_name = model.picture_name
        dictionary = self.get_dish_dictionary(form_dict, args, special_args, base_path, rel_path, pic_name)
        model.update(**dictionary)
        try:
            session.commit()
        except Exception, e:
            flash(gettext('更新菜品失败%(error)s', error=str(e)), 'error')
            return False
        return True


    def get_dish(self, Object, form_dict, args, special_args, base_path, rel_path, pic_name):
        dictionary = self.get_dish_dictionary(form_dict, args, special_args, base_path, rel_path, pic_name)
        model = Object(**dictionary)
        return model

    def update_dish_picture(self, session, dish, form_dict, args, special_args, pictures):
        base_path = ''
        rel_path = ''
        pic_name = ''
        for picture in pictures:
            if not allowed_file_extension(picture.filename, DISH_PICTURE_ALLOWED_EXTENSION):
                continue
            else:
                upload_name = picture.filename
                base_path = DISH_PICTURE_BASE_PATH
                rel_path = DISH_PICTURE_REL_PATH
                pic_name = time_file_name(secure_filename(upload_name), sign='_')
                old_picture = dish.base_path + dish.rel_path + '/' + dish.picture_name
                if old_picture:
                    try:
                        os.remove(os.path.join(base_path+rel_path+ '/', old_picture))
                    except:
                        pass
                try:
                    picture.save(os.path.join(base_path+rel_path+'/', pic_name))
                except Exception, e:
                    flash(gettext('更新菜品失败.找不到路径 %(error)s', error=str(e)), 'error')
                return base_path, rel_path, pic_name
        return base_path, rel_path, pic_name


    def get_dish_dictionary(self, form_dict, args, special_args, base_path, rel_path, pic_name):
        dictionary = {}
        for arg in args:
            dictionary[str(arg)] = form_dict[str(arg)]
        if special_args != None:
            for arg in special_args:
                if arg == 'group':
                    dictionary[str(arg)] = GetName._get_group(form_dict)
                if arg == 'brand':
                    dictionary[str(arg)] = GetName._get_brand(form_dict)
                if arg == 'dish_sort':
                    dictionary[str(arg)] = GetName._get_only_dish_sort_string(form_dict)
                if arg == 'dish_sort_id':
                    dictionary[str(arg)] = GetName._get_only_dish_sort_id(form_dict)
                if arg == 'package':
                    dictionary[str(arg)] = GetName._get_package(form_dict)

        dictionary['base_path'] = base_path
        dictionary['rel_path'] = rel_path
        dictionary['picture_name'] = pic_name
        return dictionary

def user_add_dish(dish_number, dish_id, package_id, dish_sort_id):
    '''用户在基础套餐上添加菜品'''
    dish = get_session_dish() # 得到所有菜品
    for d in dish:
        if (d.id == dish_id):
            d.package_id = package_id


def get_total_price(dishs):
    """获得点菜的总价"""
    price = 0
    if dishs:
        for d in dishs:
            number = int(d['number'])
            price = price + (int(d['price']) * number)
    return price