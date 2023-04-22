# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose


def clean(string):
    string = str(string)
    string = string.replace('\\', '')
    string = string.replace('/', '')
    string = string.replace('|', '')
    string = string.replace(':', '')
    string = string.replace('*', '')
    string = string.replace('?', '')
    string = string.replace('"', '')
    string = string.replace('<', '')
    string = string.replace('>', '')
    return string


class PixivItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    file_urls = scrapy.Field(output_processor=TakeFirst())
    files = scrapy.Field()
    title = scrapy.Field(input_processor=MapCompose(clean), output_processor=TakeFirst())
    filename = scrapy.Field(output_processor=TakeFirst())
    user_id = scrapy.Field(input_processor=MapCompose(clean), output_processor=TakeFirst())
    text = scrapy.Field(output_processor=TakeFirst())
    model_data = scrapy.Field(output_processor=TakeFirst())
