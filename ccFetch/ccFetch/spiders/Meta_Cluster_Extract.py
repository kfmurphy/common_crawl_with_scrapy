# -*- coding: utf-8 -*-
""" KFM REUSED CODE
Reused on Mon Feb 19, 2023
 Based on CC_Target_Product_IDX.py

    ''' A Crawl-Spider to get a a clusters meta data for product brand, name, description, offers present.

    The input to the process is dict of Cluster_IDs and a set of URLs to try to get meta data from.
     We only need to get one set of meta data and move on to the next Cluster Id.
      
    The output will be a list of Cluster-ID, JSON-LD Objects for the update.

    Params: 
        meta_urls:  The list of urls to target for each cluster_id we want meta data for.

    Output FEED: 'MC_META_DATA/(job_id)|(site_id).products.json'
        File of JSON Lines (one per page where JSON-LD is extacted.)
    '''

@author: KFM
"""
# import importlib
# importlib.reload(common_utilities) as utl

# import A9 Configs, Common and Job Control
import MCE_Config as cfg
import io_wrapper as iow
import job_control as jc

# mods = dir(jc)
# print(mods)

# import SRP_Utils  as utl

import os, sys
import argparse
import scrapy
import json, requests, sys, gzip, io, time
from scrapy.http import HtmlResponse
from scrapy.spiders import CrawlSpider
from scrapy.utils.project import get_project_settings
from scrapy.statscollectors import StatsCollector
from scrapy.crawler import CrawlerProcess
from scrapy.loader import ItemLoader
from scrapy import signals
from timeit import default_timer as timer
from datetime import datetime, timezone
from tqdm import tqdm

from ccFetch.items import CC_Meta_Cluster_JSON_LD    # Needs paths to find modules

LOG_ID = f"{cfg.RPC_MCE_LOG_FILE}.{datetime.now(timezone.utc)}"

class CC_CrawlSpider_Product_Extractor(scrapy.Spider):
    ''' A Crawl-Spider to get a a clusters meta data for product brand, name, description, offers present.

    The input to the process is dict of Cluster_IDs and a set of URLs to try to get meta data from.
     We only need to get one set of meta data and move on to the next Cluster Id.
      
    The output will be a list of Cluster-ID, JSON-LD Objects for the update.

    Params: 
        meta_urls:  The list of urls to target for each cluster_id we want meta data for.

    Output FEED: 'MC_META_DATA/(job_id)|(site_id).products.json'
        File of JSON Lines (one per page where JSON-LD is extacted.)
    '''
    name = 'cc_product_extract'
    # name = 'mce_extract'

    custom_settings = {
    'FEEDS': {
        '%(feed_fPath)s': {
            'format': 'jsonlines',
            'encoding': 'utf8',
            'store_empty': False,
            'item_classes': [CC_Meta_Cluster_JSON_LD],
            'fields': ['cluster_id', 'json_ld'],
            'indent': 4,
            'overwrite': True,
            'item_export_kwargs': {
                'export_empty_fields': False,
            }
        }
    },
    'DOWNLOAD_DELAY': 0.5,
    'CONCURRENT_REQUESTS': 2,
    'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
    'CONCURRENT_REQUESTS_PER_IP': 2,
    'AUTOTHROTTLE_ENABLED': True,
    'AUTOTHROTTLE_START_DELAY': 2,
    'AUTOTHROTTLE_MAX_DELAY': 60,
    'AUTOTHROTTLE_TARGET_CONCURRENCY': 1.0,
    'AUTOTHROTTLE_DEBUG': False,
    'DEFAULT_REQUEST_HEADERS': cfg.RPC_REQUEST_HEADERS,
    'LOG_FILE': LOG_ID,  
    'LOG_FILE_APPEND': False,  
    'LOG_ENABLED': True,  
    'LOG_LEVEL': 'INFO',  
    }

    def __init__(self,  **kwargs):
        # Initializing all generic variables
        self.site_id            = "mce_extract"
        self.job_id             = kwargs['job_id']
        self.node_id            = kwargs['node_id']
        self.startTime          = timer()
        
        # Get the Job Details from Control
        self.job                = jc.Job(self.job_id, self.node_id)
        self.job_prefix         = f"{self.job_id}_{self.node_id}"
        self.feed_fPath         = f"{cfg.MCE_FOLDER}/{self.job_prefix}_{cfg.RPC_MCE_FEED_PATH}"
        
        # Prepare the job
        self.pre_process()
        super().__init__(**kwargs)
        return

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        """Registers the spider_closed signal handler to do post processing."""
        spider = super(CC_CrawlSpider_Product_Extractor, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.post_process, signal=signals.spider_closed)
        return spider  
    	
    def start_requests(self):
        ''' This is the main handler for the Job.
         
        It will issues the initial set of Meta Requests for the Clusters specified in the Job...
        Each cluster will have between 1 and 3 URLs to try to get meta data from.
           
        For clusters, that fail on their first request, the will be added to a retry queue and 
        retried after the initial set of requests have been processed.  '''

        self.retry_queue = {}
        self.clusters_failed = {}
        self.clusters_complete = {}
        t = 0

        # Process the requested clusters
        for k, urls in tqdm(list(self.clusters.items())):        
            if urls:
                yield scrapy.Request(urls[0], callback=self.process_page_response, cb_kwargs={'cluster_id': k, 'retry': 0}, dont_filter = True)
                self.logger.debug(f"################## ISSUED ({t}): ### CLUSTER {k} #################")
                t += 1

        self.logger.info(f"################## CLUSTERS EXHAUSTED #################")
        return
                
    def process_page_response(self, response, cluster_id, retry):
        """    
        #   Get and page for urls and processes the response.

        # Params: 
        #   1. response - scrapy Request's response
        # Yields: JSON Items that will be sent to Feed Export file.

        """
        if response.status != 200: 
            self.logger.warning(f"################## ERROR: {response.status} ### CLUSTER {cluster_id} #################")
            urls = self.clusters[cluster_id]

            # if retries are exhausted, add to failed clusters and remove from retry queue
            # this code block will not run in a method for some reason the way scrapy works
            retry += 1
            if retry == len(urls):
                self.clusters_failed[cluster_id] = 1
            else: # Try the next url in the list
                yield scrapy.Request(urls[retry], callback=self.process_page_response, cb_kwargs={'cluster_id': cluster_id, 'retry': retry}, dont_filter = True)
                self.logger.debug(f"################## CLUSTER {cluster_id}: RETRY({retry} of {len(urls)}) ##################")

        if response.status == 200:
            jld = self.extract_json_ld(response, cluster_id)
            if jld:
                item = ItemLoader(item = CC_Meta_Cluster_JSON_LD())
                item.add_value("cluster_id", cluster_id)
                item.add_value("json_ld", jld)
                # add to clusters_complete
                self.clusters_complete[cluster_id] = 1
                self.logger.debug(f"################## COMPLETED CLUSTER {cluster_id}: RETRIES ({retry}) ##################")
                yield item.load_item()

            else: 
                # this code block will not run in a method for some reason the way scrapy works
                # if retries are exhausted, add to failed clusters and remove from retry queue
                urls = self.clusters[cluster_id]
                retry += 1
                if retry == len(urls):
                    self.clusters_failed[cluster_id] = 1
                    self.logger.debug(f"################## FAILED CLUSTER {cluster_id}: RETRIES ({retry}) ##################")
                else: # Try the next url in the list
                    self.logger.debug(f"################## CLUSTER {cluster_id}: RETRY({retry} of {len(urls)}) ##################")
                    yield scrapy.Request(urls[retry], callback=self.process_page_response, cb_kwargs={'cluster_id': cluster_id, 'retry': retry}, dont_filter = True)

            
    def extract_json_ld(self, response, cluster_id):
        ''' Extract JSON-LD Product Dict from the single HTML page.  
        Returns a dict of data related to the product 
        TODO: Check if we should return all or more than just the Product JSON-LD.
        '''
        try:

            jld = response.xpath('//script[@type="application/ld+json"]//text()').getall()

            for d in jld:
                jd = json.loads(d)
                if "@type" in jd and jd["@type"] == "Product" and "aggregateRating" not in jd:
                    return jd
        except Exception as e:
            self.logger.warning(f"################## BAD JSON-LD: {e} CLUSTER {cluster_id} #################")
        return None

    def pre_process(self):
        # Create the output folder if it does not exist
        print(f"******************************** RUN JOB **********************************************")
        print(f"********* JOB_ID            : {self.job_id} ")
        print(f"********* NODE_ID           : {self.node_id} ")
        print(f"********* CLUSTERS          : {self.job.job_kv['start']} - {self.job.job_kv['end']} ")
        print(f"********* CLUSTERS TOTAL    : {self.job.job_kv['end'] - self.job.job_kv['start']} ")
        print(f"***************************************************************************************")

        # Load the Clusters required for the job
        # self.clusters = iow.get_dict_json_kv(cfg.RPT_META_CLUSTER_URLS, self.job.job_kv['start'], self.job.job_kv['end'])
        self.clusters = iow.get_dict_json_kv(self.job.job_kv['clusters_requested'], self.job.job_kv['start'], self.job.job_kv['end'])

        return

    def post_process(self):

        if not os.path.exists(cfg.MCE_FOLDER):
            os.makedirs(cfg.MCE_FOLDER)

        # rename the logfile to include the job_prefix
        os.rename(LOG_ID, f"{cfg.MCE_FOLDER}/{self.job_prefix}.log")

        # Dump the completed and failed clusters to json files
        iow.dump_dict_json_kv(self.clusters_complete, f"{cfg.MCE_FOLDER}/{self.job_prefix}_{cfg.RPC_META_CLUSTER_COMPLETE_FNAME}")
        iow.dump_dict_json_kv(self.clusters_failed, f"{cfg.MCE_FOLDER}/{self.job_prefix}_{cfg.RPC_META_CLUSTER_FAILED_FNAME}")

        tMins = round(timer() - self.startTime)/60
        print(f"******************* TOTAL Time {tMins} Mins")

        print(f"\n################## JOB COMPLETE ###################################################")
        print(f"********* JOB_ID            : {self.job_id} ")
        print(f"********* NODE_ID           : {self.node_id} ")
        print(f"********* TOTAL CLUSTERS    : {len(self.clusters)}")
        print(f"********* SUCCESS           : {len(self.clusters_complete)} ")
        print(f"********* FAILED            : {len(self.clusters_failed)} ")
        print(f"********* TOTAL TIME        : {tMins:.2f} Mins")
        print(f"#####################################################################################\n\n")
        return
    

def combine_last_completed_clusters():
    # Load the meta_clusters_complete.json file
    # clusters_completed = iow.get_dict_list_from_json_file(cfg.RPC_META_CLUSTER_COMPLETE, key='cluster_id')
    clusters_completed = iow.get_dict_json_kv(cfg.RPC_META_CLUSTER_COMPLETE)
    
    fPath = "/Users/kelly/Data/CACHE/RPC/META_CLUSTER_EXTRACT/COMPLETE_585_|0_1000|_mce_extract.json"
    last_completed_clusters  = iow.get_dict_from_json_lines(fPath, key='cluster_id', key_only=True)

    # Combine the two dicts
    completed_clusters = {**clusters_completed, **last_completed_clusters}

    iow.dump_dict_json_kv(completed_clusters, cfg.RPC_META_CLUSTER_COMPLETE)


    return

def initialize(args):



    settings = get_project_settings()
    process = CrawlerProcess(settings)

    process.crawl(CC_CrawlSpider_Product_Extractor, job_id=args.job_id, node_id=args.node_id)

    # the job will block here until the crawling is finished
    process.start()         

    return 



if __name__ == '__main__':

    # combine_last_completed_clusters()

    parser = argparse.ArgumentParser(description="Meta Data Product Extractor")
    parser.add_argument('job_id',    type=str, help='Start cluster index to split jobs across nodes')
    parser.add_argument('node_id',   type=str, help='End cluster index to split jobs across nodes')
    args = parser.parse_args()

    # RUN JOB 
    initialize(args)  
    pass

