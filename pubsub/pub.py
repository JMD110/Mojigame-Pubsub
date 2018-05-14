# -*- coding:utf8 -*-

from mypubsub import RedisBase

obj = RedisBase()
msg = '我们是快乐的好朋友,我们天天快乐歌唱 -.-'
obj.publish_msg(msg)
