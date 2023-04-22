# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import mimetypes
# useful for handling different item types with a single interface
import os
from pathlib import Path

import scrapy
from itemadapter import ItemAdapter
from loguru import logger
from scrapy.pipelines.files import FilesPipeline
from usepy import useAdDict
from usepy import usePath
import csv


class PixivPipeline(FilesPipeline):

    def get_media_requests(self, item, info):
        urls = ItemAdapter(item).get(self.files_urls_field, [])
        if urls:
            return scrapy.Request(urls)

    def file_path(self, request, response=None, info=None, *, item=None):
        title = item.get('title')
        filename = item.get('filename')
        user_id = item.get('user_id')
        media_ext = Path(request.url).suffix
        if media_ext not in mimetypes.types_map:
            media_ext = ""
            media_type = mimetypes.guess_type(request.url)[0]
            if media_type:
                media_ext = mimetypes.guess_extension(media_type)
        return f'{user_id}/{title}/{filename}{media_ext}'


class CivitaiPipeline(PixivPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        title = item.get('title')
        filename = item.get('filename')
        media_ext = Path(request.url).suffix
        if media_ext not in mimetypes.types_map:
            media_ext = ""
            media_type = mimetypes.guess_type(request.url)[0]
            if media_type:
                media_ext = mimetypes.guess_extension(media_type)
        return f'/{title}/{filename}{media_ext}'


class CivitaiTextPipeline():
    def process_item(self, item, spider):
        data = useAdDict(ItemAdapter(item).asdict())
        if data.text:
            path = os.path.join(os.getcwd(), spider.settings.get('FILES_STORE'), data.title, f"{data.filename}.txt")
            stats = usePath.exists(path)
            if stats:
                logger.info(f"{path} 已下载")
            else:
                with open(path, "w") as f:
                    f.write(data.text)
        return item


class CivitaiModelPipeline():

    def __init__(self):
        self.f = open('C站.csv', mode='a', encoding='utf-8-sig', newline='')
        self.fp = csv.writer(self.f)
        self.fp.writerow(
            ['图片ID', '图片链接', '批评', '笑', '喜欢', '不喜欢', '心', '评论数', "模型ID", "模型链接", "模型名字", "模型评分", "评分人数", "模型下载数",
             "模型评论数", "喜欢模型人数", "模型类型"])

    def process_item(self, item, spider):
        datas = useAdDict(ItemAdapter(item).asdict())
        data = datas.model_data
        if data:
            self.fp.writerow(data.values())
        return item

    def close_spider(self, spider):
        self.f.close()
