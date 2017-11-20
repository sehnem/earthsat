import glob
from earthsat import Goes16
from satpy.scene import Scene
from datetime import datetime
from satpy.resample import get_area_def


goes = Goes16('ggg', datetime(2017,11,19,15,30), datetime(2017,11,19,15,35))

scn = Scene(
    base_dir="/home/josue/Documentos/DataAnalysis/goes/data/",
    reader='abi_l1b')


scn.load('C01')


