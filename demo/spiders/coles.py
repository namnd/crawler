from scrapy.spider import Spider
from scrapy.selector import Selector

from demo.items import DemoItem

class ColesSpider(Spider):
    name = 'coles'
    allowed_domains = ['coles.com.au']
    start_urls = [
        "http://shop.coles.com.au/online/SearchDisplay?multiSearch=&showResultsPage=true&langId=-1&beginIndex=500&sType=SimpleSearch&browseView=true&pageSize=100&resultCatEntryType=&catalogId=10576&pageView=image&urlLangId=-1&categoryId=478564&storeId=10601"
    ]

    def parse(self, response):
        sel = Selector(response)
        products = sel.xpath('//div[@class="outer-prod prodtile"]')
        items = []
        for product in products:
            i = DemoItem()
            i['name'] = product.xpath('.//a[@class="product-url"]/text()').extract()
            i['url'] = product.xpath('.//span[@class="item"]/a[@class="product-url"]/@href').extract()
            i['img'] = product.xpath('.//a[@class="product-url"]/img/@src').extract()

            i['price'] = product.xpath('.//div[@class="price"]/text()').extract()
            i['unit_price'] = product.xpath('.//div[@class="unit-price"]/text()').extract()

            items.append(i)
        return items
