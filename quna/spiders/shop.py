import scrapy
import re
from items import ShopItem
from bs4 import BeautifulSoup
import urllib.request
from scrapy.http import Request

class HotelSpider(scrapy.Spider):
    name = 'shop'
    allowed_domains = ['travel.qunar.com']
    start_urls = ['http://travel.qunar.com/place/?from=header']

    def start_requests(self):

        url = 'http://travel.qunar.com/place/?from=header'
        response = urllib.request.urlopen(url)
        # html=urllib.request.urlopen(url).read().decode('utf-8')
        html = response.read().decode('utf-8')
        soup = BeautifulSoup(html, "html5lib")
        div_list = soup.find('div', class_='contbox current')
        #获取城市的链接
        for li in div_list.find_all('li'):
            href = li.find('a').get('href')
            #item['scene_city']=li.find('a').get_text()
            href=href+'-jingdian'
            print(href)
            response = urllib.request.urlopen(href)
            # html=urllib.request.urlopen(url).read().decode('utf-8')
            html = response.read().decode('utf-8')
            soup = BeautifulSoup(html, "html5lib")
            div_list = soup.find('div', class_='listbox')
            #获取每个城市景点链接
            for li in div_list.find_all('li'):
                href=li.find('a').get('href')
                response = urllib.request.urlopen(href)
                # html=urllib.request.urlopen(url).read().decode('utf-8')
                html = response.read().decode('utf-8')
                soup = BeautifulSoup(html, "html5lib")
                div = soup.find('div', class_='contbox box_padd')
                # 获取更多周边购物链接
                for ll in div.find_all('li'):
                    if ll.get('data-type') == '3':
                        self.url=ll.find('a').get('href')
                        print(self.url)
                        yield Request(self.url, self.parse)

    def parse(self, response):
        item=ShopItem()
        html=response.text
        soup=BeautifulSoup(html,'html5lib')
        div_list = soup.find('div', class_='listbox')
        for li in div_list.find_all('li'):
            if li.find('a') is not None:
                name=li.find('a').get_text()
                print(name)
            # name=li.find('span',class_='cn_tit').get_text()
            # print(name)
            #if li.find('a') is not None:
                href = li.find('a').get('href')
                id = re.findall("\d+", href)
                print(id)
            if li.find('span',class_='cur_score') is not None:
                score = li.find('span', class_='cur_score').get_text()
            if li.find('div',class_='distance') is not None:
                distance = li.find('div', class_='distance').get_text()
            item['shop_id']=id
            item['shop_name']=name
            item['shop_score']=score
            item['shop_distance']=distance
            yield item
        # 判断是否有下一页
        page=soup.find('div',class_='b_paging')
        next=page.find('a',class_='page next')
        if next is not None:
            self.page=next.get('href')
            yield Request(url=self.page,callback=self.parse)