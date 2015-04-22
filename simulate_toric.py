import math
import copy
import time
import sys
import os


import load_errors
import toric_lattice
import parametrized_perfect_matching as perfect_matching


home = os.environ['HOME']

        
class Timer():
   def __enter__(self): self.start = time.time()
   def __exit__(self, *args): print time.time() - self.start


testvec4=[0.926639, 0.006904, 0.003904, 0.003904, 0.000012, 0.000024,0.000012,
               0.000048, 0.000048, 0.001062, 0.042477, 0.006868, 0.003904,0.003904,
               0.000012, 0.000024, 0.000012, 0.000048, 0.000048, 0.000147]



        

def squashMatching(size,matching):


   flip_array=[[1]*(2*size) for _ in range(2*size)]

   m=2*size
    
   for [(pt,p0,p1),(qt,q0,q1)] in matching:

      flips=[]

      d0=(q0-p0)%m
      d1=(q1-p1)%m

      if d0 < m-d0:
         end0=q0
         for x in range(1,d0,2):
            flips+=[[(p0+x)%m,p1]]                
      else:
         end0=p0
         for x in range(1,m-d0,2):
            flips+=[[(q0+x)%m,q1]]
                    
      if d1 < m-d1:
         for y in range(1,d1,2):
            flips+=[[end0,(p1+y)%m]]
      else:
         for y in range(1,m-d1,2):
            flips+=[[end0,(q1+y)%m]]
 
         
      for flip in flips:
         flip_array[flip[0]][flip[1]]*=-1

   return flip_array

           




###
###          RUN CODE 
###


def run2D(size=4,p=0.1):

   L=toric_lattice.PlanarLattice(size)

   L.applyRandomErrors(p,p)
   L.measureStars()
   L.measurePlaquettes()
   
   #Uncomment display function for debugging
   #L.showArrayText("errors","Z")

   L.findAnyons()

   matchingX=perfect_matching.match_toric_2D(size,L.positions_anyons_P)
   matchingZ=perfect_matching.match_toric_2D(size,L.positions_anyons_S)

   L.apply_matching("X",matchingX)
   L.apply_matching("Z",matchingZ)

   return L.measure_logical()









def run3D(size=4,tSteps=5,errorVec=testvec4,timespace=[1,1],stabilizersNotComplete=0):

   L=toric_lattice.PlanarLattice(size)
   PL=toric_lattice.Lattice3D(size)

   xcount = 0
   zcount = 0 

   for i in range(tSteps):                     # loop over time                                                       

        L.measureNoisyStabilizers("plaquette",errorVec,stabilizersNotComplete)
        L.measureNoisyStabilizers("star",errorVec,stabilizersNotComplete)

        PL.addMeasurement(L)         # add the updated 2D lattice to 3D array
   
   L.measurePlaquettes(0)                      # measure one more layer with
   L.measureStars(0)                           # perfect stabilizers and add
   PL.addMeasurement(L)                        # this to the parity Lattice

   PL.findAnyons()

   matchingX=perfect_matching.match_toric_3D(size,PL.anyon_positions_P,timespace)
   matchingZ=perfect_matching.match_toric_3D(size,PL.anyon_positions_S,timespace)

   flipsX=squashMatching(size,matchingX)
   flipsZ=squashMatching(size,matchingZ)

   L.apply_flip_array("Z",flipsZ)
   L.apply_flip_array("X",flipsX)

   return L.measure_logical()









def run3Drandom(size=4,tSteps=5,p=0.05,pLie=0.01,timespace=[1,1]):

   L=toric_lattice.PlanarLattice(size)
   PL=toric_lattice.Lattice3D(size)
   
   for i in range(tSteps):                     # loop over time      
                
        L.applyRandomErrors(p,p)
        L.measurePlaquettes(pLie)               
        L.measureStars(pLie)                    
        PL.addMeasurement(L)         # add the updated 2D lattice to 3D array

   L.measurePlaquettes(0)                      # measure one more layer with
   L.measureStars(0)                           # perfect stabilizers and add
   PL.addMeasurement(L)             # this to the parity Lattice

   PL.findAnyons()

   matchingX=perfect_matching.match_toric_3D(size,PL.anyon_positions_P,timespace)
   matchingZ=perfect_matching.match_toric_3D(size,PL.anyon_positions_S,timespace)

   flipsX=squashMatching(size,matchingX)
   flipsZ=squashMatching(size,matchingZ)
   
   L.apply_flip_array("Z",flipsZ)
   L.apply_flip_array("X",flipsX)

# uncomment to display the final error state of the array
 #  L.showArrayText("errors","X")

   return L.measure_logical()
   

