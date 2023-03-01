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
from job_control import Job, Job_Control
from gcp_wrapper import GCP_Wrapper as GCP
gcp = GCP()  # Get a global instance for the wrapper.

import os, sys
import argparse
from timeit import default_timer as timer
from tqdm import tqdm
import json

class MCE_Controller():
    ''' Consolidates the outputs from the MCE_Extraction process.
    Consolidates the working files from the extraction in to a single set of out
     of outputs for downstream processing.
    '''
    def __init__(self,  **kwargs):
        # Initializing all generic variables
        self.startTime                  = timer()
        self.clusters_requested_fPath   = kwargs['clusters_requested_fPath']

        # Create a new job, add nodes and Initiate the job
        self.control = Job_Control()
        self.job_id = self.control.job_id
        self.node_id = self.control.node_id
        
        # Create job nodes and allocate the job for each of the nodes
        self.prepare_job()

        # initialize the job
        self.control.initialize()

        return
	
    
    def prepare_job(self):
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
        self.clusters_requested = gcp.get_kv_dict_from_jsonlines_file(self.clusters_requested_fPath)
        
        # set the number of nodes for the job. 
        # the optimum size is 5000 clusters per node.
        # self.control.create_job_nodes(len(self.clusters_requested)//5000 + 1)
        num_nodes = (len(self.clusters_requested)//5000 + 1)
        self.control.create_job_nodes(num_nodes)

        # build a dict for each job to be processed. 
        job_params = self.allocate_job(len(self.clusters_requested), self.control.num_nodes)

        # add job KV to each job node
        for i, job in enumerate(self.control.get_job_nodes()):
            job_kv = self.define_job(job_params[i])
            self.control.set_job_for_node(job.node_id, job_kv)
 
        return

    def define_job(self, node_params):
        """ Define the job parameters for each node here.
        This will be the general job parameters for each node.

        Node specific parameters can be added to each job through node_param.

        Returns a key/value dict for the jobs paramerters.
        """
        job_kv = {"gcp_output_folder": f"{cfg.GCP_RPC_MCE_PATH}/{self.job_id}/",
               "clusters_requested_fPath": self.clusters_requested_fPath,
               }
        # add the node specific parameters to the job
        job_kv.update(node_params)
        return job_kv

    def allocate_job(self, size, num_nodes):
        """ Divide the clusters to be processed among the nodes
        """
        num_keys_per_node = size // num_nodes
        remainder = size % num_nodes
        start = 0
        end = num_keys_per_node
        node_params = []
        for i in range(num_nodes):
            if i < remainder:
                end += 1
            node_params.append({'start': start, 'end': end})
            start = end
            end += num_keys_per_node
        return node_params

if __name__ == '__main__':

    # combine_last_completed_clusters()

    parser = argparse.ArgumentParser(description="Meta Data Product Extractor")
    parser.add_argument('job_id',    type=str, help='Start cluster index to split jobs across nodes')
    parser.add_argument('node_id',   type=str, help='End cluster index to split jobs across nodes')
    args = parser.parse_args()

    # RUN JOB 
    # RUN JOB 
    # https://storage.cloud.google.com/rpg-prod/RPC/META_CLUSTER_EXTRACT/JOB_2023.02.23.18.51.53/JOB_2023.02.23.18.51.53_meta_clusters_failed.json
    processor = MCE_Controller(clusters_requested_fPath="RPC/META_CLUSTER_EXTRACT/JOB_2023.02.23.18.51.53/JOB_2023.02.23.18.51.53_meta_clusters_failed.json")
    processor.run()
    pass


