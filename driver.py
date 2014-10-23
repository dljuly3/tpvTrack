import netCDF4
import matplotlib.pyplot as plt

import my_settings
import preProcess
import llMesh
import segment
import basinMetrics
import correspond
import tracks

def demo():
  #setup -----------------
  info = my_settings.info
  filesData = my_settings.filesData
  fMesh = my_settings.fMesh  
  fMetr = my_settings.fMetr
  fSeg = my_settings.fSeg
  fCorr = my_settings.fCorr
  fTrack = my_settings.fTrack
  fMetrics = my_settings.fMetrics
  
  rEarth = my_settings.rEarth
  dRegion = my_settings.dFilter
  latThresh = my_settings.latThresh
  
  #pre-process ------------------------
  if (False):
    mesh = preProcess.demo_eraI(fMesh, filesData, fMetr, my_settings.rEarth, dRegion, latThresh, info=info)
  else:
    #if already processed input data
    mesh = preProcess.demo_eraI(fMesh, [], fMetr, my_settings.rEarth, dRegion, latThresh)
  
  cell0 = llMesh.Cell(mesh,0)
  if (True):
    print 'index: ', cell0.ind, 'nbrs: ', cell0.get_nbrInds()
  
  #segment --------------------------
  dataMetr = netCDF4.Dataset(fMetr,'r'); nTimes = len(dataMetr.dimensions['time'])
  if (True):
    segment.run_segment(fSeg, info, dataMetr, cell0, mesh)
    segment.run_plotBasins(my_settings.fDirSave, dataMetr, fSeg, mesh)
  
  dataMetr.close()
  
  #spatial metrics ------------------------
  dataMetr = netCDF4.Dataset(fMetr,'r')
  dataSeg = netCDF4.Dataset(fSeg,'r')
  if (True):
    basinMetrics.run_metrics(fMetrics, info, mesh, dataMetr, dataSeg, 0, nTimes-1)
  
  dataMetr.close()
  dataSeg.close()
  
  #basinMetrics.print_metrics(fMetrics)
  
  #time correspondence -----------------
  dataMetr = netCDF4.Dataset(fMetr,'r')
  dataSeg = netCDF4.Dataset(fSeg,'r')
  dataMetrics = netCDF4.Dataset(fMetrics, 'r')
  if (True):
    correspond.run_correspond(fCorr, dataMetr, dataSeg, mesh, my_settings.deltaT, my_settings.trackMinMaxBoth, my_settings.areaOverlap, 0, nTimes-1, dataMetrics)
    correspond.plot_correspondences(my_settings.fDirSave, fCorr, nTimes-1, mesh)
  
  dataMetrics.close()
  dataSeg.close()
  dataMetr.close()
  
  #time tracks -------------------------
  if (True):
    #since appending to fTrack over time, wipe file before starting (if it exists)
    my_settings.silentremove(fTrack)
    
    for iTime in xrange(nTimes-2, -1, -1):
      #tracks.run_tracks(fTrack, fCorr, iTime, nTimes-2, fMetrics=fMetrics)
      tracks.run_tracks(fTrack, fCorr, iTime, nTimes-2, trackOnlyMajor=True)
    tracks.plot_tracks_cells(fTrack, mesh, my_settings.fDirSave)
  
  #time metrics ----------------------

if __name__=='__main__':
  demo()
