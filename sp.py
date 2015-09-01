
import sys
import os
import time
import math
import copy
import spin_lattice

import load_errors
import planar_lattice
import planar_lattice_P




home = os.environ['HOME']


import perfect_matching





        
class Timer():
   def __enter__(self): self.start = time.time()
   def __exit__(self, *args): print time.time() - self.start





        



def squashMatching(size,error_type,matching):

   channel=0 if error_type=="X" else 1

   flip_array=[[1]*(2*size+1) for _ in range(2*size+1)]

#   m=2*size

   for [(pt,p0,p1),(qt,q0,q1)] in matching:


      flips = []
      # if both matched errors are at boundaries: do nothing
#      if channel==1 and (p1==-1 or p1==size*2+1)and(q1==-1 or q1==size*2+1):
 #        flips+=[]

               
  #    elif channel==0 and (p0==-1 or p0==size*2+1)and(q0==-1 or q0==size*2+1):
   #      flips+=[]
    
      if (p0 in [-1,size*2+1] and q0 in [-1,size*2+1]) or (p1 in [-1,size*2+1] and q1 in [-1,size*2+1]):
         flips+=[]

      else:

         s0=int(math.copysign(1,q0-p0))
         s1=int(math.copysign(1,q1-p1))
         
         range0=range(1,abs(q0-p0),2)
         range1=range(1,abs(q1-p1),2)         
         for x in range1:
            flips+=[[p0,p1+s1*x]]
         for y in range0:
            flips+=[[p0+s0*y,q1]]

         
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




testvec4=[0.926639, 0.006904, 0.003904, 0.003904, 0.000012, 0.000024,0.000012,
               0.000048, 0.000048, 0.001062, 0.042477, 0.006868, 0.003904,0.003904,
               0.000012, 0.000024, 0.000012, 0.000048, 0.000048, 0.000147]

testvec3=[0.96288, 0.003438, 0.00132, 0.00132, 0.000002, 0.000006,
               0.000002, 0.000018, 0.000018, 0.002292, 0.021877, 0.002552, 0.00132,
               0.00132, 0.000002, 0.000006, 0.000002, 0.000018, 0.000018, 0.002552]






def run2D(size=4,p=0.03,pLie=0,showArray=False):

   L=planar_lattice.PlanarLattice(size)

   L.applyRandomErrors(p,p)
   L.measureStars(pLie)
   L.measurePlaquettes(pLie)

   #L.showArray("errors","X")
   #L.showArray("stabilizers","X")

   #L.showArrayText("errors","Z")
   #L.showArrayText("stabilizers","X")

   L.findAnyons()

   matchingX=perfect_matching.match_planar_2D(size,"plaquette",L.positions_anyons_P)
   matchingZ=perfect_matching.match_planar_2D(size,"star",L.positions_anyons_S)

   
   L.apply_matching("X",matchingX)
   L.apply_matching("Z",matchingZ)
   
   if showArray==True:
      L.showArrayText("errors","X")
      L.showArrayText("errors","Z")

   return L.measure_logical()






def run3Drandom(size=4,tSteps=5,p=0.05,pLie=0.00,timespace = [1,1],showTextArray=False):

   t0 = time.time()
   L=planar_lattice.PlanarLattice(size)
   PL=planar_lattice.PlanarLattice3D(size)
   
   L.applyRandomErrors(0,0)   # leave this here for initialisation
   

   for i in range(tSteps):                     # loop over time      
                
      L.applyRandomErrors(p,p)
      L.measurePlaquettes(pLie)               
      L.measureStars(pLie)                    

        
        #L.constructLists()
      PL.addMeasurement(L)         # add the updated 2D lattice to 3D array



   L.measurePlaquettes(0)                      # measure one more layer with
   L.measureStars(0)                           # perfect stabilizers and add
   PL.addMeasurement(L)             # this to the parity Lattice
#   L.showArray("stabilizers","X")
#   L.showArray("errors","X")

   if showTextArray==True: L.showArrayText("errors","X")
   
   PL.findAnyons()

   matchingX=perfect_matching.match_planar_3D(size,"plaquette",PL.anyon_positions_P,timespace)
   matchingZ=perfect_matching.match_planar_3D(size,"star",PL.anyon_positions_S,timespace)


   flipsX=squashMatching(size,"X",matchingX)
   flipsZ=squashMatching(size,"Z",matchingZ)
   
   #L.showArray("errors","X")

   L.apply_flip_array("Z",flipsZ)
   L.apply_flip_array("X",flipsX)
#   L.showArray("errors","X")
   #L.showArray("errors","X")
   #L.showArray("errors","Z")

   return L.measure_logical()
   






#---------------------------------------------







        






def run3D(size=4,tSteps=5,errorVec3 = testvec4, errorVec4=testvec4,timespace=[1,1],boundary_weight = 1,stabilizersNotComplete=0):


   t0 = time.time()
   L=planar_lattice.PlanarLattice(size)
   PL=planar_lattice.PlanarLattice3D(size)

   L.applyRandomErrors(0,0)   # leave this here for initialisation                                                    


#   t1 = time.time()
#   print 'initialisation ',t1-t0
   for i in range(tSteps):                     # loop over time                                                       

        L.measureNoisyStabilizers("plaquette",errorVec3, errorVec4,stabilizersNotComplete)
        L.measureNoisyStabilizers("star",errorVec3,errorVec4,stabilizersNotComplete)                                
        PL.addMeasurement(L)         # add the updated 2D lattice to 3D array

#        L.showArrayText("stabs")

   L.measurePlaquettes(0)                      # measure one more layer with
   L.measureStars(0)                           # perfect stabilizers and add
   PL.addMeasurement(L)             # this to the parity Lattice

   PL.findAnyons()
   
#   print 'P anyons', sum([len(_) for _ in PL.anyon_positions_P])
 #  print 'S anyons', sum([len(_) for _ in PL.anyon_positions_S])
   

#   t2 = time.time()
#   print 'loop over timeslices ', t2 -t1  

   matchingX=perfect_matching.match_planar_3D(size,"plaquette",PL.anyon_positions_P,timespace,boundary_weight)

#   t3 = time.time()
 #  print 'perfect matching ', t3 -t2  


   #matchingZ=perfect_matching.match_toric_3D(size,PL.anyon_positions_S,timespace)

   flipsX=squashMatching(size,"X",matchingX)
   #flipsZ=squashMatching(size,matchingZ)
#   t4 = time.time()
 #  print 'squash matching ',t4-t3
#   L.showArray("errors","X")

   #L.apply_flip_array("Z",flipsZ)
   L.apply_flip_array("X",flipsX)

 #  L.showArray("errors","X")
   #L.showArray("errors","Z")

   return L.measure_logical()











def run3Dphase(size=8,tSteps=8,phaseParameters=0,timespace=[1,1],boundary_weight = 1):

# choose phaseParameters=0 to take the default values (as below )
# otherwise this should be a list of the form       [sdInX,sdInYsdInZ,Pj,prX,prY,prZ,initStateError,measureError]

   L=planar_lattice_P.PlanarLattice(size)


#   generateArray(sdInX=0.01,sdInY=0.01,sdInZ=0.01,Pj=0.0016,prX=0.01/3,prY=0.01/3,prZ=0.01/3,initStateError=0.01,measureError=0.01): Default values    
   if phaseParameters ==0:
      pX,pY,pZ=0.002,0.002,0.002
      L.generateArray()
      d_error=0
   else: 
      sdInX,sdInY,sdInZ,Pj,prX,prY,prZ,initStateError,measureError,dataQubitError=phaseParameters
#      print "sp.run3Dphase sdInZ =",sdInZ

      L.generateArray(sdInX,sdInY,sdInZ,Pj,prX,prY,prZ,initStateError,measureError)
      d_error = dataQubitError/3.
   
 #     print L.errorArray[1][2][0]


   PL=planar_lattice.PlanarLattice3D(size)

#   L.applyRandomErrors(0,0)   # leave this here for initialisation                                                    
   

   for i in range(tSteps):                     # loop over time                                                       

      L.measureNoisyStabilizers("plaquette")
      #L.measurePlaquettes(0)
      L.applyRandomErrorsXYZ(d_error,d_error,d_error)
       
      L.measureNoisyStabilizers("star")
      #L.measureStars(0) 
      L.applyRandomErrorsXYZ(d_error,d_error,d_error)
      PL.addMeasurement(L)         # add the updated 2D lattice to 3D array

   L.measurePlaquettes(0)                      # measure one more layer with
   L.measureStars(0)                           # perfect stabilizers and add
   PL.addMeasurement(L)             # this to the parity Lattice

   PL.findAnyons()
   


   matchingX=perfect_matching.match_planar_3D(size,"plaquette",PL.anyon_positions_P,timespace,boundary_weight)
   matchingZ=perfect_matching.match_planar_3D(size,"star",PL.anyon_positions_S,timespace,boundary_weight)

   flipsX=squashMatching(size,"X",matchingX)
   flipsZ=squashMatching(size,"Z",matchingZ)



   L.apply_flip_array("X",flipsX)
   L.apply_flip_array("Z",flipsZ)


   return L.measure_logical()







def run3Dspin(size=8,errortype='normal',orbit='abrupt',tSteps=8,phaseParameters=0,timespace=[1,1],boundary_weight = 1):

# choose phaseParameters=0 to take the default values (as below )
# otherwise this should be a list of the form       [sdInX,sdInYsdInZ,Pj,prX,prY,prZ,initStateError,measureError]

   L=spin_lattice.SpinLattice(size)


#   generateArray(sdInX=0.01,sdInY=0.01,sdInZ=0.01,Pj=0.0016,prX=0.01/3,prY=0.01/3,prZ=0.01/3,initStateError=0.01,measureError=0.01): Default values    
   if phaseParameters ==0:
      pX,pY,pZ=0.002,0.002,0.002
      L.generateArray()
      d_error=0
   else: 
      sdInX,sdInY,sdInZ,Pj,prX,prY,prZ,initStateError,measureError,dataQubitError=phaseParameters
#      print "sp.run3Dphase sdInZ =",sdInZ

      L.generateArray(errortype,orbit,sdInX,sdInY,sdInZ,Pj,prX,prY,prZ,initStateError,measureError)
      d_error = dataQubitError/3.
   
 #     print L.errorArray[1][2][0]


   PL=planar_lattice.PlanarLattice3D(size)

   L.applyRandomErrors(0,0)   # leave this here for initialisation                                                    
   

   for i in range(tSteps):                     # loop over time                                                       

      L.measureNoisyStabilizers("plaquette")
      #L.measurePlaquettes(0)
      L.applyRandomErrorsXYZ(d_error,d_error,d_error)
       
      L.measureNoisyStabilizers("star")
      #L.measureStars(0) 
      L.applyRandomErrorsXYZ(d_error,d_error,d_error)
      PL.addMeasurement(L)         # add the updated 2D lattice to 3D array

   L.measurePlaquettes(0)                      # measure one more layer with
   L.measureStars(0)                           # perfect stabilizers and add
   PL.addMeasurement(L)             # this to the parity Lattice

   PL.findAnyons()
   


   matchingX=perfect_matching.match_planar_3D(size,"plaquette",PL.anyon_positions_P,timespace,boundary_weight)
   matchingZ=perfect_matching.match_planar_3D(size,"star",PL.anyon_positions_S,timespace,boundary_weight)

   flipsX=squashMatching(size,"X",matchingX)
   flipsZ=squashMatching(size,"Z",matchingZ)



   L.apply_flip_array("X",flipsX)
   L.apply_flip_array("Z",flipsZ)


   return L.measure_logical()



def run3DspinWithDipole(size=8,errortype='normal',orbit='abrupt',tSteps=8,phaseParameters=0,timespace=[1,1],boundary_weight = 1):

# choose phaseParameters=0 to take the default values (as below )
# otherwise this should be a list of the form       [sdInX,sdInYsdInZ,Pj,prX,prY,prZ,initStateError,measureError]

   L=spin_lattice.SpinLattice(size)

   ## GENERATE SPIN ARRAY
#   generateArray(sdInX=0.01,sdInY=0.01,sdInZ=0.01,Pj=0.0016,prX=0.01/3,prY=0.01/3,prZ=0.01/3,initStateError=0.01,measureError=0.01): Default values    
   if phaseParameters ==0:
      pX,pY,pZ=0.002,0.002,0.002
      pDipole=0.001
      L.generateArray()
      d_error=0
   else: 
      sdInX,sdInY,sdInZ,Pj,prX,prY,prZ,initStateError,measureError,dataQubitError,pDipole=phaseParameters
      d_error = dataQubitError/3.
      L.generateArray(errortype,orbit,sdInX,sdInY,sdInZ,Pj,prX,prY,prZ,initStateError,measureError)

   
   ## GENERAGE LATTICE 
   PL=planar_lattice.PlanarLattice3D(size)
   L.applyRandomErrors(0,0)   # leave this here for initialisation                                                    
   

   for i in range(tSteps):                     # loop over time                                                       

      L.measureNoisyStabilizers("plaquette")
      L.applyRandomErrorsXYZ(d_error,d_error,d_error)
      L.applyDipoleErrors(pDipole)

      L.measureNoisyStabilizers("star")
      L.applyRandomErrorsXYZ(d_error,d_error,d_error)
      L.applyDipoleErrors(pDipole)

      PL.addMeasurement(L)         # add the updated 2D lattice to 3D array

   L.measurePlaquettes(0)                      # measure one more layer with
   L.measureStars(0)                           # perfect stabilizers and add
   PL.addMeasurement(L)             # this to the parity Lattice

   PL.findAnyons()
   
   matchingX=perfect_matching.match_planar_3D(size,"plaquette",PL.anyon_positions_P,timespace,boundary_weight)
   matchingZ=perfect_matching.match_planar_3D(size,"star",PL.anyon_positions_S,timespace,boundary_weight)

   flipsX=squashMatching(size,"X",matchingX)
   flipsZ=squashMatching(size,"Z",matchingZ)



   L.apply_flip_array("X",flipsX)
   L.apply_flip_array("Z",flipsZ)


   return L.measure_logical()







def run3Dtest(size=8,tSteps=100,errorVec3 = testvec4, errorVec4=testvec4,timespace=[1,1],boundary_weight = 1):

   errvec_file = "error_vectors/basic_0.txt"
   errorVec3, errorVec4 = [[] if x=={} else x[0.0] for x in load_errors.load(errvec_file)]
   

   t0 = time.time()
   L=planar_lattice.PlanarLattice(size)
   PL=planar_lattice.PlanarLattice3D(size)

   L.applyRandomErrors(0,0)   # leave this here for initialisation                                                    


#   t1 = time.time()
#   print 'initialisation ',t1-t0
   for i in range(tSteps):                     # loop over time                                                       

        L.measureNoisyStabilizers("plaquette",errorVec3, errorVec4)
        L.measureNoisyStabilizers("star",errorVec3,errorVec4)                                
        PL.addMeasurement(L)         # add the updated 2D lattice to 3D array


   L.measurePlaquettes(0)                      # measure one more layer with
   L.measureStars(0)                           # perfect stabilizers and add
   PL.addMeasurement(L)             # this to the parity Lattice

   PL.findAnyons()
   
#   print 'P anyons', sum([len(_) for _ in PL.anyon_positions_P])
 #  print 'S anyons', sum([len(_) for _ in PL.anyon_positions_S])
   

#   t2 = time.time()
#   print 'loop over timeslices ', t2 -t1  

   matchingX=perfect_matching.match_planar_3D(size,"plaquette",PL.anyon_positions_P,timespace,boundary_weight)

#   t3 = time.time()
 #  print 'perfect matching ', t3 -t2  


   #matchingZ=perfect_matching.match_toric_3D(size,PL.anyon_positions_S,timespace)

   flipsX=squashMatching(size,"X",matchingX)
   #flipsZ=squashMatching(size,matchingZ)
#   t4 = time.time()
 #  print 'squash matching ',t4-t3
#   L.showArray("errors","X")
   
   Lbefore = copy.copy(L)

   #L.apply_flip_array("Z",flipsZ)
   L.apply_flip_array("X",flipsX)

   if L.measure_logical[0]==-1:

      Lbefore.showArray("errors","X")
      L.showArray("errors","X")
      
   #L.showArray("errors","Z")

   return L.measure_logical()








def run3Dshow(size=8,tSteps=20,errorVec3 = testvec4, errorVec4=testvec4,timespace=[1,1],boundary_weight = 1,stabilizersNotComplete=0):


   L=planar_lattice.PlanarLattice(size)
   PL=planar_lattice.PlanarLattice3D(size)

   L.applyRandomErrors(0,0)   # leave this here for initialisation                                                    


#   t1 = time.time()
#   print 'initialisation ',t1-t0
   for i in range(tSteps):                     # loop over time                                                       

        L.measureNoisyStabilizers("plaquette",errorVec3, errorVec4,stabilizersNotComplete)
        L.measureNoisyStabilizers("star",errorVec3,errorVec4,stabilizersNotComplete)                                
        PL.addMeasurement(L)         # add the updated 2D lattice to 3D array


   L.measurePlaquettes(0)                      # measure one more layer with
   L.measureStars(0)                           # perfect stabilizers and add
   PL.addMeasurement(L)             # this to the parity Lattice

   PL.findAnyons()
   
   


   matchingX=perfect_matching.match_planar_3D(size,"plaquette",PL.anyon_positions_P,timespace,boundary_weight)


#   t3 = time.time()
 #  print 'perfect matching ', t3 -t2  


   #matchingZ=perfect_matching.match_toric_3D(size,PL.anyon_positions_S,timespace)

   flipsX=squashMatching(size,"X",matchingX)
   #flipsZ=squashMatching(size,matchingZ)
#   t4 = time.time()
 #  print 'squash matching ',t4-t3


   Lbefore = copy.deepcopy(L)

   #L.apply_flip_array("Z",flipsZ)
   L.apply_flip_array("X",flipsX)
   log = L.measure_logical()

   if log[0]==-1:

      print 'P anyons', sum([len(_) for _ in PL.anyon_positions_P])
      print PL.anyon_positions_P
      print matchingX
      for x in flipsX:
         print x
      
      perfect_matching.match_planar_3D(size,"plaquette",PL.anyon_positions_P,timespace,boundary_weight,True)
   
      Lbefore.showArray("errors","X")
      L.showArray("errors","X")
      
   #L.showArray("errors","Z")



   return L.measure_logical()
