import boto3
import botocore
import os
import datetime as dt
import numpy as np
import pandas as pd


def list_files(bucket, prefix=''):
    out = []
    client = boto3.client('s3')
    result = client.list_objects(Bucket=bucket, Prefix=prefix)
    result = result['Contents']
    for i in range(len(result)):
        out.append(str(result[i]['Key']))
    return out


def list_dir(bucket, prefix=''):
    out = []
    client = boto3.client('s3')
    result = client.list_objects(Bucket=bucket, Prefix=prefix, Delimiter='/')
    for o in result.get('CommonPrefixes'):
        out.append(o.get('Prefix'))
    return out


def eval_input(bucket, instr, prefix=''):
    if prefix is not '':
        prefix = prefix + '/'
    valid_inputs = list_dir(bucket, prefix)
    valid_inputs = [string.split('/')[-2] for string in valid_inputs]
    if instr not in valid_inputs:
        valid_inputs_str = '\n'.join(valid_inputs)
        raise ValueError('Not a valid input, valid values are:\n' +
                         valid_inputs_str)
    else:
        return instr


def files_to_df(files):
    filename = [file.split('/')[-1] for file in files]
    atr = [i[-1].split('_') for i in [i.split('-') for i in filename]]
    mode, band, obs_start, obs_end, file_creation = [], [], [], [], []
    for a in atr:
        mode.append(int(a[0][1]))
        band.append(int(a[0][-2:]))
        obs_start.append(str(a[2][1:-1]))
        obs_end.append(str(a[3][1:-1]))
        file_creation.append(str(a[4][1:-4]))
    df = pd.DataFrame({'path': files, 'mode': mode, 'band': band,
                       'obs_start': obs_start, 'obs_end': obs_end,
                       'file_creation': file_creation})
    df['obs_start'] = pd.to_datetime(df['obs_start'], format='%Y%j%H%M%S')
    df['obs_end'] = pd.to_datetime(df['obs_end'], format='%Y%j%H%M%S')
    df['file_creation'] = pd.to_datetime(df['file_creation'], format='%Y%j%H%M%S')
    df = df.set_index('obs_start')
    return df


class Goes16():

    def __init__(self, product, start, end=None, bands=None, bucket='noaa-goes16'):
        """
        start = dt.datetime(2017,10,13,10)
        end = dt.datetime(2017,10,13,10, 30)
        goes = Goes16_data('ABI-L2-CMIPF', start, end)
        """

        # inicializar primeiro o reposítório local

        self.bucket = bucket
        self.product = eval_input(bucket, product)

        if end is None:
            end = start + dt.timedelta(1)

        interval = pd.date_range(start, end, freq='H')
        files = []
        for d in interval:
            hour = str(d.timetuple().tm_hour).zfill(2)
            day = str(d.timetuple().tm_yday).zfill(3)
            year = str(d.timetuple().tm_year)
            prefix = '/'.join([self.product, year, day, hour])
            try:
                files.extend(list_files(bucket, prefix))
            except:
                continue
        files = files_to_df(files)
        files = files[(files.index >= start) & (files.index <= end)]
        if bands is not None:
            if type(bands) is int:
                bands = [bands]
            files = files[files['band'].isin(bands)]
        self.files = files

    def download(self, path='./'):
        s3 = boto3.resource('s3')
        for filename in self.files.path:
            output = path + filename.split('/')[-1]
            if os.path.isfile(output):
                continue
            try:
                s3.Bucket(self.bucket).download_file(filename, output)
            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code'] == "404":
                    print("The object does not exist.")
                else:
                    raise
