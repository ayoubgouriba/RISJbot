# -*- coding: utf-8 -*-
from RISJbot.spiders.newsrssfeedspider import NewsRSSFeedSpider
from RISJbot.loaders import NewsLoader
# Note: mutate_selector_del_xpath is somewhat naughty. Read its docstring.
from RISJbot.utils import mutate_selector_del
from scrapy.loader.processors import Identity, TakeFirst
from scrapy.loader.processors import Join, Compose, MapCompose
from scrapy.http import Request
from urllib.parse import urlparse, urlunparse
from datetime import datetime

class BusinessInsiderFRSpider(NewsRSSFeedSpider):
    """This class contains code in common with BusinessInsiderSpider,
       but is built on a different base: BI France doesn't publish a sitemap
       that I can find, so this is a NewsRSSFeedSpider."""

    name = 'businessinsiderfr'
    # allowed_domains = ['businessinsider.fr']
    start_urls = ['http://www.businessinsider.fr/feed/']

#    def url_to_request(self, url, callback=None, meta={}):
#        if callback is None:
#            callback = self.parse_page
#        # Overridden to ensure "[?&]IR=C is present on the request. Without
#        # this, BI will redirect to your 'local' edition.
#        url = url.strip()
#        p = urlparse(url)
#        if "IR=C" in p.query:
#            pass
#        elif p.query:
#            url = urlunparse((p.scheme, p.netloc, p.path, p.params,
#                              p.query+"&IR=C", p.fragment))
#        else:
#            url = urlunparse((p.scheme, p.netloc, p.path, p.params,
#                              "IR=C", p.fragment))
#        
#        return Request(url, callback=callback, meta=meta)

    def parse_page(self, response):
        """@url http://www.businessinsider.fr/meilleures-entreprises-equilibre-vie-pro-vie-privee-selon-glassdoor?IR=C
        @returns items 1
        @scrapes bodytext bylines fetchtime modtime headline
        @scrapes section source summary url language
        @noscrapes keywords

        """
        s = response.selector
        # Remove any content from the tree before passing it to the loader.
        # There aren't native scrapy loader/selector methods for this.
        # CSS is better for operating on classes than XPath, otherwise
        # either will do.        
#        mutate_selector_del(s, 'xpath', '//div[@id="see-also-links"]')
#        mutate_selector_del(s, 'xpath', '//div[contains(@class, "popular-video")]')
#        mutate_selector_del(s, 'xpath', '//span[contains(@class, "caption-source")]')
        mutate_selector_del(s, 'xpath', '//p[contains(@class, "wp-caption-text")]')
        mutate_selector_del(s, 'xpath', '//div[contains(@class, "pod-fb-like")]')

        l = NewsLoader(selector=s)


        # Add a number of items of data that should be standardised across
        # providers. Can override these (for TakeFirst() fields) by making
        # l.add_* calls above this line, or supplement gaps by making them
        # below.
        l.add_fromresponse(response)
        l.add_htmlmeta()
        l.add_schemaorg(response)
        l.add_opengraph()
        l.add_scrapymeta(response)
        #l.add_schemaorg_bylines()
        #l.add_dublincore()

        l.add_xpath('bodytext', '//div[contains(@class, "post-content")]//text()')
        l.add_xpath('bylines', '//a[@rel="author"]//text()')
        # BI prints times for recent articles as "hours since published". But
        # helpfully includes a unix timestamp in its metadata.
#        ts = s.xpath('//span[@data-bi-format="date"]/@rel').extract_first()
#        if ts:
#            l.add_value('modtime', datetime.fromtimestamp(int(ts)).isoformat())
#        l.add_xpath('section', '//h2[contains(@class, "vert-name")]//text()')

        return l.load_item()

