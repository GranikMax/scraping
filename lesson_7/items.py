import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def convert_price(price: str):
    price = price.replace('\xa0', '').replace(' ', '')
    try:
        price = int(price)
    except Exception:
        return price
    return price


class LeroymerlinItem(scrapy.Item):
    title = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    price = scrapy.Field(input_processor=MapCompose(convert_price), output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())
    characteristics = scrapy.Field()
    _id = scrapy.Field()
    #