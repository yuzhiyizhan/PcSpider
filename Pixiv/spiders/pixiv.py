import json
import math
import re
import urllib.parse
from urllib.parse import urlencode

import scrapy
from scrapy.loader import ItemLoader
from scrapy_redis.spiders import RedisSpider
from scrapy_redis.utils import bytes_to_str
from usepy import useAdDict

from ..items import PixivItem


# 作者ID爬虫
class PixivSpider(scrapy.Spider):
    name = 'pixiv'
    # notify = Notify.from_settings(settings=settings)
    cookies = {
        "first_visit_datetime_pc": "2023-03-26+21%3A11%3A22",
        "yuid_b": "IjhVKUM",
        "p_ab_id": "4",
        "p_ab_id_2": "5",
        "p_ab_d_id": "1165756428",
        "_fbp": "fb.1.1679832685342.805244096",
        "_im_vid": "01GWEX9CH4RQ4CRTYWRZYWMEKG",
        "_ga_MZ1NL4PHH0": "GS1.1.1679832692.1.0.1679832701.0.0.0",
        "PHPSESSID": "82551544_GaKQJg9x2LyXyHlalAOAKzHFIP9o1Djj",
        "device_token": "b1904ae4142c435081c82d3160c373da",
        "c_type": "24",
        "privacy_policy_agreement": "0",
        "privacy_policy_notification": "0",
        "a_type": "0",
        "b_type": "1",
        "__utmz": "235335808.1680248692.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)",
        "__utmc": "235335808",
        "_ga_75BBYNYN9J": "GS1.1.1680943842.19.1.1680943880.0.0.0",
        "__utmv": "235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=82551544=1^9=p_ab_id=4=1^10=p_ab_id_2=5=1^11=lang=zh=1",
        "QSI_S_ZN_5hF4My7Ad6VNNAi": "v:0:0",
        "adr_id": "1WsjRUpOZpNrW5iNowemsCT8EjZy2YxgiLMbxR8Lxsx5smGp",
        "_gid": "GA1.2.892784361.1680933617",
        "cto_bundle": "SE7VkF8lMkJsb1lTRFVCVUNJVmlJZHV3QnF0MXhCT1BHdWtOa1YzWHZLeEtzRDFmWmsxWk5wZnZ1SWZ3cFdiZFhPOHllQUNSTXAlMkJVQ1pXNGZpQ3J3NWhBaXdFbXJpU3NocFMxUm56UnZ6c3AzWjJpUjloTyUyQjUyREd3YjhlTTRsRDRlQkpUVyUyQlVLZEIxJTJGNlNsQjg4RVNzdmFuRGJRJTNEJTNE",
        "__cf_bm": "G1H9MYkMT0n4YDJj09H4.hHYmg52_hyNdkthdyVChxM-1680942804-0-AejUFv48zxPmcbnVV/X5k+RbRPKaGO36/yB3auSQBH7wlkOFb0K8N372pDb/jNX7yz2uK/vadYT6ofqWM1Z/lBjjhjFCKJVoLOJFtiNn+lHz",
        "__utma": "235335808.1003715957.1679832684.1680933521.1680943876.14",
        "__utmt": "1",
        "__utmb": "235335808.1.10.1680943876",
        "tag_view_ranking": "EZQqoW9r8g~-98s6o2-Rp~0ZyHpNKAnH~2R7RYffVfj~Cp5keYns6b~7sEkq9z6Iz~XZdHBcII9S~FoqBnm7jCA~YIg5d0-NIH~vshhCHuYdi~hEuKWOJ6dp~3kGxmFZ333~jrWtah1X09~0xsDLqCEW6~Lt-oEicbBr~ftjGob_MSz~xufWQ15ZA3~Lzgc4VxM4k~_hSAdpN9rx~1CWwi2xr7g~JBT12jV9gz~bjOUs__Hus~8Le-BdaoRB~eVxus64GZU~uW5495Nhg-~RIm1W1ofw1~1WiF9FWDcG~VIOKa7rioU~ugghbxPdF0~Mgn3A1jkKS~uJM7KMdzad~y9uOd2-7zI~5kpAzh6cLj~D8nxEy1yJb~W7Wq4zH7SU~NGg_zXgKEd~SOCpnnQ8rf~azESOjmQSV~48UjH62K37~KN7uxuR89w~AGF29gcJU3~aSdrnGinfC~jpIZPQ502H~ogJrAPwW_n~Jcz3briDT3~RTJMXD26Ak~T_Vcohvd0e~0F5Qa_BYny~kGYw4gQ11Z~kqu7T68WD3~gmtw28vspD~CkDjyRo6Vc~dqqWNpq7ul~rD40aEPPmV~vwjAXgC5v3~98FF78f4J0~VfrCXBGpnO~ELSyDiVgix~b_rY80S-DW~beDpZWMfWQ~HFV5XeAh2k~EmhsFxSBo-~CdSz2Tqqq0~CiSfl_AE0h~KhVXu5CuKx~jnd_LG9_hg~E89mjha8tL~n94c_ezAjj~u3EAZmzDcl~euQIlGHCIi~1n-RsNEFpK~SapL8yQw4Y~o3L0-iL7Cp~GpCbNmiehA~kkVEciGw_C~IAC1aKgM9_~3gjIvNWGCE~MM6RXH_rlN~faHcYIP1U0~rHikrACO7E~HLWLeyYOUF~RcahSSzeRf~5oPIfUbtd6~tgP8r-gOe_~KOnmT1ndWG~3c2bnRBtyw~KC--pudNUr~W9lTrvxrgW~DwQ1Y7U5kv~2WDB03M6vH~jTSl_ciRq2~flP_TL6uNz~SIpXPnQ53M~7fCik7KLYi~_qCshdJxT4~F3cbycMFub~_vCZ2RLsY2~NBTasQsWI0~LlXnve21-S~3djIjKmUtG",
        "_ga": "GA1.1.1003715957.1679832684"
    }

    # user_id = list(
    #     set([12651854, 68170659, 70138098, 24378074, 22950794, 37480543, 2100924,
    #          60886812, 19018383, 14656176, 81972884, 36559040, 60886812, 76189568, 976698, 56171845,
    #          82816539, 17674535, 68255388, 80119571, 57777652, 65912860, 38072409, 75867586, 64293348, 55274365,
    #          64293348, 55274365, 14698013, 3384404]))
    user_id = [3384404]

    def start_requests(self):
        for i in self.user_id:
            url = f'https://www.pixiv.net/ajax/user/{i}/profile/all?lang=zh'
            yield scrapy.Request(url=url, callback=self.parse, cookies=self.cookies, meta={'user_id': i})
            # break

    def parse(self, response, **kwargs):
        try:
            datas = useAdDict(response.json())
        except Exception as e:
            yield response.request
            raise scrapy.exceptions.IgnoreRequest('重试请求')
        manga = datas.body.manga
        illusts = datas.body.illusts
        if manga:
            for k in manga.keys():
                url = f'https://www.pixiv.net/artworks/{k}'
                response.meta['id'] = str(k)
                yield scrapy.Request(url=url, callback=self.parse_item, cookies=self.cookies, meta=response.meta)
        if illusts:
            for k in illusts.keys():
                url = f'https://www.pixiv.net/artworks/{k}'
                response.meta['id'] = str(k)
                yield scrapy.Request(url=url, callback=self.parse_item, cookies=self.cookies, meta=response.meta)

    def parse_item(self, response, **kwargs):

        datas = response.xpath('//meta[@id="meta-preload-data"]/@content').get()
        if not datas:
            yield response.request
            raise scrapy.exceptions.IgnoreRequest('重试请求')

        data = useAdDict(json.loads(datas))
        ids = response.meta.get('id')
        user_ids = response.meta.get('user_id')

        try:
            user_id = data.user.get(str(user_ids)).name + f"({user_ids})"
        except Exception as e:
            user_id = user_ids
        response.meta["user_id"] = user_id

        title = data.illust.get(ids).illustTitle
        page = data.illust.get(ids).userIllusts.get(ids).pageCount
        image_url = data.illust.get(ids).urls.original

        for i in range(page):
            item = ItemLoader(item=PixivItem(), response=response)
            url = re.sub('p\d+', f'p{i}', image_url)
            item.add_value("title", title)
            item.add_value("filename", i)
            item.add_value("file_urls", url)
            item.add_value("user_id", user_id)
            yield item.load_item()

    # def closed(self, reason):
    #     self.notify.send_message(content=f'{self.name}爬虫结束', title="爬虫结束")


class PixivSpider_Redis(RedisSpider, PixivSpider):
    name = "pixiv_redis"
    redis_key = 'pixiv:start_urls'
    custom_settings = {
        "SCHEDULER": "scrapy_redis.scheduler.Scheduler",
        "DUPEFILTER_CLASS": "Pixiv.extensions.DupeFilter.RFPDupeFilter",
        "STATS_CLASS": "scrapy_redis.stats.RedisStatsCollector",
        "SCHEDULER_PERSIST": True,
        "SCHEDULER_QUEUE_CLASS": 'scrapy_redis.queue.PriorityQueue',
    }

    def make_request_from_data(self, data):
        user_id = bytes_to_str(data)
        url = f'https://www.pixiv.net/ajax/user/{user_id}/profile/all?lang=zh'
        return scrapy.Request(url=url, callback=self.parse, cookies=self.cookies, meta={'user_id': user_id})


# 搜索接口爬虫
class PixivSpider_search(PixivSpider):
    name = "pixiv_search"
    keyword = ["明日方舟"]

    def start_requests(self):
        for key in self.keyword:
            url = f"https://www.pixiv.net/ajax/search/artworks/{urllib.parse.quote(key)}"
            params = {
                "word": key,
                "order": "date_d",
                "mode": "all",
                "p": "1",
                "s_mode": "s_tag",
                "type": "all",
                "lang": "zh",
            }
            url = f'{url}?{urlencode(params)}'
            yield scrapy.Request(url, cookies=self.cookies, meta={"key": key})

    def parse(self, response, **kwargs):
        key = response.meta.get("key")
        datas = useAdDict(response.json())
        data = datas.body.illustManga.data
        total = datas.body.illustManga.total
        if response.meta.get("page") is None:
            pages = math.ceil(total / 60)
            for i in range(2, pages + 1):
                url = f"https://www.pixiv.net/ajax/search/artworks/{urllib.parse.quote(key)}"
                params = {
                    "word": key,
                    "order": "date_d",
                    "mode": "all",
                    "p": f"{i}",
                    "s_mode": "s_tag",
                    "type": "all",
                    "lang": "zh",
                }
                url = f'{url}?{urlencode(params)}'
                response.meta["page"] = True
                yield scrapy.Request(url, cookies=self.cookies, meta=response.meta)

        for i in data:
            ids = i.id
            title = i.title
            url = f'https://www.pixiv.net/artworks/{ids}'
            response.meta['id'] = str(ids)
            response.meta['title'] = title
            yield scrapy.Request(url=url, callback=self.parse_item, cookies=self.cookies, meta=response.meta)

    def parse_item(self, response, **kwargs):
        ids = response.meta.get('id')
        title = response.meta.get('title')
        user_id = response.meta.get('key')
        datas = response.xpath('//meta[@id="meta-preload-data"]/@content').get()
        data = useAdDict(json.loads(datas))
        image_url = data.illust.get(ids).urls.original
        page = data.illust.get(ids).userIllusts.get(ids).pageCount
        for i in range(page):
            item = ItemLoader(item=PixivItem(), response=response)
            url = re.sub('p\d+', f'p{i}', image_url)
            item.add_value("title", f"{title}({ids})")
            item.add_value("filename", i)
            item.add_value("file_urls", url)
            item.add_value("user_id", user_id)
            yield item.load_item()


class PixivSpider_Search_Redis(RedisSpider, PixivSpider_search):
    name = "pixiv_server_redis"
    redis_key = 'pixiv_server:start_urls'
    custom_settings = {
        "SCHEDULER": "scrapy_redis.scheduler.Scheduler",
        "DUPEFILTER_CLASS": "Pixiv.extensions.DupeFilter.RFPDupeFilter",
        "STATS_CLASS": "scrapy_redis.stats.RedisStatsCollector",
        "SCHEDULER_PERSIST": True,
        "SCHEDULER_QUEUE_CLASS": 'scrapy_redis.queue.PriorityQueue',
    }

    def make_request_from_data(self, data):
        key = bytes_to_str(data)
        url = f"https://www.pixiv.net/ajax/search/artworks/{urllib.parse.quote(key)}"
        params = {
            "word": key,
            "order": "date_d",
            "mode": "all",
            "p": "1",
            "s_mode": "s_tag",
            "type": "all",
            "lang": "zh",
        }
        url = f'{url}?{urlencode(params)}'
        yield scrapy.Request(url, callback=self.parse, cookies=self.cookies, meta={"key": key})
