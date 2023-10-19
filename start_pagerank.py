#!/usr/bin/python

import subprocess
import time

from google.cloud import dataproc_v1
from google.cloud import storage
from google.cloud import dataproc_v1 as dataproc


resultat_timer_pig = ""
resultat_timer_pyspark = ""

bucket = "gs://bigdata_cdl/"
region = "europe-central2"
projetId = "bigdata-401112"
clusterName = "pagerank"
typeData = "page_links_en.nt.bz2"


def files_copy():

    ## copy pig code
    command_copy_pig_pagerank = "gsutil cp pagerank_pig.py %s " % (bucket, )
    subprocess.run([command_copy_pig_pagerank], shell=True)

    ## copy pig code
    command_copy_pig_pagerank = "gsutil cp pagerank_pyspark.py %s " % (bucket, )
    subprocess.run([command_copy_pig_pagerank], shell=True)

    ## copy pig code
    command_copy_pig_pagerank = "gsutil cp pagerank_test.py %s " % (bucket, )
    subprocess.run([command_copy_pig_pagerank], shell=True)

    ## copy pig code
    command_copy_pyspark_pagerank = "gsutil cp pagerank-notype.py %s " % (bucket, )
    subprocess.run([command_copy_pyspark_pagerank], shell=True)
    
    ## Clean out directory
    command_delete_out_directory = "gsutil rm -rf %sout" % (bucket, )
    subprocess.run([command_delete_out_directory], shell=True)

def run_cluster_python(number_node): # Create the cluster client.
    cluster_client = dataproc_v1.ClusterControllerClient(
        client_options={"api_endpoint": "%s-dataproc.googleapis.com:443" % (region, )}
    )

    # Create the cluster config.
    cluster = {
        "project_id": projetId,
        "cluster_name": clusterName,
        "config": {
            "master_config": {"num_instances": 1, "machine_type_uri": "n1-standard-4"},
            "worker_config": {"num_instances": number_node, "machine_type_uri": "n1-standard-4"},
        },
    }

    # Create the cluster.
    operation = cluster_client.create_cluster(
        request={"project_id": projetId, "region": region, "cluster": cluster}
    )
    result = operation.result()

    print(f"Cluster created successfully: {result.cluster_name}")


    global resultat_timer_pig 
    resultat_timer_pig = execute_pagerank_pig()

    global resultat_timer_pyspark
    resultat_timer_pyspark = execute_pagerank_pyspark()

    operation = cluster_client.delete_cluster(
    request={
            "project_id": projetId,
            "region": region,
            "cluster_name": clusterName,
        }
    )
    operation.result()

    print(f"Cluster {clusterName} successfully deleted.")

def execute_pagerank_pig():
    command_jobs_pagerank = "gcloud dataproc jobs submit pig --region %s --cluster %s -f %spagerank_pig.py" % (region, clusterName, bucket, )

    start = time.time()    
    subprocess.run([command_jobs_pagerank], shell=True)
    end = time.time()

    result = end - start


    print(f"Job PIG finished successfully : {result} \n")

    return result

def execute_pagerank_pyspark():
    command_jobs_pagerank = "gcloud dataproc jobs submit pyspark --region %s --cluster %s %spagerank_test.py  -- gs://public_lddm_data/%s 3" % (region, clusterName, bucket, typeData, )

    start = time.time()    
    subprocess.run([command_jobs_pagerank], shell=True)
    end = time.time()


    result = end - start

    print(f"Job Pyspark finished successfully : {result} \n")

    return result

def write_space():
    file = open("resultat.txt", "a")
    file.write("--------------------------------------------------------------------------------------\n")
    file.close()
    
def write_result(result_time, pig, num_node):

    file = open("resultat.txt", "a")
    if (pig == True):
        file.write("resultat PIG %s nodes : %s\n" % (num_node, result_time, ))
    else:
        file.write("resultat Pyspark %s nodes : %s\n" % (num_node, result_time, ))
    file.close()

def run_main():
    files_copy()
    iteration = [2]
    for it in iteration:
        run_cluster_python(it)
        write_space()
        write_result(resultat_timer_pig, True, it)
        write_result(resultat_timer_pyspark, False, it)

run_main()