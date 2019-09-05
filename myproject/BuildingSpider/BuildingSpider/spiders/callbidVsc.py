
#设置页码数爬取
import scrapy
from datetime import datetime
from  ..items import CallBidItem
import re
from scrapy.http import Request
from urllib.parse import urlencode
import requests
from pybloom_live import BloomFilter
import hashlib
import html2text as ht  # pip install html2text

# global g_province, g_type
g_province = '四川'


class BidSpider(scrapy.spiders.Spider):
    name = "callbidVsc"
    allow_domains = ["scbid.com"]
    base_urls = ['http://www.scbid.com/zh/news/web_zbxx_19.shtml?']
    end_page =5 #设置爬取页码数
    start_urls=[]
    for count in range(1, end_page):
        params = {
            'a': '2',
            'b': '0',
            'page': str(count)
        }
        url = base_urls[0] + urlencode(params)
        start_urls.append(url)

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url,callback = self.parse)


    def parse(self, response):
        print("*" * 50)
        # bids = response.css('table .t1 tr')#css选择器
        bids = response.xpath(r'//div[@class="ui bidlist"]/div[@class="list"]/span')#css选择器
        for bid in bids:
            item = CallBidItem()
            try:
                nname = re.search(r'title="(.*?)"', bid.extract()).group(1)
                npurl = bid.re_first('href="(.*?)"')
                ndate01 = re.search(r's-time" title="(.*?)">', bid.extract()).group(1)
                ndate02 = re.search(r'e-time" title="(.*?)">', bid.extract()).group(1)

                bloomnmb = nname
                # md文本
                text_maker = ht.HTML2Text()
                text_maker.bypass_tables = False
                htmlfile = requests.get(response.urljoin(npurl))
                htmlfile.encoding = 'gbk'
                htmlpage = htmlfile.text
                text = text_maker.handle(htmlpage)
                md = text.split('#')  # split post content

                item['name']= nname
                item['province'] = g_province
                item['dom'] = self.allow_domains[0]

                item['purl'] = response.urljoin(npurl)
                item['docnmb'] = '--'
                item['startaffich'] =  ndate01
                item['endaffich'] =  ndate02

                item['startRegistration'] = None
                item['endRegistration'] = None
                item['type'] = '--'

                item['tenderee'] = '--'
                item['tenderer'] = '--'
                item['district'] = '--'

                item['bloomnb'] = bloomnmb
                item['md'] = ''.join(md)
                yield item
            except:
                pass
