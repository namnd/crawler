from scrapy.contrib.spiders import CrawlSpider
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from groceries_crawler.items import GroceryItem
from scrapy.http import FormRequest
class ColesSpider(CrawlSpider):
    name = 'coles'
    allowed_domains = ['shop.coles.com.au']
    start_urls = [
        "http://shop.coles.com.au/online/national/"
    ]
    rules = [
        Rule(SgmlLinkExtractor(restrict_xpaths=('//a[@class="browseAllSubCategory"]')),
             follow=True, callback="parse_page")
    ]

    def parse_page(self, response):
        sel = Selector(response)
        url = "{}/{}".format(response.url,'ColesCategoryView')
        items = self.process_items(response)
        data_index = sel.xpath("""//a[contains(@class,"action-change-page") \
                        and contains(@title,"Next page of results")]/@data-beginindex""")
        if len(data_index) > 0:
            begin_index = int(data_index[0].extract())
            print "HELLO"
            FormRequest.from_response(
                response,
                formdata={
                    'beginIndex': str(begin_index),
                    'pageSize': '40'
                },
                callback=self.parse_page
            )
        #return items
        return None

    def process_items(self, response):
        items = []
        sel = Selector(response)
        products = sel.xpath("""//div[contains(@class,"outer-prod") and contains(@class,"prodtile")]""")
        for product in products:
            item=GroceryItem()

            item['name'] = product.xpath(""".//a[@class="product-url"]/text()""").extract()
            item['price'] = product.xpath(""".//div[@class="price"]/text()""").extract()

            items.append(item)
        return items

