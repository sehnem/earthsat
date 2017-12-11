from botocore import UNSIGNED
from botocore.client import Config
import datetime as dt
import numpy as np
import pandas as pd
import os

# TODO: Review tools
# TODO: Create dateinput function (google it!)
# TODO: As download is generic for any satellite create a function for download
#       from S3 with desired features (progressbar, chuncks, etc.)

# Fast test data
import boto3
bucket = 'noaa-goes16'
client = boto3.client('s3', config=Config(signature_version=UNSIGNED))
product = 'ABI-L2-CMIPF'


def list_dir(bucket, client, prefix=''):
    out = {'dir': [], 'file': []}
    ls = client.list_objects_v2(Bucket=bucket, Prefix=prefix, Delimiter='/')
    if 'CommonPrefixes' in ls:
        for o in ls.get('CommonPrefixes'):
            out['dir'].append(o.get('Prefix'))
    if 'Contents' in ls:
        for file in ls.get('Contents'):
            out['file'].append(file)
    return out



# TODO: Mantain for future use, but probable will not be use on GOES16

def eval_input(bucket, instr, client, prefix=''):
    if prefix is not '':
        prefix = prefix + '/'
    valid_inputs = list_dir(bucket, client, prefix)
    valid_inputs = [string.split('/')[-2] for string in valid_inputs]
    if instr not in valid_inputs:
        valid_inputs_str = '\n'.join(valid_inputs)
        raise ValueError('Not a valid input, valid values are:\n' +
                         valid_inputs_str)
    else:
        return instr


def parse_dates():
    pass

#bk = conn.get_bucket('my_bucket_name')
#key = bk.lookup('my_key_name')
#print key.size

# https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console

#class ProgressPercentage(object):
#    def __init__(self, filename):
#        self._filename = filename
#        self._size = float(os.path.getsize(filename))
#        self._seen_so_far = 0
#        self._lock = threading.Lock()
#
#    def __call__(self, bytes_amount):
#        # To simplify we'll assume this is hooked up
#        # to a single filename.
#        with self._lock:
#            self._seen_so_far += bytes_amount
#            percentage = round((self._seen_so_far / self._size) * 100,2)
#            LoggingFile('{} is the file name. {} out of {} done. The percentage completed is {} %'.format(str(self._filename), str(self._seen_so_far), str(self._size),str(percentage)))
#            sys.stdout.flush()



#link = "http://indy/abcde1245"
#file_name = "download.data"
#with open(file_name, "wb") as f:
#        print "Downloading %s" % file_name
#        response = requests.get(link, stream=True)
#        total_length = response.headers.get('content-length')
#
#        if total_length is None: # no content length header
#            f.write(response.content)
#        else:
#            dl = 0
#            total_length = int(total_length)
#            for data in response.iter_content(chunk_size=4096):
#                dl += len(data)
#                f.write(data)
#                done = int(50 * dl / total_length)
#                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
#                sys.stdout.flush()