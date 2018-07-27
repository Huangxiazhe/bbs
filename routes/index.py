from flask import (
    render_template,
    Blueprint,
    send_from_directory,
)

from models.simple_model import Topic
from routes import current_user

main = Blueprint('index', __name__)
"""
网站首页
显示网站所有话题
"""


@main.route("/")
def index():
    # 返回网站首页
    ms = Topic.all()
    user = current_user()
    return render_template("index.html", ms=ms, user=user)


@main.route('/images/<filename>')
def image(filename):
    # 返回图片资源
    # 不要直接拼接路由，不安全，比如
    # open(os.path.join('images', filename), 'rb').read()
    return send_from_directory('images', filename)
