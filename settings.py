# -*- coding: utf-8 -*-
import random


BOT_NAME = 'zhihuuser'

SPIDER_MODULES = ['zhihuuser.spiders']
NEWSPIDER_MODULE = 'zhihuuser.spiders'


DOWNLOAD_DELAY = random.uniform(2.0,10.0)


# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
  'authorization':'Bearer Mi4wQUNBQ3RjLTlGZ3NBWUlJOWFPZktDeGNBQUFCaEFsVk5leXBKV1FDZk1HTDV3STBSb3FwdV81ZU5hWDUtd3ZlR0Z3|1495375601|62bece6d7a2e6c26e09944e82bc5a0c267e7e8fd'
}

ITEM_PIPELINES = {
   'zhihuuser.pipelines.MongoPipeline': 300,
}
MONGO_URI = {
  'MONGO_HOST' : "127.0.0.1",
  'MONGO_PORT' : 27017,
}
  # 'MONGO_HOST' = "127.0.0.1" , #主机ip
  #  'MONGO_PORT' = 27017, # 端口号
  # 'MONGO_DB' = "Spider",  # 库名
  # 'MONGO_COLL' = "heartsong", # collection名
  # MONGO_USER = "zhangsan"
  # MONGO_PSW = "123456"
MONGO_DATABASE = {
  'MONGO_DB' : "zhihuSpider",
}

