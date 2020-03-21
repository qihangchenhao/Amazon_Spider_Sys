#usr/env/bin python
#coding=utf-8
import time
from exts import db
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
from manage import Good_Rating
import datetime

def get_star_rating(star,goods_id,goods_name):
    print( "开始爬虫")
    check_rate = Good_Rating.query.filter_by(asin=goods_id).filter_by(star=star).all()
    if len(check_rate) != 0:
        for ra in check_rate:
            db.session.delete(ra)
            db.session.commit()
            print("删除旧数据")
    url='https://www.amazon.com/product-reviews/%s/ref=cm_cr_arp_d_hist_1?ie=UTF8&showViewpoints=0&pageNumber=1&reviewerType=all_reviews&filterByStar=%s_star'%(goods_id,star)
    print("正在获取asin为%s的%s_star的评价"%(goods_id,star))
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('window-size=1920x3000')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--hide-scrollbars')
    chrome_options.add_argument('blink-settings=imagesEnabled=false')
    chrome_options.add_argument('--headless')
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome('./chromedriver', chrome_options=chrome_options )
    # browser = webdriver.Chrome('/bin/chromedriver', chrome_options=chrome_options)
    browser.set_page_load_timeout(40)
    browser.set_script_timeout(40)
    browser.get(url)
    try:
        while True:
            if browser.find_elements_by_xpath('//*[@id="cm_cr-review_list"]/div/div/span/span[2]/a'):
                browser.find_element_by_xpath('//*[@id="cm_cr-review_list"]/div/div/span/span[2]/a').click()
            time.sleep(4)
            rate_time=browser.find_elements_by_xpath('//*[@class="a-section celwidget"]/span')
            rate_title=browser.find_elements_by_xpath('//*[@class="a-section celwidget"]/div[2]/a[2]/span')
            name = browser.find_elements_by_xpath('//*[@class="a-section celwidget"]/div[1]/a/div[2]/span')
            info = browser.find_elements_by_xpath('//*[@class="a-section celwidget"]/div[4]/span/span')
            with open("./download_fiels/%s-%s_star-%s商品评论.csv"%(goods_name.replace(r"/","或"),star,datetime.datetime.now().strftime('%Y-%m-%d')),"w",encoding='utf-8-sig') as f:
                for s in range(len(name)):
                    f.write("%s,%s,%s,%s\n"%(name[s].text.replace("\n","").replace(",","，"),rate_time[s].text.replace("\n","").replace(",","，"),rate_title[s].text.replace("\n","").replace(",","，"),info[s].text.replace("\n","").replace(",","，")))
                    r_info = Good_Rating(asin=goods_id,star=star,author=name[s].text.replace("\n","").replace(",","，"),rating_time=rate_time[s].text.replace("\n","").replace(",","，"),rating_title=rate_title[s].text.replace("\n","").replace(",","，"),content=info[s].text.replace("\n","").replace(",","，"))
                    try:
                        db.session.add(r_info)
                        db.session.commit()
                        print("更新数据成功")
                    except:
                        db.session.rollback()
            browser.find_element_by_xpath('//*[@class="a-text-center celwidget a-text-base"]/ul/li[2]/a').click()
    except Exception as e:
        db.session.close()
        print(e)
        print("评论抓取结束")
        return "success"