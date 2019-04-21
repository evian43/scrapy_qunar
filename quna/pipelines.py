# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
from twisted.enterprise import adbapi
import MySQLdb
from scrapy import log
import copy
import json

class QunaPipeline(object):
    def process_item(self, item, spider):
        return item

# class PipelineToJson(object):
#     def __init__(self):
#         #self.f=open('city.json','w',encoding='utf-8')
#         self.f=open('scene.json','w',encoding='utf-8')
#         #self.f=open('hotel.json','w',encoding='utf-8')
#         #self.f=open('restaurant.json','w',encoding='utf-8')
#         #self.f=open('nearby.json','w',encoding='utf-8')
#         #self.f = open('shop.json', 'w', encoding='utf-8')
#
#     def process_item(self,item,spider):
#         content=json.dumps(dict(item),ensure_ascii=False)+'\n'
#         #self.city.write(content)
#         #self.scene.write(content)
#         self.f.write(content)
#         return item
#
#     def close_spider(self,spider):
#         #self.city.close()
#         #self.scene.close()
#         self.f.close()


class PipelineToMysql(object):
    def __init__(self):
        dbparams=dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            use_unicode=True,
        )
        self.post=adbapi.ConnectionPool('MySQLdb',**dbparams)

    def process_item(self,item,spider):
        # cityItem=copy.deepcopy(item)
        # query=self.post.runInteraction(self._conditional_insert,cityItem)
        Item=copy.deepcopy(item)
        query=self.post.runInteraction(self._conditional_insert,Item)
        query.addErrback(self.handle_error)
        return item

    def _conditional_insert(self,tb,item):
        #将数据插入数据库中的city1表
        # sql="insert into city1  (city_id,city_name,province,area) values (%s,%s,%s,%s)"
        # params=(item["city_id"],item["city_name"],item['province'],item['area'])
        #将数据插入数据库中的hotel表
        # sql='insert into hotel (hotel_id,hotel_name,hotel_distance,hotel_score) values (%s,%s,%s,%s)'
        # params=(item["hotel_id"],item["hotel_name"],item["hotel_distance"],item["hotel_score"])
        #将数据插入数据库中的restaurant表
        # sql = 'insert into restaurant (restaurant_id,restaurant_name,restaurant_distance,restaurant_score) values (%s,%s,%s,%s)'
        # params = (item["restaurant_id"], item["restaurant_name"], item["restaurant_distance"], item["restaurant_score"])
        #将数据插入数据库中的nearby表
        # sql = 'insert into nearby (nearby_id,nearby_name,nearby_distance,nearby_score) values (%s,%s,%s,%s)'
        # params = (item["nearby_id"], item["nearby_name"], item["nearby_distance"], item["nearby_score"])
        #将数据插入数据库中的shop表
        # sql = 'insert into shop (shop_id,shop_name,shop_distance,shop_score) values (%s,%s,%s,%s)'
        # params = (item["shop_id"], item["shop_name"], item["shop_distance"], item["shop_score"])
        #将数据库插入数据库中的scene表
        sql = 'insert into scene (scene_id, scene_name, scene_cityrank, scene_infor, scene_suggest,scene_score, scene_address,scene_phone,scene_time,scene_ticket,scene_season,scene_transport,scene_comment_sum,scene_5,scene_4,scene_3,scene_2,scene_1,scene_good,scene_mid,scene_bad) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        params = (item["scene_id"],item["scene_name"],item["scene_cityrank"],item["scene_infor"],item["scene_suggest"],item["scene_score"],item["scene_address"],item["scene_phone"],item["scene_time"],item["scene_ticket"],item["scene_season"],item["scene_transport"],item["scene_comment_sum"],item["scene_5"],item["scene_4"],item["scene_3"],item["scene_2"],item["scene_1"],item["scene_good"],item["scene_mid"],item["scene_bad"])

        tb.execute(sql,params)

    def handle_error(self,e):
        log.err(e)
