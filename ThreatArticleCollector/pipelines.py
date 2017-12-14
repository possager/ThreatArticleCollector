# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# -*- coding: utf-8 -*-
import os
import json
import zipfile
import hashlib
import shutil
import scrapy
import time
# from scrapy.http import Request
from scrapy.exceptions import DropItem
from scrapy.contrib.pipeline.images import ImagesPipeline

def str_md5(src):
    m2 = hashlib.md5()
    m2.update(src)
    smd5 = m2.hexdigest()
    return smd5

def is_str(s):
    return isinstance(s, basestring)

def write_orig_html(item, spider, path):
    if item['html']:
        fhtml = open(str_md5(item['url']) + '.html', 'w')
        print str_md5(item['url'])
        if is_str(item['html']):
            # fhtml.write(item['html'].encode('utf-8'))
            fhtml.write(item['html'].encode('utf-8','ignore'))
        fhtml.close()
        f = zipfile.ZipFile(path + '/' + str_md5(item['url']) + '.zip', 'w', zipfile.ZIP_DEFLATED)
        if item['img_urls'] and item['image_paths']:
            for img_each in item['image_paths'][0]:
                try:
                    filename = os.path.basename(img_each)
                    img_orig = "img_tmp/"+img_each
                    print img_orig
                    shutil.move(img_orig,filename)
                    f.write(filename)
                    os.remove(filename)
                except:
                    print "=====",item
                    pass
        f.write(str_md5(item['url']) + '.html')
        f.close()
        os.remove(str_md5(item['url']) + '.html')

def write_date_json(item, spider, path):
    item_b=item
    del(item_b['html'])
    with open(path + '/' + str_md5(item['url']) + '.json', 'w') as fjson:
        json.dump(dict(item_b), fjson)

class ThreatcollectPipeline(object):
    def process_item(self, item, spider):
        orig_path = "output/" + spider.allowed_domains[0] + "/orig_html/" + item['publish_time']
        if not os.path.exists(orig_path):
            os.makedirs(orig_path)
        write_orig_html(item, spider, orig_path)
        date_path = "output/" + spider.allowed_domains[0] + "/data/" + item['publish_time']
        if not os.path.exists(date_path):
            os.makedirs(date_path)
        write_date_json(item, spider, date_path)
        return item

class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if not os.path.exists("img_tmp"):
            os.makedirs("img_tmp")
        if item['img_urls']:
            for image_url in item['img_urls']:
                # yield scrapy.Request(url=image_url,meta={'max_retry_times':2})
                yield scrapy.Request(url=image_url, meta={'dont_retry': True})
                # yield Request(image_url)

    def item_completed(self, results, item, info):
        if item['img_urls']:
            image_paths = [x['path'] for ok, x in results if ok]
            if not image_paths:
                raise DropItem("Item contains no images")
            item['image_paths'].append(image_paths)
            return item
        else:
            return item

    def file_path(self, request, response=None, info=None):
        image_guid = request.url.split('/')[-1]
        return 'full/%s' % (image_guid)






class setDefaultValue(object):
    def process_item(self,item,spider):
        for field in item.fields:
            item.setdefault(field,None)
        return item
