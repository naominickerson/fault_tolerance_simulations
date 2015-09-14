A Python library for fault tolerance simulations of the surface code
using the [Blossom 5 implementation by Kolgomorov](http://pub.ist.ac.at/~vnk/software.html) [1] of Edmond's perfect matching algorithm [2].

Three different fault tolerance scenarios are covered by this library

* Surface code (planar and toric) under random noise
* Surface code (planar and toric) under noise defined by a superoperator description of noisy stabilizer measurements
* Planar code implemented in solid state spins

### Compiling the perfect matching code

Use command ``make`` in directory blossom5/ to compile the perfect matching code to be used by the decoder. 

# Surface code under random noise


## Toric code under random noise

```python

import st

size = 8    # The lattice dimension, L. Number of qubits = 2*L^2
tSteps = 8  # The number of complete rounds of stabilizer measurement
pErr = 0.1  # The probability of a physical error on each qubit in any one round of measurement
pLie = 0.05 # The probability that a stabilizer outcome is misreported

result = st.run3Drandom(size,tSteps,pErr,pLie)

```
The result is a vector describing the state of the encoded logical qubits after error correction has been attempted. E.g. 

```python
result = [[1,1],[-1,1]]
```

This means that the first logical qubit has no logical error, while the second logical qubit has ended up with an X flip. 

This function should be run a large number of times to build up statistics on the success probability of the decoder under the given error rates.


## Planar code under random noise

This functions very similarly to the toric code 

```python

import sp

result = sp.run3Drandom(size,tSteps,pErr,pLie)

```

Since the planar code only encodes one qubit, the result is now just an array of 2 elements, e.g.

```python
result = [1,-1]
```
would correspond to the case where a Z flip had occurred on the logical qubit after the attempted error correction. 


# Error described by a stabilizer superoperator

This variant of the code puts a more general form of errors into the code, characterised by the superoperator describing the true (noisy) process of measuring each stabilizer. This superoperator provides a full description of the noisy measurement, and if physical errors are made up of randomly applied Pauli operations, this superoperator can be decomposed into Kraus operators that are simply some product of Pauli operations on the qubits in the stabilizer combined with a possible misreported stabilizer outcome. For more detail see [[3](http://www.nature.com/ncomms/journal/v4/n4/abs/ncomms2773.html)], [[4](http://arxiv.org/abs/1406.0880)].

This superoperator decomposition is specified through a text file of the form found in ``` example_error_vec.txt ```. 

##Toric Code


### Defining the noise model

For the toric code, all stabilizer measurements are 4 body operations, so only one superoperator must be specified. If we measure a stabilizer which, if noiseless, should return an EVEN (+1) parity outcome. Physical errors occuring during the measurement circuit, however, will sometimes result in a different operation even when an EVEN result is reported. The input to the toric code simulator takes as input the probabilities of the following possibilities, where for example EVEN,IIXX describes the case where an even parity projection is followed by X errors on 2 of the 4 qubits (in any configuration). Only errors of up to two qubits are specified since 3 or more qubit errors are very unlikely to occur in the low error regime. 

<table>
  <thead>
    <tr>
      <td> Parity projection </td>
      <td> Qubit errors </td>
      <td> Probability </td>
    </tr>
  </thead>
  <tbody>
    <tr><td> EVEN </td><td> I I I I </td><td>p<sub>EVEN,0</sub></tr>
    <tr><td> EVEN </td><td> I I I Z </td><td>p<sub>EVEN,1</sub></tr>
    <tr><td> EVEN </td><td> I I I X </td><td>p<sub>EVEN,2</sub></tr>
    <tr><td> EVEN </td><td> I I I Y </td><td>p<sub>EVEN,3</sub></tr>
    <tr><td> EVEN </td><td> I I X X </td><td>p<sub>EVEN,4</sub></tr>
    <tr><td> EVEN </td><td> I I X Y </td><td>p<sub>EVEN,5</sub></tr>
    <tr><td> EVEN </td><td> I I Y Y </td><td>p<sub>EVEN,6</sub></tr>
    <tr><td> EVEN </td><td> I I X Z </td><td>p<sub>EVEN,7</sub></tr>
    <tr><td> EVEN </td><td> I I Y Z </td><td>p<sub>EVEN,8</sub></tr>
    <tr><td> EVEN </td><td> I I Z Z </td><td>p<sub>EVEN,9</sub></tr>
    <tr><td> ODD </td><td> I I I I </td><td>p<sub>ODD,0</sub></tr>
    <tr><td> ODD </td><td> I I I Z </td><td>p<sub>ODD,1</sub></tr>\
    <tr><td> ODD </td><td> ... </td></tr>
  </tbody>
</table>

These probabilities are input through a text file with the following format: 

```
#ERRORVEC4

p_error_1 p_EVEN,0  p_EVEN,1  p_EVEN,2 p_EVEN,3 .... p_ODD,0 p_ODD,1 ... p_ODD,9  
p_error_2 p_EVEN,0  p_EVEN,1  p_EVEN,2 p_EVEN,3 .... p_ODD,0 p_ODD,1 ... p_ODD,9  
p_error_3 p_EVEN,0  p_EVEN,1  p_EVEN,2 p_EVEN,3 .... p_ODD,0 p_ODD,1 ... p_ODD,9  
...

```

### Simulating fault tolerance

With the superoperator defined in the textfile, these values can be imported using the ```load_errors``` module, and toric code error correction simulated using the ```st.run3D()``` function.

```python

import st
import load_errors

size=6
tSteps=5
timespace=[1,1]
stabilizersNotComplete=0

## Load error vector from file                                                                                           
evecs3,evecs4 = load_errors.load("example_errorvec.txt")
error_vector4 = evecs4[evecs4.keys()[0]]


[x,z],[x2,z2] = st.run3D(size,tSteps,error_vector4,timespace,stabilizersNotComplete)


```

The ```timespace``` parameter is a vector of two integers, that defines relative weightings between the time and space directions in the perfect matching attempt to correct this errors. This parameter should be optimised for the specific errors considered.
The ```stabilizersNotComplete``` parameter gives the probability that a given stabilizer is not evaluated. For example if ```stabilizersNotComplete=0.01```, the code will simulate the even that 1% of stabilizer measurements are not recorded, and the correction procedure will attempt to fix the code without any information about those stabilizer measurements.





# Solid state spin implementation of the surface code

Simulations of our solid state implementation of the surface code call only on the planar variant of the code. Each simulation generates a lattice of spins via ```arrayMaker.py``` which takes a number of parameters to construct a superoperator for each stabilizer on the defective lattice. For more detail on this model, see [[5](http://arxiv.org/abs/1406.5149)].

```python

import sp

size=6                 # The size of the lattice

# ----- ORBIT TYPE ------- #
orbit='circle'         # the orbit 'abrupt' or 'circle' determines the phase interpolating function used to generate error                               superoperator from spin misalignment

# ----- POSITIONAL ERROR DISTRIBUTION ------- #
# ------------------------------------------------------------#
# ------- (distance from probe to data qubit is unity) ------- #
errortype= 'pillbox'   # the shape of the error distribution for qubit position on lattice
                      #     'normal' - a 3D normal distribution of errors. Standard
                      #         deviation in each dimension specified by parameters: sdInX, sdInY and sdInZ 
                   #     'disc' - a 2D uniform circlular distribution, the radius is specified by sdInX, sdInY
                      #     'pillbox' - a 3D cylindrical (in z-dimension) uniform distribution
                      #           the radius of the cylinder is specified by sdInX & sdInY, and the half-height of the
                      #           cylinder by sdInZ
sdInX=0.1              # in-plane (x) error parameter for qubit position
sdInY=0.1              # in-plane (y) error parameter for qubit position
sdInZ=0.05             # z-dirn or height error parameter for qubit position //note: physical location errors where average                     
# ----- ERROR PARAMETERS ------- #                      
pJ=0.0004              # Phase Jitter - pJ = O(delta^2)
                       # where delta is a small error in the phase accumulation on the probe, ideal phase being pi/2 with   
                       # a symmetric distribution of possible phase errors parametrised by delta. This arises from an error in
                       # the  interaction time between probe qubit and data qubit. The constants in front of delta^2 depend on 
                       #the  type of random distribution being considered. E.g. for a bimodal distribution {+delta ,-delta}
                       #then pJ~delta^2/4, for a uniform distribution (-delta,+delta) then pJ~delta^2/12.  This manifests
                       #itself as a phase error on both the data qubit and the probe qubit occuring with probability pJ.
                       # This is described by an error map: 
                       # E(rho) = (1-pJ) rho + pJ* Z_data.Z_probe (rho) Z_data.Z_probe
                       # where rho is the state after the ideal interaction.

pX=0.001/3              
pY=0.001/3
pZ=0.001/3             #three components (Pauli-X,Y,Z) of the probe flip error

prep=0.01              #probe initialisation error - phi_probe = (1-prep) |+> + prep |->

pLie=0.05              # probability of a measurment error. Applies a measurement operator of the form
                       #M_even(rho) = (1-pLie)|even><even| + pLie |odd><odd|
                       
pErr=0.002             # data qubit decoherence - randomly apply an X,Y or Z with this probability between cycles             


tSteps=20
timespace=[1,1]
boundary=1

result = sp.run3Dspin(size,errortype,orbit,tSteps,[sdInX,sdInY,sdInZ,pJ,pX,pY,pZ,prep,meas,data],timespace,boundary)

```


[1] Kolmogorov, V. Blossom V: a new implementation of a minimum cost perfect matching algorithm. Math. Prog. Comp. 1, 43–67 (2009).<br>
[2] Edmonds, J. Paths, Trees, and Flowers, Canad. J. Math. 17, 449–467 (1965) .<br>
[3] [Topological quantum computing with a very noisy network and local error rates approaching one percent <br>
NH Nickerson, Y Li, SC Benjamin Nature communications 4, 1756](http://www.nature.com/ncomms/journal/v4/n4/abs/ncomms2773.html) <br>
[4] [Freely Scalable Quantum Technologies using Cells of 5-to-50 Qubits with Very Lossy and Noisy Photonic Links
NH Nickerson, JF Fitzsimons, SC Benjamin arXiv preprint arXiv:1406.0880](http://arxiv.org/abs/1406.0880) <br>
[5] [A silicon-based surface code quantum computer, J O'Gorman, NH Nickerson, P Ross, JJL Morton, SC Benjamin arXiv preprint arXiv:1406.5149](http://arxiv.org/abs/1406.5149)
