from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

import secret

from models.base_model import db
from routes import formatted_time, count

from routes.index import main as index_routes
from routes.topic import main as topic_routes
from routes.reply import main as reply_routes
from routes.user import main as user_routes
from routes.message import main as message_routes, mail

"""
在 flask 中，模块化路由的功能由 蓝图（Blueprints）提供
蓝图可以拥有自己的静态资源路径、模板路径
"""


def configured_app():
    app = Flask(__name__)
    # 设置 secret_key 来使用 flask 自带的 session
    # 这个字符串随便你设置什么内容都可以
    app.secret_key = secret.secret_key

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:{}@localhost/web21?charset=utf8mb4'.format(
        secret.database_password
    )
    db.init_app(app)
    mail.init_app(app)

    # 注册蓝图
    # 有一个 url_prefix 可以用来给蓝图中的每个路由加一个前缀
    app.register_blueprint(index_routes)
    app.register_blueprint(topic_routes, url_prefix='/topic')
    app.register_blueprint(reply_routes, url_prefix='/reply')
    app.register_blueprint(user_routes, url_prefix='/user')
    app.register_blueprint(message_routes, url_prefix='/message')

    app.template_filter()(count)
    app.template_filter()(formatted_time)

    # admin = Admin(app, name='web21', template_mode='bootstrap3')
    # admin.add_view(ModelView(User, db.session))
    # admin.add_view(ModelView(Topic, db.session))
    # admin.add_view(ModelView(Reply, db.session))
    # admin.add_view(ModelView(Messages, db.session))
    # Add administrative views here

    return app


# 运行代码
if __name__ == '__main__':
    # app.add_template_filter(count)
    # debug 模式可以自动加载你对代码的变动, 所以不用重启程序
    # host 参数指定为 '0.0.0.0' 可以让别的机器访问你的代码
    # 自动 reload jinja
    app = configured_app()
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    config = dict(
        debug=True,
        host='localhost',
        port=3000,
    )
    app.run(**config)
