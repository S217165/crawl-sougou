# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CollectdataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    链接 = scrapy.Field()
    来源 = scrapy.Field()
    移动端标题 = scrapy.Field()
    新闻原网址 = scrapy.Field()
    文章类型 = scrapy.Field()
    标题 = scrapy.Field()
    标签 = scrapy.Field()
    来源_ID = scrapy.Field()
    来源图标 = scrapy.Field()
    个人网站 = scrapy.Field()
    发表时间 = scrapy.Field()
    图片链接 = scrapy.Field()
    来源网址 = scrapy.Field()