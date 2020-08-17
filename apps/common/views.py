from flask import Blueprint, request, make_response, jsonify
from exts import alidayu
from utils import restful
from utils.captcha import Captcha
from .forms import SMSCaptchaForm
from utils import zlcache
from io import BytesIO
import qiniu
from tasks import send_sms_captcha

bp = Blueprint('common', __name__, url_prefix='/c')


#@bp.route('/sms_captcha/')
#def sms_captcha():
#    telephone = request.args.get('telephone')
#    if not telephone:
#        return restful.params_error(message='请填入手机号码')
#
#    captcha = Captcha.gene_text(number=4)
#    if alidayu.send_sms(telephone, code=captcha):
#        return restful.success()
#    else:
#        return restful.params_error(message='短信验证码发送失败')

@bp.route('/sms_captcha/', methods=['POST'])
def sms_captcha():
    form = SMSCaptchaForm(request.form)
    if form.validate():
        telephone = form.telephone.data
        captcha = Captcha.gene_text(number=4)
        print('短信验证码为: %s' % captcha)
        zlcache.set(telephone, captcha.lower())
        #send_sms_captcha.delay(telephone, captcha)
        return restful.success()

        #if alidayu.send_sms(telephone, code=captcha):
        #    return restful.success()
        #else:
        #    return restful.params_error(message='短信验证码发送失败')
    else:
        return restful.params_error(message='参数错误')


@bp.route('/captcha/')
def graph_captcha():
    text, image = Captcha.gene_graph_captcha()
    zlcache.set(text.lower(), text.lower())
    out = BytesIO()
    image.save(out, 'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return resp


@bp.route('/uptoken/')
def uptoken():
    access_key = ''
    secret_key = ''
    
    q = qiniu.Auth(access_key, secret_key)
    bucket = ''
    
    token = q.upload_token(bucket)
    return jsonify({'uptoken': token})