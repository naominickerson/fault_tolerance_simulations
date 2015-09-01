import sp
import random
import sys
import os
import imp
import load_errors

random.seed(0)


#run3Dspin(size,errortype,orbit,tsteps,[sdInX,sdInY,sdInZ,jitter,pX,pY,pZ,prep,meas,data],[time,space],edge)


size=8
errortype='normal'
orbit='circle'
tSteps=20
sd=0.01
pDipole=0.001
pJ=0.0004
pX,pY,pZ = 0.001/3,0.001/3,0.001/3
initError = 0.01
measureError = 0.01
dataQubitError=0.002

X,Z,Q = 0,0,0

phaseParameters = [sd,sd,0.5*sd,pJ,pX,pY,pZ,initError,measureError,dataQubitError,pDipole]

n_trials=100
spaceweight=1400
boundary=1200

for i in range(n_trials):
    [x,z] = sp.run3DspinWithDipole(size,errortype,orbit, tSteps,phaseParameters,[1000,spaceweight],boundary)

    X+= 1 if x==1 else 0
    Z+= 1 if z==1 else 0
    Q += 1 if x == 1 and z ==1 else 0


print 'lattice size: ',size
print 'probe orbit: ',orbit
print 'error distribution',errortype
print 'sd in plane',sd
print X,' /',Z,'/',n_trials,'were successfully decoded: ',Q

