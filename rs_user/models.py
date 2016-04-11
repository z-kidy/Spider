# -*- coding: utf-8 -*-
from peewee import *

db = MySQLDatabase('RS', user='kidy', password='xxxxx', charset='utf8')

class Person(Model):
    id            = IntegerField(primary_key=True)
    name          = CharField()
    gender        = CharField(default=u'未知')
    register_time = DateTimeField()         # 注册时间
    online_time   = IntegerField()      # 在线时长
    credits       = IntegerField()      # 积分
    gold          = IntegerField()      # 金币
    upload        = BigIntegerField()   # 上传量
    download      = BigIntegerField()   # 下载量
    seed          = IntegerField()      # 发种数
    rp            = IntegerField()      # 人品

    class Meta:
        database = db
