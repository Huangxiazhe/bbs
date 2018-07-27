from flask_mail import Message, Mail
from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from models.simple_model import Messages, User
from routes import current_user, login_required

from secret import admin_mail

mail = Mail()
main = Blueprint('message', __name__)
"""
邮件相关页面
包括
    收发的所有邮件
    编辑发送电子邮件
    邮件详细信息
    发布新话题
"""


@main.route('/')
@login_required
def index():
    # 返回邮件页面
    # 包括站内私信和发送的电子邮件
    u = current_user()

    sent_mail = Messages.all(sender_id=u.id)
    received_mail = Messages.all(receiver_id=u.id)

    t = render_template(
        'mail/index.html',
        send=sent_mail,
        received=received_mail,
    )
    return t


@main.route("/add", methods=["POST"])
@login_required
def add():
    # 发电子邮件
    form = request.form.to_dict()
    form['receiver_id'] = int(form['receiver_id'])
    u = current_user()
    form['sender_id'] = u.id

    r = User.one(id=form['receiver_id'])
    m = Message(
        subject=form['title'],
        body=form['content'],
        sender=admin_mail,
        recipients=[r.email]
    )
    mail.send(m)

    m = Messages.new(form)
    return redirect(url_for('.index'))





@main.route('/view/<int:id>')
@login_required
def view(id):
    # 返回邮件详细信息
    mail = Messages.one(id=id)
    u = current_user()
    # if u.id == mail.receiver_id or u.id == mail.sender_id:
    if u.id in [mail.receiver_id, mail.sender_id]:
        return render_template('mail/detail.html', mail=mail)
    else:
        return redirect(url_for('.index'))
