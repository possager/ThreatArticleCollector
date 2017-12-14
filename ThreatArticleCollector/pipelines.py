# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ThreatarticlecollectorPipeline(object):
    def process_item(self, item, spider):
        return item
        print(dict(item))

class setDefaultValue(object):
    def process_item(self,item,spider):
        for field in item.fields:
            item.setdefault(field,None)
        return item
