import time
from functools import wraps

from flask import session, redirect, url_for

from models.simple_model import User


def current_user():
    # 从 session 中找到 user_id 字段, 找不到就 -1
    # 然后用 id 找用户
    # 找不到就返回 None
    uid = session.get('user_id')
    u = User.one(id=uid)
    if u:
        return u
    else:
        return User.guest()


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user = current_user()
        if user.is_guest():
            return redirect(url_for('user.login_view'))
        else:
            return f(*args, **kwargs)

    return wrapper


def formatted_time(current_time):
    time_format = '%Y/%m/%d %H:%M:%S'
    localtime = time.localtime(current_time)
    formatted = time.strftime(time_format, localtime)
    return formatted


def count(input):
    return len(input)
