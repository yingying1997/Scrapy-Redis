# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class DmbjItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 一级标题
    first_title = scrapy.Field()
    # 二级标题
    second_title = scrapy.Field()
    # 内容
    content = scrapy.Field()
    pass
