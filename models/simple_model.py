import hashlib

from sqlalchemy import Column, String, UnicodeText, Integer, Unicode

import secret
from models.base_model import SQLMixin, db


class User(SQLMixin, db.Model):
    """
    User 是一个保存用户数据的 model
    """
    username = Column(String(50), nullable=False)
    password = Column(String(256), nullable=False)
    image = Column(String(100), nullable=False, default='/images/3.jpg')
    signature = Column(UnicodeText, nullable=False, default='这家伙很懒，什么个性签名都没有留下。')
    email = Column(String(50), nullable=False, default=secret.test_mail)

    def topics(self):
        # 返回该用户对应的所有 topic
        ts = Topic.all(user_id=self.id)
        return ts

    def replies(self):
        # 返回该用户对应的所有 reply
        rs = Reply.all(user_id=self.id)
        return rs

    @staticmethod
    def guest():
        # 返回一个游客用户， id 为 0
        form = dict(
            id=0,
            username='【游客】',
            password='【游客】',
            signature='登录后可设置个性签名',
            image='/images/3.jpg',
        )
        u = User(**form)
        return u

    def is_guest(self):
        # 判断用户是否为游客
        # 只有游客用户 id 为 0
        return self.id == 0

    @classmethod
    def salted_password(cls, password):
        """
        对用户密码加盐
        对加盐的密码用摘要算法处理
        """
        salted = password + secret.salt
        hash = hashlib.sha256(salted.encode('ascii')).hexdigest()
        return hash

    @classmethod
    def register(cls, form):
        # 注册成功， 将用户数据加入数据库， 返回用户对象
        # 失败则返回 None
        name = form.get('username', '')
        pwd = form.get('password', '')
        if len(name) > 2 and User.one(username=name) is None:
            u = User.new(form)
            u.password = u.salted_password(pwd)
            u.save()
            return u
        else:
            return None

    @classmethod
    def validate_login(cls, form):
        # 判断用户是否通过登录验证
        # 通过， 返回用户对象
        # 否， 返回 None
        user = User.one(username=form['username'])
        if user is not None and user.password == User.salted_password(form['password']):
            return user
        else:
            return None


class Topic(SQLMixin, db.Model):
    """
    Topic 是一个保存话题数据的 model
    """
    views = Column(Integer, nullable=False, default=0)
    title = Column(Unicode(50), nullable=False)
    content = Column(UnicodeText, nullable=False)
    user_id = Column(Integer, nullable=False)

    @classmethod
    def new(cls, form, user_id):
        # 新增 topic 对象
        form['user_id'] = user_id
        m = super().new(form)
        return m

    @classmethod
    def get(cls, id):
        # 返回 topic 对象， 同时该对象浏览 +1
        m = cls.one(id=id)
        m.views += 1
        m.save()
        return m

    def user(self):
        # 返回该对象对应的用户
        u = User.one(id=self.user_id)
        return u

    def replies(self):
        # 返回该对象对应的所有 reply
        rs = Reply.all(topic_id=self.id)
        return rs

    def reply_count(self):
        # 返回该对象对应的所有 reply 的数量
        count = len(self.replies())
        return count


class Reply(SQLMixin, db.Model):
    """
    Reply 是一个保存回复数据的 model
    """
    content = Column(UnicodeText, nullable=False)
    topic_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)

    @classmethod
    def new(cls, form, user_id):
        # 新增 reply 对象
        form['user_id'] = user_id
        m = super().new(form)
        return m

    def user(self):
        # 返回该对象对应的用户
        u = User.one(id=self.user_id)
        return u

    def topic(self):
        # 返回该对象对应的 topic
        t = Topic.one(id=self.topic_id)
        return t


class Messages(SQLMixin, db.Model):
    """
    Messages 是一个保存邮件数据的 model
    """
    title = Column(Unicode(50), nullable=False)
    content = Column(UnicodeText, nullable=False)
    sender_id = Column(Integer, nullable=False)
    receiver_id = Column(Integer, nullable=False)

    def sender(self):
        # 返回邮件对应发送者
        u = User.one(id=self.sender_id)
        return u

    def receiver(self):
        # 返回邮件对应接收者
        u = User.one(id=self.receiver_id)
        return u