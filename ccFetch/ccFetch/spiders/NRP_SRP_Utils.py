#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Jan 06 13:15:15 2023

Utility Functions Refactored from Cat-39_Spider.

@author: KFM
"""

import os, sys, json
import time
from datetime import datetime, timezone
from timeit import default_timer as timer
import SRP_Config  as cfg


def check_folder_exists(fPath):
    if not os.path.isdir(fPath):
        os.makedirs(fPath)
    return fPath

def get_last_export_lable():
    ''' creates a new dir for export and returns lable for it'''
    subfolders= [f.path for f in os.scandir(cfg.RPG_EXPORTS) if f.is_dir()]
    subfolders = sorted(subfolders, reverse=True)
    lable = subfolders[0]

    return lable

def get_utc_timeString(micro=False):
    ''' Returns UTC Str Zero Filled for Correct Sorting of timestamps'''
    utc = datetime.now(timezone.utc)
    mth = str(utc.month).zfill(2)
    d = str(utc.day).zfill(2)
    h = str(utc.hour).zfill(2)
    min = str(utc.minute).zfill(2)
    sec = str(utc.second).zfill(2)
    ms = str(utc.microsecond).zfill(7)

    if micro:   return f"{utc.year}.{mth}.{d}.{h}.{min}.{sec}.{ms}"
    else:       return f"{utc.year}.{mth}.{d}.{h}.{min}.{sec}"

def get_json_list_from_json_file(fPath):
    ''' Returns a list of JSON dicts from a file'''
    if not fPath: return
    output = []
    with open(fPath) as f:
        for line in f:
            output.append(json.loads(line))
    return output

def get_json_generator_from_file(fPath):
    ''' Returns a list of JSON dicts from a file'''
    if not fPath: return
    output = []
    with open(fPath) as f:
        for line in f:
            yield json.loads(line)

def get_dict_list_from_json_file(fPath, key, key_only=False):
    ''' Returns a dict of JSON dicts from a file'''
    if not fPath: return
    output = {}
    with open(fPath) as f:
        for line in f:
            d = json.loads(line)
            output[d[key]] = 1 if key_only else d
    return output

def get_dict_json_kv(fPath):
    ''' Returns a dict of JSON Key/Values for dicts load from a file.
    Returns empty dict if file not found.'''
    d = {}
    # check if file exists on disk
    if not fPath or not os.path.isfile(fPath):
        print(f'File not found: {fPath}')
        return d

    # load k,v into dict from file
    with open(fPath) as f:
        for line in f:
            k, v = json.loads(line)
            d[k] = v
    return d

def dump_dict_json_kv(d, fPath, mode='w'):
    ''' Writes a dict of JSON Key/Values to a file'''
    if not fPath: return
    with open(fPath, mode) as f:
        for k, v in d.items():
            f.write(json.dumps([k, v])+"\n")
    return
    
def get_dict_from_json_lines(fPath, key, key_only=False):
    ''' Returns a dict of JSON Key/Values for dicts load from a file.
    Returns empty dict if file not found.'''
    d = {}
    # check if file exists on disk
    if not fPath or not os.path.isfile(fPath):
        print(f'File not found: {fPath}')
        return d

    # load k,v into dict from file
    with open(fPath) as f:
        for line in f:
            j = json.loads(line)
            d[j[key]] = j if not key_only else 1
    return d

def dump_dict_to_json_lines(d, fPath):
    ''' Writes a dict of JSON Key/Values to a file'''
    if not fPath: return
    with open(fPath, 'w') as f:
        for k, v in d.items():
            f.write(json.dumps(v)+"\n")
    return

def load_dict_from_file(fPath):
    ''' Returns a dict from a file'''
    if not fPath: return
    output = {}
    with open(fPath) as f:
        for line in f:
            k, v = line.split(',')
            output[k] = v
    return output
  
def get_all_files_from_folder(folder, prefix=None, suffix=None):
    ''' Returns a list of files (fPaths) from a folder 
    in reverse order (olderst to newest)'''
    jobs = []

    # check folder exists
    if not os.path.isdir(folder): return jobs

    with os.scandir(folder) as it:
        for entry in it:
            if prefix and suffix and entry.name.startswith(prefix) and entry.name.endswith(suffix) and entry.is_file():
                jobs.append(entry)
            elif prefix and entry.name.startswith(prefix) and entry.is_file():
                jobs.append(entry)
            elif suffix and entry.name.endswith(suffix) and entry.is_file():
                jobs.append(entry)
            elif not prefix and not suffix and entry.is_file():
                jobs.append(entry)
            
    # Sort files by time of creation oldest to newest
    jobs = sorted(jobs, key=lambda entry: entry.name, reverse=False)
    # extract the fPath from the entry into a list
    jobs = [entry.path for entry in jobs]
    return jobs


def get_fPath_for_id(bucket, suffix, last=True):
    ''' Returns a list of file entry objects that have matching suffix.
    params: 
        bucket: path to folder/bucket
        suffix: id including full extension to find
        last: boolean, default True: returns the latest fPath.  If False, returns all matches unsorted.'''

    fPaths = []

    with os.scandir(bucket) as it:
        for entry in it:
            if entry.name.endswith(suffix): 
                fPaths.append(entry.path)

        if last and fPaths: 
            fPaths = sorted(fPaths, reverse=True)
            return fPaths[0]
        elif fPaths: 
            return fPaths
    return None


def get_all_job_logs():
    ''' Returns a list of jobs (fPaths to job file) that have been completed in reverse order.'''
    job_logs = []

    with os.scandir(cfg.SRP_SITE_PRICE_UPDATES) as it:
        for entry in it:
            if entry.name.endswith(".job.log") and entry.is_file():
                job_logs.append(entry)
                print(entry.name)
    job_logs = sorted(job_logs, key=lambda entry: entry.name, reverse=True)
    return job_logs

def get_all_SPU_jobs():
    ''' Returns a list of Site_Price_Update (SPU) jobs that have been completed. 
    (fPaths to job file) that have been completed in reverse order.'''
    jobs = []

    with os.scandir(cfg.SRP_SITE_PRICE_UPDATES) as it:
        for entry in it:
            if entry.name.endswith(".json") and entry.is_file():
                jobs.append(entry)
    jobs = sorted(jobs, key=lambda entry: entry.name, reverse=True)
    return jobs

def get_all_SPU_job_ids():
    ''' Returns a list of site_ids from the Site_Price_Update (SPU) jobs that have been completed. 
    (fPaths to job file).'''
    jobs = []

    with os.scandir(cfg.SRP_SITE_PRICE_UPDATES) as it:
        for entry in it:
            if entry.name.endswith(".json") and entry.is_file():
                jobs.append(entry)
    jobs = sorted(jobs, key=lambda entry: entry.name, reverse=True)
    return jobs

def rename_bucket_files():
    ''' TODO: this is incomplete.  Used only to renamce Site_Price_Update (SPU) jobs. 
    Needs to be generalized if useful'''

    job_id = "2023.01.04.08.35"
    prefix = "SPU"
    SPUs = utl.get_all_SPU_site_ids()
    SPUs = None

    for spu in SPUs:
        name = spu.name.split("|")[1]
        new_fPath = f"{cfg.SRP_SITE_PRICE_UPDATES}/SPU|{job_id}|{name}"
        print(new_fPath)
        os.rename(spu.path, new_fPath)
    return

def dict_to_list(d):
    output = []
    for k, v in d.items():
        output.append(v)

    return output

def dedupe_site_index():
    ''' Dedupes a site index that has been extracted from multiple cc indexs.
    Returns a list of cc_index recoreds that are unqiues. '''
    fPath = "/Users/kelly/Data/STAGED/SITE_PRODUCT_CC_INDEX/2023-1-5.16.1.456229|amitybicycles--com-.uniques.json"
    fPath2 = "/Users/kelly/Data/STAGED/SITE_PRODUCT_CC_INDEX/2023-1-5.16.40.71527|amitybicycles--com-.json"
    d = {}

    fPaths = [fPath, fPath2]

    for fp in fPaths:
        with open(fp, 'r') as f:
            for line in f:
                jd = json.loads(line)
                d[jd['urlkey']] = jd
    
    idx_list = dict_to_list(d)
    return idx_list

def convert_to_www(url):
    ''' Inserts a WWW into URLS and returns the new url. '''

    segments = url.split("//")
    url = f"{segments[0]}//www.{segments[1]}"
    return url


def compare_site_index():
    ''' Dedupes a site index that has been extracted from multiple cc indexs.
    Returns a list of cc_index recoreds that are unqiues. '''
    fPath = "/Users/kelly/Data/STAGED/SITE_PRICE_UPDATES/2023-1-3.13.45|amitybicycles--com-.json"
    fPath2 = "/Users/kelly/Data/STAGED/SITE_PRODUCT_CC_INDEX/2023-01-05.17.04.0746211|amitybicycles--com-.json"
    d = {}
    missing = []

    fPaths = [fPath, fPath2]

    with open(fPath2, 'r') as f:
        for line in f:
            jd = json.loads(line)
            d[jd['url']] = jd
    
    with open(fPath, 'r') as f:
        for line in f:
            jd = json.loads(line)
            if convert_to_www(jd['url']) not in d: missing.append(jd)

    return missing


# def get_total_job_stats(job_id=JOB_LOG):
#     ''' Returns Total Job Stats combined for each Spider Crawl for Job ID.'''
#     #  Using a copy of dict because it contains objects we do not want to export
#     total_items = 0
#     total_time = 0
#     with open(job_id, 'r') as f:            
#         for line in f:
#             stats = json.loads(line)
#             print(stats)
#             total_items += stats.get('item_scraped_count', 0)
#             total_time  += stats.get('elapsed_time_seconds', 0)

#     items_per_sec = total_items / total_time

#     return total_items, total_time, items_per_sec

# def start_sequentially(process, crawlers):
#     deferred = process.crawl(Cycling_Spider, crawlers[0]['netloc'], crawlers[0]['merchant_key'], crawlers[0]['base_cat'])

#     if len(crawlers) > 1:
#         deferred.addCallback(lambda _: start_sequentially(process, crawlers[1:]))
#     return

