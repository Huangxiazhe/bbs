from sqlalchemy import create_engine

import secret
from app import configured_app
from models.base_model import db
from models.simple_model import User, Topic


def reset_database():
    url = 'mysql+pymysql://root:{}@localhost/?charset=utf8mb4'.format(secret.database_password)
    e = create_engine(url, echo=True)

    with e.connect() as c:
        c.execute('DROP DATABASE IF EXISTS bbs')
        c.execute('CREATE DATABASE bbs CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
        c.execute('USE bbs')

    db.metadata.create_all(bind=e)


def generate_fake_date():
    form = dict(
        username='seizer',
        password='123'
    )
    form['password'] = User.salted_password(form['password'])
    u = User.new(form)

    with open('markdown_demo.md', encoding='utf8') as f:
        content = f.read()
    form = dict(
        title='markdown demo',
        content=content
    )
    Topic.new(form, u.id)


if __name__ == '__main__':
    app = configured_app()
    with app.app_context():
        reset_database()
        generate_fake_date()
