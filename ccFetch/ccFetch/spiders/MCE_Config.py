#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 8, 2023

@author: KFM
"""

import os, sys

# ******************************************************************************
# Set Basic environemnt vars in order to locate the common config file
# This is the first thing that needs to be done.
# The common config file will set the rest of the environment vars

# determine what OS we are running on
if sys.platform == 'darwin':
    # Set local paths to common config file
    A9_SRC_PATH             = "/Volumes/GoogleDrive/My Drive/A9_SRC"
    A9_COMMON               = "/Volumes/GoogleDrive/My Drive/A9_SRC/A9_Common"
    if not A9_COMMON in sys.path:       sys.path.insert(0, A9_COMMON)

elif sys.platform == 'win32':
    # Set local paths to common config file
    pass
else:       
    # Set GCP paths to common config file
    A9_SRC_PATH     = "/content/drive/MyDrive/A9_SRC"
    A9_COMMON       = f"{A9_SRC_PATH}/A9_Common"

    if not A9_SRC_PATH in sys.path: sys.path.insert(0, A9_SRC_PATH)
    if A9_COMMON not in sys.path: sys.path.append(A9_COMMON)

# ******************************************************************************
# IMPORT COMMON CONFIG FILE
# This will import all vars into this namespace
# This will override and local vars you have set to this point if they are the same name
from common_config import *
# print(f"A9_NAMESPACE: {A9_NAMESPACE} == 'ALPHA-9'")


# ******************************************************************************
# LOCAL CONFIG VARS
# Add local config vars to the namespace here  
# or you can also overide any of the common config vars here

# TEST_NAMESPACE = 'ALL-GOOD-MF'
# print(f"TEST_NAMESPACE: {TEST_NAMESPACE} == 'ALL-GOOD-MF ...'")
print(f"RPC PATH: {RPC_PATH}")
RPC_SPIDER              = f"{RPC_PATH}/meta_cluster_update/ccFetch"
RPC_MCE_PATH            = f"{RPC_PATH}/meta_cluster_update/ccFetch/ccFetch/spiders"

if not RPC_SPIDER in sys.path:      sys.path.insert(1, RPC_SPIDER)
if not RPC_MCE_PATH in sys.path:    sys.path.insert(2, RPC_MCE_PATH)

# All environment vars are now in single namespace
# ******************************************************************************

print(f"\n********************* MCE PATHS *********************")
for p in sys.path:
    print(p)


RPG_EXPORTS               = f"{CACHE_RPG}/EXPORTS"
MCE_FOLDER                = check_folder_exists(CACHE_RPC+"/META_CLUSTER_EXTRACT")

RPT_BRANDS_DICT           = f"{RPG_EXPORTS}/brands_dict.json"    
RPT_MERCHANTS_DICT        = f"{RPG_EXPORTS}/merchants_dict_cat39.json"    # Specific set based on cat-39 scrapper
RPT_META_CLUSTER_URLS     = f"{RPG_EXPORTS}/meta_urls.json"    # Specific set based on cat-39 scrapper

RPC_META_CLUSTER_SKIP     = f'{MCE_FOLDER}/CLUSTERS_0_1327_meta_cluster_update.json'
RPC_META_CLUSTER_COMPLETE = f'{MCE_FOLDER}/meta_clusters_complete.json'
RPC_META_CLUSTER_FAILED   = f'{MCE_FOLDER}/meta_clusters_failed.json'

RPC_MCE_LOG_FILE                = f"{MCE_FOLDER}/mce_extract.log"
RPC_META_CLUSTER_SKIP           = f'{MCE_FOLDER}/CLUSTERS_0_1327_meta_cluster_update.json'
RPC_META_CLUSTER_COMPLETE_FNAME = f'meta_clusters_complete.json'
RPC_META_CLUSTER_FAILED_FNAME   = f'meta_clusters_failed.json'
RPC_MCE_EXTRACT_FNAME           = f"mce_extract.json"
RPC_MCE_FEED_PATH               = f"mce_extract.json"

GCP_RPC_MCE_PATH          = f"RPC/META_CLUSTER_UPDATES"

RPC_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en',
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}