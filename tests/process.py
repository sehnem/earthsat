from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np
 
def rebin(a, shape):
    sh = shape[0],a.shape[0]//shape[0],shape[1],a.shape[1]//shape[1]
    return a.reshape(sh).mean(-1).mean(1)

Esun_Ch_01 = 441.868715 
Esun_Ch_02 = 663.274497
Esun_Ch_03 = 726.721072
d2 = 0.3

path = '/home/josue/aws/276/17/OR_ABI-L1b-RadF-M3C01_G16_s20172761700388_e20172761711155_c20172761711202.nc'
nc = Dataset(path)
radiance = nc.variables['Rad'][:]
nc.close()
ch1 = (radiance * np.pi * d2) / Esun_Ch_01
ch1 = np.sqrt(ch1)
ch1 = np.maximum(ch1, 0.0)
ch1 = np.minimum(ch1, 1.0)


path = '/home/josue/aws/276/17/OR_ABI-L1b-RadF-M3C02_G16_s20172761700388_e20172761711155_c20172761711192.nc'
nc = Dataset(path)
radiance = nc.variables['Rad'][:]
nc.close()
radiance = rebin(radiance, [10848, 10848])
ch2 = (radiance * np.pi * d2) / Esun_Ch_02
ch2 = np.sqrt(ch2)
ch2 = np.maximum(ch2, 0.0)
ch2 = np.minimum(ch2, 1.0)


path = '/home/josue/aws/276/17/OR_ABI-L1b-RadF-M3C03_G16_s20172761700388_e20172761711155_c20172761711204.nc'
nc = Dataset(path)
radiance = nc.variables['Rad'][:]
nc.close()
ch3 = (radiance * np.pi * d2) / Esun_Ch_03
ch3 = np.sqrt(ch3)
ch3 = np.maximum(ch3, 0.0)
ch3 = np.minimum(ch3, 1.0)
del radiance


#green = 0.48358168 * ch2 + 0.45706946 * ch1 + 0.06038137 * ch3
green = 0.48358168 * ch2 + 0.45603695 * ch1 + 0.06038137 * ch3
del ch3
truecolor = np.stack([ch2, green, ch1], axis=2)
del ch1, ch2, green

truecolor[truecolor == [0, 0.48358168, 0]]=np.nan

fig = plt.figure(frameon=False)
ax = fig.add_axes([0, 0, 1, 1])
ax.axis('off')
im = plt.imshow(truecolor*0.9)
fig.savefig('/home/josue/figura.png', dpi=1200, bbox_inches='tight')
