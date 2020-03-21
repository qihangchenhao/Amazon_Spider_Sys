#usr/env/bin python
#coding=utf-8
from flask import Flask
from exts import db
import config
import json
from goods_star import get_star_info
from manage import Amazon
import datetime
# 输出时间
# BlockingScheduler

app = Flask(__name__)
db.init_app(app)
app.config.from_object(config)
app.app_context().push()
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False




f=open("./download_fiels/%s长期监控商品信息.csv" % (datetime.datetime.now().strftime('%Y-%m-%d')), "w",encoding='utf-8-sig')
f1=open("./download_fiels/%s短期监控商品信息.csv" % (datetime.datetime.now().strftime('%Y-%m-%d')), "w",encoding='utf-8-sig')
spider_info = Amazon.query.filter_by(flag=0).all()
for info in spider_info:
    print("启动爬虫")
    get_star_info(info.asin,info.url)


# '''crontab -e  #进入任务计划设置
#
# 每天早上6点
# 0 6 * * * touch /home/new   #在home下创建一个new文件
#
# 每两个小时
# 0 */2 * * * touch /home/new   #每2个小时在home下创建一个new文件
#
# 晚上11点到早上8点之间每两个小时和早上八点
# 0 23-7/2,8 * * * command
#
# 每个月的4号和每个礼拜的礼拜一到礼拜三的早上11点
# 0 11 4 * 1-3 command
#
# 每天的下午4点、5点、6点的5 min、15 min、25 min、35 min、45 min、55 min时执行命令。
# 5,15,25,35,45,55 16,17,18 * * * command
# '''
# 加载任务,使之生效
#crontab /etc/crontab

# 查看任务
#crontab -l