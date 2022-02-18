# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 22:26:46 2022

@author: jonat
"""
import scrapy
from scrapy.crawler import CrawlerProcess
import json
from scrapy.selector import Selector
import re

class OSCARSpider(scrapy.Spider):
    name = "wmo_oscar"
    start_urls = ['https://space.oscar.wmo.int/requirements']
    

    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "referer": "https://space.oscar.wmo.int/requirements",
        "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"98\", \"Google Chrome\";v=\"98\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
        }
    
    def parse(self, response):
        url = "https://space.oscar.wmo.int/requirements?themes=&applicationareas=&layers=&requirementcoverages=&iDisplayStart=0&iDisplayLength=50&iSortCol_0=1&sSortDir_0=asc&draw=0"
        
        request = scrapy.Request(url, callback=self.parse_api, headers=self.headers)
        
        yield request
        
    def parse_api(self,response):
        raw_data = response.body    ##Returns string
        data = json.loads(raw_data) ##JSON object
        for dat in data['aaData']:
            result = re.search('>(.*)<', dat[1])
            print(result.group(1))
            print("\n")
        yield data
        
        
        
