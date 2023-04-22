import json
from urllib.parse import urlencode

import execjs
import scrapy
from loguru import logger
from scrapy.loader import ItemLoader
from usepy import useAdDict

from ..items import PixivItem


class CivitaiSpider(scrapy.Spider):
    name = "civitai"
    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": {
            "authority": "civitai.com",
            "pragma": "no-cache",
            "cache-control": "no-cache",
            "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"96\", \"Google Chrome\";v=\"96\"",
            "sec-ch-ua-mobile": "?0",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
            "sec-ch-ua-platform": "\"Windows\"",
            "content-type": "application/json",
            "accept": "*/*",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://civitai.com/",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7"
        },
        "ITEM_PIPELINES": {
            'Pixiv.pipelines.CivitaiModelPipeline':302,
            'Pixiv.pipelines.CivitaiPipeline': 300,
            "Pixiv.pipelines.CivitaiTextPipeline": 301,
        }
    }
    cookies = {
        '__Host-next-auth.csrf-token': 'f1825213cbcfccbcc754a76c2586c8892f437e95cc8cd00622a2a52bb6929aae%7Ce451878ec2460481777c0985b73e2e036b3db2199c48137de05bf875866e0da0',
        '__stripe_mid': 'aa8a0aab-be49-4afe-b671-a50c536e193723ef91',
        '__Secure-next-auth.callback-url': 'https%3A%2F%2Fcivitai.com%2Fmodels%2F6424%2Fchilloutmix',
        'f_types': '%5B%22LORA%22%5D',
        '__stripe_sid': 'd1948c75-34ef-49da-8297-044e807bdf32a998ca',
        '__Secure-civitai-token': 'eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..bK7Kn6tzTyKgh0Ot.hd6UIoiOmsBPlZeBMdGz-nK_KfgmvCgNrtbdb41VqwrFHtT9SDsL_iJRKBwipqVh6t3MJyKNgDcmANru3qg83qY09zuzAG6tJXskU3I9IfX9LcV7U_Um9MpZSGFVLELxA3fiuoistoUa_KxQtGYMsCA76Z2dR19dDQSCJPL6XUntM7j8-N-1EuJ-DrQ6a35DeuUKm_m9yfZmm3TzU_v6JD28PXGwKSqdR1qcPoc0-W8l5cBCrVeyr7Xl4dhEhI9oHu9g3do-8d2PRfAuugLFde4lhxmZO-g9dc3UunK5g6Qk2ghGqoyGks5ljNjOlaa_LODeYBPE0D8MtNltz__paQKkTrezrO5NQjPgpAy8pPGkfy4fMU78Gcurj1-sFQTXz28g8xTucdSlk8JsxBD3RzD2R4XnDIWdFGpyAA_1qnF8foqHjE__smYUCtqBNKxiWaw39jTQUBuA8UYjVCWcgjVTUzn9kGK7RH4BHxYhHlJOmAkq1Pj70Zqc3nSsrCJJkzeWomdZhYMpn080Jt2HX2ytpJUBHdijDdf2S4Z4HLRdnw23YiuKMH-WrwGGuFrJPr4nfmgqT6KRURrgS1bp9B7I92YEdiB3wCc0muNAypF_hMU5czUbI1pTHk30d0SZ_Kd09ttIDwkSlpI01g_Z4H6Wu0EujRCRrbrdgycA6-219QC6ZZT3s20PX5vBh1sDtTFX1vrAr8chsttERLsRtJ8CqNfqAUwktwvoeyk9B4ZixnpJcDhGANHXRTxxkGwFe3LQmAUBx2k_oiefhXTgNJsfNzXRoEJVNIdQGhQhblY-lOLo--sUFLd8AEpo4dhtwZ1fci1IA4PUIcyigVtDGZake53sP3r_uchoML6ZiWzp6pfWzlC2QTB1RsL_DljYrtTfmwDJt4i_p7tuKSDpiYnjKsHwMqODD73LQ3-FbWxkH4iVAve-xrs_awG1njFmvCYMedF-pHI1E7HdAOWomHoGGAqiqJkH5irUjrYJVKTmc6Ib3iFntkRe-S5iNL14nI2JrZ0sSoKl27hJtYjJ6puA5SpHe3A.Y7AmT5yhhJoOC7cRLe5CFw',
    }
    result = open("f.js", "r").read()
    f = execjs.compile(result)

    def start_requests(self):
        urls = "https://civitai.com/api/trpc/image.getInfinite"
        params = {
            "input": "{\"json\":{\"period\":\"AllTime\",\"sort\":\"Most Reactions\",\"cursor\":null},\"meta\":{\"values\":{\"cursor\":[\"undefined\"]}}}",
        }
        url = f'{urls}?{urlencode(params)}'
        yield scrapy.Request(url=url, cookies=self.cookies, callback=self.parse, dont_filter=True)

    def parse(self, response, **kwargs):
        try:
            datas = useAdDict(response.json())
        except Exception as e:
            yield response.request
            raise scrapy.exceptions.IgnoreRequest("没有返回数据，重试请求")
        nextCursor = datas.result.data.json.nextCursor
        if nextCursor:
            urls = "https://civitai.com/api/trpc/image.getInfinite"
            params = {
                "input": "{\"json\":{\"period\":\"AllTime\",\"sort\":\"Most Reactions\",\"cursor\":\"%s\"},\"meta\":{\"values\":{\"cursor\":[\"bigint\"]}}}" % nextCursor,
            }
            url = f'{urls}?{urlencode(params)}'
            yield scrapy.Request(url=url, cookies=self.cookies, callback=self.parse, dont_filter=True)
        items = datas.result.data.json
        items = dict(items).get("items")
        for data in items:
            if data.nsfw != True:
                ids = data.id
                url = data.url
                urls = f"https://imagecache.civitai.com/xG1nkqKTMzGDvpLrqFT7WA/{url}/width=450/{ids}.jpeg"
                item = ItemLoader(item=PixivItem(), response=response)
                item.add_value("title", "civitai")
                item.add_value("filename", ids)
                item.add_value("file_urls", urls)
                stats = data.stats
                yield item.load_item()
                yield scrapy.Request(url=f"https://civitai.com/images/{ids}", callback=self.parse_text,
                                     dont_filter=True, meta={"ids": ids, "stats": stats})
                # break

    def parse_text(self, response, **kwargs):
        item = ItemLoader(item=PixivItem(), response=response)
        meta = useAdDict(response.meta)
        ids = meta.ids
        datas = response.xpath("//script[@id='__NEXT_DATA__']//text()").get()
        data = useAdDict(json.loads(datas))
        e = data.props.pageProps.trpcState.json.queries[0].state.data
        if e:
            e = e.meta
            try:
                text = self.f.call("$", e)
                item.add_value("title", "civitai")
                item.add_value("filename", ids)
                item.add_value("text", text)
                # yield item.load_item()
            except execjs._exceptions.ProgramError as e:
                logger.error(f"id: {ids}没有prompt")
        urls = "https://civitai.com/api/trpc/tag.getVotableTags,commentv2.getInfinite,commentv2.getCount,commentv2.getThreadDetails,image.getResources,user.getEngagedModels"
        params = {
            "batch": "1",
            "input": "{\"0\":{\"json\":{\"id\":%s,\"type\":\"image\",\"authed\":true}},\"1\":{\"json\":{\"entityId\":%s,\"entityType\":\"image\",\"limit\":3,\"cursor\":null,\"authed\":true},\"meta\":{\"values\":{\"cursor\":[\"undefined\"]}}},\"2\":{\"json\":{\"entityId\":%s,\"entityType\":\"image\",\"authed\":true}},\"3\":{\"json\":{\"entityId\":%s,\"entityType\":\"image\",\"authed\":true}},\"4\":{\"json\":{\"id\":%s,\"authed\":true}},\"5\":{\"json\":null,\"meta\":{\"values\":[\"undefined\"]}}}" % (
                ids, ids, ids, ids, ids)
        }
        url = f'{urls}?{urlencode(params)}'
        yield scrapy.Request(url, callback=self.parse_model, dont_filter=True, meta=response.meta)

    def parse_model(self, response, **kwargs):
        item = ItemLoader(item=PixivItem(), response=response)
        meta = useAdDict(response.meta)
        datas = useAdDict(response.json()[4])
        data = datas.result.data.json[0]
        stats = meta.stats
        item_model = {
            "image_id": meta.ids,
            "iamge_url": f"https://civitai.com/images/{meta.ids}",
            "cryCountAllTime": stats.cryCountAllTime,
            "laughCountAllTime": stats.laughCountAllTime,
            "likeCountAllTime": stats.likeCountAllTime,
            "dislikeCountAllTime": stats.dislikeCountAllTime,
            "heartCountAllTime": stats.heartCountAllTime,
            "commentCountAllTime": stats.commentCountAllTime,
            "modelId":data.modelId,
            "modelUrl":f"https://civitai.com/models/{data.modelId}",
            "modelName":data.modelName,
            "modelRating":data.modelRating,
            "modelRatingCount":data.modelRatingCount,
            "modelDownloadCount":data.modelDownloadCount,
            "modelCommentCount":data.modelCommentCount,
            "modelFavoriteCount":data.modelFavoriteCount,
            "modelType":data.modelType,
        }
        item.add_value("model_data",item_model)
        yield item.load_item()
