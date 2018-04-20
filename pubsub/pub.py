# -*- coding:utf8 -*-

from mypubsub import RedisBase

obj = RedisBase()
msg = 'hello world'
obj.publish_msg(msg)
