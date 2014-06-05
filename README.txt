
050614 toric_lattice	-removed 'constructArray and constructList methods, and made everything work the the self.array data layout
       			-added documentation for all methods

050614 example_toric1	- this contains a simple example using the st.run3Drandom() function. 

050614 example_toric2  	- contains an example using the st.run3D() function, using the test error vector. 
       			- added load_errors function to demonstrate importing the error vectors from a file








To include in released code: 

## for both: 
-----------

perfect_matching.py  (DONE)
load_errors.py	     (DONE)
/blossom5/	     (DONE)
example_errorvec.txt (DONE)

TORIC version
-------------
toric_lattice.py (DONE)
simulate_toric.py (DONE)
example_toric1 (DONE)
example_toric2 (DONE)

PLANAR version
--------------
planar_lattice.py
sp.py (simplified version)
example_planar1
example_planar2




perfect_matching.py 

## 30 Oct: made changes to link between this part to generate graph and the blossom5.pyMatch code. Now pass 3 lists 
## to this function nodes1, nodes2 and weights. new function get_matching_fast()

## 11 March: noticed an edge case where the matching fails. The problem was not enough links between boundary nodes in 
## different layers. To fix this added additional edges linking two boundary nodes.

## 12/03/14: Update, the change seems to improve performance in low error region but make it worse at higher error rates
## including significantly lowering the threshold. 


