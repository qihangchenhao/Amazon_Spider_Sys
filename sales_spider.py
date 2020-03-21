#usr/env/bin python
#coding=utf-8
import time
from exts import db
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
from manage import Good_Rating
import datetime
from manage import Amazon
from flask import Flask
import config
from selenium.webdriver.common.action_chains import ActionChains
app = Flask(__name__)
db.init_app(app)
app.config.from_object(config)
app.app_context().push()

info = Amazon.query.all()
asin_list = [asin.asin for asin in info]
url_list = [url.url for url in info]

def login_amazon():
    chrome_options = Options()
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--disable-dev-shm-usage')
    # chrome_options.add_argument('window-size=1920x3000')
    # chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument('--hide-scrollbars')
    # chrome_options.add_argument('blink-settings=imagesEnabled=false')
    # chrome_options.add_argument('--headless')
    # prefs = {"profile.managed_default_content_settings.images": 2}
    # chrome_options.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome('/Users/chenhao/PycharmProjects/FangTx/spider/chromedriver',
                               chrome_options=chrome_options)
    # browser = webdriver.Chrome('/bin/chromedriver', chrome_options=chrome_options)
    browser.get('https://www.amazon.com/')

    elem = browser.find_element_by_xpath('//*[@id="nav-link-accountList"]/span[2]')
    chain = ActionChains(browser)
    chain.move_to_element(elem).perform()

    browser.find_element_by_xpath('//*[@id="nav-flyout-ya-signin"]/a/span').click()
    time.sleep(2)
    email = browser.find_element_by_xpath('//*[@id="ap_email"]')
    email.send_keys('1707878588@qq.com')
    time.sleep(1)
    passwd = browser.find_element_by_xpath('//*[@id="ap_password"]')
    passwd.send_keys('AMYAMY')
    check_login = browser.find_element_by_xpath('//*[@id="authportal-main-section"]/div[2]/div/div/form/div/div/div/div[3]/div[2]/div/label/div/label/input')
    check_login.click()
    submit = browser.find_element_by_xpath('//*[@id="signInSubmit"]')
    submit.click()
    time.sleep(1)
    try:
        fs = browser.find_element_by_xpath('//*[@id="continue"]')
        if fs:
            fs.click()
    except:
        pass
    try:
        yanzhengma = browser.find_element_by_xpath('//*[@id="cvf-page-content"]/div/div/div[1]/form/div[2]/input')
        if yanzhengma:
            yzm = input("请输入验证码")
            yanzhengma.send_keys(yzm)
        else:
            pass
    except:
        pass
    return browser



def get_spider(url_list,asin_list):
    browser = login_amazon()
    browser.set_page_load_timeout(40)
    browser.set_script_timeout(40)
    for i in range(len(url_list)):
        browser.get(url_list[i])
        time.sleep(1000)


get_spider(url_list,asin_list)