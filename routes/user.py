import uuid
import os

from werkzeug.utils import redirect
from flask import (
    render_template,
    Blueprint,
    request,
    url_for,
    session,
)

from models.simple_model import User
from routes import current_user, login_required

main = Blueprint('user', __name__)
"""
用户相关页面
包括
    注册
    登录
    个人主页
    个人设置

用户登录后, 会写入 session, 并且定向到 首页
"""


@main.route("/login/view", methods=['GET'])
def login_view():
    # 返回用户登录界面
    return render_template("user/login_view.html")


@main.route("/register/view", methods=['GET'])
def register_view():
    # 返回用户注册界面
    return render_template("user/register_view.html")


@main.route("/register", methods=['POST'])
def register():
    # 用户注册处理函数
    # 注册成功， 定向的登录界面
    # 失败， 返回注册页面
    form = request.form
    # 用类函数来判断
    u = User.register(form)
    if u is not None:
        return redirect(url_for('.login_view'))
    else:
        return redirect(url_for('.register_view'))


@main.route("/login", methods=['POST'])
def login():
    # 用户登录处理函数
    # 成功， 定向到首页, 设置 session
    # 失败， 返回登录页面
    form = request.form
    u = User.validate_login(form)
    if u is None:
        return redirect(url_for('.login_view'))
    else:
        # session 中写入 user_id
        session['user_id'] = u.id
        # 设置 cookie 有效期为 永久
        session.permanent = True
        return redirect(url_for('index.index'))


@main.route("/<int:id>")
@login_required
def detail(id):
    # 返回到用户主页， 主页包含用户发表话题，回复等
    user = User.one(id=id)
    topics = user.topics()
    replies = user.replies()

    return render_template("user/detail.html", user=user, topics=topics, replies=replies)


@main.route('/setting')
@login_required
def setting():
    # 返回到用户设置页面，可在该页面对用户资料进行更改
    u = current_user()
    return render_template('user/setting.html', user=u)


@main.route('/setting/save', methods=['POST'])
@login_required
def save_setting():
    # 保存设置
    u = current_user()
    form = request.form.to_dict()
    User.update(u.id, **form)

    return redirect(url_for('.setting'))


@main.route('/setting/changepass', methods=['POST'])
@login_required
def change_pass():
    # 更改密码， 然后跳转到登录页面
    u = current_user()
    form = request.form.to_dict()
    if u.password == User.salted_password(form['old_pass']):
        User.update(u.id, password=User.salted_password(form['new_pass']))
    return redirect(url_for('.login'))


@main.route('/image/add', methods=['POST'])
@login_required
def avatar_add():
    # 上传用户图片
    file = request.files['avatar']

    # ../../root/.ssh/authorized_keys
    # filename = secure_filename(file.filename)
    suffix = file.filename.split('.')[-1]
    filename = '{}.{}'.format(str(uuid.uuid4()), suffix)
    path = os.path.join('images', filename)
    file.save(path)

    u = current_user()
    User.update(u.id, image='/images/{}'.format(filename))

    return redirect(url_for('.setting'))
