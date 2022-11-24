import scrapy
from scrapy.spidermiddlewares.httperror import HttpError

# script to check URL from URN
#
# - prints the output to the console
# - use '--logfile spider.log' to write log output to file
# 
# run:
#    scrapy runspider urnChecker.py  --logfile spider.log

class BlogSpider(scrapy.Spider):
    name = 'urnChecker'

    def start_requests(self):
        filename = "urnFileFromDNB.csv" # URN / URL list from DNB
        # Layout:
        # URN;URL;URN_ID
        with open(filename, "r") as fd:
            lines = fd.read().splitlines()
            for line in lines:
                if line.startswith('urn:'): # for preventing header
                    urn, url, urn_id = line.split(';')
                    # generator for calling urls
                    # passing urn as argument to use it in callback functions
                    yield scrapy.Request(url=url, cb_kwargs=dict(urn=urn),
                        callback=self.parse, # 200 OK
                        errback=self.error_parse, # any other statuscode
                        dont_filter=True)

    def parse(self, response, urn):
        url=response.url
        # check for soft404 
        #print(urn, url, 'URL works -> ',response.status)

    def error_parse(self, failure):
        urn = failure.request.cb_kwargs['urn']
        url = failure.request.url
        if failure.check(HttpError):
            response = failure.value.response
            print(urn, url,"HttpError", response.status)
        elif failure.check(DNSLookupError):
            print(urn+';'+url+';DNSLookupError')

        elif failure.check(TimeoutError, TCPTimedOutError):
            print(urn+';'+url+';DNSLookupError')