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
import threading

# Create csv file in openshift
print('Creating training_dataset.csv file...')
with open('training_dataset.csv', 'w', newline='') as file:
	writer = csv.writer(file)
	writer.writerow(["timestamp", "apiload", "memoryusage", "cpu", "podid", "clusterid"])
  
# Connect to s3 bucket
print('Connecting to s3 bucket...')
session = boto3.Session(
    aws_access_key_id = 'AKIA5UBFMXG4DJITDQOB',
    aws_secret_access_key = '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'
)
s3_resource = session.resource('s3')
bucket = s3_resource.get_bucket('machinetrainers')
key = boto.s3.key.Key(bucket, 'training_dataset.csv')

def printit():
	threading.Timer(10.0, printit).start()
	print('Appending new data to file...')
	with open('training_dataset.csv', 'a', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(["2020-02-23 7:00:10", 5111.11, 765.92, 3.74, "10.11.12.13", "14.15.16.17"])
	print('Updating file on s3 bucket...')
	with open('training_dataset.csv') as f:
    		key.send_file(f)
	# Read csv file from s3
	client = boto3.client('s3', aws_access_key_id='AKIA5UBFMXG4DJITDQOB',
        	aws_secret_access_key='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')
	object_key = 'training_dataset.csv'
	csv_obj = client.get_object(Bucket = 'machinetrainers', Key=object_key)
	body = csv_obj['Body']
	csv_string = body.read().decode('utf-8')
	df = pd.read_csv(StringIO(csv_string))
	print('File updated!')
	print(df)
	

printit()



# print('Write to s3 bucket')
# # Data to write
# with open('training_dataset.csv', 'a', newline='') as file:
# 	writer = csv.writer(file)
# 	writer.writerow(["timestamp", "apiload", "memoryusage", "cpu", "podid", "clusterid"])
# 	writer.writerow(["2020-02-23 7:00:10", 5111.11, 765.92, 3.74, "10.11.12.13", "14.15.16.17"])
# 	writer.writerow(["2020-02-23 8:00:10", 6111.11, 865.92, 4.74, "10.11.12.13", "14.15.16.17"])

# # Connect to s3 bucket
# session = boto3.Session(
#     aws_access_key_id = 'AKIA5UBFMXG4DJITDQOB',
#     aws_secret_access_key = '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'
# )
# s3_resource = session.resource('s3')
# # Write to csv file
# bucket = 'machinetrainers' # already created on S3
# csv_buffer = StringIO()
# df.to_csv(csv_buffer)
# # s3_resource = boto3.resource('s3')
# s3_resource.Object(bucket, 'df.csv').put(Body=csv_buffer.getvalue())

# # Read csv file from s3
# client = boto3.client('s3', aws_access_key_id='AKIA5UBFMXG4DJITDQOB',
#         aws_secret_access_key='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')
# object_key = 'df.csv'
# csv_obj = client.get_object(Bucket = 'machinetrainers', Key=object_key)
# body = csv_obj['Body']
# csv_string = body.read().decode('utf-8')

# df = pd.read_csv(StringIO(csv_string))
# print(df)
