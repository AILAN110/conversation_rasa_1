#!/usr/bin/env python
# _*_coding:utf-8 _*_
__author__ = 'lan'
import requests
from lxml import etree
import json
import os

CITY_JSON_PATH = "city_info.json"
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
}


def get_city_url():
    city_dict = {}
    url = "https://you.ctrip.com/sitemap/spotdis/c0"
    res = requests.get(url, headers=header).text
    html = etree.HTML(res)
    urls = html.xpath("//div[@class='sitemap_toptag cf']/ul/li/a")
    for i in urls:
        city_url = "https:{}".format(i.attrib['href'])
        city = i.text.strip()
        city_dict[city] = city_url
    with open(CITY_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(city_dict, f, ensure_ascii=False)
    return city_dict


def get_travel_list(url):
    res = requests.get(url, headers=header).text
    html = etree.HTML(res)
    travel_name=html.xpath("//div[@class='card_list in_card']/ul/li/dl/dt/span/text()")
    return list(travel_name)


def get_travel_info(city):
    # print(city)
    if os.path.exists(CITY_JSON_PATH):
        with open(CITY_JSON_PATH, "r", encoding="utf-8") as f:
            city_dict = json.load(f)
    else:
        city_dict = get_city_url()
    # print(city_dict)
    if city not in city_dict:
        return None

    city_url = city_dict[city]
    return get_travel_list(city_url)


# if __name__ == '__main__':
#     a=get_travel_info("云南")
#     print(a)