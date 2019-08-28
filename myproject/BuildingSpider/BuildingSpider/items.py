# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath('.')))
from  BuildingPlat.models import CallBid, WinBid
from scrapy_djangoitem import DjangoItem

class CallBidItem(DjangoItem):
    django_model = CallBid

class WinBidItem(DjangoItem):
    django_model = WinBid
