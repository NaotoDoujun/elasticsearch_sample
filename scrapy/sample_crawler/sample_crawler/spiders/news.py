import scrapy
import base64
from scrapy_splash import SplashRequest
from sample_crawler.items import Headline

#
# parse rule is for May 19th 2022 YahooJP News
#
class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['news.yahoo.co.jp']
    start_urls = ['http://news.yahoo.co.jp/']

    def start_requests(self):
        yield SplashRequest(self.start_urls[0], self.parse, 
            args={
                'wait': 0.5,
            }
        )

    def parse(self, response):
        for url in response.css('section.topics a::attr("href")').re(r'/pickup/\d+$'):
            abs_url = response.urljoin(url)
            yield scrapy.Request(abs_url, self.parse_topics, 
                meta={
                    'splash': {
                        'args': {
                            'html': 1,
                            'png': 1,
                            'wait': 0.5,
                        },
                    }
                }
            )

    def parse_topics(self, response):
        item = Headline()
        item['title'] = response.css('article a>p::text').extract_first().replace('\u3000', '')
        item['text'] = response.css('p.highLightSearchTarget::text').extract_first().replace('\u3000', '')
        item['url'] = response.url
        item['screenshot'] = response.data['png']
        item['time'] = response.css('time::text').extract_first()
        yield item
