# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ThreatcollectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    html = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    publisher = scrapy.Field()
    spider_time = scrapy.Field()
    publish_time = scrapy.Field()
    publisher_href = scrapy.Field()
    publisher_id = scrapy.Field()
    url = scrapy.Field()
    article_id = scrapy.Field()
    img_urls = scrapy.Field()
    image_paths = scrapy.Field()