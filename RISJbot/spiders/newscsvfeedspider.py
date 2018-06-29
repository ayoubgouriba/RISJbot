# -*- coding: utf-8 -*-
import logging
from scrapy.spiders import CSVFeedSpider
from scrapy.http import Request
from RISJbot.utils import etree_to_recursive_dict

logger = logging.getLogger(__name__)

class NewsCSVFeedSpider(CSVFeedSpider):
    """Fetch URLs to crawl from a publicly available CSV file, one of
       whose fields is 'url'. URLs found are fetched and parsed."""
    def parse_row(self, response, row):
        url = row['url']
        if url:
            yield self.url_to_request(url, meta=meta)
        else:
            self.logger.debug('No URL for %s' % row))

    def parse(self, response):
        return self.parse_page(response)

    def parse_page(self, response):
        raise NotImplementedError

    def url_to_request(self, url, callback=None, meta={}):
        if callback is None:
            callback = self.parse_page
        return Request(url.strip(), callback=callback, meta=meta)

