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


def list_files(bucket, client, prefix=''):
    out = []
    result = client.list_objects(Bucket=bucket, Prefix=prefix)
    result = result['Contents']
    for i in range(len(result)):
        out.append(str(result[i]['Key']))
    return out
#result['Contents'][1]['Size']


def list_dir(bucket, client, prefix=''):
    out = []
    result = client.list_objects(Bucket=bucket, Prefix=prefix, Delimiter='/')
    for o in result.get('CommonPrefixes', client):
        out.append(o.get('Prefix'))
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


#bk = conn.get_bucket('my_bucket_name')
#key = bk.lookup('my_key_name')
#print key.size

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
