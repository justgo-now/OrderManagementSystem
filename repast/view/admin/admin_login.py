# coding: utf-8

"""用户登陆相关"""

from flask import redirect, render_template, request
from wtforms import form, fields, validators
from flask.ext import login
from flask.ext.admin import helpers

from repast.models.admin_user import AdminUser
from repast.models.database import db
from repast import app


class LoginForm(form.Form):
    """定义用户登陆的Form"""

    user_name = fields.TextField(u'昵称', validators=[validators.required()])
    password = fields.PasswordField(u'密码', validators=[validators.required()])

    def validate_user_name(self, field):
        user = self.get_user()
        if not user:
            raise validators.ValidationError(u'昵称不存在')

        if not user.check_password(self.password.data):
            raise validators.ValidationError(u'密码错误')

    def get_user(self):
        user = AdminUser.query.filter(AdminUser.name == self.user_name.data).first()
        return user


class RegisterForm(form.Form):
    """定义用户注册的form"""

    user_name = fields.TextField(u'昵称', validators=[validators.required()])
    password = fields.PasswordField(u'密码', validators=[validators.required()])

    def validate_user_name(self, field):
        if AdminUser.query.filter(AdminUser.name == field.data).count() > 0:
            raise validators.ValidationError(u'昵称重复')


class MyAnonymousUser(object):
    """This is the default object for representing an anonymous user."""

    def is_authenticated(self):
        return False

    def is_active(self):
        return False

    def is_anonymous(self):
        return True

    def get_id(self):
        return

    def is_superuser(self):
        """猫吧超级超级管理员权限"""
        return False

    def is_normal_superuser(self):
        """猫吧普通管理员权限"""
        return False

    def is_manageruser(self):
        """酒吧超级管理员权限"""
        return False

    def is_normal_manageruser(self):
        """酒吧普通管理员权限"""
        return False


login_manager = login.LoginManager()
login_manager.setup_app(app)

login_manager.anonymous_user = MyAnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return AdminUser.query.filter(AdminUser.id == user_id).first()


def login_view():
    login_form = LoginForm(request.form)
    if helpers.validate_form_on_submit(login_form):
        user = login_form.get_user()
        login_user_with_remember(user)
        if user.is_normal_superuser() or user.is_normal_manageruser():
            return redirect('/admin')

        return redirect('/admin')

    return render_template('admin_page/auth.html', form=login_form)


def register_view():
    register_form = RegisterForm(request.form)
    if helpers.validate_form_on_submit(register_form):
        user = AdminUser(name=register_form.user_name.data, password=register_form.password.data,
                         admin='1111')
        db.add(user)
        db.commit()

        login_user_with_remember(user)
        if user.admin:
            return redirect('/admin')

        return redirect('/admin')

    return render_template('admin_page/auth.html', form=register_form)


@login.login_required
def logout_view():
    login.logout_user()
    return redirect('/admin')


def login_user_with_remember(user):
    """检查form字段的内容是否记录用户自动登陆"""

    if request.form.get('remember', None):
        login.login_user(user, remember=True)

    login.login_user(user, remember=False)