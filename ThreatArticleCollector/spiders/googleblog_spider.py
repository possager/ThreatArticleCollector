#_*_coding:utf-8_*_
import scrapy
from ThreatArticleCollector.items import ThreatcollectItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Compose
from scrapy.loader.processors import MapCompose
from scrapy.loader.processors import Join
from scrapy.loader.processors import TakeFirst
from w3lib.html import remove_tags
import time



class FooglebolgSpider(scrapy.Spider):
    name = 'googleblog'
    start_urls=['https://security.googleblog.com/']

    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3291.0 Safari/537.36',
        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url,callback=self.parse)

    def parse(self, response):
        def deal_img_urls(data):
            print(data)
            return 'has dealed somethings'

        def deal_img_urls2(data2):
            print(data2)
            return data2+' add by deal2'



        for i in response.xpath('//*[@id="Blog1"]/div[@class="post"]'):
            itemloderArticle=ItemLoader(item=ThreatcollectItem(),selector=i)
            itemloderArticle.add_xpath('title','.//h2/a/text()')
            itemloderArticle.add_xpath('url','.//h2/a/@href')
            itemloderArticle.add_xpath('publish_time','.//div[@class="post-header"]/div[@class="published"]/span/text()',Join())
            itemloderArticle.add_xpath('publisher','.//div[@class="post-body"]/div[contains(@class,"post-content")]/script/text()',MapCompose(remove_tags))
            itemloderArticle.add_xpath('article_id','.//@data-id')
            itemloderArticle.add_value('img_urls',i.re(r'src="(.*?)"'),deal_img_urls,deal_img_urls2)
            itemloderArticle.add_value('spider_time',time.time()*1000)
            # itemloderArticle.add_value('publisher_id',None)
            # itemloderArticle.add_value()

            # print(itemloderArticle.selector.re(r'src=".*?"'))
            # itemloderArticle.add_xpath('content','')
            # print(i.xpath('.//h2/a/text()').extract_first('nothing').strip())
            item1=itemloderArticle.load_item()
            yield item1
            print(dict(item1))
        print(response.url)
        print(response)
        nexturl=response.xpath('//*[@id="Blog1_blog-pager-older-link"]/@href').extract()
        yield scrapy.Request(url=nexturl[0],headers=response.headers)

        print('it is href   ',nexturl)
        # return item1

