import boto3
import botocore
from botocore import UNSIGNED
from botocore.client import Config
from datetime import datetime
import os
import tools


def goes_filter(files, bands, start, end):
    if bands is None:
        bands = list(range(1, 17))
    else:
        if type(bands) is int:
            bands = [bands]
    drop = []
    for i, file in enumerate(files):
        date = datetime.strptime(files[i]['Key'][52:-36], '%Y%j%H%M%S')
        band = int(files[i]['Key'][44:46])
        if date < start or date > end or band not in bands:
            drop.append(i)
    for index in sorted(drop, reverse=True):
        del files[index]
    return files


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
        self.client = boto3.client('s3', config=Config(signature_version=UNSIGNED))
        self.product = tools.eval_input(bucket, product, self.client)
        
        
        if end is None and start is None:
            files = tools.last_archive(self.bucket, self.client,
                                       self.product + '/', 3)
                
        elif end is None:
            
        else:



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
