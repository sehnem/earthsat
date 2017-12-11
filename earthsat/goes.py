import boto3
import botocore
from botocore import UNSIGNED
from botocore.client import Config
import time
import datetime as dt
from datetime import datetime
import os
import tools


def band_filter(files, bands):
    if bands is None:
        bands = list(range(1, 17))
    else:
        if type(bands) is int:
            bands = [bands]
    drop = []
    for i, file in enumerate(files):
        band = int(files[i]['Key'][44:46])
        if band not in bands:
            drop.append(i)
    for index in sorted(drop, reverse=True):
        del files[index]
    return files


def date_filter(files, start, end):
    drop = []
    for i, file in enumerate(files):
        date = datetime.strptime(file['Key'][52:-36], '%Y%j%H%M%S')
        if date <= start or date >= end:
            drop.append(i)
    for index in sorted(drop, reverse=True):
        del files[index]
    return files


def date_to_prefix(product, dates):
    prefixes = []
    for date in dates:
        prefix = date.strftime(product+'/%Y/%j/%H/')
        if prefix not in prefixes:
            prefixes.append(prefix)
    return prefixes


def closest_date(files, date):
    dates = []
    rfiles = []
    date = date.extend(time.mktime(date))
    for file in files:
        datev = datetime.strptime(file['Key'][52:-36], '%Y%j%H%M%S')
        dates.extend(time.mktime(datev))
    c_date = min(dates, key=lambda x: abs(x-date))
    stamp = datetime.fromtimestamp(c_date).strftime('%Y%j%H%M%S')
    for file in files:
        if file['Key'][52:-36] == stamp:
            rfiles.extend(file)
    return rfiles


def last_archive(bucket, client, prefix, depth, ftype='file'):
    for x in range(depth-1):
        prefix = list_dir(bucket, client, prefix)['dir'][-1]
    return list_dir(bucket, client, prefix)[ftype]


class Goes16():

    def __init__(self, product, start=None, end=None, bands=None):
        """
        start = dt.datetime(2017,10,13,10)
        end = dt.datetime(2017,10,13,10, 30)
        goes = Goes16_data('ABI-L2-CMIPF', start, end)
        datetime(2017,11,19,15,45)
        """

        # inicializar primeiro o reposítório local

        self.bucket = 'noaa-goes16'
        self.client = boto3.client('s3',
                                   config=Config(signature_version=UNSIGNED))
        self.product = tools.eval_input(self.bucket, product, self.client)
        files = []
        if end is None and start is None:
            files.extend(last_archive(self.bucket, self.client,
                                      self.product + '/', 3))
            band_filter(files, bands)

        else:
            if end is None:
                date = start
                dates = [date + dt.timedelta(hours=x) for x in range(-1, 2)]
            else:
                days = (end-start).days + 1
                dates = [start + dt.timedelta(days=x) for x in range(0, days)]
            prefixes = date_to_prefix(self.product, dates)
            for prefix in prefixes:
                try:
                    files.extend(tools.list_dir(self.bucket, self.client,
                                                prefix)['file'])
                except FileNotFoundError:
                    print('Folder {} not found.'.format(prefix))
                    continue
            if end is None:
                files = closest_date(files, date)
            else:
                files = date_filter(files, start, end)
            files = band_filter(files, bands)


    def download(self, path='./'):
        s3 = boto3.resource('s3', config=Config(signature_version=UNSIGNED))
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
