import math
import copy
import time
import sys
import os
import imp

import load_errors
import toric_lattice
import parametrized_perfect_matching as perfect_matching

home = os.environ['HOME']
#toric_lattice = imp.load_source('toric_lattice','%s/perfect_matching/toric_lattice.py'%home)
#perfect_matching = imp.load_source('perfect_matching','%s/perfect_matching/perfect_matching.py'%home)

#import toric_lattice
#import planar_lattice
#import perfect_matching

        
class Timer():
   def __enter__(self): self.start = time.time()
   def __exit__(self, *args): print time.time() - self.start


testvec4=[0.926639, 0.006904, 0.003904, 0.003904, 0.000012, 0.000024,0.000012,
               0.000048, 0.000048, 0.001062, 0.042477, 0.006868, 0.003904,0.003904,
               0.000012, 0.000024, 0.000012, 0.000048, 0.000048, 0.000147]



        

def squashMatching(size,matching):

   #channel=0 if error_type=="X" else 1

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

           

         
            
            

            
            
                    



########################################################
########################################################
###
###          RUN CODE 
###
########################################################
########################################################

def run2D(size=4,p=0.1):

   L=toric_lattice.PlanarLattice(size)

   L.applyRandomErrors(p,p)
   L.measureStars()
   L.measurePlaquettes()

   

   #L.showArray("errors","Z")
   #L.showArray("stabilizers","X")

   L.findAnyons()
   #print L.positions_anyons_P

   matchingX=perfect_matching.match_toric_2D(size,L.positions_anyons_P)
   matchingZ=perfect_matching.match_toric_2D(size,L.positions_anyons_S)

   #print matching

   L.apply_matching("X",matchingX)
   L.apply_matching("Z",matchingZ)

   #L.showArray("errors","Z")
   #L.showArray("errors","Z")

   return L.measure_logical()












        

def run3Dasynchronous(size=4,tSteps=5,pErr=0.01,pLie=0.01,asynchronicity=1,timespace=[1,1]):
 
  # The asynchronicity factor, A, splits each 'round' of the error correction into A rounds
  # in each round the probably of physical errors is reduced by a factor of A, and the probability
  # of any given stabilizer being measured is 1/A. 

   pMeasure = 1/float(asynchronicity)
   total_timesteps = int(tSteps*asynchronicity)
   p = pErr/asynchronicity


   L=toric_lattice.PlanarLattice(size)
   PL=toric_lattice.Lattice3D(size)

   L.applyRandomErrors(0,0)   # leave this here for initialisation                                                    
   xcount,zcount = 0,0

   L=toric_lattice.PlanarLattice(size)
   PL=toric_lattice.Lattice3D(size)
   
   L.applyRandomErrors(0,0)   # leave this here for initialisation
   
   for i in range(total_timesteps):                     # loop over time      
                
        L.applyRandomErrors(p,p)
        L.measurePlaquettes(pLie,pMeasure)               
        L.measureStars(pLie,pMeasure)                    

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

   return L.measure_logical()





def run3D(size=4,tSteps=5,errorVec=testvec4,timespace=[1,1],stabilizersNotComplete=0):

   L=toric_lattice.PlanarLattice(size)
   PL=toric_lattice.Lattice3D(size)

   L.applyRandomErrors(0,0)   # leave this here for initialisation                                                    
   xcount = 0
   zcount = 0 
   #t0=time.time()
   for i in range(tSteps):                     # loop over time                                                       

        L.measureNoisyStabilizers("plaquette",errorVec,stabilizersNotComplete)
        L.measureNoisyStabilizers("star",errorVec,stabilizersNotComplete)

        #for p0,p1 in L.positions_Q: 
         #  x,z = L.array[p0][p1]
          # if x ==-1: xcount +=1
          # if z ==-1: zcount +=1
         
#        L.showArrayText("stabs")
        PL.addMeasurement(L)         # add the updated 2D lattice to 3D array
#   print xcount, zcount
 #  t1 = time.time()
  # print 'tsteps completed ',t1-t0
   
   L.measurePlaquettes(0)                      # measure one more layer with
   L.measureStars(0)                           # perfect stabilizers and add
   PL.addMeasurement(L)             # this to the parity Lattice

   PL.findAnyons()
#   print 'P anyons', sum([len(_) for _ in PL.anyon_positions_P])
 #  print 'S anyons', sum([len(_) for _ in PL.anyon_positions_S])


   #print PL.anyon_positions_P
  # t2 = time.time()
   #print 'find anyons ',t2-t1

   matchingX=perfect_matching.match_toric_3D(size,PL.anyon_positions_P,timespace)
  # t3 = time.time()
   #print 'matching X ',t3-t2
#   matchingZ=perfect_matching.match_toric_3D(size,PL.anyon_positions_S,timespace)

   flipsX=squashMatching(size,matchingX)
 #  flipsZ=squashMatching(size,matchingZ)
#   t4 = time.time()
 #  print 'squash matching ',t4-t3
   #L.showArray("errors","X")

  # L.apply_flip_array("Z",flipsZ)
   L.apply_flip_array("X",flipsX)

   #L.showArray("errors","X")
   #L.showArray("errors","Z")

   return L.measure_logical()





def run3Dmissing(size=4,tSteps=5,errorVec=testvec4,timespace=[1,1]):

   stabsNotComplete = 0.01

   L=toric_lattice.PlanarLattice(size)
   PL=toric_lattice.Lattice3D(size)

   L.applyRandomErrors(0,0)   # leave this here for initialisation                                                    
   xcount = 0
   zcount = 0 

   for i in range(tSteps):                     # loop over time                                                       

        L.measureNoisyStabilizers("plaquette",errorVec,stabsNotComplete)
        L.measureNoisyStabilizers("star",errorVec,stabsNotComplete)

#        L.showArrayText("stabs")
        PL.addMeasurement(L)         # add the updated 2D lattice to 3D array

   
   L.measurePlaquettes(0)                      # measure one more layer with
   L.measureStars(0)                           # perfect stabilizers and add
   PL.addMeasurement(L)             # this to the parity Lattice

   PL.findAnyons()

   matchingX=perfect_matching.match_toric_3D(size,PL.anyon_positions_P,timespace)
#   matchingZ=perfect_matching.match_toric_3D(size,PL.anyon_positions_S,timespace)

   flipsX=squashMatching(size,matchingX)
 #  flipsZ=squashMatching(size,matchingZ)

  # L.apply_flip_array("Z",flipsZ)
   L.apply_flip_array("X",flipsX)


   return L.measure_logical()











def run3Drandom(size=4,tSteps=5,p=0.05,pLie=0.01,timespace=[1,1]):

   L=toric_lattice.PlanarLattice(size)
   PL=toric_lattice.Lattice3D(size)
   
   L.applyRandomErrors(0,0)   # leave this here for initialisation
   
   for i in range(tSteps):                     # loop over time      
                
        L.applyRandomErrors(p,p)
        L.measurePlaquettes(pLie)               
        L.measureStars(pLie)                    


#        L.showArrayText("all",0)
        #L.constructLists()
        PL.addMeasurement(L)         # add the updated 2D lattice to 3D array

   L.measurePlaquettes(0)                      # measure one more layer with
   L.measureStars(0)                           # perfect stabilizers and add
   PL.addMeasurement(L)             # this to the parity Lattice

   PL.findAnyons()
   #print PL.anyon_positions_P

   matchingX=perfect_matching.match_toric_3D(size,PL.anyon_positions_P,timespace)
   matchingZ=perfect_matching.match_toric_3D(size,PL.anyon_positions_S,timespace)

   flipsX=squashMatching(size,matchingX)
   flipsZ=squashMatching(size,matchingZ)
   
   #L.showArray("errors","X")

   L.apply_flip_array("Z",flipsZ)
   L.apply_flip_array("X",flipsX)

 #  L.showArrayText()
   #L.showArray("errors","X")
   #L.showArray("errors","Z")

   return L.measure_logical()
   














def run3Dtest(size=8,tSteps=100,errorVec=testvec4,timespace=[1,1]):


   errvec_file = "error_vectors/basic_0.txt"
   error_vector3, error_vector4 = [[] if x=={} else x[0.0] for x in load_errors.load(errvec_file)]
   errorVec = error_vector4

#   print error_vector3
 #  print error_vector4

   L=toric_lattice.PlanarLattice(size)
   PL=toric_lattice.Lattice3D(size)

   L.applyRandomErrors(0,0)   # leave this here for initialisation                                                    
   xcount = 0
   zcount = 0 
   #t0=time.time()
   for i in range(tSteps):                     # loop over time                                                       

        L.measureNoisyStabilizers("plaquette",errorVec)
        L.measureNoisyStabilizers("star",errorVec)                                                                   

        #for p0,p1 in L.positions_Q: 
         #  x,z = L.array[p0][p1]
          # if x ==-1: xcount +=1
          # if z ==-1: zcount +=1
           
        PL.addMeasurement(L)         # add the updated 2D lattice to 3D array
#   print xcount, zcount
 #  t1 = time.time()
  # print 'tsteps completed ',t1-t0
   
   L.measurePlaquettes(0)                      # measure one more layer with
   L.measureStars(0)                           # perfect stabilizers and add
   PL.addMeasurement(L)             # this to the parity Lattice

   PL.findAnyons()
#   print 'P anyons', sum([len(_) for _ in PL.anyon_positions_P])
 #  print 'S anyons', sum([len(_) for _ in PL.anyon_positions_S])


   #print PL.anyon_positions_P
  # t2 = time.time()
   #print 'find anyons ',t2-t1

   matchingX=perfect_matching.match_toric_3D(size,PL.anyon_positions_P,timespace)
  # t3 = time.time()
   #print 'matching X ',t3-t2
   matchingZ=perfect_matching.match_toric_3D(size,PL.anyon_positions_S,timespace)

   flipsX=squashMatching(size,matchingX)
   flipsZ=squashMatching(size,matchingZ)
#   t4 = time.time()
 #  print 'squash matching ',t4-t3
#   L.showArray("errors","X")

   L.apply_flip_array("Z",flipsZ)
   L.apply_flip_array("X",flipsX)

 #  L.showArray("errors","X")
   #L.showArray("errors","Z")

   return L.measure_logical()
