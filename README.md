This folder includes 5 python files and README.md.  
**1. README.md**
------
Shown as above and follows.

**2. pointExample.py**
----
###### Usages:  
> illustrate the difference between copying pointer of an array and copy the exact value of the same array

**3. lvisRead.py**
----
###### Usages:  
> import "h5py" package to read LVIS data which is stored in the HDF5 file

**4. lvisClass.py**
----
###### Usages:  
> A class to hold LVIS data with methods to read
###### Content:
- "lvisData" class includes functions as follows:
1. __ init __ (self,filename,setElev=False,minX=-100000000,maxX=100000000,minY=-1000000000,maxY=100000000,onlyBounds=False):  
Class initialiser. Calls a function to read LVIS data within bounds;       
minX,minY and maxX,maxY;  
setElev=1 converts LVIS's stop and start;  
elevations to arrays of elevation;  
onlyBounds sets "bounds" to the corner of the area of interest.

2. readLVIS(self,filename,minX,minY,maxX,maxY,onlyBounds):  
Read LVIS data from file.

3. setElevations(self):
Decodes LVIS's RAM efficient elevation;  
format and produces an array of elevations per waveform bin.

4. getOneWave(self,ind):   
Return a single waveform.

5. dumpCoords(self):   
Dump coordinates.

6. dumpBounds(self):   
Dump bounds


**5. processLVIS.py**
----
###### Usages:  
> inherit "lvisData" class from lvisClass.py to build "lvisGround" class, in order to process LVIS data (e.g. calculate statistics, reproject (import "pyproj" package), denoise the signal, set the elevation, find the ground, etc.)
###### Content:
- "lvisGround" class includes functions as follows:
1. estimateGround(self,sigThresh=5,statsLen=10,minWidth=3,sWidth=0.5):  
Processes waveforms to estimate ground.
Only works for bare Earth.
DO NOT USE IN TREES.

2. setThreshold(self,sigThresh):  
Set a noise threshold.

3. CofG(self):  
Find centre of gravity of denoised waveforms   
  **Process:**
  >1. set parameters;
  2. save and process raw data (the number of columns and rows, exact values and formats)
  3. loop over to calculate the center of signal gravity at every point  
  (add up gravity at every position (AKA same "i"):      "waves[i,j]* z[i,j]" ;  
   divide the value above by the sum-up of all waves[i,j] to calculate the mean value;  
   calculate and save the half value of the sum-up gravity at one position)  
  4. loop over to find the wave at the center of signal gravity:  
  sum up gravity again, but quit the loop when the sum-up gravity is larger than the half value.
  5. print out serial numbers of waves at center of gravity

4. reproject(self,inEPSG,outEPSG):  
Reproject footprint coordinates.

5. findStats(self,statsLen=10):  
Finds standard deviation and mean of noise

6. denoise(self,threshold,sWidth=0.5,minWidth=3):  
Denoise waveform data.

**6. lvisExample.py**
----
###### Usages:  
>Import classes built in the .py files above to create objects and call the function to process LVIS data, which can help figure out the center of gravity of signal
###### Process:
1. Read file
2. Set some bounds to achieve suitable "Minimum workable example"
3. create object of "lvisGround"
4. set elevation
5. denoise   
(find statistics; set threshold; denoise the waveform data; find the center of gravity of signal)
6. estimate the ground

References
----------
- Martelli, A., Ravenscroft, A.M. & Holden, S., (2017). Python in a Nutshell Third., Sebastopol: O'Reilly Media, Inc, USA, pp.171-194.

- Andrew Collette. (2014, March). Python and HDF5, O'Reilly Media, Inc, USA,. Retrieved from https://link-gale-com.ezproxy.is.ed.ac.uk/apps/doc/A364854241/LitRC?u=ed_itw&sid=LitRC&xid=55555e2e
