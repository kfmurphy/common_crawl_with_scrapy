# -*- coding: utf-8 -*-
""" KFM REUSED CODE
Reused on Mon Feb 19, 2023
 Based on CC_Target_Product_IDX.py

    '''
    '''

@author: KFM
"""

# import A9 Configs, Common and Job Control
import MCE_Config as cfg
import io_wrapper as iow
from job_control import Job
from gcp_wrapper import GCP_Wrapper as GCP
gcp = GCP()  # Get a global instance for the wrapper.

import os, sys
import argparse
from timeit import default_timer as timer
from tqdm import tqdm
import json

class MCE_Post_Processor():
    ''' Consolidates the outputs from the MCE_Extraction process.
    Consolidates the working files from the extraction in to a single set of out
     of outputs for downstream processing.
    '''
    def __init__(self,  **kwargs):
        # Initializing all generic variables
        self.site_id            = "mce_extract"
        self.job_id             = kwargs['job_id']
        self.node_id            = kwargs['node_id']
        self.startTime          = timer()

        # Get the Job Details from Control
        self.job                = Job(self.job_id, self.node_id)

        return
	
    def run(self):
        ''' Process the results of the MCE Extractor.
         Combines the outputs into signle files for each of the three categories:
        and eliminates duplicates. 
        '''

        self.pre_run()
        self.processes_cluster_extracts()
        self.processes_cluster_complete_fail()
        self.post_run()

        return
    
    def processes_cluster_extracts(self):
        """ Consolidates all clusters extracted into a single file.  Each Job is appended to the file.
        Builds a dictionary of clusters that have been extracted.  This is used to determine which clusters
        have been completed and which have failed.  Failed clusters will be extracted a second time.
        """
        self.local_cluster_extract    = cfg.MCE_FOLDER + f"/{self.job_id}_mce_extract.json"
        for f in self.extract_jobs:
            fName = f.split(self.job_id)[-1]
            fPath = f"{cfg.MCE_FOLDER}/{fName}"
            # check if file already exists
            if os.path.exists(fPath): continue
            gcp.download_to_file(f, fPath)
            iow.append_file_to_file(fPath, self.local_cluster_extract)

        return
    
    def processes_cluster_complete_fail(self):
        """ 
        Takes as input the requested clusters and the clusters that have been extracted.
        Builds two dicts of clusters that have been completed and failed.
        """

        self.clusters_extracted     = iow.get_dict_from_json_lines(self.local_cluster_extract, key="cluster_id", key_only=True)
        self.clusters_requested     = iow.get_dict_json_kv(cfg.RPT_META_CLUSTER_URLS)
        self.clusters_failed        = self.clusters_requested.copy()  # pop extracted clusters from this list
        self.clusters_complete      = {} # add extracted clusters to this list

        for k, v in self.clusters_extracted.items():
            if k in self.clusters_requested:
                self.clusters_failed.pop(k)
                self.clusters_complete[k] = 1
        
        return

    def pre_run(self):
        """ Locate paths to all the files to be processed."""
        # Create the output folder if it does not exist
        print(f"******************************** RUN JOB **********************************************")
        print(f"********* JOB_ID            : {self.job_id} ")
        print(f"********* NODE_ID           : {self.node_id} ")
        print(f"***************************************************************************************")

        # create local working folder if not exists
        if not os.path.exists(cfg.MCE_FOLDER):
            os.makedirs(cfg.MCE_FOLDER)

        # Get lo the files to be processed
        self.extract_jobs = gcp.get_all_files_from_folder(self.job.job_kv['GCP_DATA_FOLDER'], suffix="_mce_extract.json")

        return

    def post_run(self):
        """ Move all outputs to GCP outputs for next stage of pipeline"""
        job_output = self.job.job_kv['GCP_DATA_FOLDER'] + f"/{self.job_id}"

        gcp.dump_dict_json_kv(self.clusters_failed,        f"{job_output}_{cfg.RPC_META_CLUSTER_FAILED_FNAME}")
        gcp.dump_dict_json_kv(self.clusters_complete,      f"{job_output}_{cfg.RPC_META_CLUSTER_COMPLETE_FNAME}")
        gcp.upload_from_file(self.local_cluster_extract,   f"{job_output}_{cfg.RPC_MCE_EXTRACT_FNAME}")

        tMins = round(timer() - self.startTime)/60

        # Signal the job is complete
        self.job.set_job_complete()

        print(f"\n################## JOB COMPLETE ###################################################")
        print(f"********* JOB_ID            : {self.job_id} ")
        print(f"********* NODE_ID           : {self.node_id} ")
        print(f"********* CLUSTERS REQ      : {len(self.clusters_requested)}")
        print(f"********* SUCCESS           : {len(self.clusters_complete)} ")
        print(f"********* FAILED            : {len(self.clusters_failed)} ")
        print(f"********* TOTAL JOB TIME    : {tMins:.2f} Mins")
        print(f"#####################################################################################\n\n")
        return

    


if __name__ == '__main__':

    # combine_last_completed_clusters()

    parser = argparse.ArgumentParser(description="Meta Data Product Extractor")
    parser.add_argument('job_id',    type=str, help='Start cluster index to split jobs across nodes')
    parser.add_argument('node_id',   type=str, help='End cluster index to split jobs across nodes')
    args = parser.parse_args()

    # RUN JOB 
    # RUN JOB 
    processor = MCE_Post_Processor(job_id=args.job_id, node_id=args.node_id)
    processor.run()
    pass


