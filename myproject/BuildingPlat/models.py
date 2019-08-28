from django.db import models
from mdeditor.fields import MDTextField
from tinymce.models import HTMLField

# Create your models here.
class CallBid(models.Model):

    name = models.CharField('项目名称', max_length=100, default='--')#项目名称
    district = models.CharField('地区', max_length=100, default='--')#地区
    type = models.CharField('种类', max_length=100, default='--')#种类

    dom = models.CharField('域名', max_length=100, default='--')  # 种类
    purl = models.URLField(max_length=225, verbose_name='链接网址', default='--')#连接网址
    tenderee = models.CharField('招标单位', max_length=100, default='--')#招标人

    tenderer = models.CharField('投标单位', max_length=100, default='--')#投标单位
    address = models.CharField('施工地址', max_length=100, default='--')#施工地址
    docnmb = models.CharField('公告文件号', max_length=100, default='--')#公告文件号

    startaffich = models.DateField('公告发布日期', null=True)#公告发布日期
    endaffich = models.DateField('公告截止日期', null=True)  # 公告截止日期
    startRegistration = models.DateTimeField('报名开始日期', null=True)  # 报名开始日期

    endRegistration= models.DateTimeField('报名结束日期', null=True)  # 报名结束日期
    crawltime = models.DateTimeField('爬取时间', null=True)  # 爬取时间日期
    bloomnb = models.CharField('哈希值', max_length=200)  # 哈希值

    md =MDTextField('MD富文本编辑器',null = True)
    content = HTMLField('HTML富文本编辑器',null = True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'callbidsql'
        verbose_name_plural ='招标信息'
        unique_together = [["name", "docnmb"]]
        ordering = ["startaffich"]



class WinBid(models.Model):

    name = models.CharField('项目名称', max_length=100, default='--')  # 项目名称
    district = models.CharField('地区', max_length=100, default='--')  # 地区
    type = models.CharField('种类', max_length=100, default='--')  # 种类

    dom = models.CharField('域名', max_length=100, default='--')  # 种类
    purl = models.URLField(max_length=225, verbose_name='链接网址', default='--')  # 连接网址
    publisher = models.CharField('发布部门', max_length=100, default='--')  # 发布部门

    address = models.CharField('施工地址', max_length=100, default='--')  # 施工地址
    docnmb = models.CharField('公告文件号', max_length=100, default='--')  # 公告文件号
    winner = models.CharField('中标单位',max_length=100, default='--')#中标单位

    startaffich = models.DateField('公告发布日期', null=True)  # 公告发布日期
    endaffich = models.DateField('公告截止日期', null=True)  # 公告截止日期
    crawltime = models.DateTimeField('爬取时间', null=True)  # 爬取时间日期

    bloomnb = models.CharField('哈希值', max_length=200)  # 哈希值
    md =MDTextField('MD富文本编辑器',null = True)
    content = HTMLField('HTML富文本编辑器',null = True)

    class Meta:
        db_table = 'winbidsql'
        verbose_name_plural = '中标信息'
        unique_together = [["name", "docnmb"]]
        ordering = ["startaffich"]

    def __str__(self):
        return self.name





