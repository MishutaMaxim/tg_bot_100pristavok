import requests
from bs4 import BeautifulSoup

from config import SITE


def get_results(string):
    params = {'q': str(string)}
    raw_response = requests.get(SITE, params=params).text
    result = parse_response(raw_response)
    return result


def parse_response(html_text) -> list:
    result = []
    soup = BeautifulSoup(html_text, 'lxml')
    table = soup.findAll('tr', class_="item main_item_wrapper")
    for item in table:
        title = item.find('div', class_="title title-b").text.split('[')[0]
        category = item.find('div', class_="title title-b").text.split('[')[1][:-1]
        price = item.findAll('div', class_="cost prices clearfix")
        sell_price = price[0].text.strip()
        trade_price = price[1].text.strip()
        game = {'title': title,
                'category': category,
                'trade_price': sell_price,
                'sell_price': trade_price}
        result.append(game)
    return result
