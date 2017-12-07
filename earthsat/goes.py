import boto3
import botocore
from botocore import UNSIGNED
from botocore.client import Config
import os
import pandas as pd
import tools


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
        datetime(2017,11,19,15,45)
        """

        # inicializar primeiro o reposítório local

        self.bucket = bucket
        self.client = boto3.client('s3', config=Config(signature_version=UNSIGNED))
        self.product = tools.eval_input(bucket, product, self.client)


        if end is None:
            interval = pd.date_range(start, start, freq='H')
        else:
            interval = pd.date_range(start, end, freq='H')
        files = []
        for d in interval:
            hour = str(d.timetuple().tm_hour).zfill(2)
            day = str(d.timetuple().tm_yday).zfill(3)
            year = str(d.timetuple().tm_year)
            prefix = '/'.join([self.product, year, day, hour])
            try:
                files.extend(tools.list_files(bucket, self.client, prefix=prefix))
            except:
                continue
        files = files_to_df(files)
        if end is None:
            nd_files = files[~files.index.duplicated(keep='first')].index
            dt_file = nd_files[nd_files.get_loc(start, method='nearest')]
            files = files[files.index == dt_file]
        else:
            files = files[(files.index >= start) & (files.index <= end)]
        if bands is not None:
            if type(bands) is int:
                bands = [bands]
            files = files[files['band'].isin(bands)]
        self.files = files

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
