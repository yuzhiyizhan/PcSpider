from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from Pixiv.spiders.civitai import CivitaiSpider

process = CrawlerProcess(get_project_settings())


def worker(spider):
    process.crawl(spider)


def call_error(worker):
    worker_exception = worker.exception()
    if worker_exception:
        print("Worker return exception: {}".format(worker_exception))


if __name__ == "__main__":
    tasks = [CivitaiSpider]
    for i in tasks:
        worker(i)
    process.start()
