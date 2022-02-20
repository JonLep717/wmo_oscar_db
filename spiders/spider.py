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
    
    custom_settings = {
        "FEEDS": {"output.csv":{"format":"csv"}},
    }

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
        base_url_displaystart = "https://space.oscar.wmo.int/requirements?themes=&applicationareas=&layers=&requirementcoverages=&iDisplayStart="
        base_url_draw = "&iDisplayLength=50&iSortCol_0=1&sSortDir_0=asc&draw="
        draw = 0
        for x in range(0,751,50):
            url = base_url_displaystart+str(x)+base_url_draw+str(draw)
            request = scrapy.Request(url, callback=self.parse_api, headers=self.headers)
            yield request
        
    def parse_api(self,response):
        raw_data = response.body    ##Returns string
        data = json.loads(raw_data) ##JSON object
        reqs = {}
        for dat in data['aaData']:
            result_reqid = re.search('>(.*)<',dat[0])
            result_reqname = re.search('>(.*)<', dat[1])
            result_reqid = result_reqid.group(1)
            result_reqname = result_reqname.group(1)
            reqs['Id'] = result_reqid
            reqs['Requirement'] = result_reqname
            yield reqs
        
        
        
