#!/usr/bin/python

import subprocess
import time

from google.cloud import dataproc_v1
from google.cloud import storage
from google.cloud import dataproc_v1 as dataproc


resultat_timer = ""

def files_copy():
    ## copy data
    command_copy_data = "gsutil cp small_page_links.nt gs://bigdata_cdl/"
    subprocess.run([command_copy_data], shell=True)

    ## copy pig code
    command_copy_pig_pagerank = "gsutil cp pagerank.py gs://bigdata_cdl/"
    subprocess.run([command_copy_pig_pagerank], shell=True)

    ## Clean out directory
    command_delete_out_directory = "gsutil rm -rf gs://bigdata_cdl/out"
    subprocess.run([command_delete_out_directory], shell=True)

def create_cluster(number_worker):    
    command_create_cluster = "gcloud dataproc clusters create cluster-a35a --enable-component-gateway --region europe-central2 --zone europe-central2-c --master-machine-type n1-standard-4 --master-boot-disk-size 500 --num-workers %s --worker-machine-type n1-standard-4 --worker-boot-disk-size 500 --image-version 2.0-debian10 --project bigdata-401112" % (number_worker, )
    
    subprocess.run(command_create_cluster, shell=True)

def create_cluster_python(): # Create the cluster client.
    cluster_client = dataproc_v1.ClusterControllerClient(
        client_options={"api_endpoint": f"europe-central2-dataproc.googleapis.com:443"}
    )

    # Create the cluster config.
    cluster = {
        "project_id": "bigdata-401112",
        "cluster_name": "pagerank",
        "config": {
            "master_config": {"num_instances": 1, "machine_type_uri": "n1-standard-2"},
            "worker_config": {"num_instances": 3, "machine_type_uri": "n1-standard-2"},
        },
    }

    # Create the cluster.
    operation = cluster_client.create_cluster(
        request={"project_id": "bigdata-401112", "region": "europe-central2", "cluster": cluster}
    )
    result = operation.result()

def delete_cluster():
    commande_delete_cluster = "gcloud dataproc clusters delete pagerank --region europe-central2"

    subprocess.run([commande_delete_cluster], shell=True)
    


def execute_pagerank_pig():
    command_jobs_pagerank = "gcloud dataproc jobs submit pig --region europe-west1 --cluster cluster-a35a -f gs://bigdata_cdl/pagerank.py"

    start = time.time()    
    subprocess.run([command_jobs_pagerank], shell=True)
    end = time.time()

    result = end - start

    global resultat_timer 
    resultat_timer = result

def execute_pagerank_python_pig():
    # Create the job client.
    job_client = dataproc_v1.JobControllerClient(
        client_options={"api_endpoint": f"europe-central2-dataproc.googleapis.com:443"}
    )

    # Create the job config.
    job = {
        "placement": {"cluster_name": "pagerank"},
        "pyspark_job": {"main_python_file_uri": f"gs://bigdata_cdl/pagerank.py"},
    }

    start = time.time()

    operation = job_client.submit_job_as_operation(
        request={"project_id": "bigdata-401112", "region": "europe-central2", "job": job}
    )

    #response = operation.result()

    end = time.time()

    result = end - start

    global resultat_timer 
    resultat_timer = result

    print(resultat_timer)


def write_result(result_time):
    file = open("resultat.txt", "a")
    file.write("resultat PIG : %s\n" % (result_time, ))
    file.close()

def run_main():
    files_copy()
    iteration = [1]
    for it in iteration:
        create_cluster(it)
        execute_pagerank_pig()
        write_result(resultat_timer)
        delete_cluster()

def run_main_python():
    files_copy()
    iteration = [1]
    for it in iteration:
        create_cluster_python()
        execute_pagerank_python_pig()
        write_result(resultat_timer)
        delete_cluster()

#run_main_python()

#create_cluster_python()
execute_pagerank_python_pig()