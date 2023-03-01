# -*- coding: utf-8 -*-
""" KFM - Created on Jan 10 2023

This is a base Crawl Spider built on Scrapy Framework 
to search the Common Crawl Indexes over a period of time
to find all products for a given site_id (Merchant base URL) and build a
extract index for a given set..

This is second of three step pipeline to extract all product data for a given site_id.
    1. CC_Target_Product_Set        - Produces the target URL for site ID
    2. CC_Target_Product_IDX     - (this) Produces a Target CC Index to extract target URL (products)
    3. CC_Target_Product_Extract - Extracts the target URL (products) from the Common Crawl

Processing Details:  See class definition for inputs, outputs and processing algo.

This crawler takes as input a set of target URLs for Site_ID.  This is used to eliminate
duplicate extracts of same product data.

This crawler produces an Index of Common Crawl Files/Offsets that can be used to extract
the target URL set for Site ID.

@author: KFM
"""

import os, sys
import argparse
import json, requests, sys, gzip, io, time
# from datetime import datetime, timezone
from timeit import default_timer as timer

import gzip
from io import StringIO, BytesIO
from scrapy.http import HtmlResponse
import scrapy, json, requests, sys, gzip, io, time
from scrapy.spiders import CrawlSpider
from scrapy.utils.project import get_project_settings
from scrapy.statscollectors import StatsCollector
from scrapy.crawler import CrawlerProcess
from scrapy.loader import ItemLoader

import SRP_Config  as cfg
import SRP_Utils  as utl
from ccFetch.items import CC_IDX_RECORD
from cc_index import CDX   # An input file of all CC-CDX Records in JSON format.

# JOB_ID    = utl.get_utc_timeString(micro=False)

class CC_CrawlSpider_Product_IDX(scrapy.Spider):
    ''' Searches the Common Crawl Index for all products with Site_id.
    Params: 
        site_ID: The site to search for.
    THe search will go back over past two years of the index unless 
    The search will only add the most recent unique record of the product.

    Params: 
        Site_id:    the Merchant_Site_ID used to identify this site.  
                    Products for this site will be searched.

    Inputs:     
        CC_CDX JSON Records - Record for each index that goes back to 2012
        {
          "id": "CC-MAIN-2022-49",
          "name": "November/December 2022 Index",
          "timegate": "https://index.commoncrawl.org/CC-MAIN-2022-49/",
          "cdx-api": "https://index.commoncrawl.org/CC-MAIN-2022-49-index"
        },

        Source TPS:  path/CC_TARGET_PRODUCT_SET/TPS_{site_ID}.json - provides 
        a set of URLs that used as to target the search of common crawl to extract 
        only these products.
    
    Output FEED: 
        path/CC_TARGET_PRODUCT_CC_IDX/CC_IDX_{Site_ID}.json

    Process Algo:
        Load target_urls into dict
        For each cdx index in common crawl:
            Search each of these for all product URLs
                Process each result to build IDX Records that match the target URL set.
                Export each IDX Record to Feed Exporter.

    '''
    name = 'crawl_cc_cdx' 

    custom_settings = {
    'FEEDS': {
        '%(_target_fPath)s': {
            'format': 'jsonlines',
            'encoding': 'utf8',
            'store_empty': False,
            'item_classes': [CC_IDX_RECORD],
            'fields': ['cc_idx_record'],
            'indent': 4,
            'overwrite': True,
            'item_export_kwargs': {
                'export_empty_fields': False,
            }
        }
    },  
    'LOG_FILE': '%(log_id)s',  
    'LOG_FILE_APPEND': True,  
    'LOG_ENABLED': True,  
    'LOG_LEVEL': 'INFO',  
}

    def __init__(self, site_id, **kwargs):
        self.job_id             = JOB_ID
        self.log_id             = LOG_ID
        self.site_id            = site_id
        self.record_list        = []
        self.idx_records        = {}      # Unique Set of records for the site
        self.items              = 0
        self._source_fPath      = utl.get_fPath_for_id(cfg.CC_TARGET_PRODUCT_SET, f"{self.site_id}.json")                   # path used in crawler settings.
        self._target_fPath      = f"{cfg.CC_TARGET_PRODUCT_IDX}/IDX|{self.job_id}|{self.site_id}.json"       # path used in crawler settings.
        id                      = site_id.split("-")
        self.site_url           = f"www.{id[0]}.{id[2]}/product/*"                                          # /* will get all pages under path.  TODO: This path will be unique to each site. Need to track this with Site_id.
        self.target_set         = utl.get_dict_list_from_json_file(self._source_fPath, key='url')           # Dict of URLs that define that target set of URLs to build CC IDX records for (the final output).
        
        # Process
        self.initialize_cc_cdx()
        super().__init__(**kwargs)
        return

    def initialize_cc_cdx(self):
        ''' Loads the CDXs from CC that will be searched for Site ID.'''
        self.CDX        = []
        idx_years       = ["2022", "2021"]  # TODO determine how far back in into the index we need to go for a given site.  CC Crawls sites broadly, not deep.  So not all products are in single crawl.
        
        for yr in idx_years:
            for cdx in CDX:
                if yr in cdx['name']: self.CDX.append(cdx['cdx-api'])

        print("Initializing Common Crawl Searches for:")
        for cdx in self.CDX: print(f"    >> {cdx} ")

        return

    def start_requests(self):
        ''' Initiates Scrapy Requests across the set of CDXs requested to search.
        This first request determines the number of page search requests that will be required
        to satisfy the search on this CDX.
        Response from this request returns the number opf pages to process.  The response is passed to 
        to call back to make the actual search requests for each page to be processed.'''
        # Iterate over CDX to get pages to be requested
        for cdx in self.CDX:
            idx_page_count_url  = f"{cdx}?url={self.site_url}&showNumPages=true"
            yield scrapy.Request(idx_page_count_url, callback=self.process_page_requests, cb_kwargs={'cdx': cdx}, dont_filter = True)
        return

    def process_page_requests(self, response, cdx):
        ''' Process the responses from each CDX search request.  Response may be multiple pages long.
        First request (start requests) determines the number of pages to process, 
        this method makes the second set of requests per CDX to gether all results for this CDX.
        Page Response are then passed for parsing the results.'''

        if response.status == 200:
            page_count_resp = json.loads(response.text)
            total_pages = int(page_count_resp['pages'])
            if total_pages > 1: print(f"Total SRPs to Process: {total_pages}")

            # Iterate over number of pages
            for page in range(0, total_pages):
                cc_url = f'{cdx}?url={self.site_url}&page={page}&output=json'
                print(f"REQUESTED {cc_url}")
                yield scrapy.Request(cc_url, callback=self.parse_cc_idx_responses, dont_filter = True)
        return

    def parse_cc_idx_responses(self, response):
        ''' Searches the Common Crawl Index for all products in the Site_id.
        THe search will go back over past two years of the index.
        The search will only add the most recent unique record of the product.'''

        if response.status == 200:
            records = response.body.splitlines()
            print(f">>>> PROCESSING IDX RESPONSES: {len(records)} FROM: {response}")
            for record in records:
                jd = json.loads(record.decode())
                target_found = self.target_set.get(jd['url'], False)
                if target_found: 
                    isIndexed = target_found.get('isIndexed', False)
                    if not isIndexed:
                        target_found['isIndexed'] = True 
                        item = ItemLoader(item = CC_IDX_RECORD())
                        item.add_value("cc_idx_record", jd)
                        yield item.load_item()
  
        return 

def initialize(site_id):
    print(f"******************************** RUN JOB **********************************************")
    print(f"********* JOB_ID    : {JOB_ID} ")
    print(f"********* SITE_ID   : {args.site_id} ")
    print(f"********* LOG_ID    : {LOG_ID} ")
    print(f"***************************************************************************************")
    startTime = timer()

    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(CC_CrawlSpider_Product_IDX, site_id)

    # the job will block here until the crawling is finished
    # process.start()         

    tMins = round(timer() - startTime)/60
    print(f"******************* TOTAL Time {tMins} Mins")

    return 


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Common Crawl Target Product Extractor")
    parser.add_argument('site_id',  type=str, help='Require: Site Id (or Merchant_ID) is required to search the Common Crawl')
    parser.add_argument('job_id', type=str, help='Optional: Job Id to lable pipeline outputs')
    args = parser.parse_args()

    # JOB CONTROL
    JOB_ID    = args.job_id
    LOG_ID    = f'{cfg.CC_TARGET_PRODUCT_IDX}/IDX|{JOB_ID}.log'
    
    # RUN JOB 
    initialize(args.site_id)  

