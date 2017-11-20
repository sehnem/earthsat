import glob
from earthsat import Goes16
from satpy.scene import Scene
from datetime import datetime
from satpy.resample import get_area_def


goes = Goes16('ABI-L2-CMIPF', datetime(2017,11,19,15,40), bands=[1,2,3,4])
goes.download('/home/josue/Documentos/DataAnalysis/goes/data/')


scn = Scene(
    base_dir="/home/josue/Documentos/DataAnalysis/goes/data/",
    reader='abi_l1b')


scn.load('C01')


