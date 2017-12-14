# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class ProxiesItem(scrapy.Item):
    # Primary Fields
    ip          = Field()
    port        = Field()
    anonymity   = Field()
    checked     = Field()
    country     = Field()
    city        = Field()
    isp         = Field()

    # Housekeeping fields
    url         = Field()
    project     = Field()
    spider      = Field()
    server      = Field()
    date        = Field()

