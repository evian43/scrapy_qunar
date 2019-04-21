# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QunaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class CityItem(scrapy.Item):
    city_id=scrapy.Field()  #城市id
    city_name=scrapy.Field()  #城市名称
    province=scrapy.Field()  #所属省份
    area=scrapy.Field()  #所属地区
    url=scrapy.Field() #链接

class SceneItem(scrapy.Item):
    scene_id=scrapy.Field() #景点id
    scene_name=scrapy.Field() #景点名称
    #scene_city=scrapy.Field()#景点所属城市
    scene_cityrank=scrapy.Field()#景点所属城市排名
    scene_infor=scrapy.Field()#景点简介
    scene_suggest=scrapy.Field()#景点建议游玩时间
    scene_score=scrapy.Field()#景点评分
    scene_address=scrapy.Field() #景点地址
    scene_phone=scrapy.Field() #景点电话
    scene_time=scrapy.Field()#开放时间
    scene_ticket=scrapy.Field()#门票
    scene_season=scrapy.Field()#旅游时节
    scene_transport=scrapy.Field()#交通指南
    scene_comment_sum=scrapy.Field()#点评数量
    scene_5=scrapy.Field()#5分点评数量
    scene_4=scrapy.Field()#4分点评数量
    scene_3=scrapy.Field() #3分点评数量
    scene_2=scrapy.Field() #2分点评数量
    scene_1=scrapy.Field()#1分点评数量
    scene_good=scrapy.Field()#好评数量
    scene_mid=scrapy.Field() #中评数量
    scene_bad=scrapy.Field() #差评数量

class HotelItem(scrapy.Item):
    hotel_id=scrapy.Field()#酒店id
    hotel_name=scrapy.Field()#酒店名称
    hotel_distance=scrapy.Field() #酒店距景点距离
    hotel_score=scrapy.Field() #酒店评分

class RestaurantItem(scrapy.Item):
    restaurant_id=scrapy.Field()#餐厅id
    restaurant_name=scrapy.Field()#餐厅名称
    restaurant_distance=scrapy.Field()#餐厅距景点距离
    restaurant_score=scrapy.Field()#餐厅评分

class NearbyItem(scrapy.Item):
    nearby_id=scrapy.Field()#附近景点id
    nearby_name=scrapy.Field()#景点名称
    nearby_distance=scrapy.Field()#距离
    nearby_score=scrapy.Field()#评分

class ShopItem(scrapy.Item):
    shop_id=scrapy.Field()#购物商场id
    shop_name=scrapy.Field()#购物商场名称
    shop_distance=scrapy.Field()#距离
    shop_score=scrapy.Field()#评分


