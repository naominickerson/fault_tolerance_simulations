import sp
import random
import sys
import os
import imp
import load_errors

home = os.environ['HOME']
sp = imp.load_source('sp','%s/perfect_matching-master-3/sp.py'%home)

random.seed(0)

try:
    size, errortype, tSteps, sd, output_file = sys.argv[1:]
    size = int(size)
    errortype=str(errortype)
    tSteps=int(tSteps)
    sd = float(sd)
except:
    print "Usage: [size] [errortype] [tSteps] [sdPlane] [output_file] "
    sys.exit(-1)

#run3Dspin(size,errortype,tsteps,[sdInX,sdInY,sdInZ,jitter,pX,pY,pZ,prep,meas,data],[time,space],edge)

X,Z,Q = 0,0,0

n_trials=1500
timeweight=1400
boundary=1200

for i in range(n_trials):
    [x,z] = sp.run3Dspin(size,errortype,tSteps,[sd,sd,0.5*sd,0.0004,0.001/3,0.001/3,0.001/3,0.01,0.05,0.002],[1000,timeweight],boundary)

    X+= 1 if x==1 else 0
    Z+= 1 if z==1 else 0
    Q += 1 if x == 1 and z ==1 else 0


f = open(output_file, 'a')
f.write("%d %f %d %d %d %d| %d %d %d\n"%(size, sd, n_trials, tSteps,timeweight,boundary, X, Z, Q))
f.close()

