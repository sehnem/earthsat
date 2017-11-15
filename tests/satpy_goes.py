import glob
from satpy.scene import Scene
from datetime import datetime
from satpy.resample import get_area_def

scn = Scene(
    base_dir="/home/josue/Documentos/DataAnalysis/goes/data/",
    reader='abi_l1b')


for name in ["C{channel:02d}".format(channel=chn + 1) for chn in range(3)]:
    scn.load([name])
    scn.save_dataset(name, filename=name+'.png')
    del scn[name]

