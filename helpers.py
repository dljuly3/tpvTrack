import numpy as np
import math

def index_2dTo1d(iLat, iLon, nLon):
  """
  Convert a 2-dimensional index to flat 1-dimension:
  
  Arguments:
  iLat - latitude index [0,nLat-1]
  iLon - longitude index [0,nLon-1]
  nLon - number of longitude points
  """
  return iLat*nLon+iLon
  
def index_1dTo2d(ind, nLon):
  """
  Convert a flat 1D index to a 2D index:
  
  Arguments:
  ind - cell index [0,nCells-1]
  nLon - number of longitude points
  """
  iLon = ind%nLon
  iLat = (ind-iLon)/nLon
  return (iLat, iLon)

def flatten_2dTo1d(vals, nLat, nLon):
  """
  #flatten a 2D array so vals[lat][lon] -> vals[iLat*nLon+iLon]
  
  Arguments:
  vals - input array
  nLat - number of latitude points
  nLon - number of longitude points. nCells = nLat*nLon
  """
  
  valsOut = np.ravel(vals)
  return valsOut

def unflatten_1dTo2d(vals, nLat, nLon):
  """
  #unflatten a 1D array so vals[iLat*nLon+iLon] -> vals[lat][lon]
  
  Arguments:
  vals - input array
  nLat - number of latitude points
  nLon - number of longitude points. nCells = nLat*nLon
  """
  
  valsOut = np.reshape(vals, (nLat,nLon))
  return valsOut

def calc_distSphere_multiple(r, lat1, lon1, lat2, lon2):
  """
  Return the distance between 1 latitude/longitude 1 point and >=1 lat/lon2 points on a sphere
  
  Arguments:
  r - radius of sphere
  lat1 - latitude of point 1 (in radians)
  lon1 - longitude of point 1 (in radians)
  lat2 - latitude of point 2 (in radians) (or np.array)
  lon2 - longitude of point 2 (in radians) (or np.array)
  """
  
  dlat = lat2-lat1
  dlon = lon2-lon1
  latTerm = np.sin(.5*dlat); latTerm = latTerm*latTerm;
  lonTerm = np.sin(.5*dlon); lonTerm = lonTerm*lonTerm*np.cos(lat1)*np.cos(lat2);
  dAngle = np.sqrt(latTerm+lonTerm)
  dist = 2.*r*np.arcsin(dAngle)
  
  return dist

def distance_on_unit_sphere(lat1, long1, lat2, long2):

    '''
    Shamelessly taken from: http://www.johndcook.com/blog/python_longitude_latitude/
    '''
 
    # Convert latitude and longitude to
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
         
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
         
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
         
    # Compute spherical distance from spherical coordinates.
         
    # For two locations in spherical coordinates
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) =
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
     
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) +
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )
 
    # Remember to multiply arc by the radius of the earth
    # in your favorite set of units to get length.
    return arc
