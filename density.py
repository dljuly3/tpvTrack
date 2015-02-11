#####################################################
# density.py
#
# Written by Dylan Lusk
# Last Modified: 02/09/15
#
# Create density tracks for Nick's tracking algorithm
#####################################################

import numpy as np
import datetime as dt
import math
import netCDF4 as nc
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from mpl_toolkits.basemap import Basemap
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm

import basinMetrics
import correspond
import tracks
import my_settings

def plot_density_map(fTracks,mintime):

   mintimesteps = mintime #filter out anything less than this number

   metricNames = ['thetaExtr', 'latExtr', 'lonExtr']
   latInd = metricNames.index('latExtr')
   lonInd = metricNames.index('lonExtr')
   varKey = 'thetaExtr'
   varInd = metricNames.index(varKey); varMin = 270.; varMax = 310.

   trackList, timeList = tracks.read_tracks_metrics(fTrack, metricNames)

   m = Basemap(projection='ortho',lon_0=0,lat_0=89.5, resolution='l')
  
   ax = plt.gca()
   m.drawcoastlines()

   for iTrack,track in enumerate(trackList):
      nTimes = track.shape[0]
      if (True):
         if (nTimes<mintimesteps): 
            continue
    
      lat = track[:,latInd]
      lon = track[:,lonInd]
      x,y = m(lon,lat)
