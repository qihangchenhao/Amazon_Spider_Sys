# -*- coding: utf-8 -*-
import os
from urllib.parse import urlparse, urljoin
from flask import render_template, Blueprint, request, Flask, Response, session, send_from_directory, redirect
from flask_login import login_user, login_required,logout_user
from manage import User
import config
from manage import Amazon
from model import login_manager
from exts import db
import json
import re
from  goods_star import get_star_info
from good_rating import get_star_rating
import datetime


app = Flask(__name__)
login_manager.init_app(app)
app.config.from_object(config)
db.init_app(app)
app.app_context().push()

app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
userRoute = Blueprint('user', __name__, url_prefix='/user', template_folder='templates',static_folder='static')
DEFAULT_MODULES = [userRoute]


@app.route('/',methods=['GET'])
def index():
    return render_template('login.html')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@userRoute.before_request
def before_request():
    pass


@app.route('/index',methods=['GET'])
@login_required
def back_index():
    return render_template('index.html')



@userRoute.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if not request.form:
            return render_template('login.html')
        username = str(request.form.get("username"))
        pasawd = str(request.form.get("passwd"))
        session["usernema"]=username
        user = User.query.filter(User.accountNumber == username,
                                 User.password == pasawd).first()
        if user:
            login_user(user,remember=True)
            return render_template('index.html')
        else:
            return render_template('login.html')
    if request.method == 'GET':
        return render_template('login.html')


@userRoute.route('/rating_table/get_goods_name',methods=["POST"])
@userRoute.route('/rating_table',methods=["GET","POST"])
@login_required
def get_rating_table():
    if request.method == "GET":
        return render_template("rating_table.html")
    if request.method =="POST":
        spider_info = Amazon.query.filter_by(flag=0).all()
        res = []
        for info in spider_info:
            dict = {}
            dict['goods_name'] = info.goods_name
            dict['asin'] = info.asin
            res.append(dict)
        return Response(json.dumps(res))


@userRoute.route('/rating_start',methods=["POST","GET"])
@login_required
def start_rating_spider():
    if request.method=="GET":
        return render_template("rating_table.html")
    if request.method == "POST":
        asin = request.form.get('goods')
        star = request.form.get('good_star')
        print(asin,star)
        spider_info = Amazon.query.filter_by(asin=asin).first()
        print("启动评价爬虫进程")
        get_star_rating(star,asin,spider_info.goods_name)
    return render_template('rating_table.html')


@userRoute.route('/goods_star',methods=["GET","POST"])
@login_required
def put_goods_star():
    spider_info = Amazon.query.filter_by(flag=0).all()
    res = []
    for info in spider_info:
        dict = {}
        dict['goods_name'] = info.goods_name
        dict['sum_star'] = info.sum_star
        dict['rating_num'] = info.rating_num
        dict['star'] = info.star
        dict['asin'] = info.asin
        res.append(dict)
    if request.method=="GET":
        return render_template("goods_star.html")
    if request.method=="POST":
        page = int(request.values.get('page'))
        if page >= int((len(res)/10)+1):
            return  Response(json.dumps(res[0 + 10 * int((len(res)/10)):10 + 10 * int((len(res)/10))]))
        else:
            return Response(json.dumps(res[0 + 10 * page:10 + 10 * page]))


@userRoute.route('/goods_star_long',methods=["GET","POST"])
@login_required
def put_goods_star_long():
    spider_info = Amazon.query.filter_by(flag=0).filter_by(spider_time=0).all()
    res = []
    for info in spider_info:
        dict = {}
        dict['goods_name'] = info.goods_name
        dict['sum_star'] = info.sum_star
        dict['rating_num'] = info.rating_num
        dict['star'] = info.star
        dict['asin'] = info.asin
        res.append(dict)
    if request.method=="GET":
        return render_template("goods_star_long.html")
    if request.method=="POST":
        page = int(request.values.get('page'))
        if page >= int((len(res)/10)+1):
            return  Response(json.dumps(res[0 + 10 * int((len(res)/10)):10 + 10 * int((len(res)/10))]))
        else:
            return Response(json.dumps(res[0 + 10 * page:10 + 10 * page]))


@userRoute.route('/goods_star_short',methods=["GET","POST"])
@login_required
def put_goods_star_short():
    spider_info = Amazon.query.filter_by(flag=0).filter_by(spider_time=1).all()
    res = []
    for info in spider_info:
        dict = {}
        dict['goods_name'] = info.goods_name
        dict['sum_star'] = info.sum_star
        dict['rating_num'] = info.rating_num
        dict['star'] = info.star
        dict['asin'] = info.asin
        res.append(dict)
    if request.method=="GET":
        return render_template("goods_star_short.html")
    if request.method=="POST":
        page = int(request.values.get('page'))
        if page >= int((len(res)/10)+1):
            return  Response(json.dumps(res[0 + 10 * int((len(res)/10)):10 + 10 * int((len(res)/10))]))
        else:
            return Response(json.dumps(res[0 + 10 * page:10 + 10 * page]))


@userRoute.route('/setting/restart_spider',methods=["GET","POST"])
# @login_required
def restart_spider():
    if request.method=="POST":
        f = open("./download_fiels/%s长期监控商品信息.csv" % (datetime.datetime.now().strftime('%Y-%m-%d')), "w",
                 encoding='utf-8-sig')
        f1 = open("./download_fiels/%s短期监控商品信息.csv" % (datetime.datetime.now().strftime('%Y-%m-%d')), "w",
                  encoding='utf-8-sig')
        spider_info = Amazon.query.filter_by(flag=0).all()
        for info in spider_info:
            print("启动爬虫")
            get_star_info(info.asin,info.url)
        return Response('success')


@userRoute.route('/add_shop',methods=["GET","POST"])
@login_required
def add_good():
    add_msg=[{"msg":"添加成功"}]
    if request.method=="GET":
        return render_template("add_shop.html")
    if request.method=="POST":
        shopurl = request.form.get("shopurl").replace("ref(.*?)?","")
        spider_time = request.form.get("spider_time")
        if spider_time=="0":
            print('长期监控')
        else:
            print("短期监控")
        if "www.amazon.com" in shopurl or "www.amazon.cn" in shopurl:
            try:
                goods_name = re.findall("https://www.amazon.com/(.*?)/dp", shopurl)[0]
            except:
                goods_name=""
            goods_id = re.findall(r'[A-Z0-9]{10,11}', shopurl)[0]
            if not Amazon.query.filter_by(asin=goods_id).first():
                add_good = Amazon(asin=goods_id,flag=0,goods_name=goods_name,sum_star="0",rating_num="0",star="",url=shopurl,spider_time=spider_time)
                db.session.add(add_good)
                db.session.commit()
            else:
                add_msg[0]['msg'] = "添加失败"
            return render_template("index.html",add_msg=add_msg)
        else:
            add_msg[0]['msg']="添加失败"
            return render_template("add_shop.html",add_msg=add_msg)


@userRoute.route('/logout',methods=['GET', 'POST'])
@login_required
def logout():
    if request.method=="POST":
        logout_user()
        return render_template('login.html')
    else:
        return ""


@userRoute.route('/setting/get_spider_data',methods=["POST"])
@userRoute.route('/setting',methods=["GET"])
@login_required
def ret_setting():
    if request.method == "GET":
        return render_template("setting.html")
    if request.method == "POST":
        amazon_infos = Amazon.query.all()
        datas=[]
        for amazon_info in amazon_infos:
            amazon_json = {}
            amazon_json['id'] = amazon_info.id
            amazon_json['asin'] = amazon_info.asin
            amazon_json['goods_name'] = amazon_info.goods_name
            amazon_json['sum_star'] = amazon_info.sum_star
            amazon_json['rating_num'] = amazon_info.rating_num
            amazon_json['star'] = amazon_info.star
            amazon_json['flag'] = amazon_info.flag
            datas.append(amazon_json)
    return Response(json.dumps(datas))


@userRoute.route('/delete',methods=["POST"])
@login_required
def delete_good():
        if request.method == "POST":
            del_id = int(request.values.get("id").strip("delete"))
            del_amazon = Amazon.query.filter_by(id=del_id).first()
            db.session.delete(del_amazon)
            db.session.commit()
            print("删除成功")
            return Response("success")



@userRoute.route('/download_fiels',methods=["POST"])
@userRoute.route('/get_download',methods=["GET"])
@login_required
def download():
    file_name = os.listdir('./download_fiels')
    if request.method=="POST":
        file_list=[]
        for i in file_name:
            dict={}
            dict['file']=i
            file_list.append(dict)
        return Response(json.dumps(file_list))
    if request.method=="GET":
        return render_template("download_fiels.html")


@userRoute.route('/downloads_fiels/delete', methods=["POST"])
def delete_fiels():
    fiel_name = request.values.get("name")
    os.remove('./download_fiels/%s'%fiel_name)
    return Response("success")


@userRoute.route('/setting/alter_setting',methods=["POST"])
@login_required
def setting_spider():
    if request.method == "POST":
        amazon_infos = Amazon.query.all()
        alter_flag_id=[]
        for amazon_info in amazon_infos:
            try:
                flag = request.form.get(("%d"%amazon_info.id))
                if not flag:
                    alter_flag_id.append(amazon_info.id)
                else:
                    alert_spider = Amazon.query.filter_by(id=amazon_info.id).first()
                    alert_spider.flag=flag
                    db.session.commit()
                    print(flag)
                    print(alert_spider.flag)
            except:
                print("出错了")
        for not_spider_id in alter_flag_id:
            not_spider = Amazon.query.filter_by(id=not_spider_id).first()
            not_spider.flag="1"
            db.session.commit()
        return Response(json.dumps([{"key":"success"}]))


@userRoute.route('/download_fiels/<file>',methods=["GET"])
@login_required
def put_files(file):
    return send_from_directory('./download_fiels', file, as_attachment=True)


@app.errorhandler(404)
def miss(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def error(e):
    return render_template('500.html'), 500


for module in DEFAULT_MODULES:
    app.register_blueprint(module)


if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(host='127.0.0.1',port='5000',threaded=True)
