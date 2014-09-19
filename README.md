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
