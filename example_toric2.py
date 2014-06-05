import simulate_toric as st
import random
import load_errors 

n_trials = 100
success_count = 0

size=6
tSteps=5

random.seed(0)


## Load error vector from file
evecs3,evecs4 = load_errors.load("example_errorvec.txt")
error_vector4 = evecs4[evecs4.keys()[0]]



for i in range(n_trials):
    [x,z],[x2,z2] = st.run3D(size,tSteps,error_vector4)

    if x==1 and z==1 and x2==1 and z2==1: success_count+=1


print 'lattice size: ',size
print 'time steps: ', tSteps
print 'random errors applied according the test error vector'
print 
print success_count,' /',n_trials,' were successfully decoded: ',success_count
