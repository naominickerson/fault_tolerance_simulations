import random
import os
import csv
import subprocess
import time
import copy
import math

import blossom5.pyMatch as pm

## Functions to perform minimum weight matching on the toric and planar topological codes
## There are 4 variants of this here to carry out the matching in the 2D and 3D (imperfect
## measurement) cases, and for the toric and planar codes. Each takes a list of anyon_positions,
## constructs the corresponding graph problem, and interfaces with the Blossom V algorithm (Kologomorov)
## to perform minimum weight matching.  



def normal_weights(pos1,pos2,lattice_size):
    m = lattice_size
    [p0,p1],[q0,q1]=pos1,pos2
    w0=(p0-q0)%m
    w1=(p1-q1)%m
    weight=min([w0,m-w0])+min([w1,m-w1])
    return weight

def xy_configurations(pos1,pos2,lattice_size,weighted_configurations):

    # weighted_separations is a dictionary of known anyon separation 
    # configurations, (a,b)  where a<b, and their relative probabilities
    ## e.g. {(2,2): 0.2, (0,4): 0.5, (0,6): 0.01 ... }

    m=lattice_size
    [p0,p1],[q0,q1]=pos1,pos2
    
    w0=abs((p0-q0)%m)
    w1=abs((p1-q1)%m)

    w0 = min([m-w0,w0])
    w1 = min([m-w1,w1])

    t=[w0,w1]
    t.sort()
    w0,w1=t

    default = min(weighted_configurations.values())/100.
    weight = weighted_configurations.get((w0,w1),None)

    if weight==None:
        weight = -(w0+w1)*math.log(default)
    else:
        weight = -math.log(weight)

    return int(weight*10000)


def xy_weighted(pos1,pos2,lattice_size,weighted_separations):
    # weighted_separations is a hash, of known separations
    # and their relative probabilities:  
    ## {s1: p1, s2: p2, s3: p3 ... }

    m = lattice_size
    [p0,p1],[q0,q1]=pos1,pos2
    
    w0=abs((p0-q0)%m)
    w1=abs((p1-q1)%m)

    w0 = min([m-w0,w0])
    w1 = min([m-w1,w1])

    default = None
    wmin = min(weighted_separations.values())
    w = weighted_separations.get((w0+w1),default)

    if w==None:
        return -int(math.log(wmin)*1000)*lattice_size*(w0+w1)
    else: 
        return -int(math.log(w)*1000)


def xy_fixed_weights(pos1,pos2,lattice_size,lmbda):
    m = lattice_size
    [p0,p1],[q0,q1]=pos1,pos2
    
    w0=abs((p0-q0)%m)
    w1=abs((p1-q1)%m)

    w0 = min([m-w0,w0])
    w1 = min([m-w1,w1])

    if (w0+w1) == lmbda :
        return w0+w1
    else:
        return (w0+w1)*100


def n_times_weights(pos1,pos2,lattice_size,n_corr):
    m = lattice_size
    [p0,p1],[q0,q1]=pos1,pos2
    w0=(p0-q0)%m
    w1=(p1-q1)%m

    ww0 = m-w0
    ww1 = m-w1

    w0_corr = w0%n_corr==0
    ww0_corr = ww0%n_corr==0
    w1_corr = w1%n_corr==0
    ww1_corr = ww1%n_corr==0

    if w0_corr and ww0_corr:
        w0=min([w0,ww0])
    elif (not w0_corr) and ww0_corr:
        w0=ww0
    elif w0_corr and (not ww0_corr):
        w0=w0
    elif (not w0_corr) and (not ww0_corr):
        w0=100*m*w0

    if w1_corr and ww1_corr:
        w1=min([w1,ww1])
    elif (not w1_corr) and ww1_corr:
        w1=ww1
    elif w1_corr and (not ww1_corr):
        w1=w1
    elif (not w1_corr) and (not ww1_corr):
        w1=100*m*w1

    
    return w0+w1


#### Parametrized Decoders

def match_toric_2D_with_xy_weighted(lattice_size,anyon_positions,weighted_configurations):
    return match_toric_2D_by_weights(lattice_size,anyon_positions,xy_weighted,[weighted_configurations])

def match_toric_2D_with_xy_configurations(lattice_size,anyon_positions,weighted_configurations):
    return match_toric_2D_by_weights(lattice_size,anyon_positions,xy_configurations,[weighted_configurations])

def match_toric_2D_with_xy_fixed(lattice_size,anyon_positions,lmbda):
    return match_toric_2D_by_weights(lattice_size,anyon_positions,xy_fixed_weights,[lmbda])

def match_toric_2D_with_ncorr(lattice_size,anyon_positions,n_corr):
    return match_toric_2D_by_weights(lattice_size,anyon_positions,n_times_weights,[n_corr])

def match_toric_2D(lattice_size,anyon_positions):
    return match_toric_2D_by_weights(lattice_size,anyon_positions,normal_weights)



def match_toric_2D_by_weights(lattice_size,anyon_positions,weight_function,weight_function_params = []):
    """ Uses perfect matching to return a matching to fix the 2D TORIC code from the given positions of '-1' stabilizer outcomes in the code. 

    Assumptions:
    -----------
    Perfect measurement, meaning there must be an even number of anyons. 

    Parameters:
    ----------
    lattice_size -- size of the code.
    anyon_positions -- List of all '-1' stabilizer outcomes in the code. E.g. [[x0,y0],[x1,y1],..]. 

    Returns:
    -------
    The perfect matching, a list of paired anyon positions.

    """
    
    nodes_list=anyon_positions
    n_nodes=len(nodes_list)

    if n_nodes==0: return []

 
    graphArray=[]

    ##fully connect the nodes within the 2D layer
    ## node numbering starts at 0 
    for i in range(n_nodes-1):
        pos1=nodes_list[i]

        for j in range(n_nodes-i-1):
            pos2=nodes_list[j+i+1]
            
            params = [pos1,pos2,2*lattice_size]+weight_function_params

            weight = weight_function(*params)
            graphArray+=[[i,j+i+1,weight]]

    # for g in graphArray:
    #     print g

    n_edges=len(graphArray)

    ## Use the blossom5 perfect matching algorithm to return a matching
    matching=pm.getMatching(n_nodes,graphArray)
    
    ## REFORMAT MATCHING
    matching_pairs=[[i,matching[i]] for i in range(n_nodes) if matching[i]>i]

    #print matching_pairs

    points=[] if len(matching_pairs)==0 else [[nodes_list[i] for i in x] for x in matching_pairs]
  
    return points
















def match_toric_3D(lattice_size,anyon_positions,weights=[1,1]):

    
    """ Uses perfect matching to return a matching to fix the 3D TORIC code from the given positions of '-1' stabilizer outcomes in the code. 

    Parameters:
    ----------
    lattice_size -- size of the code.
    anyon_positions -- List of all '-1' stabilizer outcomes in the code, a space + time coordinate. E.g. [[x0,y0,t0],[x1,y1,t1],..]. 
    weights -- A 2-component list, [space_weight,time_weight] containting multiplicative weightings for space and time dimensions. Default: [1,1]

    Returns:
    -------
    The perfect matching, a list of paired anyon positions.

    """

    # time direction cutoff
    cutoff = 15

    #tp0 = time.time()

    nodes_list=[item for sublist in anyon_positions for item in sublist]
    n_nodes=len(nodes_list)

    
    if n_nodes==0:
        return []
    
    m=2*lattice_size
    wT,wS=weights
 
    graphArray=[]

    ##fully connect the nodes within the 2D layer
    ## node numbering starts at 0 



    
    time_lookup={}
    for t in range(cutoff+1):
        time_lookup[t]=t*wT

     
    weight_lookup = {}
    for i in range(m): 
        weight_lookup[i]={}
        for j in range(m):
            diff = abs(i-j)
            weight_lookup[i][j] = min([diff,m-diff])*wS
    
    n_nodes_minus_1 = n_nodes-1

    for i in range(n_nodes_minus_1):
        (pt,p0,p1)=nodes_list[i]
      
        i_plus_1 = i+1
        
        
        for j in range(n_nodes_minus_1 - i):
            indexj = j+i_plus_1
            (qt,q0,q1)=nodes_list[indexj]

 
            wt=(qt-pt)
            if wt>=cutoff: break
            # the list of nodes is ordered by time so break as soon as difference between pt and qt is >=10

            weight = weight_lookup[q0][p0]+weight_lookup[q1][p1]+time_lookup[wt]
            graphArray+=[[i,indexj,weight]]

    n_edges=len(graphArray)


    ## PERFORM MINIMUM WEIGHT MATCHING
    ## Use Blossom5 algorithm to generating a matching

    matching=pm.getMatching(n_nodes,graphArray)

    ## REFORMAT MATCHING 

    matching_pairs=[[i,matching[i]] for i in range(n_nodes) if matching[i]>i]
    points=[] if len(matching_pairs)==0 else [[nodes_list[i] for i in x] for x in matching_pairs]

    return points















def match_planar_2D(lattice_size,stabilizer_type,anyon_positions):
    

    if anyon_positions==[]:
        matching=[]
        return matching
    
    N_nodes=len(anyon_positions)

    if N_nodes==0:
        return []

    node_index = []
    count = 0

    graphArray = []


    for i in range(N_nodes-1):
        (p0,p1)=anyon_positions[i]
        
        for j in range(N_nodes-i-1):
            indexj = j+i+1
            (q0,q1)= anyon_positions[j+i+1]
            weight=abs(p0-q0)+abs(p1-q1)
            graphArray+=[[i,indexj,weight]]
            #newline=str(i)+' '+str(i+j+1)+' '+str(weight)+'\n'
            #graphStr+=newline

    # for every node, create a boundary node and joining edge
    boundary_node_positions=[]
    
    for i in range(N_nodes):

        (p0,p1)=anyon_positions[i]
        
        if stabilizer_type=="star":
            (b0,b1)=(p0,-1 if p1<lattice_size else 2*lattice_size+1)
        elif stabilizer_type=="plaquette":
            (b0,b1)=(-1 if p0<lattice_size else 2*lattice_size+1,p1)
        else:
            print "stabilizer_type must be either **star** or **plaquette**"
            return 0
        
        boundary_node_positions+=[[b0,b1]]

        #add edge to graph
        weight=abs(p0-b0)+abs(p1-b1)
        graphArray+=[[i,i+N_nodes,weight]]
        #newline=str(i)+' '+str(i+N_nodes)+' '+str(weight)+'\n'
        #graphStr+=newline

    
    # fully connect boundary nodes with weight 0
    N_boundary_nodes=len(boundary_node_positions)

    for i in range(N_boundary_nodes-1):
        for j in range(N_boundary_nodes-i-1):
            graphArray+=[[i+N_nodes,i+N_nodes+j+1,0]]
            
            #newline=str(i+N_nodes)+' '+str(i+N_nodes+j+1)+' '+str(0)+'\n'
            #graphStr+=newline
    



################ MATCHING ###################
        
    matching=pm.getMatching(2*N_nodes,graphArray)

#############################################

    matching_pairs=[[i,matching[i]] for i in range(2*N_nodes) if matching[i]>i]
  
    all_positions=anyon_positions+boundary_node_positions    

    points=[] if len(matching_pairs) == 0 else [[all_positions[i] for i in x] for x in matching_pairs]

    return points


    







