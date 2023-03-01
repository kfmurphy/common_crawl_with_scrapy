# -*- coding: utf-8 -*-

"""KFM Created on Jan 12 2023

This is a base Crawl Spider built on Scrapy Framework 
to search the Common Crawl Indexes over a period of time
to find all products for a given site_id (Merchant base URL) and build a
extract index for a given product set ...

This component (CC_Scheduler) will drive the following pipeline.
Three step pipeline to extract all product data 
from Common Crawl for a given Site_id.
    1. CC_Target_Product_Set     - (this) Produces the target URL for site ID
    2. CC_Target_Product_IDX     - Produces a Target CC Index to extract target URL (products)
    3. CC_Target_Product_Extract - Extracts the target URL (products) from the Common Crawl

Processing Details:  See class definition for inputs, outputs and processing algo.

The Scheduler is responsible to distribute jobs across a set of Processors that run 
the above pipeline.  It should be assumed that these jobs are distributed across many nodes in 
a cluster of containers.

Each container runs a single Processor_Node instance, this executes the a set of jobs
for the pipline for a single instance (site_id). 

The container instance should be self-contained python environment to Process
the full CC_Pipeline process for a single site_id instance.

@author: KFM
"""


import os, sys, json
import argparse, runpy
from timeit import default_timer as timer
import SRP_Config  as cfg
import SRP_Utils  as utl
# import CC_Target_Product_Set       as Process_Target_URLS
# import CC_Target_Product_IDX       as Process_Target_IDXS
# import CC_Target_Product_Extract   as Process_Target_Extracts

JOB_ID    = utl.get_utc_timeString(micro=False)
LOG_FILE  = f'{cfg.CC_TARGET_PRODUCT_SET}/TPS|{JOB_ID}.log'

class CC_Processor():
    ''' Processes a Pipeline Job for a Site ID to extract target Products from Common Crawl.

    Params: 
        job_id:  An allocated Job ID used to identify related files for the job.  
        site_id:  the Merchant_Site_ID used to identify site that will be processed.
        
    Inputs:
        - All inputs are handled by the CC-component parts.

    Output FEED: 
        - multiple outputs will be produced by the pipeine components and fed to the next process.

    Process Algo:
        Read Latesst Set of URLS for Site ID Exported from RPG.
        For site_url in Latest Site_id Price_Update:
            if site_url not in RPG_URLS:
                Append site_url to CC_Target_Product_Set (Target Output)
    '''

    def __init__(self, job_id, site_id):

        return 


def initialize():
    print(f"***********************************************************************************")
    print(f"********* LOADING JOB: SITE_ID: [{args.site_id}], JOB_ID: [{JOB_ID}] ")
    print(f"***********************************************************************************")

    try:
        TPS = runpy.run_module("CC_Target_Product_Set", run_name=f"__main__")
    except SystemExit as exeption:
        exitcode = exeption.code
    else:
        exitcode = 0
    
    print(f"TPS-Status: {exitcode}")
    if exitcode == 0:
        try:
            TPS = runpy.run_module("CC_Target_Product_IDX", run_name="__main__")
        except SystemExit as exeption:
            exitcode = exeption.code
        else:
            exitcode = 0

    print(f"IDX-Status: {exitcode}")
    if exitcode == 0:
        try:
            TPS = runpy.run_module("CC_Target_Product_Extract", run_name="__main__")
        except SystemExit as exeption:
            exitcode = exeption.code
        else:
            exitcode = 0

    print(f"EXTRACT-Status: {exitcode}")

    return exitcode


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Common Crawl Target Product Extractor")
    parser.add_argument('site_id',  type=str, help='Require: Site Id (or Merchant_ID) is required to search the Common Crawl')
    parser.add_argument('-job_id', type=str, default=JOB_ID, help='Optional: Job Id to lable pipeline outputs')
    args = parser.parse_args()
    sys.argv.append(JOB_ID)


    initialize()



    # for spu in SPUs:
    #     name = spu.name.split("|")[1]
    #     new_fPath = f"{cfg.SRP_SITE_PRICE_UPDATES}/SPU|{job_id}|{name}"
    #     print(new_fPath)
    #     os.rename(spu.path, new_fPath)









    

