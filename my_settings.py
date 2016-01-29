#module for storing the files/parameters/... for the tracking code.
#Is it necessary to reload the import to re-call all functions?

import glob
import os, errno
import numpy as np
import datetime as dt
from mpi4py import MPI


#User settings

commWorld = MPI.COMM_WORLD
myRank = commWorld.Get_rank()
nRanks = commWorld.size
def getLimits_startStop(iStartGlobal, iEndGlobal, iWork=myRank, nWork=nRanks):
  #assign contiguous chunks in a sequence to processors. just leave the leftovers to the last processor(s).
  #when the length isn't divisible by the number of workers, this isn't the best solution but we can optimize for that later.
  
  szChunk = int(np.ceil( (iEndGlobal-iStartGlobal)/float(nWork) )) #interval must cover length s.t. # elements for all but last worker
  if (szChunk<1):
    print 'Check logic in getLimits_startStop for your strange case w/ more workers than elements'
  
  iStart = iStartGlobal+iWork*szChunk
  iEnd = iStart+szChunk-1
  iEnd = min(iEndGlobal,iEnd)
  
  return (iStart,iEnd)

rEarth = 6370.e3 #radius of spherical Earth (m)
dFilter = 300.e3 #radius for whether local extremum is regional extremum
areaOverlap = .01 #fraction of tpv area overlap for candidate correspondence

latThresh = 30.*np.pi/180. #segment N of this latitude (in radians)
trackMinMaxBoth = 0 #0-min, 1-max (2-both shouldn't be used w/o further development)
info = '30N_eraI_1979-2010'
mintimesteps = 8; #minimum number of timesteps to use in tracking

#Possible input types: 'eraI' and 'wrf_trop' thus far
inputType = 'eraI'

#######################################################################################
# USE THIS FOR ERA-INT FILES
#######################################################################################
if (inputType == 'eraI'):
    #Data location and names to pull
    fDirData = '/data01/Research/ERAInt/'
    #filesData = sorted(glob.glob(fDirData+'ecmwf_*.nc'), key=os.path.getmtime)
    dates = range(1979,2011)
    months = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
    filesData = []
    for x in xrange(len(dates)):
        for y in xrange(len(months)):
            fname = fDirData + 'ecmwf_' + months[y] + '_' + str(dates[x]) + '.nc'
            if os.path.isfile(fname) is True:
                filesData.append(fname)
            
    print filesData
#######################################################################################
# USE THIS FOR WRF FILES
#######################################################################################
if (inputType == 'wrf_trop'):
    #Data location and names to pull
    fDirData = '/data01/Research/track_files/20c/nick_tracks/'
    filesData = [fDirData + 'wrf_tracks_75-76.nc']
            
    print filesData

fileMap = fDirData+'wrfout_mapProj.nc' #for inputType=wrf_trop

#time information of input data
deltaT = 6.*60.*60. #timestep between file times (s)
timeStart = dt.datetime(1979,1,1,0) #time=timeStart+iTime*deltaT
timeDelta = dt.timedelta(seconds=deltaT)
#select time intervals within filesData[iFile]...end[-1] means use all times
nFiles = len(filesData)
iTimeStart_fData = [0]*nFiles
iTimeEnd_fData = [-1]*nFiles
if (True): #a quick check of specified times
  if (len(iTimeStart_fData) != nFiles or len(iTimeEnd_fData) != nFiles):
    print "Uhoh, wrong iTime*_data settings in my_settings.py"
    import sys
    sys.exit()


fDirSave = '/data01/Research/ERAInt/tracks/PNA/'
if not os.path.exists(fDirSave):
    os.makedirs(fDirSave)

fMesh = filesData[0]  
fMetr = fDirSave+'fields.nc'
fSegFmt = fDirSave+'seg_{0}.nc'
fSeg = fSegFmt.format(myRank)
fSegFinal = fDirSave+'seg.nc'; fSeg = fSegFinal #for after running seg in parallel...
fCorr = fDirSave+'correspond_horizPlusVert.nc'
fTrackFmt = fDirSave+'tracks_{0}.nc'
fTrack = fTrackFmt.format(myRank)
fTrackFinal = fDirSave+'tracks_low.nc'
fMetrics = fDirSave+'metrics.nc'


#possible input types: eraI, wrf_trop
doPreProc = False
doSeg = True
doMetrics = True
doCorr = True
doTracks = True

def silentremove(filename):
  #from http://stackoverflow.com/questions/10840533/most-pythonic-way-to-delete-a-file-which-may-not-exist
  print "Removing file (if it exists): ",filename
  try:
      os.remove(filename)
  except OSError as e: # this would be "except OSError, e:" before Python 2.6
      if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
          raise # re-raise exception if a different error occured
