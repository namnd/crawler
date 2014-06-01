from scrapy.contrib.spiders import CrawlSpider
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.selector import XmlXPathSelector
AJAXCRAWL_ENABLED = True
from demo.items import DemoItem
class ColesSpider(CrawlSpider):
    name = 'coles'
    allowed_domains = ['coles.com.au']
    start_urls = [
        "http://shop.coles.com.au/online/SearchDisplay?searchTermScope=&multiSearch=&searchType=2&maxPrice=&showResultsPage=true&langId=-1&beginIndex=0&sType=SimpleSearch&browseView=true&metaData=&manufacturer=&resultCatEntryType=&catalogId=10576&pageView=[Ljava.lang.String%3B%4032533253&minPrice=&urlLangId=-1&categoryId=930340&storeId=10601"
    ]
    rules = [
             Rule(SgmlLinkExtractor(restrict_xpaths=('//a[@class="btn-aqua action-change-page"]')),
                    follow=True, callback="parse_item")
    ]

    def parse_item(self, response):
        sel = Selector(response=response)
        products = sel.xpath("""//div[contains(@class,"outer-prod prodtile")]""")
        items = []
        for product in products:
            item = DemoItem()
            item['name'] = product.xpath(""".//a[@class="product-url"]/text()""").extract()
            item['price'] = product.xpath(""".//div[@class="price"]/text()""").extract()
            items.append(item)
        return items
