from scrapy.selector import Selector
from scrapy import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapyFootballSpider.items import FootballTitle,FootballImage,FootballUrl

class FootballSpiderImage(Spider):
    name = "footballImage"
    allowed_domains = ["dongqiudi.com"]
    start_urls = ["https://www.dongqiudi.com"]

    def parse(self,response):
        item_image = FootballImage()
        image_urls = \
        response.xpath('//img[starts-with(@src,"http://img.dongqiudi.com/data/")]')
        image_urls = image_urls.css('img::attr(src)').extract()
        for image_url in image_urls:
            item_image["imgUrl"] = image_url
            print("imgUrl is:" + image_url)
            yield item_image


class FootballSpiderTitle(Spider):
    name = "footballTitle"
    allowed_domains = ["dongqiudi.com"]
    start_urls = ["https://www.dongqiudi.com"]

    def parse(self,response):
        item_title = FootballTitle()
        title = response.xpath('//title/text()')[0].extract()
        print("Title is:" + title)
        item_title["title"] = title
        yield item_title

class FootballSpiderUrl(CrawlSpider):
    name = "footballUrl"
    allowed_domains = ["dongqiudi.com"]
    start_urls = ["http://dongqiudi.com"]
    rules = [Rule(LinkExtractor(allow=('/article/'),),callback="parse_item",\
                  follow = True)]

    def parse_item(self,response):
        self.log("processing page : %s" % response.url)

        item_url = FootballUrl()
        item_url['url'] = response.url
        title = response.xpath('//title/text()')[0].extract()
        print("processing page title : %s" % title)
        item_url["title"] = title
        return item_url
