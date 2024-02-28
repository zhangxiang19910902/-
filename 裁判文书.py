import requests
import execjs



uinfo =[
    {
      "username": "15523218583",
      "password": "mg8r1J}oLGW137,4"
    },
    {
      "username": "18501579941",
      "password": "Va3198fTC,9_9lPu"
    },
    {
      "username": "18550247495",
      "password": "hJP0m&816!15tIOb"
    },
    {
      "username": "13217908561",
      "password": "341{QwCoKy[697aU"
    },
    {
      "username": "18321081846",
      "password": "2y;sZ16e9PZ+9gY0"
    },
    {
      "username": "13170905795",
      "password": "575xZ]l+G82VdK7s"
    },
    {
      "username": "13764379482",
      "password": "1O0/1Yu=y19aZa1H"
    },
    {
      "username": "13764843710",
      "password": "e%em60]B0f0RC8Z0"
    },
    {
      "username": "13239169109",
      "password": "$I8Nq=A20J5q8b2l"
    },
    # {
    #   "username": "13033507627",
    #   "password": "9y652,c$JwXkM44V"
    # },
    {
      "username": "13126044206",
      "password": "l3`Q33fOAt6u9(0M"
    },
    {
      "username": "13086108516",
      "password": "x88E8}N6c,x4n4VU"
    },
    # {
    #   "username": "13138750544",
    #   "password": "72YNmDy1aq:12I5,"
    # },
    {
      "username": "17507901729",
      "password": "hH29wV8667xQ=lY^"
    },
    {
      "username": "18626071637",
      "password": "3D9p8Pz0wUw02G#_"
    },
    {
      "username": "15579018127",
      "password": "0S9wWX7Li4od[4'5"
    },
    {
      "username": "18662678745",
      "password": "606i7*muNX4q^DE5"
    },
    {
      "username": "13057274734",
      "password": "9T!pb07x)84MCp8O"
    },
    {
      "username": "15711781705",
      "password": "/36Gkc62xX22PT#f"
    },
    {
      "username": "18217242409",
      "password": "5t9K4s>G&M0p1rR8"
    }
  ]

cookies = {
    'wzws_sessionid': 'gDM4LjE4MS43Ni4yMTKgZdwvGIE5ZmVhNzCCNmY2OTAx',
    'SESSION': '856ace32-ee39-4819-8e87-6afbe804e4cf',
    # 'wzws_cid': '8773b014db60de4400d563c3b55879ef38c1e2aba1e845ef01d043237e4d89d3eae9c7a88ea0f11843c9e9217fd9a36abfd0addef5fa6794e779686441cec08477826f32271be30b15c9f3f1ed63b19bbb4f45f3bec7a24e31dbc91ec544a5b7',
}

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Cookie': 'wzws_sessionid=gDM4LjE4MS43Ni4yMTKgZdwvGIE5ZmVhNzCCNmY2OTAx; SESSION=b88dccbe-8551-4a14-b6d1-8376f5ba06c6; wzws_cid=b7e2858530fd65b0457c4c968dffc64725db79c23b1fff5cc6f32a5d6217534a3b88ae4a890111520086d628ee3fa8abff8275a7996f99d48a39e74e5772293105b96db791f35efe6fb048333142b566',
    'Origin': 'https://wenshu.court.gov.cn',
    'Referer': 'https://wenshu.court.gov.cn/website/wenshu/181217BMTKHNT2W0/index.html?pageId=9058b53a0d1a038981df60198a827004&s2=%E6%9C%80%E9%AB%98%E4%BA%BA%E6%B0%91%E6%B3%95%E9%99%A2',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

data = {
    'pageId': '9058b53a0d1a038981df60198a827004',
    's2': '最高人民法院',
    'sortFields': 's50:desc',
    'ciphertext': '1110110 1000101 1101000 1100101 1001111 111000 1101001 1111000 111001 1110001 1010011 1000011 1101000 1000110 1010000 1110000 1101101 110001 1000110 1101011 110011 111001 1100001 1010110 110010 110000 110010 110100 110000 110010 110010 110110 1101101 1110111 1110111 1000100 1010101 1111000 1000010 110110 1101001 1000001 1110011 1010001 1001011 1100011 1010110 1011001 1110100 1110010 1101000 1101111 1000001 1000001 111101 111101',
    'pageNum': '1',
    'pageSize': '15',
    'queryCondition': '[{"key":"s33","value":"北京市"},{"key":"cprq","value":"2024-02-20 TO 2024-02-29"}]',
    'cfg': 'com.lawyee.judge.dc.parse.dto.SearchDataDsoDTO@queryDoc',
    '__RequestVerificationToken': 'Lea41xS5SjPXr4YopWj9B6FH',
    'wh': '919',
    'ww': '1920',
    'cs': '0',
}

response = requests.post('https://wenshu.court.gov.cn/website/parse/rest.q4w', cookies=cookies, headers=headers, data=data)
response.encoding = 'utf-8'
res_json = response.json()
result = res_json['result']
secretKey = res_json['secretKey']
with open(r'E:\zx_框架爬虫\js逆向网站\裁判文书网des\des.js', encoding='utf-8') as s:
    sign = s.read()

ctx = execjs.compile(sign).call('DES3', result,secretKey,'')
print(res_json['result'])
print(ctx)