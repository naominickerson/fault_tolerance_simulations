import sp
import random

n_trials = 100
success_count = 0

size=5
tSteps=5

random.seed(0)


for i in range(n_trials):
    x,z = sp.run3D(size,tSteps)

#    print [x,z]
    if x==1 and z==1: success_count+=1


print 'lattice size: ',size
print 'time steps: ', tSteps
print 'random errors applied according the test error vector'
print 
print success_count,' /',n_trials,' were successfully decoded: ',success_count
