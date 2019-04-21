# -*- coding: utf-8 -*-

import scrapy
import re
from items import SceneItem
from bs4 import BeautifulSoup
import urllib.request
from scrapy.http import Request

class SceneSpider(scrapy.Spider):
    name = 'scene'
    allowed_domains = ['travel.qunar.com']
    start_urls = ['http://travel.qunar.com/place/?from=header']

    def __init__(self):
        #设置爬虫时的头部请求信息
        self.headers = {
            'content-type: application/json;charset=UTF-8',
            #'Accept-Encoding': 'gzip, deflate',
            'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
        }


    def start_requests(self):

        url = 'http://travel.qunar.com/place/?from=header'
        response = urllib.request.urlopen(url)
        # html=urllib.request.urlopen(url).read().decode('utf-8')
        html = response.read().decode('utf-8')
        soup = BeautifulSoup(html, "html5lib")
        div_list = soup.find('div', class_='contbox current')
        for li in div_list.find_all('li'):
            href = li.find('a').get('href')
            #item['scene_city']=li.find('a').get_text()
            self.url=href+'-jingdian'
            yield Request(self.url, self.parse)


    # def __init__(self):
    #     with open('city.json','r+',encoding='utf-8') as f:
    #         self.source_data=json.loads(''.join(f.readlines()))


    def parse(self, response):
        html=response.text
        soup=BeautifulSoup(html,'html5lib')
        if soup.find('div',class_='listbox') is not None:
            #for div_listbox in soup.find('div', class_='listbox'):
            div_listbox=soup.find('div',class_='listbox')
            if div_listbox.find('li') is not None:
                for li in div_listbox.find_all('li'):
                    href = li.find('a').get('href')
            #             #景点翻页
            # for div_page in soup.find('div',class_='b_paging'):
            #             page=li.find_all('a',class_='page').get_text()
            #             for i in page:
            #                 href=href+'-1-'+i
                            #scene = li.find('span', class_='cn_tit').get_text()
                            #scene_name= re.sub("[A-Za-z0-9\']", "", scene)
                            #item['scene_name']=scene_name
                    #进入详情页
                    print(href)
                    yield scrapy.Request(url=href,callback=self.Scene_Info)
        #判断是否有下一页
        page=soup.find('div',class_='b_paging')
        next=page.find('a',class_='page next')
        if next is not None:
            self.page=next.get('href')
            yield Request(url=self.page,callback=self.parse)

    def Scene_Info(self,response):
        #获取景点基本信息
        item = SceneItem()
        html=response.text
        soup=BeautifulSoup(html,'html5lib')
        #爬取景点id和景点名称
        div_title=soup.find('div',class_='b_title clrfix')
        if div_title is not None:
            scene=div_title.find('h1', class_='tit').get_text()
            scene_name= re.sub("[A-Za-z0-9\']", "", scene)
            item['scene_name']=scene_name
            if div_title.find('a').get('data-id') is not None:
                scene_id=div_title.find('a').get('data-id')
            else:
                href=div_title.find('a').get('href')
                scene_id=re.findall("\d+", href)[0]
            item['scene_id']=scene_id
            print(scene_name)
            print(scene_id)

        #爬取景点所属城市排名
        div_rank=soup.find('div',class_='ranking')
        if div_rank is not None:
            scene_rank=div_rank.get_text().split('\n')[0]
            item['scene_cityrank']=scene_rank
            print(scene_rank)
        else:
            item['scene_cityrank']=None

        #爬取建议游玩时间
        div_time=soup.find('div',class_='time')
        if div_time is not None:
            suggest=div_time.get_text()
            item['scene_suggest']=suggest
            print(suggest)
        else:
            item['scene_suggest']=None

        #爬取景点评分
        div_score=soup.find('span',class_='cur_score')
        if div_score is not None:
            score=div_score.get_text()
            item['scene_score']=score
            print(score)
        else:
            item["scene_score"]=None

        #爬取景点简介
        div_content = soup.find('div', class_='e_db_content_box')
        if div_content is not None:
            if div_content.find('p') is not None:
                content=div_content.find('p').get_text()
                item['scene_infor']=content
                print(content)
            else:
                item['scene_infor']=None
        else:
            item['scene_infor']=None

        #爬取景点地址
        td = soup.find('td', class_='td_l')
        link = {}
        if td is not None:
            for dl in td.find_all('dl'):
                if dl.find('dt') is not None:
                    key = dl.find('dt').get_text()
                    print(key)
                if dl.find('dd') is not None:
                    content = dl.find('dd').get_text()
                    print(content)
                link[key] = content
        else :
            item['scene_address'] = None
            item['scene_phone'] = None
        if link:
            if '地址:'in link:
                item['scene_address']=link['地址:']
            else:
                item['scene_address']=None
            if '电话:' in link:
                item['scene_phone']=link['电话:']
            else:
                item['scene_phone']=None
        else:
            item['scene_address']=None
            item['scene_phone']=None

        #爬取景点开放时间
        dl = soup.find('dl', class_='m_desc_right_col')
        if dl is not None:
            if dl.find('dd') is not None:
                open_time=dl.find('dd').get_text()
                print(open_time)
                item['scene_time']=open_time
            else:
                item['scene_time']=None
        else:
            item['scene_time']=None

        #爬取景点门票
        div_price = soup.find('div', class_="b_detail_section b_detail_ticket")
        if div_price is not None:
            if div_price.find('p') is not None:
                price=div_price.find('p').get_text()
                print(price)
                item['scene_ticket']=price
            else:
                item['scene_ticket']=None
        else:
            item['scene_ticket']=None

        #爬取旅游时节
        div_season = soup.find('div', class_='b_detail_section b_detail_travelseason')
        if div_season is not None:
            season=div_season.find('p')
            if season is not None:
                season=season.get_text()
                print(season)
                item['scene_season']=season
            else:
                item['scene_season']=None
        else:
            item['scene_season']=None

        #爬取交通指南
        div_trans = soup.find('div', class_='b_detail_section b_detail_traffic')
        if div_trans is not None:
            div = div_trans.find('div', class_='e_db_content_box e_db_content_dont_indent')
            if div is not None:
                trans=div.get_text()
                print(trans)
                item['scene_transport']=trans
            else:
                item['scene_transport']=None
        else:
            item['scene_transport']=None

        #爬取评论数量
        div_comment = soup.find('div', class_='b_detail_section b_detail_comment')
        if div_comment is not None:
            num = div_comment.find('span').get_text()
            num = re.sub('[\(\)]', '', num)
            item['scene_comment_sum']=num
            div_star=div_comment.find('div',class_='star-top')
            if div_star is not None:
                number={}
                for li in div_star.find_all('li'):
                    score=li.find('em').get_text()
                    width=li.find('div',class_='rate').get('style')
                    percent=re.sub('[a-zA-z\:\%]','',width)
                    #print(percent)
                    n=(int(percent)+6)*10**(-2)
                    total=int(n*int(num))
                    number[score]=total
                item['scene_5']=number['5分']
                item['scene_4']=number['4分']
                item['scene_3']=number['3分']
                item['scene_2']=number['2分']
                item['scene_1']=number['1分']
                item['scene_good']=number['5分']+number['4分']
                item['scene_mid']=number['3分']
                item['scene_bad']=number['2分']+number['1分']

        yield item

