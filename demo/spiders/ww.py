from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from demo.items import DemoItem
from scrapy.selector import XmlXPathSelector

from demo.items import DemoItem

class WwSpider(CrawlSpider):
    name = 'ww'
    allowed_domains = ['woolworthsonline.com.au']
    start_urls = ['http://www2.woolworthsonline.com.au/Shop/Browse/bakery']

    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths=('//a[@class="_jumpTop"]')),callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        sel = Selector(response=response)
        products = sel.xpath("""//div[contains(@class,"product-stamp-middle")]""")
        items = []
        for product in products:
            item = DemoItem()
            item['name'] = product.xpath(""".//span[contains(@class,"description")]/text()""").extract()
            item['price'] = product.xpath(""".//span[contains(@class,"price")]/text()""").extract()
            items.append(item)
        return items
