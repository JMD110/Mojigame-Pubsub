# 订阅者 消费者 发布者
# -*- coding:utf-8 -*-

import redis

class RedisBase():

	def __init__(self):

		self.__conn = redis.Redis(host='',password='',port=6379) 
		# host填写你服务器地址,password填写你redis设置的密码
		self.pub = 'test'
		# self.sub = 'test'

	def publish_msg(self, msg):

		self.__conn.publish(self.pub, msg)


	def subscribe_msg(self):

		pub = self.__conn.pubsub()
		pub.subscribe(self.pub)
		pub.parse_response()
		return pub
