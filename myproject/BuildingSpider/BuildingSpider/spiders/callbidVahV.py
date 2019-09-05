
#设置页码数爬取
import scrapy
from datetime import datetime
from  ..items import CallBidItem
import re
from scrapy.http import Request
from urllib.parse import urlencode
from pybloom_live import BloomFilter
import hashlib
import html2text as ht  # pip install html2text
import requests
import json
from http.cookiejar import CookieJar
import urllib.request
from urllib.request import  HTTPCookieProcessor, build_opener
from bs4 import BeautifulSoup

global g_province
g_province = '安徽'


class CallBidSpider(scrapy.spiders.Spider):
    name = "callbidVah"
    allow_domains = ["ahtba.org.cn"]
    base_urls = ['http://www.ahtba.org.cn/Notice/AnhuiNoticeSearch?']
    end_page =5 #设置爬取页码数
    start_urls=[]
    for count in range(1, end_page):
        params = {
            'spid': '714',
            'scid': '597',
            'srcode': '',
            'sttype': '施工',
            'stime': '36500',
            'stitle': '',
            'sCompanyName': '',
            'isPageBarSearch': '1',
            'pageNum': str(count),
            'pageSize': '15'
        }
        url = base_urls[0] + urlencode(params)
        start_urls.append(url)

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse)


    def parse(self, response):
        print("*" * 50)
        # bids = response.css('table .t1 tr')#css选择器
        bids = response.xpath('//div[@class="iweifa_right_nr"]/p')#css选择器
        for bid in bids:
            item = CallBidItem()
            try:
                nname = re.search(r'title="(.*?)"', bid.extract()).group(1)
                npurl = bid.re_first('href="(.*?)"')
                ndate = re.search(r'class="fr">(.*?)<', bid.extract()).group(1)
                url_time = {'createTme': datetime.strptime(ndate, "%Y-%m-%d").strftime("%Y%%2F%m%%2F%d")}
                bloomnmb = nname
                url_info = npurl + '&' + urlencode(url_time)
                url_info = response.urljoin(url_info)
                # url_info = response.urljoin( npurl)
                # querypram={
                #     'id':'149989',
                #     'createTime':datetime.strptime(ndate, "%Y-%m-%d").strftime("%Y/%m/%d"),
                # }
                # Headers={
                # "Accept": '*/*',
                # 'Referer': response.urljoin(npurl),
                # 'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit 537.36(KHTML,likeGecko)Chrome/75.0.3770.100Safari/537.36',
                # 'X-Requested-With': 'XMLHttpRequest',
                # }
                # requests.get( url_info,data = querypram,headers=Headers)
                cookie_dict = {}
                cookie = CookieJar()
                handler = HTTPCookieProcessor(cookie)
                opener = build_opener(handler)
                req = urllib.request.Request(url_info.replace('Detail','Content'))
                soup = BeautifulSoup(req.text, 'lxml')
                responseV = opener.open(req)
                for item in cookie:
                    key = item.name
                    cookie_dict[key] = item.value
                responseV.close()

                Headers={
                "Accept":'*/*',
                'Accept-Encoding': 'gzip,deflate',
                'ccept-Language': 'zh-CN,zh',
                'q':'0.9',
                'Connection':'keep-alive',
                'Cookie':'ASP.NET_SessionId=nxxfb0h3hqydpjitfqwuul05;UM_distinctid=16;cf5c6366f6a0-03bc7918985ccd-e343166-e1000-16cf5c636702ba;Hm_lvt_b88419cfd6f98a39770a416b70174fbc = 1565590684,1567491504;CNZZDATA2273996 = cnzz_eid%3D637058281-1567487350-%26ntime%3D1567498162;Hm_lpvt_b88419cfd6f98a39770a416b70174fbc = 1567499865;_d_id = afd9c6dcbcb6cb19cb09a9cc8826a1',
                'Host':'www.ahtba.org.cn',
                'Referer': response.urljoin(npurl),
                'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit 537.36(KHTML,likeGecko)Chrome/75.0.3770.100Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest',
                }
                #md文本
                text_maker = ht.HTML2Text()
                text_maker.bypass_tables = False
                htmlfile =  requests.request('get',response.urljoin(url_info),headers =Headers)
                htmlfile.encoding = 'utf8'
                htmlpage = htmlfile.text
                text = text_maker.handle(htmlpage)
                md = text.split('#')  # split post content

                item['name']= nname
                item['province'] = g_province
                item['purl'] = response.urljoin(npurl)
                item['dom'] = self.allow_domains[0]

                item['docnmb'] = '--'
                item['startaffich'] = ndate
                item['endaffich'] = None

                item['startRegistration'] = None
                item['endRegistration'] = None
                item['type'] = '--'

                item['tenderee'] = '--'
                item['tenderer'] = '--'
                item['district'] = '--'
                item['bloomnb'] = bloomnmb
                item['md'] = ''.join(md)

                item['content'] = htmlpage
                item['crawltime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                yield item
            except:
                pass
