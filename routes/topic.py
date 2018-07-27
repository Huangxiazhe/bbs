from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from models.simple_model import Topic
from routes import current_user, login_required

main = Blueprint('topic', __name__)
"""
话题相关页面
包括
    topic 详细页面
    编辑新话题页面
    发布新话题
"""


@main.route('/<int:id>')
def detail(id):
    # 返回 topic 详细页面
    t = Topic.get(id)

    # 不应该放在路由里面
    # m.views += 1
    # m.save()

    # 传递 topic 的所有 reply 到 页面中
    return render_template("topic/detail.html", topic=t)


@main.route("/add", methods=["POST"])
@login_required
def add():
    # 发布新话题， 成功后跳转到新话题详细页面
    form = request.form.to_dict()
    u = current_user()
    m = Topic.new(form, user_id=u.id)
    return redirect(url_for('.detail', id=m.id))


@main.route("/new")
@login_required
def new():
    # 返回编辑新话题的页面
    return render_template("topic/new.html")
