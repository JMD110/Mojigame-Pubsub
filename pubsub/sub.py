# -*- coding:utf8 -*-

from mypubsub import RedisBase


obj = RedisBase()

redis_sub = obj.subscribe_msg()

while True:
	msg = redis_sub.parse_response()
	print('msg: %s' % msg)