import boto3
import botocore
from botocore import UNSIGNED
from botocore.client import Config
import os
import pandas as pd
import tools


class Modis():

    def __init__(self, product, hgrid, vgrid, bucket='modis-pds'):
        """
        https://earthdatascience.org/tutorials/convert-modis-tile-to-lat-lon/
        """
        
        self.bucket = bucket
        self.client = boto3.client('s3', config=Config(signature_version=UNSIGNED))
        self.product = tools.eval_input(bucket, product, self.client)


        files = []

        prefix = '/'.join([self.product, hgrid, vgrid])
        try:
            files.extend(tools.list_dir(bucket, self.client, prefix=prefix))
        except:
            pass
        
        self.files = files
        
#        files = files_to_df(files)
#        if end is None:
#            nd_files = files[~files.index.duplicated(keep='first')].index
#            dt_file = nd_files[nd_files.get_loc(start, method='nearest')]
#            files = files[files.index == dt_file]
#        else:
#            files = files[(files.index >= start) & (files.index <= end)]
#        if bands is not None:
#            if type(bands) is int:
#                bands = [bands]
#            files = files[files['band'].isin(bands)]
#        self.files = files
#
#    def download(self, path='./'):
#        s3 = boto3.resource('s3', config=Config(signature_version=UNSIGNED))
#        for filename in self.files.path:
#            output = path + filename.split('/')[-1]
#            if os.path.isfile(output):
#                continue
#            try:
#                s3.Bucket(self.bucket).download_file(filename, output)
#            except botocore.exceptions.ClientError as e:
#                if e.response['Error']['Code'] == "404":
#                    print("The object does not exist.")
#                else:
#                    raise
