import requests as requests
from bs4 import BeautifulSoup
from pyecharts import Bar

ALL_DATA=[]
def parse_page(url):
    header = {
        'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Mobile Safari/537.36'
    }
    response = requests.get(url,headers=header)
    text = response.content.decode('utf-8')
    # print(text)
    soup = BeautifulSoup(text,'html5lib')
    conMidtab = soup.find('div',class_='conMidtab')
    tables = conMidtab.find_all('table')
    for table in tables:
        trs = table.find_all('tr')[2:]
        for index, tr in enumerate(trs):
            tds = tr.find_all('td')
            city_td = tds[0]
            if index == 0:
                city_td = tds[1]
            #stripped_strings过滤空格空行
            city = list(city_td.stripped_strings)[0]
            # print(city)
            temp_td = tds[-2]
            min_temp = list(temp_td.stripped_strings)[0]
            ALL_DATA.append({"city":city,"min_temp":min_temp})
            # print({"city":city,"min_temp":min_temp})


def main():
    urls= {
        'http://www.weather.com.cn/textFC/hb.shtml',
        'http://www.weather.com.cn/textFC/db.shtml',
        'http://www.weather.com.cn/textFC/hd.shtml',
        'http://www.weather.com.cn/textFC/hz.shtml',
        'http://www.weather.com.cn/textFC/hn.shtml',
        'http://www.weather.com.cn/textFC/xb.shtml',
        'http://www.weather.com.cn/textFC/xn.shtml',
        'http://www.weather.com.cn/textFC/gat.shtml',

    }
    for url in urls:
        parse_page(url)
    ALL_DATA.sort(key=lambda data:data['min_temp'])
    # print(ALL_DATA)
    data = ALL_DATA[0:10]
    cities = list(map(lambda x:x['city'], data))
    temps = list(map(lambda x:x['min_temp'], data))
    charts = Bar("天朝最低温度排行")
    charts.add('', cities, temps)
    charts.render('temperature.html')

if __name__=='__main__':
    main()
