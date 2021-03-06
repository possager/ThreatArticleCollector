#_*_coding:utf-8_*_
import scrapy
from ThreatArticleCollector.items import ThreatcollectItem
# from scrapy.loader import ItemLoader
from ThreatArticleCollector.spiders.itemloader_ll import itemloader_ll as ItemLoader
from scrapy.loader.processors import Compose
from scrapy.loader.processors import MapCompose
from scrapy.loader.processors import Join
from scrapy.loader.processors import TakeFirst
from w3lib.html import remove_tags
import time
import re



class FooglebolgSpider(scrapy.Spider):
    name = 'googleblog'
    start_urls=['https://security.googleblog.com/']
    allowed_domains=['googleblog.com']

    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3291.0 Safari/537.36',
        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url,callback=self.parse)

    def parse(self, response):
        def deal_publish_time(publish_time_raw=None):
            if publish_time_raw:#需要注意这里边可能没有提取到，如果没有取到，这里其实也有可能不是none，而是没有传入数据，所以要在开头默认赋值
                mouth_str_dict={
                    'January':'01',
                    'February':'02',
                    'March':'03',
                    'April':'04',
                    'May':'05',
                    'June':'06',
                    'July':'07',
                    'August':'08',
                    'September':'09',
                    'October':'10',
                    'November':'11',
                    'December':'12',
                }
                publish_mouth=publish_time_raw.split(' ')
                if str(publish_mouth[0].strip()) in mouth_str_dict.keys():
                    try:
                        mouth_num_str=mouth_str_dict[str(publish_mouth[0].strip())]
                        publish_time=str(publish_mouth[2].strip())+'-'+mouth_num_str+'-'+str(publish_mouth[1])
                        publish_date= publish_time.strip(',')+' 00:00:00'
                        time_tuple=time.strptime(publish_date,'%Y-%m-%d %H:%M:%S')
                        publish_time=time.mktime(time_tuple)
                        return str(int(publish_time))
                    except Exception as e:
                        print(e)
                else:
                    return publish_mouth

            else:
                return None

        def deal_publisher(html_raw):
            response_publisher=scrapy.http.HtmlResponse(url='thisIsJavaScript',body=str(html_raw))
            publish_user=response_publisher.xpath('.//span[@class="byline-author"]/text()').extract_first(default=None)
            publish_user=publish_user.split(',')[0].split('by')[1].split('and')

            print(publish_user)
            return publish_user

        for i in response.xpath('//*[@id="Blog1"]/div[@class="post"]'):
            itemloderArticle=ItemLoader(item=ThreatcollectItem(),selector=i)
            itemloderArticle.add_xpath('title','.//h2/a/text()',TakeFirst())
            itemloderArticle.add_xpath('url','.//h2/a/@href',TakeFirst())
            itemloderArticle.add_xpath('publish_time','.//div[@class="post-header"]/div[@class="published"]/span/text()',Join(),deal_publish_time)
            itemloderArticle.add_xpath('content','.//div[@class="post-body"]/div[contains(@class,"post-content")]/script/text()',MapCompose(remove_tags))
            itemloderArticle.add_xpath('article_id','.//@data-id')
            itemloderArticle.add_value('img_urls',i.re(r'src="(.*?)"'))
            itemloderArticle.add_value('spider_time',time.time()*1000)
            itemloderArticle.add_xpath('publisher','.//div[@class="post-body"]/div[contains(@class,"post-content")]/script/text()',deal_publisher)
            itemloderArticle.add_value('html',i.extract())



            item1=itemloderArticle.load_item()
            yield item1
            # yield response.follow(url=item1['url'],headers=self.headers,meta={'item':item1},callback=self.parse_item)

        nexturl=response.xpath('//*[@id="Blog1_blog-pager-older-link"]/@href').extract()
        # yield response.follow(url=nexturl[0],headers=response.headers)

    def parse_item(self,response):
        '''
        示例而已，这个爬虫用不着这个，可以删除。并且上一个函数的yield也要删除
        :param response:
        :return:
        '''
        last_item=response.meta['item']
        itemloader1=ItemLoader(item=last_item)
        itemloader1.add_value_to_original('article_id','add in parse_item')
        item2=itemloader1.load_item()
        print(item2)
        yield item2