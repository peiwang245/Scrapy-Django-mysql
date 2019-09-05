"""""{
# 对反爬虫网页，可以设置一些headers信息，模拟成浏览器取访问网站
import urllib.request
url = "https://blog.csdn.net/qq_36411874/article/details/83650560"
file = urllib.request.urlopen(url)
print('获取当前url:', file.geturl())
print('file.getcode,HTTPResponse类型:', file.getcode)
print('file.info 返回当前环境相关的信息：', file.info())

# 爬虫模式浏览访问网页设置方法
# User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36
# 上边这个headers对应的存储user-agent信息，定义格式为：“User-Agent”,具体信息，获取一次即可，不需要每次通过F12获取
# 1，使用build_opener()修改报头
headers = ("User-Agent",
           " Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36")
opener = urllib.request.build_opener()
opener.addheaders = [headers]
data = opener.open(url).read()
fhandle = open('D:/2018110204.html', 'wb')
fhandle.write(data)
fhandle.close()
}"""

import os
from multiprocessing.pool import Pool
import requests
from urllib.parse import urlencode
from hashlib import md5

headers = {
    'Host':'www.toutiao.com',
    'Referer':'https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
    'X-Requested-With':'XMLHttpRequest'
}

def get_page(offset):
    params = {
        'offset': offset,
        'format': 'json',
        'keyword': '街拍',
        'autoload': 'true',
        'count': '20',
        'cur_tab': '1',
    }
    url = 'http://www.toutiao.com/search_content/?' + urlencode(params)
    try:
        response = requests.get(url,headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError:
        return None


def get_images(json):
    if json.get('data'):
        for item in json.get('data'):
            title = item.get('title')
            images = item.get('image_detail')
            for image in images:
                yield {
                    'image': image.get('url'),
                    'title': title
                }

#手工先创建头条图片文件夹
def save_image(item):
    if not os.path.exists(item.get('title')):
        os.mkdir(item.get('title'))
    try:
        response = requests.get(item.get('image'))
        if response.status_code == 200:
            file_path = '{0}/{1}.{2}'.format(item.get('title'), md5(response.content).hexdigest(), 'jpg')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(response.content)
            else:
                print('Already Downloaded', file_path)
    except requests.ConnectionError:
        print('Failed to Save Image')


def main(offset):
    json = get_page(offset)
    for item in get_images(json):
        print(item)
        save_image(item)


GROUP_START = 1
GROUP_END = 3

if __name__ == '__main__':
    pool = Pool()
    groups = ([x * 20 for x in range(GROUP_START, GROUP_END + 1)])
    pool.map(main, groups)
    pool.close()
    pool.join()
