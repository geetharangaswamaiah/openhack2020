import subprocess
import sys
subprocess.check_call([sys.executable, "-m", "pip", "install", 'boto3'])
      
from io import StringIO # python3; python2: BytesIO 
import boto3
import pandas as pd 

print('Hello World!')
# Data to write
timestamp = ['2020-02-20 1:00:10']
apiload = [1002.3] 
memoryusage = [400.92]
cpu = [2.3]
podid = ['10.12.13.14']
clusterid = ['10.12.13.14']
   
# Create dictionary 
dict = {'timestamp': timestamp, 'apiload': apiload, 'memoryusage': memoryusage, 'cpu': cpu, 'podid': podid, 'clusterid': clusterid}  

# Create Dataframe
df = pd.DataFrame(dict) 
print(df)

# Write to csv file
bucket = 'machinetrainers' # already created on S3
csv_buffer = StringIO()
df.to_csv(csv_buffer)
s3_resource = boto3.resource('s3')
s3_resource.Object(bucket, 'df.csv').put(Body=csv_buffer.getvalue())
