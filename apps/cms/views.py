from flask import Blueprint, views, render_template, request, redirect, session, url_for, g
from .forms import LoginForm, ResetPwdFrom, ResetEmailForm, AddBannerForm, UpdateBannerForm, AddBoardForm, UpdateBoardForm
from .models import CMSUser, CMSPermission, CMSRole
from .decorators import login_required, permission_required
import config
from exts import db, mail
from flask_mail import Message
from utils import restful
import string
import random, os
from utils import zlcache
from apps.models import BannerModel, BoardModel, HighlightPostModel, PostModel
from tasks import send_mail
from flask_paginate import Pagination, get_page_parameter
from sqlalchemy.sql import func


bp = Blueprint('cms', __name__, url_prefix='/cms')


@bp.route('/')
@login_required
def index():
    return render_template('cms/cms_index.html')



@bp.route('/logout/')
@login_required
def logout():
    del session[config.CMS_USER_ID]
    return redirect(url_for('cms.login'))


@bp.route('/upload_file/', methods=['POST'])
@login_required
def upload_file():
    file = request.files.get('file')
    name = file.name
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__name__))))
    with open(os.path.join(path, 'static', 'images'), 'wb') as fp:
        for chunk in file.chunks():
            fp.write(chunk)
    url = request.host_url + '/static/' + name
    return restful.success(data={'url':url})


@bp.route('/profile/')
@login_required
def profile():
    return render_template('cms/cms_profile.html')



@bp.route('/email_captcha/')
@login_required
def send_captcha():
    email = request.args.get('email')
    if not email:
        return restful.params_error('请传递邮箱')

    source = list(string.ascii_letters)
    source.extend(map(lambda x:str(x), range(0, 10)))
    captcha = ''.join(random.sample(source, 6))

    send_mail.delay('验证码', recipients=[email], body='验证码为: %s' % captcha)
    #message = Message('验证码', recipients=[email], body='验证码为：%s' % captcha)
    #try:
    #    mail.send(message)
    #except:
    #    return restful.server_error()
    zlcache.set(email, captcha)
    return restful.success()



@bp.route('/posts/')
@login_required
@permission_required(CMSPermission.POSTER)
def posts():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page-1) * config.PER_PAGE
    end = start + config.PER_PAGE

    post_obj = db.session.query(PostModel).outerjoin(HighlightPostModel).order_by(HighlightPostModel.create_time.desc())
    post = post_obj.slice(start, end)

    pagination = Pagination(bs_version=3, page=page, total=post_obj.count())
    context = {
        'posts': post,
        'pagination': pagination
    }
    return render_template('cms/cms_posts.html', **context)


@bp.route('/hpost/', methods=['POST'])
@login_required
@permission_required(CMSPermission.POSTER)
def hpost():
    post_id = request.form.get('post_id')
    if not post_id:
        return restful.params_error(message='请传入帖子id')

    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error(message='该帖子不存在')

    highlight = HighlightPostModel()
    highlight.post = post
    db.session.add(highlight)
    db.session.commit()
    return restful.success()


@bp.route('/uhpost/', methods=['POST'])
@login_required
@permission_required(CMSPermission.POSTER)
def uhpost():
    post_id = request.form.get('post_id')
    if not post_id:
        return restful.params_error(message='请传入帖子id')

    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error(message='该帖子不存在')

    highlight = HighlightPostModel.query.filter_by(post_id=post_id).first()
    db.session.delete(highlight)
    db.session.commit()
    return restful.success()


@bp.route('/dpost/', methods=['POST'])
@login_required
@permission_required(CMSPermission.POSTER)
def dpost():
    post_id = request.form.get('post_id')
    if not post_id:
        return restful.params_error(message='请传入帖子id')

    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error(message='该帖子不存在')

    db.session.delete(post)
    db.session.commit()
    return restful.success()



@bp.route('/comments/')
@login_required
@permission_required(CMSPermission.COMMENTER)
def comments():
    return render_template('cms/cms_comments.html')



@bp.route('/boards/')
@login_required
@permission_required(CMSPermission.BOARDER)
def boards():
    board_models = BoardModel.query.all()
    context = {
        'boards': board_models
    }
    return render_template('cms/cms_boards.html', **context)


@bp.route('/aboard/', methods=['POST'])
@login_required
@permission_required(CMSPermission.BOARDER)
def aboard():
    form = AddBoardForm(request.form)
    if form.validate():
        name = form.name.data
        board = BoardModel(name=name)
        db.session.add(board)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_errors())


@bp.route('/uboard/', methods=['POST'])
@login_required
@permission_required(CMSPermission.BOARDER)
def uboard():
    form = UpdateBoardForm(request.form)
    if form.validate():
        board_id = form.board_id.data
        name = form.name.data
        board = BoardModel.query.get(board_id)
        if board:
            board.name = name
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='该板块不存在')
    else:
        return restful.params_error(message=form.get_errors())


@bp.route('/dboard/', methods=['POST'])
@login_required
@permission_required(CMSPermission.BOARDER)
def dboard():
    board_id = request.form.get('board_id')
    if not board_id:
        return restful.params_error(message='请传入板块id')

    board = BoardModel.query.get(board_id)
    if not board:
        return restful.params_error(message='该板块不存在')

    db.session.delete(board)
    db.session.commit()
    return restful.success()



@bp.route('/fusers/')
@login_required
@permission_required(CMSPermission.FRONTUSER)
def fusers():
    return render_template('cms/cms_fusers.html')



@bp.route('/cusers/')
@login_required
@permission_required(CMSPermission.CMSUSER)
def cusers():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page-1)* config.PER_PAGE
    end = start + config.PER_PAGE

    cms_users = CMSUser.query.slice(start, end)
    pagination = Pagination(bs_version=3, page=page, total=CMSUser.query.count())

    context = {
        'cms_users': cms_users,
        'pagination': pagination
    }
    return render_template('cms/cms_cusers.html', **context)


@bp.route('/add_cuser/')
@login_required
@permission_required(CMSPermission.CMSUSER)
def add_cuser():
    if request.method == 'GET':
        roles = CMSRole.query.all()
        return render_template('cms/add_cuser.html', roles=roles)

    email = request.form.get('email')
    roles_id = request.form.getlist('roles')
    user = CMSUser.query.filter_by(email=email).first()
    print('*'*20)
    print(roles_id)
    return restful.params_error(message='lllllll')


@bp.route('/edit_cuser/')
@login_required
@permission_required(CMSPermission.CMSUSER)
def edit_cuser():
    if request.method == 'GET':
        cuser_id = request.args.get('cms_user_id')
        user = CMSUser.query.get(cuser_id)
        roles = CMSRole.query.all()
        context = {
            'roles': roles,
            'user': user
        }
        return render_template('cms/add_cuser.html', **context)

    email = request.form.get('email')
    roles_id = request.form.getlist('roles')
    user = CMSUser.query.filter_by(email=email).first()
    print('*'*20)
    print(roles_id)
    return restful.params_error(message='1111111')


@bp.route('/delete_cuser/', methods=['POST'])
@login_required
@permission_required(CMSPermission.CMSUSER)
def delete_cuser():
    cuser_id = request.form.get('cuser_id')
    if not cuser_id:
        return restful.params_error(message='请传入用户id')

    cuser = CMSUser.query.get(cuser_id)
    if not cuser:
        return restful.params_error(message='该用户不存在')

    db.session.delete(cuser)
    db.session.commit()
    return restful.success()




@bp.route('/croles/')
@login_required
@permission_required(CMSPermission.ALL_PERMISSIONS)
def croles():
    return render_template('cms/cms_croles.html')




@bp.route('/banners/')
@login_required
def banners():
    banners = BannerModel.query.all()
    return render_template('cms/cms_banners.html', banners=banners)

@bp.route('/abanner/', methods=['POST'])
@login_required
def abanner():
    form = AddBannerForm(request.form)
    if form.validate():
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel(name=name, image_url=image_url, link_url=link_url, priority=priority)
        db.session.add(banner)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_errors())


@bp.route('/ubanner/', methods=['POST'])
@login_required
def ubanner():
    form = UpdateBannerForm(request.form)
    if form.validate():
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner_id = form.banner_id.data
        banner = BannerModel.query.get(banner_id)
        if banner:
            banner.name = name
            banner.image_url = image_url
            banner.link_url = link_url
            banner.priority = priority
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='该轮播图不存在')
    else:
        return restful.params_error(message=form.get_errors())


@bp.route('/dbanner/', methods=['POST'])
@login_required
def dbanner():
    banner_id = request.form.get('banner_id')
    if not banner_id:
        return restful.params_error(message='请传入轮播图的id')

    banner = BannerModel.query.get(banner_id)
    if not banner:
        return restful.params_error(message='该轮播图不存在')

    db.session.delete(banner)
    db.session.commit()
    return restful.success()





class LoginView(views.MethodView):
    def get(self, message = None):
        return render_template('cms/cms_login.html', message = message)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session[config.CMS_USER_ID] = user.id
                if remember:
                    session.permanent = True
                return redirect(url_for('cms.index'))
            else:
                return self.get(message='邮箱或密码错误')
        else:
            return self.get(message=form.get_errors())


class ResetPwdView(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('cms/cms_resetpwd.html')

    def post(self):
        form = ResetPwdFrom(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            user = g.cms_user
            if user.check_password(oldpwd):
                user.password = newpwd
                db.session.commit()
                return restful.success()
            else:
                return restful.params_error('旧密码错误')
        else:
            return restful.params_error(form.get_errors())


class ResetEmailView(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('cms/cms_resetemail.html')

    def post(self):
        form = ResetEmailForm(request.form)
        if form.validate():
            email = form.email.data
            g.cms_user.email = email
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(form.get_errors())


bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))
bp.add_url_rule('/resetpwd/', view_func=ResetPwdView.as_view('resetpwd'))
bp.add_url_rule('/resetemail/', view_func=ResetEmailView.as_view('resetemail'))