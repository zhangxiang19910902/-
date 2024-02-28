import requests

cookies = {
    '__tst_status': '2102180200#',
    'pkulaw_v6_sessionid': 'ru3qwlsljn3syweisx23n3wl',
    'CookieId': '6c8508f84f3bdcf0f5e1af33ef48f232',
    'SUB': 'dc7f4f02-f042-4ae3-bd45-8506f586ec54',
    'preferred_username': '%E4%BA%91%E5%8D%97%E5%A4%A7%E5%AD%A6',
    'ddhgguuy_session': 'clhcfbeh61afgukj5he8n5ee93',
    'authormes': 'ae65702f4acccc5f9d20e09da15d5727878f74cdbbed0b237d27c11eccaa136452380d61f9f8c5f4bdfb',
    'referer': 'http://www.pkulaw.yn.yyttgd.top/',
    'xCloseNew': '27',
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

data = "Menu=penalty&Keywords=&SearchKeywordType=Fulltext&MatchType=Exact&RangeType=Piece&Library=apy&ClassFlag=apy&GroupLibraries=&QueryOnClick=False&AfterSearch=True&PreviousLib=apy&pdfStr=&pdfTitle=&IsSynonymSearch=false&RequestFrom=&LastLibForChangeColumn=apy&IsAdv=True&ClassCodeKey=&Aggs.Category=&Aggs.PunishmentTarget=&Aggs.PunishmentTypeNew=&Aggs.EnforcementLevel=&Aggs.DepartCode=&Aggs.LawRegional=&Aggs.PunishmentDate=&GroupByIndex=1&OrderByIndex=0&ShowType=Default&GroupValue=&AdvSearchDic.Title=&AdvSearchDic.CheckFullText=&AdvSearchDic.DocumentNO=&AdvSearchDic.Category=&AdvSearchDic.PunishmentTypeNew=&AdvSearchDic.PunishmentObject=&AdvSearchDic.EnforcementLevel=&AdvSearchDic.DepartCode=&AdvSearchDic.LawRegional=11%2C%23containAny&AdvSearchDic.PunishmentDate=%7B+'Start'%3A+'2023.01.01'%2C+'End'%3A+'2023.01.03'+%7D&TitleKeywords=&FullTextKeywords=&Pager.PageIndex=0&RecordShowType=List&Pager.PageIndex=0&Pager.PageSize=100&QueryBase64Request=&VerifyCodeResult=&isEng=chinese&OldPageIndex=&newPageIndex=&IsShowListSummary=&X-Requested-With=XMLHttpRequest"

response = requests.post(
    'http://www.pkulaw.yn.yyttgd.top/penalty/search/RecordSearch',
    cookies=cookies,
    headers=headers,
    data=data,
    verify=False,
)

print('aa')