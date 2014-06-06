import sp

import random
import load_errors 

n_trials = 20
size=6
tSteps=5

random.seed(0)



#def run3Dphase(size=8,tSteps=8,phaseParameters=0,timespace=[1,1],boundary_weight = 1):


success_count = 0
for i in range(n_trials):
    [x,z] = sp.run3Dspin(size,tSteps)

    if x==1 and z==1: success_count+=1


print 'lattice size: ',size
print 'time steps: ', tSteps
print 
print success_count,' /',n_trials,' were successfully decoded: ',success_count