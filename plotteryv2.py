import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from matplotlib.collections import PatchCollection
from mpl_toolkits.basemap import Basemap
from shapely.geometry import Point, Polygon, MultiPoint, MultiPolygon
from shapely.prepared import prep
from pysal.esda.mapclassify import Natural_Breaks as nb
from descartes import PolygonPatch
from itertools import chain
from scipy.interpolate import Rbf
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from osgeo import gdal
import shapefile

# unpickle the dataset:  
#df[0] = ID, [1] = name, [2] = elevation, [3] = latitude, [4] = longitude, 
#[5] = Monthly averages: [5][station][year][month], 
#[6] = Average Maximum Temperature: [6][station][month], 
#[7] = Standard Deviation Maximum Temperature: [7][station][month], 
#[8] = monthly maximum temperature anomalies: [8][station][year][month], 
#[9] = Maximum t-score: [9][station][year][month], 
#[10] Monthly minima (see [5]), 
#[11] = Average Minimum Temperature (see[6]), 
#[12] = Standard Deviation Minimum Temperature (see[7]), 
#[13] monthly minimum temperature anomalies (see[8]), 
#[14] Minimum t-score (see[9])

df = pd.read_pickle('biglist.pkl')
#there are fifty states and they are abbreviated like this:
states = ['MA', 'VT', 'NH', 'CT', 'RI','CA','ME', 'OR','WA','UT','NM','AZ','ID','CO','TX','WY','MT','ND','SD','NV','NE','KS','OK','LA','AR','MO','IA','MN','MS','TN','IL','KY','IN','WI','MI','OH','WV','AL','FL','GA','SC','NC','VA','PA','DC','MD','DE','NJ', 'NY','IA']

# generate the basemap and load in the shapefiles
m= Basemap(llcrnrlon=-125., llcrnrlat = 24., urcrnrlon = -66., urcrnrlat = 50., resolution=None, projection='merc')
sf = shapefile.Reader("states")

#set figure
fig = plt.figure()
ax = fig.add_subplot(111)

#generate shapefile vertices lists
verticesx = []
verticesy = []
codes = []

#Import per basemap tutorial: http://basemaptutorial.readthedocs.org/en/latest/clip.html
for shape_rec in sf.shapeRecords():
    if shape_rec.record[4] in states:
        pts = shape_rec.shape.points
        prt = list(shape_rec.shape.parts) + [len(pts)]
        for i in range(len(prt) - 1):
            for j in range(prt[i], prt[i+1]):
                verticesx.append(pts[j][0])
                verticesy.append(pts[j][1])
            codes += [Path.MOVETO]
            codes += [Path.LINETO] * (prt[i+1] - prt[i] -2)
            codes += [Path.CLOSEPOLY]
        vertice = m(verticesx, verticesy)
        vertices = [[j[i] for j in vertice] for i in range(len(vertice[0]))]
        clip = Path(vertices, codes)
        clip = PathPatch(clip, transform = ax.transData)

#Extract Variable of interest (in this case the maximum temperature t-score - for later: loop and automate, save all graphics) 
Zs = [ df[9][x][10][1] for x in range(0, len(df[9]))]

#Because RBF interpolation does not like nan, extract indices of non-nans
inds = pd.notnull(Zs).nonzero()

#collect other parameters of interest
Longs = df[4]
Lats = df[3]

#pare down lists to only non-nan values
zs = [Zs[l] for l in inds[0]]
Longs = [Longs[l] for l in inds[0]]
Lats = [Lats[l] for l in inds[0]]


#prepare longitude and latitude for RBF and mapping to meters coordinates, grid.
lons = np.array([l for l in Longs])
lats = np.array([l for l in Lats])
x , y = m(lons, lats)
longti = np.linspace(min(x)-10000, max(x)+10000, 1000)
latti = np.linspace(min(y)- 30000, max(y)+30000, 543)
XI, YI = np.meshgrid(longti, latti)

#interpolate
rbf = Rbf(x,y,zs,function='thin_plate')
ZI = rbf(XI, YI)

#set levels if desired
levelsz = np.linspace(-5,5,11)
#levelsstd = np.linspace(0,5,6)
#levelsresults= np.linspace(260, 302, 21)
#levelsavg = np.linspace(260,302,21)
#levelsanom=np.linspace(-12,10,23)

#Generate contours from interpolation using specified levels
cs = m.contourf(XI,YI,ZI, levels = levelsz, alpha = 0.5, zorder = 10)

m.colorbar(location='bottom', label='t-score')
plt.title('January 1961 Maximum Temperature Anomaly')
#fill in the state shapes
for contour in cs.collections:
    contour.set_clip_path(clip)
    
#plot the individual datapoints and draw map boundaries if desired 
#m.scatter(x, y, latlon = False,  marker = 'o', c='k',  zorder= 10)
m.readshapefile('states', 'states', drawbounds = True, color = 'w', zorder=11)
#m.savefig('map.tif', dpi=dpi)

plt.show()


