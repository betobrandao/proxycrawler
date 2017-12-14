# -*- coding: utf-8 -*-
import scrapy
from proxies.items import ProxiesItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join
from urllib.parse import urljoin
import socket
import datetime
from scrapy.http import Request

class PremproxySpider(scrapy.Spider):
    name = 'premproxy'
    allowed_domains = ['premproxy.com']
    start_urls = ['https://premproxy.com/list/']

    def parse(self, response):
        next_selector = response.xpath('(//ul[@class="pagination"])[1]/li/a[contains(text(), "next")]/@href')
        # Get the next index URLs and yield Requests
        for url in next_selector.extract():
            yield Request(urljoin(response.url, url))


        # Iterate through Proxy list and create ProxiesItems
        selectors = response.xpath('//tbody/tr[@class="anon"]')
        for selector in selectors:
            yield self.parse_item(selector, response)

    def parse_item(self, selector, response):
        # Create the loader using the selector
        l = ItemLoader(item=ProxiesItem(), selector=selector)

        l.add_xpath('ip', './td[@data-label="IP:port "]/text()',
                MapCompose(lambda i: i[:i.index(':')], str.strip))
        l.add_xpath('port', './td[@data-label="IP:port "]/text()',
                MapCompose(lambda i: i[i.index(':')+1:], str.strip,  int))
        l.add_xpath('anonymity', './td[@data-label="Anonymity Type: "]/text()',
                MapCompose(str.strip))
        l.add_xpath('checked', './td[@data-label="Checked: "]/text()',
                MapCompose(str.strip))
        l.add_xpath('country', './td[@data-label="Country: "]/text()',
                MapCompose(str.strip))
        l.add_xpath('city', './td[@data-label="City: "]/text()',
                MapCompose(str.strip))
        l.add_xpath('isp', './td[@data-label="ISP: "]/text()',
                MapCompose(str.strip))

        #housekeeping
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.datetime.now())

        return l.load_item()

