from scrapy.contrib.spiders import CrawlSpider
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector

from grocerices_crawler.items import GroceryItem
import re


'''
Only process top level Categories, lower level categories contains products from top level
'''
def process_link(link):
    pattern = "/Shop/Browse/\w+$"
    if re.match(pattern,link):
        return link
    else:
        return None

class WoolworthSpider(CrawlSpider):
    name = 'ww'
    allowed_domains = ['woolworthsonline.com.au']
    start_urls = [
        "http://www2.woolworthsonline.com.au/"
    ]
    rules = [
                Rule(SgmlLinkExtractor(restrict_xpaths=('//a[@class="navigation-link"]'),
                                       process_value=process_link)
                ),
                Rule(SgmlLinkExtractor(restrict_xpaths=('//a[@class="_jumpTop"]')),
                    follow=True, callback="parse_item"
                )
    ]

    def parse_item(self, response):
        sel = Selector(response=response)
        products = sel.xpath("""//div[contains(@class,"product-stamp-middle")]""")
        items = []
        for product in products:
            item = GroceryItem()
            item['name'] = product.xpath(""".//span[contains(@class,"description")]/text()""").extract()
            item['price'] = product.xpath(""".//span[contains(@class,"price")]/text()""").extract()
            items.append(item)
        return items
