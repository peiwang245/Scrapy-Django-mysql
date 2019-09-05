
#设置页码数爬取
import scrapy
from  ..items import WinBidItem
from datetime import  datetime
import re
from scrapy.http import Request
import html2text as ht  # pip install html2text
import requests
from urllib import parse

global  g_province
g_province = '江西省'

class BidSpider(scrapy.spiders.Spider):
    name = "winbidVjx"
    allow_domains = ["jxsggzy.cn"]
    base_urls = ['http://www.jxsggzy.cn/web/jyxx/tradeInfo.html']
    url01 = 'http://www.jxsggzy.cn'

    def start_requests(self):
        yield Request( self.base_urls[0], callback=self.parse)  # 生成器回调函数

    def parse(self, response):
        urls_info = response.xpath(r'//ul[@class = "ewb-trade-list"]/li')
        for url_info in urls_info[0:3]:
            url = url_info.xpath(r'.//a/@href').extract_first()
            type =  url_info.xpath(r'.//a/text()').extract_first()
            item = WinBidItem()
            item['type'] = type
            yield Request(url=parse.urljoin(self.url01,url), callback=self.parse_winbid,meta={'item':item})

    def parse_winbid(self,response):

        item = response.meta['item']
        url_winbid = response.xpath(r'//li[@class = "wb-tree-items haschild current"]//li[last()]//@href').extract_first()
        yield Request(url=response.urljoin(url_winbid), callback=self.parse_detail,meta={'item':item})


    def parse_detail(self, response):
        bids = response.xpath(r'//div[@class="ewb-infolist"]/ul/li')#css选择器
        for bid in bids:
            item = response.meta['item']
            try:
                bidtext = bid.xpath(r'.//a/text()').extract()
                if len(bidtext) == 1:
                    if bid.xpath(r'.//a/font/text()').extract_first():
                        if re.search(r'](.*)', bidtext[0]):
                            nname = re.search(r'](.*)', bidtext[0]).group(1) + bid.xpath(r'.//a/font/text()').extract_first()
                            district = re.search(r'\[(.*?)\]', bidtext[0]).group(1)
                        else:
                            nname = bid.xpath(r'.//a/font/text()').extract_first() + bidtext[0]
                            district = '--'
                    else:
                        nname = re.search(r'](.*)', bidtext[0]).group(1)
                        district = re.search(r'\[(.*?)\]', bidtext[0]).group(1)
                else:
                        nname = bid.xpath(r'.//a/font/text()').extract_first() + bidtext[1]
                        district = bidtext[0]
                npurl = bid.re_first('href="(.*?)"')
                ndate01 = re.search(r'"ewb-list-date">(.*?)<', bid.extract()).group(1)

                bloomnmb = nname + npurl
                purl = 'http://www.jxsggzy.cn' + npurl

                text_maker = ht.HTML2Text()
                text_maker.bypass_tables = False
                htmlfile = requests.get(purl)
                htmlfile.encoding = 'utf8'
                htmlpage = htmlfile.text
                text = text_maker.handle(htmlpage)

                item['name']= nname
                item['province'] = g_province
                item['dom'] = self.allow_domains[0]

                item['purl'] = purl
                item['publisher'] = '--'
                item['docnmb'] = '--'
                item['startaffich'] =  ndate01

                item['endaffich'] =  None
                item['winner'] = '--'
                item['district'] = district
                item['bloomnb'] = bloomnmb

                item['md'] = text
                item['content'] = htmlpage
                item['crawltime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                yield item
            except:
                pass

        next_page = response.xpath(r'//li[@class="nextlink"]//@href').extract_first()  # css选择器
        yield Request(response.urljoin(next_page), callback=self.parse_detail, meta={'item': item})