import glob
from earthsat import Goes16
from satpy.scene import Scene
from datetime import datetime
from satpy.resample import get_area_def


goes = Goes16('ABI-L1b-RadF', datetime(2017,11,20,15), bands=1)
goes.download('/home/josue/Documentos/DataAnalysis/goes/data/')

scn = Scene(
    base_dir="/home/josue/Documentos/DataAnalysis/goes/data/",
    reader='abi_l1b')

bra = scn.resample("brazil2")
bra.show('overview')

