from scrapy.spider import Spider
from scrapy.selector import Selector

from demo.items import DemoItem

class ColesSpider(Spider):
    name = 'coles'
    allowed_domains = ['coles.com.au']
    start_urls = [
        "http://shop.coles.com.au/online/national/specials-offers/specials-offers"
    ]

    def parse_item(self, response):
        sel = Selector(response)
        products = sel.xpath('//div[@class="outer-prod prodtile"]')
        items = []
        for product in products:
            i = DemoItem()
            i['name'] = product.xpath('//a[@class="product-url"]/text()').extract()
            i['url'] = product.xpath('//a[@class="product-url"]').extract()
            i['img'] = product.xpath('//a[@class="product-url"]/img/@src').extract()

            i['price'] = product.xpath('//div[@class="price"]/text()').extract()
            i['unit_price'] = product.xpath('//div[@class="unit-price"]/text()').extract()

            items.append(i)
        return items
