import simulate_toric as st
import random

n_trials = 100
success_count = 0

size=12
tSteps=1
p=0.05
pLie=0.0

random.seed(1)


for i in range(n_trials):
    [x1,z1],[x2,z2]= st.run3Drandom(size,tSteps,p,pLie)

#    print [x,z]
    if x1==1 and z1==1 and x2==1 and z1==1: success_count+=1


print 'lattice size: ',size
print 'time steps: ', tSteps
print 'random errors applied with probability p=',p
print 'lying stabilizer measurements with pLie ',pLie
print 
print success_count,' /',n_trials,' were successfully decoded: ',success_count
