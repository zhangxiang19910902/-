import re
import requests
import time
import pymysql
import bs4
import json
from scrapy import Selector
from datetime import datetime

'''
http://www.pkulaw.jssfs.yyttgd.top/law/adv/lar

http://mv616.xyz/e/member/login/ 
"name":"733744260"
"pass":"728162"
'''

def refiled(response):
    main_page = bs4.BeautifulSoup(response.text, "html.parser")
    # 获取全部数据
    node_info = main_page.find(name="div", class_="content")
    node_file = node_info.find(name="div", class_="fields")
    node_file_li = node_file.find_all("li")
    reField = {}
    for item_li in node_file_li:
        fAll = item_li.text.strip()
        # 找strong
        fTitle = item_li.find(name="strong").text.replace(
            "：", "").replace('\n', '')
        fValue = fAll.replace(fTitle, "").replace(
            "：", "").replace('\n', '')
        reField[fTitle] = fValue
    return json.dumps(reField, ensure_ascii=False)

def difang(start_time,end_time,cookies,headers,start_url):
    conn = pymysql.connect(host='rm-uf6x8ay71wjp5qm8mxo.mysql.rds.aliyuncs.com', user='root', password='Alex1985!@#',
                           db='law_bdfb', charset='utf8mb4')
    cursor = conn.cursor()
    num = 0
    data = f"Menu=law&Keywords=&SearchKeywordType=Fulltext&MatchType=Exact&RangeType=Piece&Library=lar&ClassFlag=lar&GroupLibraries=&QueryOnClick=False&AfterSearch=True&PreviousLib=lar&pdfStr=&pdfTitle=&IsSynonymSearch=false&RequestFrom=&LastLibForChangeColumn=lar&IsAdv=True&ClassCodeKey=&Aggs.RelatedPrompted=&Aggs.EffectivenessDic=&Aggs.SpecialType=&Aggs.IssueDepartment=&Aggs.TimelinessDic=&Aggs.Category=&Aggs.IssueDate=&GroupByIndex=2&OrderByIndex=0&ShowType=Default&GroupValue=&AdvSearchDic.Title=&AdvSearchDic.CheckFullText=&AdvSearchDic.IssueDepartment=&AdvSearchDic.DocumentNO=&AdvSearchDic.RatifyDepartment=&AdvSearchDic.RatifyDate=%7B+'Start'%3A+''%2C+'End'%3A+''+%7D&AdvSearchDic.IssueDate=%7B+'Start'%3A+'{start_time}'%2C+'End'%3A+'{end_time}'+%7D&AdvSearchDic.ImplementDate=%7B+'Start'%3A+''%2C+'End'%3A+''+%7D&AdvSearchDic.TimelinessDic=&AdvSearchDic.EffectivenessDic=&AdvSearchDic.Category=&AdvSearchDic.SpecialType=&TitleKeywords=&FullTextKeywords=&Pager.PageIndex=0&RecordShowType=List&Pager.PageIndex=0&Pager.PageSize=100&QueryBase64Request=&VerifyCodeResult=&isEng=chinese&OldPageIndex=&newPageIndex=&IsShowListSummary=&X-Requested-With=XMLHttpRequest"
    while True:
        try:
            response1 = requests.post(
                start_url+'/law/search/RecordSearch',
                cookies=cookies,
                headers=headers,
                data=data,
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
        print(f"{start_time}---{end_time}:一共{page}条")
        pages = int(page)//100 +1
        if pages:
            for page in range(pages):
                data = f"Menu=law&Keywords=&SearchKeywordType=Fulltext&MatchType=Exact&RangeType=Piece&Library=lar&ClassFlag=lar&GroupLibraries=&QueryOnClick=False&AfterSearch=True&PreviousLib=lar&pdfStr=&pdfTitle=&IsSynonymSearch=false&RequestFrom=&LastLibForChangeColumn=lar&IsAdv=True&ClassCodeKey=&Aggs.RelatedPrompted=&Aggs.EffectivenessDic=&Aggs.SpecialType=&Aggs.IssueDepartment=&Aggs.TimelinessDic=&Aggs.Category=&Aggs.IssueDate=&GroupByIndex=2&OrderByIndex=0&ShowType=Default&GroupValue=&AdvSearchDic.Title=&AdvSearchDic.CheckFullText=&AdvSearchDic.IssueDepartment=&AdvSearchDic.DocumentNO=&AdvSearchDic.RatifyDepartment=&AdvSearchDic.RatifyDate=%7B+'Start'%3A+''%2C+'End'%3A+''+%7D&AdvSearchDic.IssueDate=%7B+'Start'%3A+'{start_time}'%2C+'End'%3A+'{end_time}'+%7D&AdvSearchDic.ImplementDate=%7B+'Start'%3A+''%2C+'End'%3A+''+%7D&AdvSearchDic.TimelinessDic=&AdvSearchDic.EffectivenessDic=&AdvSearchDic.Category=&AdvSearchDic.SpecialType=&TitleKeywords=&FullTextKeywords=&Pager.PageIndex={page}&RecordShowType=List&Pager.PageIndex={page}&Pager.PageSize=100&QueryBase64Request=&VerifyCodeResult=&isEng=chinese&OldPageIndex={page}&newPageIndex={page}&IsShowListSummary=&X-Requested-With=XMLHttpRequest"
                while True:
                    try:
                        response3 = requests.post(
                            start_url + '/law/search/RecordSearch',
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
                print('aaa')
                print(page+1)
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
                                title = ''.join(res2.xpath("//div[@class='content']//*[@class='title']//text()").getall())
                                if title:
                                    break
                                else:
                                    print('没有取到详情页标题')
                            else:
                                print(f"错误码：{response2.status_code}")
                        except Exception as e:
                            print(f"程序报错2：{e}")

                    is_shengyuweidu = res2.xpath("//*[@id='continueTips']")
                    if is_shengyuweidu:
                        return print('cookie过期')

                    dode = ''.join(res2.xpath("//div[@class='info']//a//text()").getall()).strip()
                    title = ''.join(res2.xpath("//div[@class='content']//*[@class='title']//text()").getall()).replace('尚未施行','').replace('\n','').strip()
                    url = a
                    content = ''.join(res2.xpath("//div[@class='content']//*[@class='fulltext']").getall()).strip()
                    filed = refiled(response2)
                    textContent = ''.join(
                        res2.xpath("//div[@class='content']//*[@class='fulltext']//text()").getall()).strip()
                    ctime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    fabu_time = ''.join(
                        res2.xpath("//*[contains(text(),'公布日期')]/following-sibling::text()").getall()).strip().replace(
                        '.', '-')
                    insert = "INSERT IGNORE INTO law_difang_test (code,title,url,content,filed,textContent,ctime,fabu_time)  VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                    exe = (dode, title, url, content, filed, textContent, ctime, fabu_time)
                    cursor.execute(insert, exe)
                    conn.commit()
                    if cursor.rowcount:
                        num += 1
                        print(f'插入成功{num}条----title: {title}')
                    else:
                        print(f'数据重复----title: {title}')
    else:
        infos = ''.join(res1.xpath("//div[@class='search-no-content']//div[@class='col-wrap']//p//text()").getall()).strip()
        infos = infos.split('\n')[0]
        print(infos)

def zhongyang(start_time,end_time,cookies,headers,start_url):
    conn = pymysql.connect(host='rm-uf6x8ay71wjp5qm8mxo.mysql.rds.aliyuncs.com', user='root', password='Alex1985!@#',
                           db='law_bdfb', charset='utf8mb4')
    cursor = conn.cursor()
    num = 0
    data = f"Menu=law&Keywords=&SearchKeywordType=Fulltext&MatchType=Exact&RangeType=Piece&Library=chl&ClassFlag=chl&GroupLibraries=&QueryOnClick=False&AfterSearch=True&PreviousLib=chl&pdfStr=&pdfTitle=&IsSynonymSearch=false&RequestFrom=btnSearch&LastLibForChangeColumn=chl&IsAdv=True&ClassCodeKey=&Aggs.RelatedPrompted=&Aggs.EffectivenessDic=&Aggs.SpecialType=&Aggs.IssueDepartment=&Aggs.TimelinessDic=&Aggs.Category=&Aggs.IssueDate=&GroupByIndex=2&OrderByIndex=0&ShowType=Default&GroupValue=&AdvSearchDic.Title=&AdvSearchDic.CheckFullText=&AdvSearchDic.IssueDepartment=&AdvSearchDic.DocumentNO=&AdvSearchDic.RatifyDepartment=&AdvSearchDic.RatifyDate=%7B+'Start'%3A+''%2C+'End'%3A+''+%7D&AdvSearchDic.IssueDate=%7B+'Start'%3A+'{start_time}'%2C+'End'%3A+'{end_time}'+%7D&AdvSearchDic.ImplementDate=%7B+'Start'%3A+''%2C+'End'%3A+''+%7D&AdvSearchDic.TimelinessDic=&AdvSearchDic.EffectivenessDic=&AdvSearchDic.Category=&AdvSearchDic.SpecialType=&TitleKeywords=&FullTextKeywords=&Pager.PageIndex=0&RecordShowType=List&Pager.PageIndex=0&Pager.PageSize=100&QueryBase64Request=&VerifyCodeResult=&isEng=chinese&OldPageIndex=&newPageIndex=&IsShowListSummary=&X-Requested-With=XMLHttpRequest"

    while True:
        try:
            response1 = requests.post(
                start_url+'/law/search/RecordSearch',
                cookies=cookies,
                headers=headers,
                data=data,
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
        print(f"{start_time}---{end_time}:一共{page}条")
        pages = int(page)//100 +1
        if pages:
            for page in range(pages):
                data = f"Menu=law&Keywords=&SearchKeywordType=Fulltext&MatchType=Exact&RangeType=Piece&Library=chl&ClassFlag=chl&GroupLibraries=&QueryOnClick=False&AfterSearch=True&PreviousLib=chl&pdfStr=&pdfTitle=&IsSynonymSearch=false&RequestFrom=btnSearch&LastLibForChangeColumn=chl&IsAdv=True&ClassCodeKey=&Aggs.RelatedPrompted=&Aggs.EffectivenessDic=&Aggs.SpecialType=&Aggs.IssueDepartment=&Aggs.TimelinessDic=&Aggs.Category=&Aggs.IssueDate=&GroupByIndex=2&OrderByIndex=0&ShowType=Default&GroupValue=&AdvSearchDic.Title=&AdvSearchDic.CheckFullText=&AdvSearchDic.IssueDepartment=&AdvSearchDic.DocumentNO=&AdvSearchDic.RatifyDepartment=&AdvSearchDic.RatifyDate=%7B+'Start'%3A+''%2C+'End'%3A+''+%7D&AdvSearchDic.IssueDate=%7B+'Start'%3A+'{start_time}'%2C+'End'%3A+'{end_time}'+%7D&AdvSearchDic.ImplementDate=%7B+'Start'%3A+''%2C+'End'%3A+''+%7D&AdvSearchDic.TimelinessDic=&AdvSearchDic.EffectivenessDic=&AdvSearchDic.Category=&AdvSearchDic.SpecialType=&TitleKeywords=&FullTextKeywords=&Pager.PageIndex={page}&RecordShowType=List&Pager.PageIndex={page}&Pager.PageSize=100&QueryBase64Request=&VerifyCodeResult=&isEng=chinese&OldPageIndex={page}&newPageIndex={page}&IsShowListSummary=&X-Requested-With=XMLHttpRequest"
                while True:
                    try:
                        response3 = requests.post(
                            start_url + '/law/search/RecordSearch',
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
                print('aaa')
                print(page+1)
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
                                title = ''.join(res2.xpath("//div[@class='content']//*[@class='title']/text()").getall())
                                if title:
                                    break
                                else:
                                    print('没有取到详情页标题')
                            else:
                                print(f"错误码：{response2.status_code}")
                        except Exception as e:
                            print(f"程序报错2：{e}")

                    is_shengyuweidu = res2.xpath("//*[@id='continueTips']")
                    if is_shengyuweidu:
                        return print('cookie过期')

                    dode = ''.join(res2.xpath("//div[@class='info']//a//text()").getall()).strip()
                    title = ''.join(res2.xpath("//div[@class='content']//*[@class='title']//text()").getall()).replace('English','').replace('尚未施行','').replace('\n','').strip()
                    url = a
                    content = ''.join(res2.xpath("//div[@class='content']//*[@class='fulltext']").getall()).strip()
                    filed = refiled(response2)
                    textContent = ''.join(
                        res2.xpath("//div[@class='content']//*[@class='fulltext']//text()").getall()).strip()
                    ctime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    fabu_time = ''.join(
                        res2.xpath("//*[contains(text(),'公布日期')]/following-sibling::text()").getall()).strip().replace(
                        '.', '-')
                    insert = "INSERT IGNORE INTO law_zhongyang_test (code,title,url,content,filed,textContent,ctime,fabu_time)  VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                    exe = (dode, title, url, content, filed, textContent, ctime, fabu_time)
                    cursor.execute(insert, exe)
                    conn.commit()
                    if cursor.rowcount:
                        num += 1
                        print(f'插入成功{num}条----title: {title}')
                    else:
                        print(f'数据重复----title: {title}')
    else:
        infos = ''.join(res1.xpath("//div[@class='search-no-content']//div[@class='col-wrap']//p//text()").getall()).strip()
        infos = infos.split('\n')[0]
        print(infos)

def zhongwaitiaoyue(start_time,end_time,cookies,headers,start_url):
    conn = pymysql.connect(host='rm-uf6x8ay71wjp5qm8mxo.mysql.rds.aliyuncs.com', user='root', password='Alex1985!@#',
                           db='law_bdfb', charset='utf8mb4')
    cursor = conn.cursor()
    num = 0
    data = f"Menu=law&Keywords=&SearchKeywordType=Fulltext&MatchType=Exact&RangeType=Piece&Library=eagn&ClassFlag=eagn&GroupLibraries=&QueryOnClick=False&AfterSearch=True&PreviousLib=eagn&pdfStr=&pdfTitle=&IsSynonymSearch=false&RequestFrom=&LastLibForChangeColumn=eagn&IsAdv=True&ClassCodeKey=&Aggs.IssueDepartment=&Aggs.Kind=&Aggs.Category=&Aggs.IssueDate=&GroupByIndex=0&OrderByIndex=0&ShowType=Default&GroupValue=&AdvSearchDic.Title=&AdvSearchDic.CheckFullText=&AdvSearchDic.IssueDate=%7B+'Start'%3A+'{start_time}'%2C+'End'%3A+'{end_time}'+%7D&AdvSearchDic.IssueDepartment=&AdvSearchDic.ImplementDate=%7B+'Start'%3A+''%2C+'End'%3A+''+%7D&AdvSearchDic.Category=&AdvSearchDic.Kind=&AdvSearchDic.KnowWell=&AdvSearchDic.SubmitDepartment=&TitleKeywords=&FullTextKeywords=&Pager.PageIndex=0&RecordShowType=List&Pager.PageIndex=0&Pager.PageSize=100&QueryBase64Request=&VerifyCodeResult=&isEng=chinese&OldPageIndex=&newPageIndex=&IsShowListSummary=&X-Requested-With=XMLHttpRequest"
    while True:
        try:
            response1 = requests.post(
                start_url+'/law/search/RecordSearch',
                cookies=cookies,
                headers=headers,
                data=data,
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
        print(f"{start_time}---{end_time}:一共{page}条")
    url_list = res1.xpath("//div[@class='list-title']//h4/a[1]/@href").getall()
    if url_list:
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
                        title = ''.join(res2.xpath("//div[@class='content']//*[@class='title']/text()").getall())
                        if title:
                            break
                        else:
                            infos = ''.join(res2.xpath("//div[@style='height: 180px; line-height: 51px; text-align: center; padding-top: 60px;']//text()").getall())
                            print(infos)
                            print('没有取到详情页标题')
                    else:
                        print(f"错误码：{response2.status_code}")
                except Exception as e:
                    print(f"程序报错2：{e}")

            is_shengyuweidu = res2.xpath("//*[@id='continueTips']")
            if is_shengyuweidu:
                return print('cookie过期')

            dode = ''.join(res2.xpath("//div[@class='info']//a//text()").getall()).strip()
            title = ''.join(res2.xpath("//div[@class='content']//*[@class='title']//text()").getall()).replace('English','').replace('尚未施行','').replace('\n','').strip()
            url = a
            content = ''.join(res2.xpath("//div[@class='content']//*[@class='fulltext']").getall()).strip()
            filed = refiled(response2)
            textContent = ''.join(res2.xpath("//div[@class='content']//*[@class='fulltext']//text()").getall()).strip()
            ctime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            guojia_code = ' '.join(res2.xpath("//strong[contains(text(),'国家与国际组织：')]/following-sibling::a/@href").getall()).strip()
            if guojia_code:
                guojia_code = ', '.join(re.findall('IssueDepartment=(.*?)&way',guojia_code))
            guojia_name = ', '.join(res2.xpath("//strong[contains(text(),'国家与国际组织：')]/following-sibling::a//text()").getall()).strip()
            insert = "INSERT IGNORE INTO law_zhongwai_test (code,title,url,content,filed,textContent,ctime,guojia_code,guojia_name)  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            exe = (dode, title, url, content, filed, textContent, ctime, guojia_code, guojia_name)
            cursor.execute(insert, exe)
            conn.commit()
            if cursor.rowcount:
                num += 1
                print(f'插入成功{num}条----title: {title}')
            else:
                print(f'数据重复----title: {title}')
    else:
        infos = ''.join(res1.xpath("//div[@class='search-no-content']//div[@class='col-wrap']//p//text()").getall()).strip()
        infos = infos.split('\n')[0]
        print(infos)

def waiguofagui(start_time,end_time,cookies,headers,start_url):
    conn = pymysql.connect(host='rm-uf6x8ay71wjp5qm8mxo.mysql.rds.aliyuncs.com', user='root', password='Alex1985!@#',
                           db='law_bdfb', charset='utf8mb4')
    cursor = conn.cursor()
    num = 0
    data = f"Menu=law&Keywords=&SearchKeywordType=Fulltext&MatchType=Exact&RangeType=Piece&Library=iel&ClassFlag=iel&GroupLibraries=&QueryOnClick=False&AfterSearch=True&PreviousLib=iel&pdfStr=&pdfTitle=&IsSynonymSearch=false&RequestFrom=&LastLibForChangeColumn=&IsAdv=True&ClassCodeKey=&Aggs.IssueDepartment=&Aggs.Category=&Aggs.IssueDate=&GroupByIndex=0&OrderByIndex=0&ShowType=Default&GroupValue=&AdvSearchDic.Title=&AdvSearchDic.CheckFullText=&AdvSearchDic.IssueDepartment=&AdvSearchDic.IssueDate=%7B+'Start'%3A+''%2C+'End'%3A+''+%7D&AdvSearchDic.ImplementDate=%7B+'Start'%3A+'{start_time}'%2C+'End'%3A+'{end_time}'+%7D&AdvSearchDic.Category=&TitleKeywords=&FullTextKeywords=&Pager.PageIndex=0&RecordShowType=List&Pager.PageIndex=0&Pager.PageSize=10&QueryBase64Request=&VerifyCodeResult=&isEng=chinese&OldPageIndex=&newPageIndex=&IsShowListSummary=&X-Requested-With=XMLHttpRequest"
    while True:
        try:
            response1 = requests.post(
                start_url+'/law/search/RecordSearch',
                cookies=cookies,
                headers=headers,
                data=data,
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
        print(f"{start_time}---{end_time}:一共{page}条")

    url_list = res1.xpath("//div[@class='list-title']//h4/a[1]/@href").getall()
    if url_list:
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
                        title = ''.join(res2.xpath("//div[@class='content']//*[@class='title']/text()").getall())
                        if title:
                            break
                        else:
                            infos = ''.join(res2.xpath("//div[@style='height: 180px; line-height: 51px; text-align: center; padding-top: 60px;']//text()").getall())
                            print(infos)
                            print('没有取到详情页标题')
                    else:
                        print(f"错误码：{response2.status_code}")
                except Exception as e:
                    print(f"程序报错2：{e}")

            is_shengyuweidu = res2.xpath("//*[@id='continueTips']")
            if is_shengyuweidu:
                return print('cookie过期')

            dode = ''.join(res2.xpath("//div[@class='info']//a//text()").getall()).strip()
            title = ''.join(res2.xpath("//div[@class='content']//*[@class='title']//text()").getall()).replace('English','').replace('尚未施行','').replace('\n','').strip()
            url = a
            content = ''.join(res2.xpath("//div[@class='content']//*[@class='fulltext']").getall()).strip()
            filed = refiled(response2)
            textContent = ''.join(res2.xpath("//div[@class='content']//*[@class='fulltext']//text()").getall()).strip()
            ctime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            insert = "INSERT IGNORE INTO law_waiguo_test (code,title,url,content,filed,textContent,ctime)  VALUES (%s,%s,%s,%s,%s,%s,%s)"
            exe = (dode, title, url, content, filed, textContent, ctime)
            cursor.execute(insert, exe)
            conn.commit()
            if cursor.rowcount:
                num += 1
                print(f'插入成功{num}条----title: {title}')
            else:
                print(f'数据重复----title: {title}')
    else:
        infos = ''.join(res1.xpath("//div[@class='search-no-content']//div[@class='col-wrap']//p//text()").getall()).strip()
        infos = infos.split('\n')[0]
        print(infos)

def xianggang(start_time,end_time,cookies,headers,start_url):
    conn = pymysql.connect(host='rm-uf6x8ay71wjp5qm8mxo.mysql.rds.aliyuncs.com', user='root', password='Alex1985!@#',
                           db='law_bdfb', charset='utf8mb4')
    cursor = conn.cursor()
    num = 0
    data = f"Menu=law&Keywords=&SearchKeywordType=Fulltext&MatchType=Exact&RangeType=Piece&Library=hkd&ClassFlag=hkd&GroupLibraries=&QueryOnClick=False&AfterSearch=True&PreviousLib=hkd&pdfStr=&pdfTitle=&IsSynonymSearch=false&RequestFrom=&LastLibForChangeColumn=hkd&IsAdv=True&ClassCodeKey=&Aggs.Category=&GroupByIndex=0&OrderByIndex=&ShowType=Default&GroupValue=&AdvSearchDic.Title=&AdvSearchDic.CheckFullText=&AdvSearchDic.Category=&AdvSearchDic.TimelinessDic=&AdvSearchDic.Date=%7B+'Start'%3A+'{start_time}'%2C+'End'%3A+'{end_time}'+%7D&TitleKeywords=&FullTextKeywords=&Pager.PageIndex=0&RecordShowType=List&Pager.PageIndex=0&Pager.PageSize=100&QueryBase64Request=&VerifyCodeResult=&isEng=chinese&OldPageIndex=&newPageIndex=&IsShowListSummary=&X-Requested-With=XMLHttpRequest"
    # data = f"Menu=law&Keywords=&SearchKeywordType=Fulltext&MatchType=Exact&RangeType=Piece&Library=hkd&ClassFlag=hkd&GroupLibraries=&QueryOnClick=False&AfterSearch=True&PreviousLib=hkd&pdfStr=&pdfTitle=&IsSynonymSearch=false&RequestFrom=&LastLibForChangeColumn=hkd&IsAdv=True&ClassCodeKey=&Aggs.Category=&GroupByIndex=0&OrderByIndex=0&ShowType=Default&GroupValue=&AdvSearchDic.Title=&AdvSearchDic.CheckFullText=&AdvSearchDic.Category=&AdvSearchDic.TimelinessDic=&AdvSearchDic.Date=%7B+'Start'%3A+'{start_time}'%2C+'End'%3A+'{end_time}'+%7D&TitleKeywords=&FullTextKeywords=&Pager.PageIndex=1&RecordShowType=List&Pager.PageIndex=1&Pager.PageSize=100&QueryBase64Request=&VerifyCodeResult=&isEng=chinese&OldPageIndex=0&newPageIndex=&IsShowListSummary=&X-Requested-With=XMLHttpRequest"

    while True:
        try:
            response1 = requests.post(
                start_url+'/law/search/RecordSearch',
                cookies=cookies,
                headers=headers,
                data=data,
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
        print(f"{start_time}---{end_time}:一共{page}条")
    url_list = res1.xpath("//div[@class='list-title']//h4/a[1]/@href").getall()
    if url_list:
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
                        title = ''.join(res2.xpath("//div[@class='content']//*[@class='title']/text()").getall())
                        if title:
                            break
                        else:
                            infos = ''.join(res2.xpath("//div[@style='height: 180px; line-height: 51px; text-align: center; padding-top: 60px;']//text()").getall())
                            print(infos)
                            print('没有取到详情页标题')
                    else:
                        print(f"错误码：{response2.status_code}")
                except Exception as e:
                    print(f"程序报错2：{e}")

            is_shengyuweidu = res2.xpath("//*[@id='continueTips']")
            if is_shengyuweidu:
                return print('cookie过期')

            dode = ''.join(res2.xpath("//div[@class='info']//a//text()").getall()).strip()
            title = ''.join(res2.xpath("//div[@class='content']//*[@class='title']//text()").getall()).replace('English','').replace('尚未施行','').replace('\n','').strip()
            url = a
            content = ''.join(res2.xpath("//div[@class='content']//*[@class='fulltext']").getall()).strip()
            filed = refiled(response2)
            textContent = ''.join(res2.xpath("//div[@class='content']//*[@class='fulltext']//text()").getall()).strip()
            ctime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            fenlei_code = ' '.join(res2.xpath("//strong[contains(text(),'法规分类：')]/following-sibling::a/@href").getall()).strip()
            if fenlei_code:
                fenlei_code = ', '.join(re.findall('Category=(.*?)&way', fenlei_code))
            fenlei_name = ', '.join(res2.xpath("//strong[contains(text(),'法规分类：')]/following-sibling::a//text()").getall()).strip()
            insert = "INSERT IGNORE INTO law_xianggang_test (code,title,url,content,filed,textContent,ctime,fenlei_code,fenlei_name)  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            exe = (dode, title, url, content, filed, textContent, ctime, fenlei_code, fenlei_name)
            cursor.execute(insert, exe)
            conn.commit()
            if cursor.rowcount:
                num += 1
                print(f'插入成功{num}条----title: {title}')
            else:
                print(f'数据重复----title: {title}')
    else:
        infos = ''.join(res1.xpath("//div[@class='search-no-content']//div[@class='col-wrap']//p//text()").getall()).strip()
        infos = infos.split('\n')[0]
        print(infos)

def aomen(start_time,end_time,cookies,headers,start_url):
    conn = pymysql.connect(host='rm-uf6x8ay71wjp5qm8mxo.mysql.rds.aliyuncs.com', user='root', password='Alex1985!@#',
                           db='law_bdfb', charset='utf8mb4')
    cursor = conn.cursor()
    num = 0
    data = f"Menu=law&Keywords=&SearchKeywordType=Fulltext&MatchType=Exact&RangeType=Piece&Library=aom&ClassFlag=aom&GroupLibraries=&QueryOnClick=False&AfterSearch=True&PreviousLib=aom&pdfStr=&pdfTitle=&IsSynonymSearch=false&RequestFrom=&LastLibForChangeColumn=aom&IsAdv=True&ClassCodeKey=&Aggs.Category=&Aggs.IssueDate=&GroupByIndex=0&OrderByIndex=0&ShowType=Default&GroupValue=&AdvSearchDic.Title=&AdvSearchDic.CheckFullText=&AdvSearchDic.Category=&AdvSearchDic.LawCategory=&AdvSearchDic.IssueDate=%7B+'Start'%3A+'{start_time}'%2C+'End'%3A+'{end_time}'+%7D&AdvSearchDic.Relevance=&TitleKeywords=&FullTextKeywords=&Pager.PageIndex=0&RecordShowType=List&Pager.PageIndex=0&Pager.PageSize=100&QueryBase64Request=&VerifyCodeResult=&isEng=chinese&OldPageIndex=&newPageIndex=&IsShowListSummary=&X-Requested-With=XMLHttpRequest"
    while True:
        try:
            response1 = requests.post(
                start_url+'/law/search/RecordSearch',
                cookies=cookies,
                headers=headers,
                data=data,
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
        print(f"{start_time}---{end_time}:一共{page}条")
    url_list = res1.xpath("//div[@class='list-title']//h4/a[1]/@href").getall()
    if url_list:
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
                        title = ''.join(res2.xpath("//div[@class='content']//*[@class='title']/text()").getall())
                        if title:
                            break
                        else:
                            infos = ''.join(res2.xpath("//div[@style='height: 180px; line-height: 51px; text-align: center; padding-top: 60px;']//text()").getall())
                            print(infos)
                            print('没有取到详情页标题')
                    else:
                        print(f"错误码：{response2.status_code}")
                except Exception as e:
                    print(f"程序报错2：{e}")

            is_shengyuweidu = res2.xpath("//*[@id='continueTips']")
            if is_shengyuweidu:
                return print('cookie过期')

            dode = ''.join(res2.xpath("//div[@class='info']//a//text()").getall()).strip()
            title = ''.join(res2.xpath("//div[@class='content']//*[@class='title']//text()").getall()).replace('English','').replace('尚未施行','').replace('\n','').strip()
            url = a
            content = ''.join(res2.xpath("//div[@class='content']//*[@class='fulltext']").getall()).strip()
            filed = refiled(response2)
            textContent = ''.join(res2.xpath("//div[@class='content']//*[@class='fulltext']//text()").getall()).strip()
            ctime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            fenlei_code = ' '.join(res2.xpath("//strong[contains(text(),'法规分类：')]/following-sibling::a/@href").getall()).strip()
            if fenlei_code:
                fenlei_code = ', '.join(re.findall('Category=(.*?)&way', fenlei_code))
            fenlei_name = ', '.join(res2.xpath("//strong[contains(text(),'法规分类：')]/following-sibling::a//text()").getall()).strip()
            insert = "INSERT IGNORE INTO law_aomen_test (code,title,url,content,filed,textContent,ctime,fenlei_code,fenlei_name)  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            exe = (dode, title, url, content, filed, textContent, ctime, fenlei_code, fenlei_name)
            cursor.execute(insert, exe)
            conn.commit()
            if cursor.rowcount:
                num += 1
                print(f'插入成功{num}条----title: {title}')
            else:
                print(f'数据重复----title: {title}')
    else:
        infos = ''.join(res1.xpath("//div[@class='search-no-content']//div[@class='col-wrap']//p//text()").getall()).strip()
        infos = infos.split('\n')[0]
        print(infos)

def taiwan(start_time,end_time,cookies,headers,start_url):
    conn = pymysql.connect(host='rm-uf6x8ay71wjp5qm8mxo.mysql.rds.aliyuncs.com', user='root', password='Alex1985!@#',
                           db='law_bdfb', charset='utf8mb4')
    cursor = conn.cursor()
    num = 0
    # data = f"Menu=law&Keywords=&SearchKeywordType=Fulltext&MatchType=Exact&RangeType=Piece&Library=twd&ClassFlag=twd&GroupLibraries=&QueryOnClick=False&AfterSearch=True&PreviousLib=twd&pdfStr=&pdfTitle=&IsSynonymSearch=false&RequestFrom=&LastLibForChangeColumn=twd&IsAdv=True&ClassCodeKey=&Aggs.Category=&Aggs.RegulationOrder=&Aggs.ValidState=&Aggs.ReleaseDate=&Aggs.ReviseDate=&Aggs.AbolitionDate=&GroupByIndex=0&OrderByIndex=0&ShowType=Default&GroupValue=&AdvSearchDic.Title=&AdvSearchDic.CheckFullText=&AdvSearchDic.ValidState=&AdvSearchDic.ReleaseDate=%7B+'Start'%3A+'{start_time}'%2C+'End'%3A+'{end_time}'+%7D&AdvSearchDic.ReviseDate=%7B+'Start'%3A+''%2C+'End'%3A+''+%7D&AdvSearchDic.AbolitionDate=%7B+'Start'%3A+''%2C+'End'%3A+''+%7D&AdvSearchDic.Category=&AdvSearchDic.RegulationOrder=&AdvSearchDic.DocumentNO=&AdvSearchDic.Department=&TitleKeywords=&FullTextKeywords=&Pager.PageIndex=0&RecordShowType=List&Pager.PageIndex=0&Pager.PageSize=100&QueryBase64Request=&VerifyCodeResult=&isEng=chinese&OldPageIndex=&newPageIndex=&IsShowListSummary=&X-Requested-With=XMLHttpRequest"
    data = f"Menu=law&Keywords=&SearchKeywordType=Fulltext&MatchType=Exact&RangeType=Piece&Library=twd&ClassFlag=twd&GroupLibraries=&QueryOnClick=False&AfterSearch=True&PreviousLib=twd&pdfStr=&pdfTitle=&IsSynonymSearch=false&RequestFrom=&LastLibForChangeColumn=twd&IsAdv=True&ClassCodeKey=&Aggs.Category=&Aggs.RegulationOrder=&Aggs.ValidState=&Aggs.ReleaseDate=&Aggs.ReviseDate=&Aggs.AbolitionDate=&GroupByIndex=0&OrderByIndex=0&ShowType=Default&GroupValue=&AdvSearchDic.Title=&AdvSearchDic.CheckFullText=&AdvSearchDic.ValidState=&AdvSearchDic.ReleaseDate=%7B+'Start'%3A+'{start_time}'%2C+'End'%3A+'{end_time}'+%7D&AdvSearchDic.ReviseDate=%7B+'Start'%3A+''%2C+'End'%3A+''+%7D&AdvSearchDic.AbolitionDate=%7B+'Start'%3A+''%2C+'End'%3A+''+%7D&AdvSearchDic.Category=&AdvSearchDic.RegulationOrder=&AdvSearchDic.DocumentNO=&AdvSearchDic.Department=&TitleKeywords=&FullTextKeywords=&Pager.PageIndex=1&RecordShowType=List&Pager.PageIndex=1&Pager.PageSize=100&QueryBase64Request=&VerifyCodeResult=&isEng=chinese&OldPageIndex=0&newPageIndex=&IsShowListSummary=&X-Requested-With=XMLHttpRequest"

    while True:
        try:
            response1 = requests.post(
                start_url+'/law/search/RecordSearch',
                cookies=cookies,
                headers=headers,
                data=data,
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
        print(f"{start_time}---{end_time}:一共{page}条")
    url_list = res1.xpath("//div[@class='list-title']//h4/a[1]/@href").getall()
    if url_list:
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
                        title = ''.join(res2.xpath("//div[@class='content']//*[@class='title']/text()").getall())
                        if title:
                            break
                        else:
                            infos = ''.join(res2.xpath("//div[@style='height: 180px; line-height: 51px; text-align: center; padding-top: 60px;']//text()").getall())
                            print(infos)
                            print('没有取到详情页标题')
                    else:
                        print(f"错误码：{response2.status_code}")
                except Exception as e:
                    print(f"程序报错2：{e}")

            is_shengyuweidu = res2.xpath("//*[@id='continueTips']")
            if is_shengyuweidu:
                return print('cookie过期')

            dode = ''.join(res2.xpath("//div[@class='info']//a//text()").getall()).strip()
            title = ''.join(res2.xpath("//div[@class='content']//*[@class='title']//text()").getall()).replace('English','').replace('尚未施行','').replace('\n','').strip()
            url = a
            content = ''.join(res2.xpath("//div[@class='content']//*[@class='fulltext']").getall()).strip()
            filed = refiled(response2)
            textContent = ''.join(res2.xpath("//div[@class='content']//*[@class='fulltext']//text()").getall()).strip()
            ctime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            leibie_code = ' '.join(res2.xpath("//strong[contains(text(),'法规类别：')]/following-sibling::a/@href").getall()).strip()
            if leibie_code:
                leibie_code = ', '.join(re.findall('Category=(.*?)&way', leibie_code))
            leibie_name = ', '.join(res2.xpath("//strong[contains(text(),'法规类别：')]/following-sibling::a//text()").getall()).strip()
            insert = "INSERT IGNORE INTO law_taiwan_test (code,title,url,content,filed,textContent,ctime,leibie_code,leibie_name)  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            exe = (dode, title, url, content, filed, textContent, ctime, leibie_code, leibie_name)
            cursor.execute(insert, exe)
            conn.commit()
            if cursor.rowcount:
                num += 1
                print(f'插入成功{num}条----title: {title}')
            else:
                print(f'数据重复----title: {title}')
    else:
        infos = ''.join(res1.xpath("//div[@class='search-no-content']//div[@class='col-wrap']//p//text()").getall()).strip()
        infos = infos.split('\n')[0]
        print(infos)


def run(start_time,end_time,cookies,headers,start_url):
    print('开始爬取中央法律')
    zhongyang(start_time, end_time, cookies, headers,start_url)
    print('开始爬取地方法律')
    difang(start_time, end_time, cookies, headers,start_url)
    print('开始爬取中外条约')
    zhongwaitiaoyue(start_time, end_time, cookies, headers,start_url)
    print('开始爬取外国法律')
    waiguofagui(start_time, end_time, cookies, headers,start_url)
    print('开始爬取香港法律')
    xianggang(start_time, end_time, cookies, headers,start_url)
    print('开始爬取澳门法律')
    aomen(start_time, end_time, cookies, headers,start_url)
    print('开始爬取台湾法律')
    taiwan(start_time, end_time, cookies, headers,start_url)


if __name__ == '__main__':
    start_time ='2024.02.26'
    end_time ='2024.02.27'
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
        # 'Cookie': 'SUB=dc7f4f02-f042-4ae3-bd45-8506f586ec54; preferred_username=%E4%BA%91%E5%8D%97%E5%A4%A7%E5%AD%A6; pkulaw_v6_sessionid=mihzgowg1onviv0sbg2zzoxh; CookieId=6c8508f84f3bdcf0f5e1af33ef48f232; __tst_status=2102180200#; xCloseNew=22; ddhgguuy_session=o3oat9fqnhobclemt8d61srbr2; authormes=ae65702f4acccc5f9d20e09da15d5727878f74cdbbed0b237d27c11eccaa136452380d61f9f8c5f4bdfb; referer=http://www.pkulaw.yn.yyttgd.top/',
        'Origin': 'http://www.pkulaw.yn.yyttgd.top',
        'Referer': 'http://www.pkulaw.yn.yyttgd.top/penalty/adv',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    start_url = 'http://www.pkulaw.yn.yyttgd.top'

    run(start_time, end_time, cookies, headers,start_url)