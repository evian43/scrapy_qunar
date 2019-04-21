# -*- coding: utf-8 -*-
import scrapy
import re
from items import CityItem
from bs4 import BeautifulSoup

class CitySpider(scrapy.Spider):
    name = 'city'
    allowed_domains = ['travel.qunar.com']
    start_urls = ['http://travel.qunar.com/place/?from=header']

    def parse(self, response):
        #爬取页面的html代码
        html=response.text
        soup=BeautifulSoup(html,"html5lib")
        item=CityItem()
        #包裹所有数据的div
        div_list = soup.find('div', class_='contbox current')
        for dl_listbox in div_list.find_all('dl'):
            area = dl_listbox.find('dt').get_text() #获取区域
            for dd_ct in dl_listbox.find('dd'):
                if dd_ct.find('span') is None:
                    for li_item in dd_ct.find_all('li'):
                        href = li_item.find('a').get('href')
                        city_id = re.findall("\d+", href)[0]
                        province = li_item.find('a').get_text()
                        city_name = province
                        item['city_id']=city_id
                        item['city_name']=city_name
                        item['province']=province
                        item['area']=area
                        item['url']=href
                        #print(item)
                        yield item
                elif dd_ct.find('span') != -1:
                    dd_ct.find('span').get_text()
                    prov = dd_ct.find('span').get_text()
                    prov = ''.join(prov.split())
                    prov = prov[0:-1]
                    for li_item in dd_ct.find_all('li'):
                        if li_item is not None:
                            href = li_item.find('a').get('href')
                            city_id = re.findall("\d+", href)[0]
                            city_name = li_item.find('a').get_text()
                            item['city_id'] = city_id
                            item['city_name'] = city_name
                            item['province'] = prov
                            item['area'] = area
                            #print(item)
                            yield item

