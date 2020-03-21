#usr/env/bin python
#coding=utf-8
from exts import db
import requests
import re
from lxml import etree
from manage import Amazon
import datetime


spider_session = requests.session()
r1 = spider_session.get(url = 'https://www.amazon.com/',
                 headers={'Accept-Language': 'zh-CN,zh;q=0.9',
                     'upgrade-insecure-requests': '1',
'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'})


def get_star_info(asin,goods_url):
        goods_id = asin
        try:
            goods_name = re.findall("https://www.amazon.com/(.*?)/dp",goods_url)[0]
        except:
            goods_name = ""
        if r"/" in goods_id:
            goods_id = goods_id.replace(r"/","")
        else:
            url = "https://www.amazon.com/gp/customer-reviews/widgets/average-customer-review/popover/ref=dpx_acr_pop_?contextId=dpx&asin=%s" % goods_id
            # print(url)
            r2 = spider_session.get(url=url,
                             headers={'content-language': 'zh-CN',
                                'upgrade-insecure-requests': '1',
                                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
                        )
            html = etree.HTML(r2.text)
            try:
                sum_star = html.xpath('/html/body/div/div/div/div[1]/span/text()')[0].split(",")[0].replace("颗星，最多 5 颗星","").strip()
            except:
                sum_star=""
            try:
                rating_num = html.xpath('/html/body/div/div/div/div[2]/a/text()')[0].replace("查看全部","条评论").replace("条评论","").strip().replace(",","")
            except:
                rating_num=""

            try:
                star = "|".join(re.findall('class="a-link-normal" title="(.*?)"',r2.text)[::2])
            except:
                star = ""
            try:
                res_s = star
                new_star_list=[]
                star_list = re.findall("(.*?) 的评论都有 (.*?) 颗星", star)
                for dex in star_list:
                    # print(float(int(dex[0].strip(r"|").strip(r"%"))/100))
                    st_res = int(float(float(dex[0].strip(r"|").strip(r"%")) / 100) * int(rating_num))
                    # print(st_res)
                    new_star_list.append((st_res, dex[0]))
                for i in range(len(star_list)):
                    res_s = res_s.replace(star_list[i][0], "%d个" % new_star_list[i][0])
                    # print(res_s)
                res_s= res_s.replace("颗星", "颗星 | ").replace(" 的评论", "评论").replace("都有", "是")[:-2]
                print("商品名称:%s,商品评价星级:%s,商品评价总人数:%s,商品评价详情:%s"%(goods_name,sum_star,rating_num,res_s))
                check_amazon = Amazon.query.filter_by(asin=goods_id).first()
                r4 = spider_session.get(url=goods_url,headers={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'})
                r4_html = etree.HTML(r4.text)
                try:
                    goods_name = r4_html.xpath('//*[@id="productTitle"]')[0].text.replace("\n","").strip()
                except:
                    goods_name = r4_html.xpath('//*[@id="productTitle"]').text.replace("\n","").strip()
                print("二次抓取名称"+goods_name)
                if check_amazon:
                    spider_time = check_amazon.spider_time
                    db.session.delete(check_amazon)
                    db.session.commit()

                    print("删除旧数据")
                res = "%s,%s,%s,%s\n" % (goods_name, sum_star, rating_num, res_s)
                if spider_time=="0":
                    with open("./download_fiels/%s长期监控商品信息.csv" % (datetime.datetime.now().strftime('%Y-%m-%d')), "a",
                  encoding='utf-8-sig') as f:
                        f.write(res)
                else:
                    with open("./download_fiels/%s短期监控商品信息.csv" % (datetime.datetime.now().strftime('%Y-%m-%d')), "a",
                              encoding='utf-8-sig') as f:
                        f.write(res)
                amazon_info = Amazon(asin=goods_id, goods_name=goods_name, sum_star=sum_star,rating_num=rating_num, star=res_s,url=goods_url,spider_time=spider_time)
                db.session.add(amazon_info)
                print("更新数据成功")
                db.session.commit()
                return res
            except Exception as e:
                db.session.rollback()
                raise e
                print("数据存储失败")