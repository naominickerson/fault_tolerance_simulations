import random
import os
import csv
import subprocess
import time
import copy

import blossom5.pyMatch as pm

## match_planar_3d( lattice_size, stabilizer_type, anyon_positions, time_space_weights)
## match_toric_2D(lattice_size,anyon_positions):
## match_toric_3D(lattice_size,anyon_positions,weights):
## match_planar(lattice_size,stabilizer_type,anyon_positions,graph_file,output_file):

## 30 Oct: made changes to link between this part to generate graph and the blossom5.pyMatch code. Now pass 3 lists 
## to this function nodes1, nodes2 and weights. new function get_matching_fast()

## 11 March: noticed an edge case where the matching fails. The problem was not enough links between boundary nodes in 
## different layers. To fix this added additional edges linking two boundary nodes.

## 12/03/14: Update, the change seems to improve performance in low error region but make it worse at higher error rates
## including significantly lowering the threshold. 



## Matching functions defined here take anyon positions (in space and time) as input parameters, and performs minimum weight
## matching using the blossom5 (Kolgomorov) to determine a matching to fix the code. 

## 


def match_planar_3D(lattice_size,stabilizer_type,anyon_positions,time_space_weights=[1,1],boundary_weight = -1 ,print_graph=False):

    """ Finds a matching to fix the errors in a 3D planar code given the positions of '-1' stabilizer outcomes  
    
    Parameters:
    -----------
    lattice_size -- The dimension of the code
    stabilizer_type -- defines the stabilizer basis, can take the value "star" or "plaquette"
    anyon_positions -- A list of the locations of all '-1' value stabilizers in the 3D parity lattice. [[x0,y0,t0],[x1,y1,t1],...]
    time_space_weights -- The multiplicative weighting that should be assigned to graph edges in the [space,time] dimensions. Default: [1,1]
    boundary_weight -- multiplicative weight to be assigned to edges matching to the boundary. if no boundary_weight specified, set boundary_weight = space_weight 
    print_graph -- Set to True to print the constructed graph. Default: False.

    Returns:
    --------
    A list containing all the input anyon positions grouped into pairs. [[[x0,y0,t0],[x1,y1,t1]],[[x2,y2,t2],... 

    """

    max_time_separation = 15  # This determines the maximum time separation of edges that are added to the graph
    [wS,wT]=time_space_weights
    wB = wS if boundary_weight == -1 else boundary_weight #if boundary weight not specifiedm, let wB=wS

    total_time=len(anyon_positions)
    nodes_list=[item for sublist in anyon_positions for item in sublist]
    n_nodes=len(nodes_list)

    # exclude edge case where no anyons exist.
    if n_nodes==0:
        return []
    
    node_index=[]
    count=0

    for x in anyon_positions:
        node_index+=[[count+i for i in range(len(x))]]
        count+=len(x)

    b_node_index=[[index+n_nodes for index in t] for t in node_index]

    all_boundary_nodes=[]
    all_boundary_nodes2=[]


    ## LOOKUP TABLES

    m = 2*lattice_size +1


    weight_lookup={}
    for p in range(-1,m+1):
        weight_lookup[p]={}
        for q in range(-1,m+1):
            weight_lookup[p][q]=wS*abs(p-q)

    
    ## CONSTRUCT GRAPH
    ## create a graph containing all possible matchings between pairs of anyons (given constraints)
    ## This is represented as three lists: 

    nodes1 = []
    nodes2 = []
    weights = []

    ## PART 1: Complete graph between all real nodes
 
    for i in range(n_nodes -1):
        (pt,p0,p1)=nodes_list[i]

        for j in range(i+1,n_nodes):
            (qt,q0,q1)=nodes_list[j]

            wt=(qt-pt)
            if wt>=max_time_separation: break
                
            weight = weight_lookup[q0][p0]+weight_lookup[q1][p1]+wt*wT

            nodes1 +=[i]
            nodes2 +=[j]
            weights+=[weight]


    ## PART 2: Generate list of boundary nodes linked to each real node
    
    boundary_nodes_list = []

    for i in range(n_nodes):
        
        (pt,p0,p1)=nodes_list[i]

        if stabilizer_type =="star": 
            (bt,b0,b1)=(pt,p0,-1 if p1<lattice_size else m)
        elif stabilizer_type=="plaquette":
            (bt,b0,b1)=(pt,-1 if p0<lattice_size else m,p1)
        else: 
            print "stabilizer_type must be either *star* or *plaquette*"
            sys.exit(0)
        
        weight = weight_lookup[p0][b0]+weight_lookup[p1][b1]

        nodes1+=[i]
        nodes2+=[i+n_nodes]
        weights+=[int(weight*wB/wS)]
        
        boundary_nodes_list+=[(bt,b0,b1)]

    
    
 ## PART 3: Complete graph between all boundary nodes
 
    for i in range(n_nodes -1):
        (pt,p0,p1)=boundary_nodes_list[i]

        for j in range(i+1,n_nodes):
            (qt,q0,q1)=boundary_nodes_list[j]
            wt=(qt-pt)
            if wt>=5: break
                
            nodes1 +=[n_nodes+i]
            nodes2 +=[n_nodes+j]
            weights+=[0]




   


            


    if print_graph==True:
        print zip(nodes1,nodes2,weights)

    n_edges=len(nodes1)
    
    

    ## MAKE MATCHING.
    ## Call the blossom5 perfect matching algorithm to return a matching. 
    ## The form of the returned variable <matching> is a list of pairs of node numbers. 

    matching = pm.getMatching_fast(2*n_nodes,nodes1,nodes2,weights)


    
    if print_graph==True:
        print "Matching"
        print matching

    ## REFORMAT MATCHING PAIRS
    ## Take <matching> and turn it into a list of paired anyon positions. 

    matching_pairs=[[i,matching[i]] for i in range(2*n_nodes) if matching[i]>i]
    
    all_positions=nodes_list+boundary_nodes_list

    points=[] if len(matching_pairs)==0 else [[all_positions[i] for i in x] for x in matching_pairs]

  
    return points














def match_toric_2D(lattice_size,anyon_positions):

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

    if n_nodes==0:
        return []
    
    m=2*lattice_size   
 
    graphArray=[]

    ##fully connect the nodes within the 2D layer
    ## node numbering starts at 0 

    for i in range(n_nodes-1):
        (p0,p1)=nodes_list[i]
        
        for j in range(n_nodes-i-1):
            (q0,q1)=nodes_list[j+i+1]

            w0=(p0-q0)%m
            w1=(p1-q1)%m
            weight=min([w0,m-w0])+min([w1,m-w1])
                                    
            graphArray+=[[i,j+i+1,weight]]

    n_edges=len(graphArray)

    ## PERFORM MATCHING
    ## Use the blossom5 perfect matching algorithm to return a matching

    matching=pm.getMatching(n_nodes,graphArray)

    
    ## REFORMAT MATCHING
    matching_pairs=[[i,matching[i]] for i in range(n_nodes) if matching[i]>i]
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


    







