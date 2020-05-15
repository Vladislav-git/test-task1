from bs4 import BeautifulSoup
import json
import requests


URL = 'https://www.mebelshara.ru/contacts'
HEADERS = {'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Mobile Safari/537.36','accept':'*/*'}

def get_html(url, params=None):
    res = requests.get(url, headers=HEADERS, params=params)
    return(res)


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='city-item')
    phone = soup.find('span',class_='phone-num zphone').get_text()
    result = []
    lst = []
    for item in items:
        cities = item.find_all('div', class_='shop-list-item')
        for shop in cities:
            result.append({
                'adress': item.find('h4',class_='js-city-name').get_text() + ', ' + shop.find('div',class_='shop-address').get_text(),
                'latlon': [shop.attrs['data-shop-latitude'],shop.attrs['data-shop-longitude']],
                'name': shop.find('div',class_='shop-name').get_text(),
                'phone': phone,
                'working_hours': [shop.attrs['data-shop-mode2'],shop.attrs['data-shop-mode1']],
            })
    # print(result)
    return(result)


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        to_json = get_content(html.text)
        print(to_json)
        with open('sw_templates.json', 'w',  encoding='utf-8') as f:
            json.dump(to_json, f, ensure_ascii=False)
    else:
        print('error')


parse()
