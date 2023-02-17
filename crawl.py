import requests

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Referer': 'https://danjuanfunds.com/funding/161725/performance?fdType=5&tabKey=1',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}


# 验证是不是一个正常的请求
def verify_data(res):
    if res.status_code == 200:
        return True
    else:
        return False


def crawls(key, size):
    params = {
        'page': '1',
        'size': size,
    }
    param = {
        'key': key,
        'xq_access_token': 'undefined',
        'source': 'index',
    }
    # 爬取历年数据的链接
    resp = requests.get('https://danjuanfunds.com/djapi/v2/search', params=param, headers=headers)
    # 爬取基金名称的链接
    response = requests.get(f'https://danjuanfunds.com/djapi/fund/nav/history/{key}', params=params, headers=headers)
    time = []
    per = []
    title = None
    if verify_data(response) and verify_data(resp):
        datas = response.json()['data']['items']
        title = resp.json()['data']['items'][0]['sname']
        for data in datas:
            time.append(data['date'])
            per.append(data['value'])
    time.reverse()
    per.reverse()
    return {'time': time, 'price': per, 'title': title}


# 获取热门基金的数据
def rank(id):
    params = {
        'type': id,
        'order_by': '2y',
        'size': '10',
        'page': '1',
    }
    response = requests.get('https://danjuanfunds.com/djapi/v3/filter/fund', params=params, headers=headers).json()
    datas = response['data']['items']
    info = []
    for data in datas:
        Info = {
            'value': data['yield'],
            'name': data['fd_code'] + ':' + data['fd_name']
        }
        info.append(Info)
    return info


# 获取基金的行业占比
def get_per(key):
    paramsk = {
        'fund_code': key,
        'report_date': '2022-12-31',
    }
    response = requests.get('https://danjuanfunds.com/djapi/fundx/base/fund/record/asset/percent', params=paramsk,
                            headers=headers)
    data = response.json()['data']
    chart_list = data['chart_list']
    stock_list = data['stock_list']
    bond_list = data['bond_list']
    list1 = []
    list2 = []
    for chart in chart_list:
        info = {
            'value': chart['percent'],
            'name': chart['type_desc']
        }
        list1.append(info)
    if stock_list:
        for stock in stock_list:
            infos = {
                'value': stock['percent'],
                'name': stock['name']
            }
            list2.append(infos)
    if bond_list:
        for bond in bond_list:
            info1 = {
                'value': bond['percent'],
                'name': bond['name']
            }
            list2.append(info1)
    data = {
        'data1': list1,
        'data2': list2
    }
    return data




