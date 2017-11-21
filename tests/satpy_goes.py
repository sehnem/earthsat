import glob
from earthsat import Goes16
from satpy.scene import Scene
from datetime import datetime
from satpy.resample import get_area_def


goes = Goes16('ABI-L1b-RadF', datetime(2017,11,20,15), bands=list(range(1,4)))
goes.download('/home/josue/Documentos/DataAnalysis/goes/data/')

scn = Scene(
    filenames=glob.glob("/home/josue/Documentos/DataAnalysis/goes/data/*"),
    reader='abi_l1b')

for ch in ["C{channel:02d}".format(channel=chn + 1) for chn in range(3)]:
    scn.load([ch])

bra = scn.resample("southamerica")
del scn



from trollimage.image import Image
import numpy as np

ch1 = bra.datasets['C01']
ch2 = bra.datasets['C02']
ch3 = bra.datasets['C03']


green = 0.48358168 * ch2 + 0.45603695 * ch1 + 0.06038137 * ch3

img = Image((ch2, green, ch1), mode='RGB')


img.stretch_hist_equalize(0)
img.stretch_hist_equalize(1)
img.stretch_hist_equalize(2)
img.gamma()
pi = img.pil_image()#.resize((768,768))
pi.save('ant.png')
