from flask_script import Manager
from flask_migrate import MigrateCommand, Migrate
from exts import db
from zlbbs import create_app
from apps.cms import models as cms_models
from apps.front import models as front_models
from apps.models import BannerModel, BoardModel, PostModel, CommentModel, HighlightPostModel

CMSUser = cms_models.CMSUser
CMSRole = cms_models.CMSRole
CMSPermission = cms_models.CMSPermission

FrontUser = front_models.FrontUser

app = create_app()

manager = Manager(app)

Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
@manager.option('-e', '--email', dest='email')
def create_cms_user(username, password, email):
    user = CMSUser(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()
    print('\nCMS用户注册完成')


@manager.option('-t', '--telephone', dest='telephone')
@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
def create_front_user(telephone, username, password):
    user = FrontUser(telephone=telephone, username=username, password=password)
    db.session.add(user)
    db.session.commit()
    print('\n前台用户创建完成')


@manager.command
def create_role():
    visitor = CMSRole(name='访问者', desc='只能访问相关数据，不能修改')
    visitor.permissions = CMSPermission.VISITOR

    operator = CMSRole(name='运营', desc='管理帖子，管理评论，管理前台用户')
    operator.permissions = CMSPermission.VISITOR|CMSPermission.COMMENTER|CMSPermission.FRONTUSER|CMSPermission.POSTER

    admin = CMSRole(name='管理员', desc='拥有本系统所有权限')
    admin.permissions = CMSPermission.VISITOR|CMSPermission.POSTER|CMSPermission.COMMENTER|CMSPermission.FRONTUSER|CMSPermission.BOARDER

    developer = CMSRole(name='开发者', desc='开发人员专用')
    developer.permissions = CMSPermission.ALL_PERMISSIONS

    db.session.add_all([visitor, operator, admin, developer])
    db.session.commit()
    print('\n分组创建完成')


@manager.option('-e', '--email', dest='email')
@manager.option('-n', '--name', dest='name')
def add_user_to_role(email, name):
    user = CMSUser.query.filter_by(email=email).first()
    if user:
        role = CMSRole.query.filter_by(name=name).first()
        if role:
            user.roles.append(role)
            db.session.commit()
            print('\n用户成功添加到组')
        else:
            print('\n该组不存在')
    else:
        print('\n该邮箱对应的用户不存在')

@manager.command
def test():
    user = CMSUser.query.first()
    if user.has_permission(CMSPermission.VISITOR):
        print('\nyes')
    else:
        print('\nno')


@manager.command
def create_posts():
    for i in range(0, 218):
        title = '标题: %s' % i
        content = '内容: %s' % i
        author = FrontUser.query.first()
        board = BoardModel.query.first()
        post = PostModel(title=title, content=content)
        post.author = author
        post.board = board
        db.session.add(post)
        db.session.commit()
    print('\n帖子创建完成')


@manager.command
def delete_posts():
    while True:
        post = PostModel.query.first()
        if post:
            db.session.delete(post)
        else:
            break
    db.session.commit()
    print('\n帖子删除完成')



if __name__ == '__main__':
    manager.run()