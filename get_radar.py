from crawl import crawls
from inv_days import cal_income
import requests
from lxml import html

# 构建etree对象
etree = html.etree


# 将雷达图所需要的数据按规范封装好
def get_radars(num):
    pre = get_predicate(num)
    info = get_infos(num)
    info['data'].append(pre)
    return info


# 计算基金的预计收益，取这个方法中的最大值返回
def get_predicate(num):
    value = crawls(num, '300')['price']
    data = cal_income(value, 10)['per']
    return '{:.2f}'.format(float(data))


# 获取基金的信息，累计收益、最大回撤等信息
def get_infos(num):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Referer': 'https://danjuanfunds.com/rank-xq/performance',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    response = requests.get(f'https://danjuanfunds.com/funding/{num}', headers=headers)
    tree = etree.HTML(response.text)
    title = tree.xpath('//div[@class="style_title__BXHyp"]//text()')[0]
    ljsy = tree.xpath('//div[@class="style_abstract-item__D1adL"][1]//text()')[1]
    zdhc = tree.xpath('//li[@class="style_detail-list-item__j4rUL"][4]//text()')[1].split('%')[0]
    fxdj = tree.xpath('//div[@class="style_op-list__0vh0N"]/span[1]/text()')[0]
    chenglishijian = tree.xpath('//li[@class="style_detail-list-item__j4rUL"][2]//text()')
    jjgms = tree.xpath('//li[@class="style_detail-list-item__j4rUL"][6]//text()')
    jjgm = float(jjgms[1])
    # 统一单位
    if jjgms[2] == '万':
        jjgm /= 10000
    clsj = int(chenglishijian[1]) * 365 + int(chenglishijian[3])
    all = [float(ljsy), int(clsj), '{:.2f}'.format(float(jjgm)), 100-float(zdhc), grade(fxdj)]
    return {
        'data': all,
        'title': title
    }


# 转化风险等级为数字表达
def grade(text):
    if text == '高风险':
        return 20
    elif text == '中高风险':
        return 40
    elif text == '中风险':
        return 60
    elif text == '中低风险':
        return 80
    elif text == '低风险':
        return 100


