from botocore import UNSIGNED
from botocore.client import Config
import datetime as dt
import numpy as np
import pandas as pd


def list_files(bucket, client, prefix=''):
    out = []
    result = client.list_objects(Bucket=bucket, Prefix=prefix)
    result = result['Contents']
    for i in range(len(result)):
        out.append(str(result[i]['Key']))
    return out


def list_dir(bucket, client, prefix=''):
    out = []
    result = client.list_objects(Bucket=bucket, Prefix=prefix, Delimiter='/')
    for o in result.get('CommonPrefixes', client):
        out.append(o.get('Prefix'))
    return out


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
