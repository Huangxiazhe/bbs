from flask import (
    request,
    redirect,
    url_for,
    Blueprint,
)

from models.simple_model import Reply, User, Messages
from routes import current_user, login_required

main = Blueprint('reply', __name__)
"""
回复相关页面
包括
    添加回复
    @ 站内私信
"""


@main.route("/add", methods=["POST"])
@login_required
def add():
    # 添加回复
    # 确认回复中是否有 @ 其他用户，有则发私信
    # 完成后返回到对应话题详细页面
    form = request.form.to_dict()
    u = current_user()
    content = form['content']
    users = users_from_content(content)
    send_mails(u, users, content)
    m = Reply.new(form, user_id=u.id)
    return redirect(url_for('topic.detail', id=m.topic_id))


def users_from_content(content):
    # 内容 @123 内容
    # 如果用户名含有空格 就不行了 @name 123
    # 'a b c' -> ['a', 'b', 'c']
    parts = content.split()
    users = []

    for p in parts:
        if p.startswith('@'):
            username = p[1:]
            u = User.one(username=username)
            print('users_from_content <{}> <{}> <{}>'.format(username, p, parts))
            if u is not None:
                users.append(u)

    return users


def send_mails(sender, receivers, content):
    # 发站内私信
    print('send_mail', sender, receivers, content)
    for r in receivers:
        form = dict(
            title='AT  【{}】'.format(r.username),
            content=content,
            sender_id=sender.id,
            receiver_id=r.id
        )
        Messages.new(form)
