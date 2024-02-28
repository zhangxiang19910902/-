import re
import requests
import time
import pymysql
import bs4
import json
from scrapy import Selector
from datetime import datetime

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

def page_howmach(cookies,headers,start_url,start_date,end_date,data1):
    while True:
        try:
            response1 = requests.post(
                start_url + '/law/search/RecordSearch',
                cookies=cookies,
                headers=headers,
                data=data1,
                verify=False,
            )
            if response1.status_code == 200:
                response1.encoding = "utf-8"
                break
            else:
                print(response1.status_code)
        except Exception as e:
            print(f"程序报错1：{e}")

    res1 = Selector(text=response1.text)
    page = ''.join(res1.xpath("//span[@class='total']//strong//text()").getall()).strip()
    if page:
        print(f"{start_date}---{end_date}:一共{page}条")
        pages = int(page) // 100 + 1
        return pages
    else:
        infos = ''.join(
            res1.xpath("//div[@class='search-no-content']//div[@class='col-wrap']//p//text()").getall()).strip()
        infos = infos.split('\n')[0]
        print(infos)
        return infos

def zhongyang(cookies,headers,start_url,start_date,end_date,pages):
    conn = pymysql.connect(host='rm-uf6x8ay71wjp5qm8mxo.mysql.rds.aliyuncs.com', user='root', password='Alex1985!@#',
                           db='law_bdfb', charset='utf8mb4')
    cursor = conn.cursor()
    num = 0
    if pages:
        for page in range(pages):
            data = f"Menu=penalty&Keywords=&SearchKeywordType=Fulltext&MatchType=Exact&RangeType=Piece&Library=apy&ClassFlag=apy&GroupLibraries=&QueryOnClick=False&AfterSearch=True&PreviousLib=apy&pdfStr=&pdfTitle=&IsSynonymSearch=false&RequestFrom=&LastLibForChangeColumn=apy&IsAdv=True&ClassCodeKey=&Aggs.Category=&Aggs.PunishmentTarget=&Aggs.PunishmentTypeNew=&Aggs.EnforcementLevel=&Aggs.DepartCode=&Aggs.LawRegional=&Aggs.PunishmentDate=&GroupByIndex=1&OrderByIndex=0&ShowType=Default&GroupValue=&AdvSearchDic.Title=&AdvSearchDic.CheckFullText=&AdvSearchDic.DocumentNO=&AdvSearchDic.Category=&AdvSearchDic.PunishmentTypeNew=&AdvSearchDic.PunishmentObject=&AdvSearchDic.EnforcementLevel=&AdvSearchDic.DepartCode=&AdvSearchDic.LawRegional=01%2C%23containAny&AdvSearchDic.PunishmentDate=%7B+'Start'%3A+'{start_date}'%2C+'End'%3A+'{end_date}'+%7D&TitleKeywords=&FullTextKeywords=&Pager.PageIndex={page}&RecordShowType=List&Pager.PageIndex={page}&Pager.PageSize=100&QueryBase64Request=&VerifyCodeResult=&isEng=chinese&OldPageIndex={page}&newPageIndex={page}&IsShowListSummary=&X-Requested-With=XMLHttpRequest"
            while True:
                try:
                    response3 = requests.post(
                        start_url + '/penalty/search/RecordSearch',
                        cookies=cookies,
                        headers=headers,
                        data=data,
                        verify=False,
                        allow_redirects=False,

                    )
                    if response3.history:  # 判断是否有重定向
                        print("该请求被重定向了！")
                    else:
                        if response3.status_code == 200:
                            response3.encoding = "utf-8"
                            break
                        else:
                            print(response3.status_code)
                except Exception as e:
                    print(f"程序报错3：{e}")
            res3 = Selector(text=response3.text)
            url_list = res3.xpath("//div[@class='list-title']//h4/a[1]/@href").getall()
            for a in url_list:

                url = start_url + a
                while True:
                    time.sleep(1)
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

                dode = a.split('.html')[0].split('apy/')[-1]
                title = ''.join(res2.xpath("//div[@class='content']//*[@class='title']//text()").getall()).strip()
                url = a
                content = ''.join(res2.xpath("//div[@class='content']//*[@class='fulltext']").getall()).strip()
                filed = refiled(res2)
                textContent = ''.join(
                    res2.xpath("//div[@class='content']//*[@class='fulltext']//text()").getall()).strip()
                ctime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                fabu_time = ''.join(res2.xpath(
                    "//*[contains(text(),'处罚日期')]/following-sibling::text()").getall()).strip().replace('.',
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

def shandong(cookies,headers,start_url,start_date,end_date,pages):
    conn = pymysql.connect(host='rm-uf6x8ay71wjp5qm8mxo.mysql.rds.aliyuncs.com', user='root', password='Alex1985!@#',
                           db='law_bdfb', charset='utf8mb4')
    cursor = conn.cursor()
    num = 0
    if pages:
        for page in range(pages):
            data = f"Menu=penalty&Keywords=&SearchKeywordType=Fulltext&MatchType=Exact&RangeType=Piece&Library=apy&ClassFlag=apy&GroupLibraries=&QueryOnClick=False&AfterSearch=True&PreviousLib=apy&pdfStr=&pdfTitle=&IsSynonymSearch=false&RequestFrom=&LastLibForChangeColumn=apy&IsAdv=True&ClassCodeKey=&Aggs.Category=&Aggs.PunishmentTarget=&Aggs.PunishmentTypeNew=&Aggs.EnforcementLevel=&Aggs.DepartCode=&Aggs.LawRegional=&Aggs.PunishmentDate=&GroupByIndex=1&OrderByIndex=0&ShowType=Default&GroupValue=&AdvSearchDic.Title=&AdvSearchDic.CheckFullText=&AdvSearchDic.DocumentNO=&AdvSearchDic.Category=&AdvSearchDic.PunishmentTypeNew=&AdvSearchDic.PunishmentObject=&AdvSearchDic.EnforcementLevel=&AdvSearchDic.DepartCode=&AdvSearchDic.LawRegional=37%2C%23containAny&AdvSearchDic.PunishmentDate=%7B+'Start'%3A+'{start_date}'%2C+'End'%3A+'{end_date}'+%7D&TitleKeywords=&FullTextKeywords=&Pager.PageIndex={page}&RecordShowType=List&Pager.PageIndex={page}&Pager.PageSize=100&QueryBase64Request=&VerifyCodeResult=&isEng=chinese&OldPageIndex={page}&newPageIndex={page}&IsShowListSummary=&X-Requested-With=XMLHttpRequest"
            while True:
                try:
                    response3 = requests.post(
                        start_url + '/penalty/search/RecordSearch',
                        cookies=cookies,
                        headers=headers,
                        data=data,
                        verify=False,
                        allow_redirects=False,

                    )
                    if response3.history:  # 判断是否有重定向
                        print("该请求被重定向了！")
                    else:
                        if response3.status_code == 200:
                            response3.encoding = "utf-8"
                            break
                        else:
                            print(response3.status_code)
                except Exception as e:
                    print(f"程序报错3：{e}")
            res3 = Selector(text=response3.text)
            url_list = res3.xpath("//div[@class='list-title']//h4/a[1]/@href").getall()
            for a in url_list:
                #图书馆
                url = start_url + a
                #个人
                # url = 'https://182-150-59-104-p8888-a582.gz.80589.org' + a

                while True:
                    time.sleep(1)
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
                                print(f'没有取到详情页标题---{url}')
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

                dode = a.split('.html')[0].split('apy/')[-1]
                title = ''.join(res2.xpath("//div[@class='content']//*[@class='title']//text()").getall()).strip()
                url = a
                content = ''.join(res2.xpath("//div[@class='content']//*[@class='fulltext']").getall()).strip()
                filed = refiled(res2)
                textContent = ''.join(
                    res2.xpath("//div[@class='content']//*[@class='fulltext']//text()").getall()).strip()
                ctime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                fabu_time = ''.join(res2.xpath(
                    "//*[contains(text(),'处罚日期')]/following-sibling::text()").getall()).strip().replace('.',
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

def beijing(cookies,headers,start_url,start_date,end_date,pages):
    conn = pymysql.connect(host='rm-uf6x8ay71wjp5qm8mxo.mysql.rds.aliyuncs.com', user='root', password='Alex1985!@#',
                           db='law_bdfb', charset='utf8mb4')
    cursor = conn.cursor()
    num = 0
    if pages:
        for page in range(pages):
            data = f"Menu=penalty&Keywords=&SearchKeywordType=Fulltext&MatchType=Exact&RangeType=Piece&Library=apy&ClassFlag=apy&GroupLibraries=&QueryOnClick=False&AfterSearch=True&PreviousLib=apy&pdfStr=&pdfTitle=&IsSynonymSearch=false&RequestFrom=&LastLibForChangeColumn=apy&IsAdv=True&ClassCodeKey=&Aggs.Category=&Aggs.PunishmentTarget=&Aggs.PunishmentTypeNew=&Aggs.EnforcementLevel=&Aggs.DepartCode=&Aggs.LawRegional=&Aggs.PunishmentDate=&GroupByIndex=1&OrderByIndex=0&ShowType=Default&GroupValue=&AdvSearchDic.Title=&AdvSearchDic.CheckFullText=&AdvSearchDic.DocumentNO=&AdvSearchDic.Category=&AdvSearchDic.PunishmentTypeNew=&AdvSearchDic.PunishmentObject=&AdvSearchDic.EnforcementLevel=&AdvSearchDic.DepartCode=&AdvSearchDic.LawRegional=11%2C%23containAny&AdvSearchDic.PunishmentDate=%7B+'Start'%3A+'{start_date}'%2C+'End'%3A+'{end_date}'+%7D&TitleKeywords=&FullTextKeywords=&Pager.PageIndex={page}&RecordShowType=List&Pager.PageIndex={page}&Pager.PageSize=100&QueryBase64Request=&VerifyCodeResult=&isEng=chinese&OldPageIndex={page}&newPageIndex={page}&IsShowListSummary=&X-Requested-With=XMLHttpRequest"
            while True:
                try:
                    response3 = requests.post(
                        start_url + '/penalty/search/RecordSearch',
                        cookies=cookies,
                        headers=headers,
                        data=data,
                        verify=False,
                        allow_redirects=False,

                    )
                    if response3.history:  # 判断是否有重定向
                        print("该请求被重定向了！")
                    else:
                        if response3.status_code == 200:
                            response3.encoding = "utf-8"
                            break
                        else:
                            print(response3.status_code)
                except Exception as e:
                    print(f"程序报错3：{e}")
            res3 = Selector(text=response3.text)
            url_list = res3.xpath("//div[@class='list-title']//h4/a[1]/@href").getall()
            for a in url_list:

                url = start_url + a
                while True:
                    time.sleep(1)
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

                dode = a.split('.html')[0].split('apy/')[-1]
                title = ''.join(res2.xpath("//div[@class='content']//*[@class='title']//text()").getall()).strip()
                url = a
                content = ''.join(res2.xpath("//div[@class='content']//*[@class='fulltext']").getall()).strip()
                filed = refiled(res2)
                textContent = ''.join(
                    res2.xpath("//div[@class='content']//*[@class='fulltext']//text()").getall()).strip()
                ctime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                fabu_time = ''.join(res2.xpath(
                    "//*[contains(text(),'处罚日期')]/following-sibling::text()").getall()).strip().replace('.',
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
    # print('开始爬取中央处罚')
    # zhongyang_data1 = f"Menu=penalty&Keywords=&SearchKeywordType=Fulltext&MatchType=Exact&RangeType=Piece&Library=apy&ClassFlag=apy&GroupLibraries=&QueryOnClick=False&AfterSearch=True&PreviousLib=apy&pdfStr=&pdfTitle=&IsSynonymSearch=false&RequestFrom=&LastLibForChangeColumn=apy&IsAdv=True&ClassCodeKey=&Aggs.Category=&Aggs.PunishmentTarget=&Aggs.PunishmentTypeNew=&Aggs.EnforcementLevel=&Aggs.DepartCode=&Aggs.LawRegional=&Aggs.PunishmentDate=&GroupByIndex=1&OrderByIndex=0&ShowType=Default&GroupValue=&AdvSearchDic.Title=&AdvSearchDic.CheckFullText=&AdvSearchDic.DocumentNO=&AdvSearchDic.Category=&AdvSearchDic.PunishmentTypeNew=&AdvSearchDic.PunishmentObject=&AdvSearchDic.EnforcementLevel=&AdvSearchDic.DepartCode=&AdvSearchDic.LawRegional=01%2C%23containAny&AdvSearchDic.PunishmentDate=%7B+'Start'%3A+'{start_date}'%2C+'End'%3A+'{end_date}'+%7D&TitleKeywords=&FullTextKeywords=&Pager.PageIndex=0&RecordShowType=List&Pager.PageIndex=0&Pager.PageSize=100&QueryBase64Request=&VerifyCodeResult=&isEng=chinese&OldPageIndex=&newPageIndex=&IsShowListSummary=&X-Requested-With=XMLHttpRequest"
    # zhongyan_page = page_howmach(cookies, headers, start_url, start_date, end_date, zhongyang_data1)
    # zhongyang( cookies, headers,start_url,start_date,end_date,zhongyan_page)

    print('开始爬取山东处罚')
    shandong_data1 = f"Menu=penalty&Keywords=&SearchKeywordType=Fulltext&MatchType=Exact&RangeType=Piece&Library=apy&ClassFlag=apy&GroupLibraries=&QueryOnClick=False&AfterSearch=True&PreviousLib=apy&pdfStr=&pdfTitle=&IsSynonymSearch=false&RequestFrom=&LastLibForChangeColumn=apy&IsAdv=True&ClassCodeKey=&Aggs.Category=&Aggs.PunishmentTarget=&Aggs.PunishmentTypeNew=&Aggs.EnforcementLevel=&Aggs.DepartCode=&Aggs.LawRegional=&Aggs.PunishmentDate=&GroupByIndex=1&OrderByIndex=0&ShowType=Default&GroupValue=&AdvSearchDic.Title=&AdvSearchDic.CheckFullText=&AdvSearchDic.DocumentNO=&AdvSearchDic.Category=&AdvSearchDic.PunishmentTypeNew=&AdvSearchDic.PunishmentObject=&AdvSearchDic.EnforcementLevel=&AdvSearchDic.DepartCode=&AdvSearchDic.LawRegional=37%2C%23containAny&AdvSearchDic.PunishmentDate=%7B+'Start'%3A+'{start_date}'%2C+'End'%3A+'{end_date}'+%7D&TitleKeywords=&FullTextKeywords=&Pager.PageIndex=0&RecordShowType=List&Pager.PageIndex=0&Pager.PageSize=100&QueryBase64Request=&VerifyCodeResult=&isEng=chinese&OldPageIndex=&newPageIndex=&IsShowListSummary=&X-Requested-With=XMLHttpRequest"
    shandong_page = page_howmach(cookies,headers,start_url,start_date,end_date,shandong_data1)
    shandong(cookies, headers, start_url,start_date,end_date,shandong_page)

    # print('开始爬取北京处罚')
    # beijing_data1 = f"Menu=penalty&Keywords=&SearchKeywordType=Fulltext&MatchType=Exact&RangeType=Piece&Library=apy&ClassFlag=apy&GroupLibraries=&QueryOnClick=False&AfterSearch=True&PreviousLib=apy&pdfStr=&pdfTitle=&IsSynonymSearch=false&RequestFrom=&LastLibForChangeColumn=apy&IsAdv=True&ClassCodeKey=&Aggs.Category=&Aggs.PunishmentTarget=&Aggs.PunishmentTypeNew=&Aggs.EnforcementLevel=&Aggs.DepartCode=&Aggs.LawRegional=&Aggs.PunishmentDate=&GroupByIndex=1&OrderByIndex=0&ShowType=Default&GroupValue=&AdvSearchDic.Title=&AdvSearchDic.CheckFullText=&AdvSearchDic.DocumentNO=&AdvSearchDic.Category=&AdvSearchDic.PunishmentTypeNew=&AdvSearchDic.PunishmentObject=&AdvSearchDic.EnforcementLevel=&AdvSearchDic.DepartCode=&AdvSearchDic.LawRegional=11%2C%23containAny&AdvSearchDic.PunishmentDate=%7B+'Start'%3A+'{start_date}'%2C+'End'%3A+'{end_date}'+%7D&TitleKeywords=&FullTextKeywords=&Pager.PageIndex=0&RecordShowType=List&Pager.PageIndex=0&Pager.PageSize=100&QueryBase64Request=&VerifyCodeResult=&isEng=chinese&OldPageIndex=&newPageIndex=&IsShowListSummary=&X-Requested-With=XMLHttpRequest"
    # beijing_page = page_howmach(cookies, headers, start_url, start_date, end_date, beijing_data1)
    # beijing(cookies, headers, start_url, start_date, end_date, beijing_page)


if __name__ == '__main__':
    cookies = {
        'referer': '',
        'CookieId': '6c8508f84f3bdcf0f5e1af33ef48f232',
        'SUB': 'dc7f4f02-f042-4ae3-bd45-8506f586ec54',
        'preferred_username': '%E4%BA%91%E5%8D%97%E5%A4%A7%E5%AD%A6',
        'pkulaw_v6_sessionid': 'ezugezf5ai4pilyufhppzb2b',
        '__tst_status': '4234677887#',
        'ddhgguuy_session': 'pt8du73appto1du60tn4iqsl83',
        'userislogincookie': 'always',
        'LoginAccount': 'äº‘å\x8d—å¤§å\xad¦',
        'authormes': 'ae65702f4acccc5f9d20e09da15d5727878f74cdbbed0b237d27c11eccaa136452380d61f9f8c5f4bdfb',
        'referer': 'http://www.pkulaw.yn.yyttgd.top/',
        'xCloseNew': '28',
    }

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie': '__tst_status=2102180200#; pkulaw_v6_sessionid=ru3qwlsljn3syweisx23n3wl; CookieId=6c8508f84f3bdcf0f5e1af33ef48f232; SUB=dc7f4f02-f042-4ae3-bd45-8506f586ec54; preferred_username=%E4%BA%91%E5%8D%97%E5%A4%A7%E5%AD%A6; ddhgguuy_session=clhcfbeh61afgukj5he8n5ee93; userislogincookie=always; LoginAccount=äº‘å\x8d—å¤§å\xad¦; authormes=ae65702f4acccc5f9d20e09da15d5727878f74cdbbed0b237d27c11eccaa136452380d61f9f8c5f4bdfb; referer=http://www.pkulaw.yn.yyttgd.top/; xCloseNew=27',
        'Origin': 'http://www.pkulaw.yn.yyttgd.top',
        'Referer': 'http://www.pkulaw.yn.yyttgd.top/penalty/adv',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    start_date = '2024.01.27'
    end_date = '2024.01.30'
    start_url = 'http://www.pkulaw.yn.yyttgd.top'

    run(cookies, headers,start_url,start_date,end_date)