A Python library for fault tolerance simulations of the surface code
using the blossom 5 perfect matching algorithm

Two different scenarios are covered by this library

* Planar code implemented in solid state spins
* Surface code (planar and toric) simulated under a general description of the noise on stabilizer measurements


# Solid state spin implementation of the surface code


# Surface code under noisy stabilizer measurements

## Random Noise

### Toric code under random noise

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


### Planar code under random noise

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

## Error described by a stabilizer superoperator

This variant of the code puts a more general form of errors into the code, characterised by the superoperator describing the true (noisy) process of measuring each stabilizer. This superoperator provides a full description of the noisy measurement, and if physical errors are made up of randomly applied Pauli operations, this superoperator can be decomposed into Kraus operators that are simply some product of Pauli operations on the qubits in the stabilizer combined with a possible misreported stabilizer outcome. For more detail see (?)

This superoperator decomposition is specified through a text file of the form found in ``` example_error_vec.txt ```. 

#Toric Code

For the toric code, all stabilizer measurements are 4 body operations, so only one superoperator must be specified. If we measure a stabilizer which, if noiseless, should return an EVEN (+1) parity outcome. In 

<table>
  <thead>
    <tr>
      <td> Reported parity </td>
      <td> Qubit errors </td>
    </tr>
  </thead>
  <tbody>
    <tr><td> EVEN </td><td> I I I I </td></tr>
    <tr><td> EVEN </td><td> I I I Z </td></tr>
    <tr><td> EVEN </td><td> I I I X </td></tr>
    <tr><td> EVEN </td><td> I I I Y </td></tr>
    <tr><td> EVEN </td><td> I I I Y </td></tr>
    <tr><td> EVEN </td><td> I I X X </td></tr>
    <tr><td> EVEN </td><td> I I X Y </td></tr>
    <tr><td> EVEN </td><td> I I Y Y </td></tr>
    <tr><td> EVEN </td><td> I I X Z </td></tr>
    <tr><td> EVEN </td><td> I I Y Z </td></tr>
    <tr><td> EVEN </td><td> I I Z Z </td></tr>
    <tr><td> ODD </td><td> I I I I </td></tr>
    <tr><td> ODD </td><td> I I I Z </td></tr>\
    <tr><td> ODD </td><td> ... </td></tr>
  </tbody>
</table>

parity = EVEN, 

[[1,[I,I]],[1,[I,Z]],[1,[I,X]],[1,[I,Y]],
            [1,[X,X]],[1,[X,Y]],[1,[Y,Y]],[1,[X,Z]],
            [1,[Y,Z]],[1,[Z,Z]],[-1,[I,I]],[-1,[I,Z]],
            [-1,[I,X]],[-1,[I,Y]],[-1,[X,X]],[-1,[X,Y]],
            [-1,[Y,Y]],[-1,[X,Z]],[-1,[Y,Z]],[-1,[Z,Z]]]

```python
import st

errorVector = 

result = st.run3D(size,tSteps,errorVector,timespace=[1,1],stabilizersNotComplete=0)

```
