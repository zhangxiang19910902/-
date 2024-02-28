import re
import requests
import time
import pymysql
import bs4
import json
from scrapy import Selector
from datetime import datetime
from pymongo import MongoClient
'''
http://www-pkulaw-com-s.nmg1.yyttgd.top/penalty/adv

卡号：57726728  
密码：559550
第一步：打开链接 
http://www.90tsg.com
http://www.90tsg.com/e/member/login/
只有yn有权限
'''

def refiled( response):
    node_file_li = response.xpath("//div[@class='fields']//li//div[@class='box']")
    reField = {}
    for item_li in node_file_li:
        # 找strong
        fTitle = ''.join(item_li.xpath('.//strong//text()').getall()).replace("：", "").replace('\n', '').strip()
        fValue = ''.join(item_li.xpath('.//span//text()').getall()).replace("：", "").replace('\n', '').strip()
        if not fValue:
            fValue = ''.join(item_li.xpath('./text()').getall()).replace("：", "").replace('\n', '').strip()
        if not fValue:
            fValue = ''.join(item_li.xpath('.//a').xpath('string(.)').getall()).replace("：", "").replace('\n', '').strip()
        if fTitle:
            reField[fTitle] = fValue
        if not fTitle:
            fTitle = '处罚依据'
            fValue = ''.join(item_li.xpath('.//a').xpath('string(.)').getall()).replace("：", "").replace('\n', '').strip()
            fValue = reField[fTitle] + '、' + fValue
            reField[fTitle] = fValue
    return json.dumps(reField, ensure_ascii=False)


def beijing(cookies,headers,start_url,start_date,end_date):
    client = MongoClient('mongodb://localhost:27017/')
    collection_aaa = client.行政处罚.行政处罚_山东

    conn = pymysql.connect(host='rm-uf6x8ay71wjp5qm8mxo.mysql.rds.aliyuncs.com', user='root', password='Alex1985!@#',
                           db='law_bdfb', charset='utf8mb4')
    cursor = conn.cursor()
    num = 0

    for b in collection_aaa.find():
        url1 = b['url']
        url = 'http://www.pkulaw.yn.yyttgd.top' + url1

        while True:

            try:
                response2 = requests.get(
                    url,
                    cookies=cookies,
                    headers=headers,
                    # data=data,
                    verify=False,
                )

                if response2.status_code == 200:
                    # response2.encoding = "utf-8"
                    res2 = Selector(text=response2.text)
                    title = ''.join(res2.xpath("//div[@class='content']//*[@class='title']/text()").getall()).strip()
                    if title:
                        break
                    else:
                        print('没有取到详情页标题')
                if response2.status_code == 404:
                    # response2.encoding = "utf-8"
                    response2.encoding = 'utf-8'
                    res2 = Selector(text=response2.text)
                    title = ''.join(res2.xpath("//div[@class='errorTips']//h4/text()").getall()).strip()
                    if title:
                        print(f'{title}---{url}')
                        break

                else:
                    print(f"错误码：{response2.status_code}")
            except Exception as e:
                print(f"程序报错2：{e}")
        if '您访问的页面不存在' in title:
            continue
        is_shengyuweidu = res2.xpath("//*[@id='continueTips']")
        if is_shengyuweidu:
            return print('cookie过期')

        dode = url1.split('.html')[0].split('apy/')[-1]
        title = ''.join(res2.xpath("//div[@class='content']//*[@class='title']//text()").getall()).strip()
        url = url1
        content = ''.join(res2.xpath("//div[@class='content']//*[@class='fulltext']").getall()).strip()
        filed = refiled(res2)
        textContent = ''.join(
            res2.xpath("//div[@class='content']//*[@class='fulltext']//text()").getall()).strip()
        ctime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        fabu_time = ''.join(res2.xpath("//*[contains(text(),'处罚日期')]/following-sibling::text()").getall()).strip().replace('.',
                                                                                                    '-')
        weijie_name = ''.join(
            res2.xpath("//*[contains(text(),'处罚机关')]/following-sibling::text()").getall()).strip()
        insert = "INSERT IGNORE INTO law_xingzhengchufa_test (code,title,url,content,filed,textContent,ctime,fabu_time,weijie_name)  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        exe = (dode, title, url, content, filed, textContent, ctime, fabu_time, weijie_name)
        cursor.execute(insert, exe)
        conn.commit()
        if cursor.rowcount:
            num += 1
            print(f'插入成功{num}条----title: {title}')
        else:
            print(f'数据重复----title: {title}')

def run(cookies,headers,start_url,start_date,end_date):


    beijing(cookies, headers, start_url, start_date, end_date)


if __name__ == '__main__':
    cookies = {
        'referer': '',
        'CookieId': '6c8508f84f3bdcf0f5e1af33ef48f232',
        'SUB': 'dc7f4f02-f042-4ae3-bd45-8506f586ec54',
        'preferred_username': '%E4%BA%91%E5%8D%97%E5%A4%A7%E5%AD%A6',
        'authormes': 'ae65702f4acccc5f9d20e09da15d5727878f74cdbbed0b237d27c11eccaa136452380d61f9f8c5f4bdfb',
        'xCloseNew': '27',
        'pkulaw_v6_sessionid': 'ezugezf5ai4pilyufhppzb2b',
        'ddhgguuy_session': '7664ikscvqejfrcpijhlbbjbs5',
        '__tst_status': '4234677887#',
        'userislogincookie': 'always',
        'LoginAccount': 'äº‘å\x8d—å¤§å\xad¦',
        'referer': 'http://www.pkulaw.yn.yyttgd.top/',
    }

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie': '__tst_status=2102180200#; pkulaw_v6_sessionid=ru3qwlsljn3syweisx23n3wl; CookieId=6c8508f84f3bdcf0f5e1af33ef48f232; SUB=dc7f4f02-f042-4ae3-bd45-8506f586ec54; preferred_username=%E4%BA%91%E5%8D%97%E5%A4%A7%E5%AD%A6; ddhgguuy_session=clhcfbeh61afgukj5he8n5ee93; authormes=ae65702f4acccc5f9d20e09da15d5727878f74cdbbed0b237d27c11eccaa136452380d61f9f8c5f4bdfb; referer=http://www.pkulaw.yn.yyttgd.top/; xCloseNew=27',
        'Origin': 'http://www.pkulaw.yn.yyttgd.top',
        'Referer': 'http://www.pkulaw.yn.yyttgd.top/penalty/adv',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    start_date = '2023.01.04'
    end_date = '2023.01.04'
    start_url = 'http://www.pkulaw.yn.yyttgd.top'

    run(cookies, headers,start_url,start_date,end_date)