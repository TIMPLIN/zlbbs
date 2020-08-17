from wtforms import StringField, IntegerField
from wtforms.validators import EqualTo, regexp, ValidationError, InputRequired
from apps.forms import BaseForm
from utils import zlcache
from .models import FrontUser


class SignupForm(BaseForm):
    telephone = StringField(validators=[regexp(r'1[345789]\d{9}', message='输入正确格式的手机号码')])
    sms_captcha = StringField(validators=[regexp(r'\w{4}', message='输入正确格式的短信验证码')])
    username = StringField(validators=[regexp(r'.{2,20}', message='输入正确格式的用户名')])
    password1 = StringField(validators=[regexp(r'[0-9a-zA-z_\.]{6,20}', message='输入正确格式的密码')])
    password2 = StringField(validators=[EqualTo('password1', message='密码输入不一致')])
    graph_captcha = StringField(validators=[regexp(r'\w{4}', message='输入正确格式的图形验证码')])

    def validate_telephone(self, field):
        telephone = field.data
        if FrontUser.query.filter_by(telephone=telephone).first():
            raise ValidationError(message='该手机号已被注册')

    def validate_sms_captcha(self, field):
        sms_captcha = field.data
        telephone = self.telephone.data

        sms_captcha_cache = zlcache.get(telephone)
        if not sms_captcha_cache or sms_captcha.lower() != sms_captcha_cache.lower():
            raise ValidationError(message='短信验证码错误')


    def validate_graph_captcha(self, field):
        graph_captcha = field.data

        graph_captcha_cache = zlcache.get(graph_captcha.lower())
        if not graph_captcha_cache:
            raise ValidationError(message='图形验证码错误')



class SigninForm(BaseForm):
    telephone = StringField(validators=[regexp(r'1[345789]\d{9}', message='输入正确格式的手机号码')])
    #password = StringField(validators=[regexp(r'.{6,20}', message='输入正确格式的密码')])
    password = StringField(validators=[InputRequired(message='请输入密码')])
    remember = IntegerField()


class AddPostForm(BaseForm):
    board_id = IntegerField(validators=[InputRequired(message='请输入板块id')])
    title = StringField(validators=[InputRequired(message='请输入帖子标题')])
    content = StringField(validators=[InputRequired(message='请输入帖子内容')])


class AddCommentForm(BaseForm):
    content = StringField(validators=[InputRequired(message='请输入评论内容')])
    post_id = IntegerField(validators=[InputRequired(message='请输入帖子id')])