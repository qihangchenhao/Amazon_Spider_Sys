#usr/env/bin python
#coding=utf-8
import os
# debug=True
SECRET_KEY = os.urandom(24)
HOSTNAME = '127.0.0.1'
PORT    = '3306'
DATABASE = 'amazon'
USERNAME = 'root'
PASSWORD = '12345678'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
# SECRET_KEY = '*\xff\x93\xc8w\x13\x0e@3\xd6\x82\x0f\x84\x18\xe7\xd9\\|\x04e\xb9(\xfd\xc3'