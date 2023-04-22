# from scrapy.dupefilters import RFPDupeFilter

from scrapy_redis.dupefilter import RFPDupeFilter


class RFPDupeFilter(RFPDupeFilter):
    def request_seen(self, request):
        return False
