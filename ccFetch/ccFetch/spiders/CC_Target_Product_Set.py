# -*- coding: utf-8 -*-

"""KFM Created on Jan 10 2023

This is a base Crawl Spider built on Scrapy Framework 
to search the Common Crawl Indexes over a period of time
to find all products for a given site_id (Merchant base URL) and build a
extract index for a given product set ...

This is First of Three step pipeline to extract all product data 
from Common Crawl for a given Site_id.
    1. CC_Target_Product_Set     - (this) Produces the target URL for site ID
    2. CC_Target_Product_IDX     - Produces a Target CC Index to extract target URL (products)
    3. CC_Target_Product_Extract - Extracts the target URL (products) from the Common Crawl

Processing Details:  See class definition for inputs, outputs and processing algo.

This part of the processing takes the latest Price Update and Product Export to produce a 
TARGET SET of URLS that we want to extract from the Common Crawl>

@author: KFM
"""


import os, sys, json
import argparse
from timeit import default_timer as timer
import SRP_Config  as cfg
import SRP_Utils  as utl


class CC_Target_Product_Set():
    ''' Class outputs a target set of URLs used to target Product Extracts from Common Crawl.

    Params: 
        Site_id:  the Merchant_Site_ID used to identify this site.
        
    Inputs:
        RPG_Site_Products:  A list (dict) of of URLs that point to product (detail) pages 
        that are currently held in RPG.  This is the exclusion set.

        Site_Price_updates: A list of product price_updates from the latest crawl of a site.
        This is the current state of products at Site_ID.

    Output FEED: CC_Target_Product_Set: TPS|{job_id}|Site_id}.json
        File of JSON Lines. Each line is a single URL that we eant to extract from CC.

    Process Algo:
        Read Latesst Set of URLS for Site ID Exported from RPG.
        For site_url in Latest Site_id Price_Update:
            if site_url not in RPG_URLS:
                Append site_url to CC_Target_Product_Set (Target Output)
    '''

    def __init__(self, site_id, overwrite=False):
        # Initializing all generic variables
        if 'www' in site_id: 
            self.site_id        = site_id.replace('www', '')
            self.www_site_id    = site_id
        else: 
            self.site_id        = site_id
            self.www_site_id    = site_id.replace('--', '-www-')
        self.job_id             = JOB_ID
        self._exclude_urls      = {}        # The set of URLS that we do not want to target
        
        # Source of RPG URLS to Exclude
        self._RPG_urls_fPath       = utl.get_fPath_for_id(cfg.RPG_SITE_PRODUCT_URLS, f"{self.site_id}.json")  # source path to exclusion urls
        if not self._RPG_urls_fPath: 
            self._RPG_urls_fPath = f"{cfg.RPG_SITE_PRODUCT_URLS}/SPE|{self.site_id}.json"
        
        self._source_SPU        = utl.get_fPath_for_id(cfg.SRP_SITE_PRICE_UPDATES, f"{self.site_id}.json")  # path used in crawler settings.
        self._target_fPath      = f"{cfg.CC_TARGET_PRODUCT_SET}/TPS|{self.job_id}|{self.site_id}.json"        # Target Output fPath for Site IDX Files.

        # Processing
        if overwrite or not os.path.isfile(self._target_fPath):
            self._get_exlusion_urls(overwrite)   # load dictionary of URLs from RPG for Site_ID
            self._export_target_cc_urls()        # export target urls to file 
        return

    def _get_exlusion_urls(self, overwrite=False):
        ''' Returns a Set of URLS that are to be Excluded from the Search. 
    
        A set of URLs last exported from RPG that we already have data for.
        This set will be excluded from the Search/Extract.
        
        If the set has been produced previously, it will use that.
        If the set does not exist, it will be created and saved for futures use.
        
        A file for the given Site_Id will produced as output.'''

        # If source urls to exclude already exists, load it
        if not overwrite and os.path.isfile(self._RPG_urls_fPath):
            self._exclude_urls  = utl.get_dict_list_from_json_file(self._RPG_urls_fPath, 'url')
            return

        # If target does not exist, create it
        # We need to find the latest product export 
        # and use this to create the extract of URLs for given Site_ID.
        elif not os.path.isfile(self._source_URLS) or overwrite:
            i = 0
            found = False
            export_path = utl.get_last_export_lable()
            rpg_export = f"{export_path}/products_export.txt"
            # Extracts the URLs from RPG for given Site ID.
            # Writes URLS to RPG_SITE_PRODUCT_URLS
            with open(rpg_export) as f:
                with open(self._RPG_urls_fPath, 'w') as fo:
                    for line in f:
                        k, v = json.loads(line)
                        merchant_id = k.split("/")[0].replace("www", "")
                        if merchant_id == self.site_id:
                            found = True
                            i += 1
                            line = json.dumps({'url': v['url']}) 
                            fo.write(line+"\n") 
                            self._exclude_urls[v['url']] = {'url': v['url']}  # add to dict
                        elif found and merchant_id != self.site_id: 
                            print(f"SITE_ID:{self.site_id}, Total Products Indexed: {i}")
                            break

            if found: 
                print(f"SITE_ID:{self.site_id}, Total Products Indexed: {i}")
        return 

    def _export_target_cc_urls(self):
        ''' Exports a JSON file of Target URLS that we want to get from CC. '''

        price_updates = utl.get_json_generator_from_file(self._source_SPU)
        i = 0
        p = 0

        with open(self._target_fPath, 'w') as fo:
            for pr in price_updates:
                i += 1
                # another hack to fix www
                url = pr['url'].replace("//", "//www.")
                if url not in self._exclude_urls:
                    p += 1
                    line = json.dumps({'url': url}) 
                    fo.write(line+"\n") 

        if i and p: 
            print(f"SITE ID:             {self.site_id}")
            print(f"Total Price Updates: {i}")
            print(f"Total CC Targets:    {p}")

        return 


def initialize(site_id):
    print(f"******************************** RUN JOB **********************************************")
    print(f"********* JOB_ID    : {JOB_ID} ")
    print(f"********* SITE_ID   : {args.site_id} ")
    print(f"********* LOG_ID    : {LOG_ID} ")
    print(f"***************************************************************************************")
    startTime = timer()


    # the job will block here until the crawling is finished
    CC_Target_Product_Set(site_id, overwrite=False)

    tMins = round(timer() - startTime)/60
    print(f"******************* TOTAL Time {tMins} Mins")

    return 

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Common Crawl Target Product Extractor")
    parser.add_argument('site_id',  type=str, help='Require: Site Id (or Merchant_ID) is required to search the Common Crawl')
    parser.add_argument('job_id', type=str, help='Optional: Job Id to lable pipeline outputs')
    args = parser.parse_args()

    # JOB CONTROL
    JOB_ID      = args.job_id
    LOG_ID    = f'{cfg.CC_TARGET_PRODUCT_SET}/TPS|{JOB_ID}.log'

    
    # RUN JOB 
    initialize(args.site_id)  


    

