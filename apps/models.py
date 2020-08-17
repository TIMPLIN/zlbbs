from exts import db
from datetime import datetime
from sqlalchemy.orm import backref


class BannerModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(100), nullable=False)
    link_url = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    __mapper_args__ = {
        'order_by': priority.desc()
    }



class BoardModel(db.Model):
    __tablename__ = 'board'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)


class PostModel(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    read_count = db.Column(db.Integer, default=0, nullable=False)

    board_id = db.Column(db.Integer, db.ForeignKey('board.id'))
    author_id = db.Column(db.String(100), db.ForeignKey('front_user.id'))

    board = db.relationship('BoardModel', backref='posts')
    author = db.relationship('FrontUser', backref='posts')



class HighlightPostModel(db.Model):
    __tablename__ = 'highlight_post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    post = db.relationship('PostModel', backref='highlight')



class CommentModel(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    author_id = db.Column(db.String(100), db.ForeignKey('front_user.id'))

    post = db.relationship('PostModel', backref=backref('comments', order_by=create_time.desc()))
    author = db.relationship('FrontUser', backref='comments')

    __mapper_args__ = {
        'order_by': create_time.desc()
    }