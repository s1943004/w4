
'''
Some example functions for processing LVIS data
'''

#######################################

import numpy as np
from lvisClass import lvisData
from pyproj import Proj, transform
from scipy.ndimage.filters import gaussian_filter1d 


#######################################

class lvisGround(lvisData):
  '''
  LVIS class with extra processing steps
  '''

  #######################################################

  def estimateGround(self,sigThresh=5,statsLen=10,minWidth=3,sWidth=0.5):
    '''
    Processes waveforms to estimate ground
    Only works for bare Earth. DO NOT USE IN TREES
    '''
    # find noise statistics
    self.findStats(statsLen=statsLen)

    # set threshold
    threshold=self.setThreshold(sigThresh)


    # remove background
    self.denoise(threshold,minWidth=minWidth,sWidth=sWidth)

    # find centre of gravity of remaining signal
    self.CofG()


  #######################################################

  def setThreshold(self,sigThresh):
    '''
    Set a noise threshold
    '''
    threshold=self.meanNoise+sigThresh*self.stdevNoise
    return(threshold)


  #######################################################

  def CofG(self):
    '''
    Find centre of gravity of denoised waveforms
    '''
    m = self.nWaves # the number of points
    n = self.nBins # the number of waves
    z = np.empty((m,n)) 
    deWave = np.copy(self.denoised)
    s = np.empty(m, dtype = float) # sum of gravity at one point
    s_w = np.empty(m, dtype = float) # sum of waves at one point 
    CenterofGravity = np.empty(m, dtype = float) # weighted average gravity at one point
    
    # half value of the sum of gravity to find the wave at the center of gravity
    h_s = np.empty(m, dtype = float)
    h_s_w = np.empty(m, dtype = float)
    wave_cofg = np.empty(m, dtype = int)
    h = np.empty(m, dtype = float)
    
    # loop over to calculate the center of signal gravity at every point
    for i in range(0,m):
        s[i] = 0
        s_w[i] = 0
        res=(self.lZ0[i]-self.lZN[i])/n
        z[i]=np.arange(self.lZ0[i],self.lZN[i],-1.0*res)   # returns an array of floats
        for j in range(0,n):
           s[i] = s[i] + deWave[i,j]*z[i,j]
           s_w[i] = s_w[i]+deWave[i,j]
           if (j==n-1):
               CenterofGravity[i] = s[i]/s_w[i]
               h[i] = s[i]/2
    
    # loop over to find the wave at the center of signal gravity
    for i in range(0,m):
        h_s[i] = 0
        h_s_w[i] = 0
        res=(self.lZ0[i]-self.lZN[i])/n
        z[i]=np.arange(self.lZ0[i],self.lZN[i],-1.0*res)   # returns an array of floats
        for j in range(0,n):
           h_s[i] = h_s[i] + deWave[i,j]*z[i,j]
           if (h_s[i]>h[i]):
               wave_cofg[i] = deWave[i,j]
               print('Point',i+1,'center of gravity is at wave',deWave[i,j])
               break

    #print(m)         
    #print(CenterofGravity)


  #######################################################

  def reproject(self,inEPSG,outEPSG):
    '''
    Reproject footprint coordinates
    '''
    # set projections
    inProj=Proj(init="epsg:"+str(inEPSG))
    outProj=Proj(init="epsg:"+str(outEPSG))
    # reproject data
    x,y=transform(inProj,outProj,self.lon,self.lat)
    self.lon=x
    self.lat=y


  ##############################################

  def findStats(self,statsLen=10):
    '''
    Finds standard deviation and mean of noise
    '''

    # make empty arrays
    self.meanNoise=np.empty(self.nWaves)
    self.stdevNoise=np.empty(self.nWaves)

    # determine number of bins to calculate stats over
    res=(self.z[0,0]-self.z[0,-1])/self.nBins    # range resolution
    noiseBins=int(statsLen/res)   # number of bins within "statsLen"

    # loop over waveforms
    for i in range(0,self.nWaves):
      self.meanNoise[i]=np.mean(self.waves[i,0:noiseBins])
      self.stdevNoise[i]=np.std(self.waves[i,0:noiseBins])


  ##############################################

  def denoise(self,threshold,sWidth=0.5,minWidth=3):
    '''
    Denoise waveform data
    '''

    # find resolution
    res=(self.z[0,0]-self.z[0,-1])/self.nBins    # range resolution

    # make array for output
    self.denoised=np.full((self.nWaves,self.nBins),0)

    # loop over waves
    for i in range(0,self.nWaves):
      print("Denoising wave",i+1,"of",self.nWaves)

      # subtract mean background noise
      self.denoised[i]=self.waves[i]-self.meanNoise[i]

      # set all values less than threshold to zero
      self.denoised[i,self.denoised[i]<threshold[i]]=0.0

      # minimum acceptable width
      binList=np.where(self.denoised[i]>0.0)[0]
      for j in range(0,binList.shape[0]):       # loop over waveforms
        if((j>0)&(j<(binList.shape[0]-1))):    # are we in the middle of the array?
          if((binList[j]!=binList[j-1]+1)|(binList[j]!=binList[j+1]-1)):  # are the bins consecutive?
            self.denoised[i,binList[j]]=0.0   # if not, set to zero

      # smooth
      self.denoised[i]=gaussian_filter1d(self.denoised[i],sWidth/res)


#############################################################

