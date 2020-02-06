# Collect openshift metrics and upload to s3 bucket

import requests
from datetime import datetime
from random import randrange
import threading
import warnings
warnings.filterwarnings("ignore")
import subprocess
import sys
from io import StringIO

def installPackage(packageName):
  subprocess.check_call([sys.executable, "-m", "pip", "install", packageName])

installPackage('boto3')
import boto3
installPackage('pandas')
import pandas as pd 
import csv

# Create csv file in openshift
print('Creating training_dataset.csv file\n')
with open('training_dataset.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["timestamp", "apiload", "memoryusage", "cpuusage", "podname", "namespace"])

# Connect to s3 bucket
print('Connecting to s3 bucket\n')
session = boto3.Session(
    aws_access_key_id = 'AKIA5UBFMXG4DJITDQOB',
    aws_secret_access_key = '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'
)
s3_resource = session.resource('s3')

def getPodMetrics():
    header = {'Authorization': 'Bearer Nza8_o-UtbaprYOIpdX4bzNk6o-VaulOI_J5GWCfuXk'}
    getmemusage = 'https://prometheus-k8s-openshift-monitoring.apps.imppoc.admcoe.com/api/v1/query?query=pod_name%3Acontainer_memory_usage_bytes%3Asum%7Bnamespace%3D%22machine-trainers%22%2Cpod_name%3D%22nodejs-app-1-xhfvd%22%7D'
    response1 = requests.get(getmemusage, headers=header, verify=False)
    getcpuusage = 'https://prometheus-k8s-openshift-monitoring.apps.imppoc.admcoe.com/api/v1/query?query=pod_name%3Acontainer_cpu_usage%3Asum%7Bnamespace%3D%22machine-trainers%22%2Cpod_name%3D%22nodejs-app-1-xhfvd%22%7D'
    response2 = requests.get(getcpuusage, headers=header, verify=False)
    timestamp = datetime.fromtimestamp(response1.json()["data"]["result"][0]["value"][0])
    memoryusage = round(float(response1.json()["data"]["result"][0]["value"][1])/1000000, 2) # MB
    cpuusage = round(float(response2.json()["data"]["result"][0]["value"][1]) * 100, 2) # m cores
    podname = response1.json()["data"]["result"][0]["metric"]["pod_name"]
    namespace = response1.json()["data"]["result"][0]["metric"]["namespace"]
    return timestamp, memoryusage, cpuusage, podname, namespace

def myfunction():
    threading.Timer(60.0, myfunction).start()
    print("Getting data....................................................\n")
    # Generate a random number between 5 and 20
    rand_num = randrange(30, 100)
    # Call nodejs API deployed on openshift rand_num number of times
    app_url1 = 'http://nodejs-app-machine-trainers.apps.imppoc.admcoe.com/'
    app_url2 = 'http://nodejs-app-machine-trainers.apps.imppoc.admcoe.com/a'
    for i in range(rand_num):
        requests.get(app_url1)
        requests.get(app_url2)
    apiload = rand_num
    timestamp, memoryusage, cpuusage, podname, namespace = getPodMetrics()
    print('Data -> timestamp:',timestamp, ', memoryusage:',memoryusage, ', cpuusage',cpuusage, ', podname:',podname, ', namespace',namespace)
    print('\nAppending new data to file\n')
    with open('training_dataset.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, apiload, memoryusage, cpuusage, podname, namespace])
#         writer.writerow(["2020-02-23 7:00:10", 5111.11, 765.92, 3.74, "10.11.12.13", "14.15.16.17"])
    print('Updating file on s3 bucket\n')
    s3_resource.Object('machinetrainers','training_dataset.csv').upload_file(Filename='training_dataset.csv')
    # Read csv file from s3
    client = boto3.client('s3', aws_access_key_id='AKIA5UBFMXG4DJITDQOB',
            aws_secret_access_key='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')
    object_key = 'training_dataset.csv'
    csv_obj = client.get_object(Bucket = 'machinetrainers', Key=object_key)
    body = csv_obj['Body']
    csv_string = body.read().decode('utf-8')
    df = pd.read_csv(StringIO(csv_string))
    print('File updated!\n')
#     print(df)
    

myfunction()

