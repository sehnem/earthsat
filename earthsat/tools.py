from botocore import UNSIGNED
from botocore.client import Config
import datetime as dt
import numpy as np
import pandas as pd
import sys
import threading
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


def eval_input(bucket, instr, client, prefix=''):
    if prefix is not '':
        prefix = prefix + '/'
    valid_inputs = list_dir(bucket, client, prefix)['dir']
    valid_inputs = [string.split('/')[-2] for string in valid_inputs]
    if instr not in valid_inputs:
        valid_inputs_str = '\n'.join(valid_inputs)
        raise ValueError('Not a valid input, valid values are:\n' +
                         valid_inputs_str)
    else:
        return instr


def parse_dates():
    pass


class ProgressPercentage(object):
    def __init__(self, filename, size):
        self._filename = filename
        self._size = size
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        with self._lock:
            self._seen_so_far += bytes_amount
            bl, status = 20, ""
            progress = (self._seen_so_far / self._size)
            if progress >= 1.:
                progress, status = 1, "\r\n"
            block = int(round(bl * progress))
            text = '\r[{}] {:.0f}% {}'.format('#' * block + '-' * (bl - block),
                                              round(progress * 100, 0), status)
            sys.stdout.write(text)
            sys.stdout.flush()
