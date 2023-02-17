import csv
import requests
from lxml import html

etree = html.etree

headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # 'Cookie': 'st_si=89725721484458; st_asi=delete; ASP.NET_SessionId=uuyulutgsqa0nic3zjwqmc35; st_pvi=08942264659489; st_sp=2023-02-16%2017%3A30%3A53; st_inirUrl=http%3A%2F%2Ffund.eastmoney.com%2Ffund.html; st_sn=13; st_psi=20230216173358604-112200312944-4911093992',
        'If-Modified-Since': 'Mon, 11 May 2020 11:16:17 GMT',
        'If-None-Match': '"1D6278596E91680"',
        'Referer': 'http://fund.eastmoney.com/Company/html/fundquote.html',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    }


def rebuilt_Language(url, headers):
    response = requests.get(url=url, headers=headers, verify=False)
    response.encoding = response.apparent_encoding
    return response


def get_company_url():
    resp = rebuilt_Language('http://fund.eastmoney.com/company/80369323.html', headers)
    tree = etree.HTML(resp.text)
    div_list = tree.xpath('/html/body/div[1]/div[1]/div[4]/ul')
    name_list = []
    for div in div_list:
        names = div.xpath('./li/div/a/@href')
        for name in names:
            name_list.append('http://fund.eastmoney.com' + name)
    return name_list


def get_detail(name_list):
    detail = []
    for name in name_list:
        print(name)
        resp = rebuilt_Language(name, headers)
        tree = etree.HTML(resp.text)
        name = tree.xpath('/html/body/div[1]/div[1]/div[5]/div[1]/div[1]/div[1]/p[1]/text()')[0]
        try:
            position = tree.xpath('/html/body/div[1]/div[1]/div[5]/div[1]/div[2]/div[1]/p[1]/label/text()')[0]
        except:
            position = '--'
        scale = tree.xpath('/html/body/div[1]/div[1]/div[5]/div[1]/div[3]/ul/li[1]/label/text()')[0]
        count = tree.xpath('/html/body/div[1]/div[1]/div[5]/div[1]/div[3]/ul/li[2]/label/a/text()')[0]
        try:
            url = tree.xpath('/html/body/div[1]/div[1]/div[5]/div[1]/div[2]/div[2]/p[1]/label/text()')[0]
        except:
            url = '--'
        info = {
            'name': name, 'position': position, 'scale': scale, 'count': count, 'url': url
        }
        detail.append(info)
    return detail


if __name__ == '__main__':
    url_list = get_company_url()
    info = get_detail(url_list)
    print(info)
    header = ['name', 'position', 'scale', 'count', 'url']
    fp = open(f'./company.csv', 'w', encoding='utf-8', newline='')
    writer = csv.DictWriter(fp, header)
    writer.writeheader()
    writer.writerows(info)