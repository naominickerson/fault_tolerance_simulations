import sp
import random
import sys
import os
import imp
import load_errors

random.seed(0)


#run3Dspin(size,errortype,orbit,tsteps,[sdInX,sdInY,sdInZ,jitter,pX,pY,pZ,prep,meas,data],[time,space],edge)


size=10
errortype='normal'
orbit='circle'
tSteps=20
sd=0.1

X,Z,Q = 0,0,0

n_trials=1500
spaceweight=1400
boundary=1200

for i in range(n_trials):
    [x,z] = sp.run3Dspin(size,errortype,orbit, tSteps,[sd,sd,0.5*sd,0.0004,0.001/3,0.001/3,0.001/3,0.01,0.05,0.002],[1000,spaceweight],boundary)

    X+= 1 if x==1 else 0
    Z+= 1 if z==1 else 0
    Q += 1 if x == 1 and z ==1 else 0


print 'lattice size: ',size
print 'probe orbit: ',orbit
print 'error distribution',errortype
print 'sd in plane',sd
print X,' /',Z,'/',n_trials,'were successfully decoded: ',Q

