from wtforms import StringField, IntegerField, ValidationError
from wtforms.validators import Email, Length, InputRequired, EqualTo
from ..forms import BaseForm
from utils import zlcache
from flask import g



class LoginForm(BaseForm):
    email = StringField(validators=[Email(message='输入正确格式的邮箱'), InputRequired(message='请输入邮箱')])
    password = StringField(validators=[Length(6, 20, message='输入正确格式的密码')])
    remember = IntegerField()


class ResetPwdFrom(BaseForm):
    oldpwd = StringField(validators=[Length(6, 20, message='输入正确格式的旧密码')])
    newpwd = StringField(validators=[Length(6, 20, message='输入正确格式的新密码')])
    newpwd2 = StringField(validators=[EqualTo('newpwd', message='新密码必须一致')])


class ResetEmailForm(BaseForm):
    email = StringField(validators=[Email(message='输入正确格式的邮箱')])
    captcha = StringField(validators=[Length(6, 6, message='输入正确的验证码')])

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_cache = zlcache.get(email)
        if not captcha_cache or captcha.lower() != captcha_cache.lower():
            raise ValidationError('验证码错误')

    def validate_email(self, field):
        email = field.data
        if email == g.cms_user.email:
            raise ValidationError('不能修改为相同邮箱')


class AddBannerForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入轮播图名称')])
    image_url = StringField(validators=[InputRequired(message='请输入轮播图图片链接')])
    link_url = StringField(validators=[InputRequired(message='请输入轮播图跳转链接')])
    priority = IntegerField(validators=[InputRequired(message='请输入轮播图优先级')])

class UpdateBannerForm(AddBannerForm):
    banner_id = IntegerField(validators=[InputRequired(message='请输入轮播图的id')])



class AddBoardForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入板块名称')])

class UpdateBoardForm(AddBoardForm):
    board_id = IntegerField(validators=[InputRequired(message='请输入板块id')])