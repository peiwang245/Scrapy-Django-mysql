# Generated by Django 2.2.4 on 2019-09-02 09:52

from django.db import migrations, models
import mdeditor.fields
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WinBid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='--', max_length=100, verbose_name='项目名称')),
                ('province', models.CharField(default='--', max_length=100, verbose_name='省份')),
                ('type', models.CharField(default='--', max_length=100, verbose_name='种类')),
                ('dom', models.CharField(default='--', max_length=100, verbose_name='域名')),
                ('purl', models.URLField(default='--', max_length=225, verbose_name='链接网址')),
                ('publisher', models.CharField(default='--', max_length=100, verbose_name='发布部门')),
                ('district', models.CharField(default='--', max_length=100, verbose_name='施工区域')),
                ('docnmb', models.CharField(default='--', max_length=100, verbose_name='公告文件号')),
                ('winner', models.CharField(default='--', max_length=100, verbose_name='中标单位')),
                ('startaffich', models.DateField(null=True, verbose_name='公告发布日期')),
                ('endaffich', models.DateField(null=True, verbose_name='公告截止日期')),
                ('crawltime', models.DateTimeField(null=True, verbose_name='爬取时间')),
                ('bloomnb', models.CharField(max_length=200, verbose_name='哈希值')),
                ('md', mdeditor.fields.MDTextField(null=True, verbose_name='MD富文本编辑器')),
                ('content', tinymce.models.HTMLField(null=True, verbose_name='HTML富文本编辑器')),
            ],
            options={
                'verbose_name_plural': '中标信息',
                'db_table': 'winbidsql',
                'ordering': ['startaffich'],
                'unique_together': {('name', 'docnmb')},
            },
        ),
        migrations.CreateModel(
            name='CallBid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='--', max_length=100, verbose_name='项目名称')),
                ('province', models.CharField(default='--', max_length=100, verbose_name='省份')),
                ('type', models.CharField(default='--', max_length=100, verbose_name='种类')),
                ('dom', models.CharField(default='--', max_length=100, verbose_name='域名')),
                ('purl', models.URLField(default='--', max_length=225, verbose_name='链接网址')),
                ('tenderee', models.CharField(default='--', max_length=100, verbose_name='招标单位')),
                ('tenderer', models.CharField(default='--', max_length=100, verbose_name='投标单位')),
                ('district', models.CharField(default='--', max_length=100, verbose_name='施工区域')),
                ('docnmb', models.CharField(default='--', max_length=100, verbose_name='公告文件号')),
                ('startaffich', models.DateField(null=True, verbose_name='公告发布日期')),
                ('endaffich', models.DateField(null=True, verbose_name='公告截止日期')),
                ('startRegistration', models.DateTimeField(null=True, verbose_name='报名开始日期')),
                ('endRegistration', models.DateTimeField(null=True, verbose_name='报名结束日期')),
                ('crawltime', models.DateTimeField(null=True, verbose_name='爬取时间')),
                ('bloomnb', models.CharField(max_length=200, verbose_name='哈希值')),
                ('md', mdeditor.fields.MDTextField(null=True, verbose_name='MD富文本编辑器')),
                ('content', tinymce.models.HTMLField(null=True, verbose_name='HTML富文本编辑器')),
            ],
            options={
                'verbose_name_plural': '招标信息',
                'db_table': 'callbidsql',
                'ordering': ['startaffich'],
                'unique_together': {('name', 'docnmb')},
            },
        ),
    ]
