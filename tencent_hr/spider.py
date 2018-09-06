import json
import time

from lxml import etree
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Mobile Safari/537.36',
}
BASE_DOMAIN = 'https://hr.tencent.com/'
position = {}
def get_content(url):
    response = requests.get(url, headers=headers)
    text = response.text
    html = etree.HTML(text)
    title = html.xpath("//td[@id='sharetitle']/text()")[0]
    # tds = html.xpath("//tr[@class='c bottomline']/td")
    address = html.xpath("//tr[@class='c bottomline']/td[1]/text()")[0]
    category = html.xpath("//tr[@class='c bottomline']/td[2]/text()")[0]
    nums = html.xpath("//tr[@class='c bottomline']/td[3]/text()")[0]
    more_info = html.xpath("//ul[@class='squareli']")
    duty = more_info[0].xpath(".//text()")
    require = more_info[1].xpath(".//text()")
    position['title'] = title
    position['address'] = address
    position['category'] = category
    position['nums'] = nums
    position['duty'] = duty
    position['require'] = require
    return position


def get_details(url):
    response = requests.get(url, headers=headers)
    text = response.text
    html = etree.HTML(text)
    links = html.xpath("//tr[@class='even' or @class='odd']//a/@href")
    links = map(lambda url: BASE_DOMAIN+url, links)
    return links


def spider():
    base_url = 'https://hr.tencent.com/position.php?keywords=python&lid=0&tid=0&start={}#a'
    contents=[]
    for i in range(0,53):
        i *=10
        url = base_url.format(i)
        details = get_details(url)
        for detail in details:
            content = get_content(detail)
            contents.append(content)
            time.sleep(2)
    # print(contents)
    cont = json.dumps(contents, ensure_ascii=False)
    with open('txhr.json', 'w', encoding='utf-8') as f:
        f.write(cont)

if __name__=='__main__':
    spider()
