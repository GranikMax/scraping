import scrapy
from scrapy.http import HtmlResponse
from leroymerlin.items import LeroymerlinItem
from scrapy.loader import ItemLoader


class LeroymerlinruSpider(scrapy.Spider):
    name = 'leroymerlinru'
    allowed_domains = ['castorama.ru']

    def __init__(self, **kwargs):
        super().__init__()
        self.start_urls = [f'https://www.castorama.ru/catalogsearch/result/?q={kwargs.get("query")}&limit=96']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@class="next i-next"]')
        if next_page:
            yield response.follow(next_page[0], callback=self.parse)

        links = response.xpath('//a[contains(@class, "product-card__name")]/@href')
        for link in links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroymerlinItem(), response=response)
        loader.add_xpath('name', "//h1[@class='product-essential__name hide-max-small']/text()")
        loader.add_xpath('price', "//div[@class='product-buy-panel scrollbar-margin js-fixed-panel']//span[@class='price']/span/span/text()")
        loader.add_value('url', response.url)
        loader.add_xpath('image_urls', "//img[@class='top-slide__img swiper-lazy']/@data-src")
        yield loader.load_item()