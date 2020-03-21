#!/usr/bin/env python
#coding=utf-8
from flask import Flask
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from exts import db
import config
from flask_login import UserMixin

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    return app

app = create_app()
manager = Manager(app)
#使用Migrate绑定app和db
migrate = Migrate(app, db)
#添加迁移脚本
manager.add_command('db', MigrateCommand)



class User(db.Model, UserMixin):
    user_id = db.Column('id', db.Integer, primary_key=True)
    accountNumber = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(20), unique=True)
    __tablename__ = 'tb_user'
    # __abstract__ = True

    def __init__(self, user_id=None, account_number=None, password=None, name="anonymous"):
        self.user_id = user_id
        self.accountNumber = account_number
        self.password = password
        self.name = name

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        id = str(self.user_id)
        return id

    def __repr__(self):
        return '<User %r>' % (self.accountNumber)


class Amazon(db.Model):
    __tablename__ = 'amazon_info'
    # __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    asin = db.Column(db.String(20),primary_key=True,nullable=False)
    goods_name = db.Column(db.String(200), nullable=False)
    sum_star = db.Column(db.String(1000), nullable=False)
    rating_num = db.Column(db.String(200), nullable=False)
    star = db.Column(db.String(2000), nullable=False)
    url = db.Column(db.String(2000),nullable=False)
    flag = db.Column(db.Integer,nullable=False,default=0)
    spider_time = db.Column(db.String(10),nullable=False)
    shop_type = db.Column(db.String(10),nullable=False)

class Good_Rating(db.Model):
    __tablename__="good_rating"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    asin = db.Column(db.String(20),nullable=False)
    star = db.Column(db.String(10),nullable=False)
    author = db.Column(db.String(1000), nullable=False)
    rating_time = db.Column(db.String(300), nullable=False)
    rating_title = db.Column(db.String(2000), nullable=False)
    content = db.Column(db.String(5000), nullable=False)

class Sales_Data(db.Model):
    __tablename__="sales_data"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    asin = db.Column(db.String(20),nullable=False)
    time = db.Column(db.DateTime,nullable=False)
    reserve = db.Column(db.Integer,nullable=False)


if __name__ == "__main__":
    manager.run()


#先初始化当前的数据库环境
#python3 manage.py db init
# 把当前模型迁移到文件夹
# python3 manage.py db migrate
# 把模型迁移到数据库中
# python3 manage.py db upgrade
