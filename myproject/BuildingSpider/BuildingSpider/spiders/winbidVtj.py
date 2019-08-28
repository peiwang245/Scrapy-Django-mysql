
#设置页码数爬取
import scrapy
from datetime import datetime
from  ..items import WinBidItem
import re
from scrapy.http import Request
from pybloom_live import BloomFilter
import hashlib
import html2text as ht  # pip install html2text
import requests

global g_district, g_type
g_district = '天津'


class WinBidSpider(scrapy.spiders.Spider):
    name = "winbidVtj"
    allow_domains = ["tjconstruct.cn"]
    start_urls = ['http://www.tjconstruct.cn/Zbgs']

    # custom_settings = {
    #     'ITEM_PIPELINES': {'BuildingSpider.pipelines.winbidVtjPipeline': 350}
    # }

    end_page =5#设置爬取页码数
    for count in range(1, end_page):
        link = 'http://www.tjconstruct.cn/Zbgs/Index/'+str(count)+'?type = sgzb'
        start_urls.append(link)

    def start_requests(self):
        for url in self.start_urls[1:]:
            yield Request(url,callback = self.parse)#生成器回调函数


    def parse(self, response):
        print("*" * 50)
        bids = response.css('table .t1 tr')#css选择器
        # bids = response.xpath('//table[@class="t1"]/tr')#css选择器

        for bid in bids[1:]:
            item = WinBidItem()
            try:
                nname = re.search('_blank\">(.*?)</a>', bid.extract()).group(1)
                npurl = bid.re_first('href=\"(.*?)\"')
                kw = re.search('a>.*?;\">\s+(.*?)\s+<.*?;\">\s+(.*?)\s+<.*?;\">\s+(.*?)\s+<', bid.extract(), re.S)
                publisher = kw.group(1)
                ndocnmb = kw.group(2)
                ndate = datetime.strptime(kw.group(3), "%Y/%m/%d").strftime("%Y-%m-%d")
                bloomnmb = nname + ndocnmb

                #md文本
                text_maker = ht.HTML2Text()
                text_maker.bypass_tables = False
                htmlfile = requests.get(npurl)
                htmlfile.encoding = 'gbk'
                htmlpage = htmlfile.text
                text = text_maker.handle(htmlpage)
                md = text.split('#')  # split post content

                item['name']= nname
                item['district'] = g_district
                item['dom'] = self.allow_domains[0]

                item['purl'] = npurl
                item['publisher'] = publisher
                item['docnmb'] = ndocnmb

                item['startaffich'] = ndate
                item['endaffich'] = None
                item['type'] = '--'

                item['winner'] = '--'
                item['address'] = '--'
                item['bloomnb'] = bloomnmb

                item['md'] = ''.join(md)
                item['content'] = htmlpage
                item['crawltime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                yield item
            except:
                pass
