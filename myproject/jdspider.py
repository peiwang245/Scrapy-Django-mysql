#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import re
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "building.settings")#website可以更改为自己的项目名称
django.setup()#Django版本大于1.7 加入这行代码
from account.models import Bid
import warnings
warnings.filterwarnings("ignore")

#爬取页面
def getHTMLText(url):
    try:
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' \
                     '(KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'   #模拟浏览器登陆
        headers = {'User-Agent': user_agent}
        r = requests.get(url, headers = headers)
        return r.text
    except:
        return ''


def get_info(url):
    html = getHTMLText(url)
    #创建 beautifulsoup 对象
    soup = BeautifulSoup(html,'lxml')
    items = soup.select('table .t1 tr')#css选择器
    #商品详情提取
    for item in items:
        try:
            nname = re.search('_blank\">(.*?)</a>', str(item)).group(1)
            npurl =re.search('href=\"(.*?)\" ', str(item), re.S).group(1)
            kw = re.search('a>.*?;\">\s+(.*?)\s+<.*?;\">\s+(.*?)\s+<.*?;\">\s+(.*?)\s+<', str(item), re.S)
            ntenderee = kw.group(1)
            ndocnmb = kw.group(2)
            ndate = datetime.strptime(kw.group(3), "%Y/%m/%d").strftime("%Y-%m-%d")
            if Bid.objects.filter(name=nname).exists():
                print("Entry contained in queryset")
            else:
                Bid.objects.create(name=nname, district=g_district, type=g_type, purl=npurl,
                                   tenderee=ntenderee, docnmb=ndocnmb, startaffich=ndate)
        except:
            pass


#数据存储
global g_district, g_type
g_district = '天津'
starttime = datetime.now()
results = []
# Type=['sgzb','jlzb','sjzb','sbzb','qtzb']
Type=['sgzb']
for g_type in Type:
    for i in range(1, 4):
        try:
            rooturl = 'http://www.tjconstruct.cn/Zbgg/Index/'+str(i)+'?type='+g_type
            results = get_info(rooturl)
        except:
            pass
endtime = datetime.now()
time = (endtime - starttime).seconds
print('本次爬取共计用时：%s s' % time)
