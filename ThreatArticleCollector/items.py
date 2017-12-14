# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst




class ThreatcollectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    html = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(output_processor=TakeFirst())
    content = scrapy.Field(output_processor=TakeFirst())
    publisher = scrapy.Field()
    spider_time = scrapy.Field(output_processor=TakeFirst())
    publish_time = scrapy.Field(output_processor=TakeFirst())
    publisher_href = scrapy.Field(output_processor=TakeFirst())
    publisher_id = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    article_id = scrapy.Field(output_processor=TakeFirst())
    img_urls = scrapy.Field()
    image_paths = scrapy.Field(output_processor=TakeFirst())