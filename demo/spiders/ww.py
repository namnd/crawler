from scrapy.spider import Spider

class WwSpider(Spider):
    name = "ww"
    allowed_domains = ["woolworthsonline.com.au"]
    start_urls = (
        'http://www.woolworthsonline.com.au/',
        )

    def parse(self, response):
        pass 
