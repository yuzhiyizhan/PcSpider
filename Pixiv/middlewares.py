# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import aiohttp
from scrapy import signals
from scrapy.http import HtmlResponse
from scrapy.utils.project import get_project_settings


# useful for handling different item types with a single interface


class PixivSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class PixivDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        if response.status != 200:
            return request

        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        return request

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class Ja3DownloaderMiddleware:
    # def __init__(self):
    #     self.session = pyhttpx.HttpSession(browser_type='chrome')

    async def process_request(self, request, spider):
        if request.meta.get('Pipeline'):
            return
        proxies = {
            'https': '127.0.0.1:7890',
            'http': '127.0.0.1:7890',
        }

        data = {"url": request.url, "headers": dict(get_project_settings().get('DEFAULT_REQUEST_HEADERS')),
                "proxies": proxies, "cookies": request.cookies, "method": request.method}
        async with aiohttp.ClientSession() as client:
            response = await client.post(url='http://127.0.0.1:5959/middlewares', json=data)
            text = await response.text()
            return HtmlResponse(request.url, body=text, encoding="utf-8", request=request)

        # if request.method == 'GET':
        #     response = self.session.get(request.url, headers=get_project_settings().get('DEFAULT_REQUEST_HEADERS'),
        #                                 proxies=proxies, cookies=request.cookies)
        # elif request.method == 'POST':
        #     response = self.session.post(request.url, headers=get_project_settings().get('DEFAULT_REQUEST_HEADERS'),
        #                                  proxies=proxies, cookies=request.cookies)
        # else:
        #     raise ValueError(f"未知请求方式: {request.method}")
        #
        # return HtmlResponse(response.request.url, body=response.text, encoding=response.encoding, request=request)


class Ja3GoDownloaderMiddleware:
    async def process_request(self, request, spider):
        if request.meta.get('Pipeline'):
            return
        async with aiohttp.ClientSession() as client:
            url = request.url
            headers = dict(get_project_settings().get('DEFAULT_REQUEST_HEADERS'))
            proxies = "http://127.0.0.1:7890"
            cookies = request.cookies
            ja3 = "771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,0-23-65281-10-11-35-16-5-13-18-51-45-43-27-21,29-23-24,0"
            data = {
                "url": url,
                "method": request.method,
                "headers": headers,
                "proxies": proxies,
                "cookies": cookies,
                "ja3": ja3
            }
            responses = await client.post(url='http://127.0.0.1:5959/middlewares', json=data)
            text = await responses.text()
            return HtmlResponse(request.url, body=text, encoding="utf-8", request=request)
