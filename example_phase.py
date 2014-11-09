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
sd=0.1

sdInX = sd
sdInY= sd
sdInZ=sd*0.5
jitter = 0.0004
pX=0.001/3
pY=0.01/3
pZ=0.01/3
prep = 0.01
meas = 0.05
data = 0.002

X,Z,Q = 0,0,0

n_trials=10
spaceweight=1400
boundary=1200

corrected = 0

for i in range(n_trials):

    [x,z] = sp.run3Dspin(size,errortype,orbit, tSteps,[sdInX,sdInY,sdInZ,jitter,pX,pY,pZ,prep,meas,data],[1000,spaceweight],boundary)

    corrected+=1 if [x,z]==[1,1] else 0
    X+= 1 if x==1 else 0
    Z+= 1 if z==1 else 0
    Q += 1 if x == 1 and z ==1 else 0


print 'lattice size: ',size
print 'probe orbit: ',orbit
print 'error distribution',errortype
print 'sd in plane',sd
print corrected,'/',n_trials,'were successfully decoded: '

