'''
An example of how to use the 
LVIS python scripts
'''

from processLVIS import lvisGround



if __name__=="__main__":
  '''Main block'''

  filename='/geos/netdata/avtrain/data/3d/oosa/week4/lvis_antarctica/ILVIS1B_AQ2015_1014_R1605_070717.h5'

  # find bounds
  b=lvisGround(filename,onlyBounds=True)

  # set some bounds
  x0=b.bounds[0]
  y0=b.bounds[1]
  x1=(b.bounds[2]-b.bounds[0])/150+b.bounds[0]
  y1=(b.bounds[3]-b.bounds[1])/150+b.bounds[1]


  # read in bounds
  lvis=lvisGround(filename,minX=x0,minY=y0,maxX=x1,maxY=y1)

  # set elevation
  lvis.setElevations()

  # denoise test
  lvis.findStats()
  threshold=lvis.meanNoise+5*lvis.stdevNoise
  lvis.denoise(threshold)
  lvis.CofG()

  # find the ground
  lvis.estimateGround()