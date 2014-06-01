from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from groceries_crawler.items import GroceryItem

class AldiSpider(CrawlSpider):
    name = 'aldi'
    allowed_domains = ['aldi.com.au']
    start_urls = ['http://www.aldi.com.au/']

    rules = (
        Rule(SgmlLinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        sel = Selector(response)
        i = GroceryItem()
        #i['domain_id'] = sel.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = sel.xpath('//div[@id="name"]').extract()
        #i['description'] = sel.xpath('//div[@id="description"]').extract()
        return i
