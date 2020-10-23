import requests
import urllib
import os
import sys
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.item import Item
try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup




class RowItem(Item):
    id = scrapy.Field()
    name = scrapy.Field()
    row = scrapy.Field()



class NocSpider(scrapy.Spider):
    name = "brickest_spider"
    start_urls = ["http://noc.esdc.gc.ca/English/NOC/QuickSearch.aspx?ver=16&val65=*"]

    def parse(self, response):
        """ Main function that parses downloaded pages """
        yield response.follow(self.start_urls[0], callback=self.parse_title)

        a_selectors = \
            response.xpath(
                "//*[@id=\"wb-cont\"]/ul/li/a"
            )
        # Loop on each tag
        for selector in a_selectors:
            link = selector.xpath("@href").get()
            request = response.follow("https://noc.esdc.gc.ca/English/NOC/"+link, callback=self.parse_title)
            yield request

    @staticmethod
    def parse_title(response):
        # row_selectors = \
        #     response.xpath(
        #         "//*[@id=\"wb-cont\"]/ul[@style='list-style-type: disc']"
        #     )
        row_selectors = \
            response.xpath(
                 "//*[@id=\"wb-cont\"]").css("ul[style='list-style-type: disc']")
        title_selectors = \
            response.xpath(
                "//*[@id=\"wb-cont\"]/h4"
            )

        title_selectors_h5 = \
            response.xpath(
                "//*[@id=\"wb-cont\"]/h5"
            )
        if title_selectors_h5:
            title_selectors = title_selectors_h5

        id_selectors =  \
            response.xpath(
                "//*[@id=\"mh1\"][@property=\"name\"]"
            )

        if id_selectors:
            id = id_selectors.xpath("text()").get().split()[0]
            name = ' '.join(id_selectors.xpath("text()").get().split()[1:])
        else:
            return


        titles = ['']
        if title_selectors:
            for selector in title_selectors:
                text = selector.xpath("text()").get()
                if 'duties:' not in text:
                    titles.append(text)
            if len(titles)>1:
                titles.remove('')

        for titles_rows_selector in zip(titles, row_selectors):
            item = RowItem()
            item['id'] = id
            item['name'] = name+': '+titles_rows_selector[0] if name else titles_rows_selector[0]
            item['row'] = '. '.join(titles_rows_selector[1].xpath('li/text()').getall())
            yield item


def main():
    if os.path.exists('NOC_jd.json'):
        os.remove('NOC_jd.json')
        print('Old NOC_jd.json removed')
    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'json',
        'FEED_URI': 'NOC_jd.json',
        'FEED_EXPORT_ENCODING': 'utf-8'
    })
    process.crawl(NocSpider)
    process.start() # the script will block here until the crawling is finished


if __name__ == '__main__':
    main()
