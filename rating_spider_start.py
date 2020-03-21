#usr/env/bin python
#coding=utf-8
from flask import Flask
from exts import db
import config
from good_rating import get_star_rating
from manage import Amazon

app = Flask(__name__)
db.init_app(app)
app.config.from_object(config)
app.app_context().push()
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

spider_info = Amazon.query.filter_by(flag=0).all()
for i in spider_info:
    get_star_rating("one",i.asin,i.goods_name)


