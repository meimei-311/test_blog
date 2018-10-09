#encoding: utf-8

from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager
from flask_login import UserMixin, AnonymousUserMixin, current_user
from flask import redirect, url_for
# from pymongo import MongoClient
# from bson.objectid import ObjectId
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from datetime import datetime
import time
# from markdown import markdown
# import bleach
# from app import db
from database import db


def generate_reset_password_confirmation_token(email, expiration=3600):
    s = Serializer(current_app.config['SECRET_KEY'], expiration)
    return s.dumps({'password_reset': email})


def generate_change_email_confirmation_token(email, expiration=3600):
    s = Serializer(current_app.config['SECRET_KEY'], expiration)
    return s.dumps({'change_email': email})


def encrypt_passowrd(password):
    return generate_password_hash(password)


def verify_password(user_password, password):
    return check_password_hash(user_password, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_ARTICLES | Permission.MODERATE_COMMENTS, False),
            'ADMINISTER': (0xff, False)
        }
        for r in roles:  # 历遍roles字典
            role = Role.query.filter_by(name=r).first()  # 查询Role类里是否存在这种name的角色
            if role is None:  # 如果Role类里面没有找到
                role = Role(name=r)  # 则新建角色，以r的值为名字(其实是用户组的名字)
            role.permissions = roles[r][0]  # 为该role的权限组分配值，从字典取值
            role.default = roles[r][1]  # 为该role的默认权限组分配布尔值，默认是False
            db.session.add(role)  # 增加角色
        db.session.commit()


class User(UserMixin, db.Model):
###User继承UserMixin和db.Model类的功能属性
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    activate = db.Column(db.Boolean, default=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def can(self, permission):
        return self.role is not None and \
               (self.role.permissions & permission) == permission

    def is_administrator(self):
        return self.role is not None and \
                (self.role.permissions & Permission.ADMINISTER) == Permission.ADMINISTER

    def __repr__(self):
        return '<User %r>' % self.username

class Post(db.Model):
    __tablename__ = 'ariticle'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String(100))
    body = db.Column(db.Text)
    issuing_time = db.Column(db.DateTime)
    body_html = db.Column(db.Text)
    comments = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship('User', backref=db.backref('articles'))

    def __init__(self, body):
        self.body = body
        self.body_html = ''

    def new_article(self):
        self.body_html = body_html(self.body)
        collection = {
            'username': current_user.username,
            'user_id': current_user.id,
            'body': self.body,
            'issuing_time': datetime.utcnow(),
            'body_html': self.body_html,
            'comments': []
        }



class Temp(UserMixin):
    is_active = True
    is_anonymous = False
    is_authenticated = True
    email = ''
    username = ''

    def __init__(self, id, username, email, password, activate, role, name, location, about_me, last_since,
                 member_since):
        self.id = str(id)
        self.username = username
        self.email = email
        self.password_hash = password
        self.activate = activate
        self.name = name
        self.location = location
        self.about_me = about_me
        self.last_since = last_since
        self.member_since = member_since
        # conn = MongoClient().blog.Role.find_one({'name': role})
        self.role = Role(name=role, permission=conn.get('permissions'), default=conn.get('default'))

    def get_id(self):
        return self.id

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def can(self, permission):
        return self.role is not None and \
               (self.role.permission & permission) == permission

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def __repr__(self):
        return self.username

    def ping(self):
        pass
        # MongoClient().blog.User.update({'temp': self.email}, {'$set': {'last_since': datetime.utcnow()}})

    def is_following(self, user):
        # temp = MongoClient().blog.User.find_one({'username': self.username}).get('following')
        pass
        for i in range(temp.__len__()):
            if temp[i][0] == user.username:
                return True
        return False


class AnonymousUser(AnonymousUserMixin):
    def can(self, permission):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser
