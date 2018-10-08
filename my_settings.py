#module for storing the files/parameters/... for the tracking code.
#Is it necessary to reload the import to re-call all functions?

import glob
import os, errno
import numpy as np
import datetime as dt

rEarth = 6370.e3 #radius of spherical Earth (m)
dFilter = 300.e3 #radius for whether local extremum is regional extremum
areaOverlap = .01 #fraction of tpv area overlap for candidate correspondence
segRestrictPerc = 10. #percentile of boundary amplitudes to restrict watershed basins [0,100]

latThresh = 30.*np.pi/180. #segment N of this latitude
trackMinMaxBoth = 0 #0-min, 1-max (2-both shouldn't be used w/o further development)

#netcdf files will have this as a global attribute, and some figures will carry this name
#info = '30N_eraI_2006-06-01To09-30'
info = 'demo_eraI_data_2006-08-01To08-04'

#set the working directory of the data
#fDirData = '/data02/cases/summer2006/eraI/pv/'
#fDirData = '/data01/tracks/summer07/eraI/'
fDirData = './example_eraI/'

#enter an explicit list of files or allow the glob.glob function to pick them out for you
#filesData = sorted(glob.glob(fDirData+'eraI_theta-u-v_2pvu_2006-06-01_09-30*'), key=os.path.ge    tmtime)
filesData = sorted(glob.glob(fDirData+'ERAI*.nc'), key=os.path.getmtime)
print filesData

#set the start date/time
timeStart = dt.datetime(2006,8,1,0)

#set directory to save files
#fDirSave = '/data01/tracks/summer07/tpvTrack/'
#fDirSave = '/data01/tracks/summer06/closedContour/'
#fDirSave = '/data01/tracks/wrf/algo/'
fDirSave = './test-tpvTrack_metadata/'

#time information of input data
deltaT = 6.*60.*60. #timestep between file times (s)
timeDelta = dt.timedelta(seconds=deltaT)
#select time intervals within filesData[iFile]...end[-1] means use all times
iTimeStart_fData = [0]
iTimeEnd_fData = [-1]
if (True): #a quick check of specified times
  nFiles = len(filesData)
  if (len(iTimeStart_fData) != nFiles or len(iTimeEnd_fData) != nFiles):
    print "Uhoh, wrong iTime*_data settings in my_settings.py"
    import sys
    sys.exit()

if not os.path.exists(fDirSave):
    os.makedirs(fDirSave)

fMesh = filesData[0]  
fMetr = fDirSave+'fields.nc'
fSeg = fDirSave+'seg.nc'
fCorr = fDirSave+'correspond_horizPlusVert.nc'
fTrack = fDirSave+'tracks_low_horizPlusVert.nc'
fMetrics = fDirSave+'metrics.nc'

inputType = 'eraI'
doPreProc = True
doSeg = True
doMetrics = True
doCorr = True
doTracks = True

#for inputType=wrf_trop
fileMap = fDirData+'wrfout_mapProj.nc'

def silentremove(filename):
  #from http://stackoverflow.com/questions/10840533/most-pythonic-way-to-delete-a-file-which-may-not-exist
  print "Removing file (if it exists): ",filename
  try:
      os.remove(filename)
  except OSError as e: # this would be "except OSError, e:" before Python 2.6
      if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
          raise # re-raise exception if a different error occured
