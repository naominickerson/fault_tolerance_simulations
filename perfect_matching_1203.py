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


def match_planar_3D(lattice_size,stabilizer_type,anyon_positions,time_space_weights,boundary_weight = 1,print_graph=False):

    max_time_separation = 15

    t00 = time.time()

    total_time=len(anyon_positions)
    nodes_list=[item for sublist in anyon_positions for item in sublist]
    n_nodes=len(nodes_list)

    [wS,wT]=time_space_weights
    wB = wS if boundary_weight == 1 else boundary_weight

    if n_nodes==0:
        return []
    
    node_index=[]
    count=0

    for x in anyon_positions:
        node_index+=[[count+i for i in range(len(x))]]
        count+=len(x)

    b_node_index=[[index+n_nodes for index in t] for t in node_index]

    all_boundary_nodes=[]
    


    boundary_node=None
    

    ## LOOKUP TABLES

    m = 2*lattice_size +1


    weight_lookup={}
    for p in range(-1,m+1):
        weight_lookup[p]={}
        for q in range(-1,m+1):
            weight_lookup[p][q]=wS*abs(p-q)

    
#------------------------------------------------------------

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


#-------------------------------------

    ## PART 2: Create boundary node for each 

    for t in range(total_time):

        n_list_t=anyon_positions[t]
        n_nodes_t=len(n_list_t)
        n_index_t=node_index[t]
        b_index_t=b_node_index[t]
        
        n_nodes_t_minus1 = n_nodes_t - 1

        # for every node, create a boundary node and joining edge



        boundary_node_positions_t=[]
        
        if stabilizer_type == "star": 
            for i in range(n_nodes_t):
                (pt,p0,p1)=n_list_t[i]
                (bt,b0,b1)=(t,p0,-1 if p1<lattice_size else m)
                boundary_node_positions_t+=[[bt,b0,b1]]                
                #weight=sW*(abs(p0-b0)+abs(p1-b1))
                weight = weight_lookup[p0][b0]+weight_lookup[p1][b1]

                nodes1+=[n_index_t[i]]
                nodes2+=[b_index_t[i]]
                weights+=[int(weight*wB/wS)]

                if i==0:
                    if isinstance(boundary_node,int):
                        boundary_node_update=b_index_t[0]
                        nodes1+=[boundary_node_update]
                        nodes2+=[boundary_node]
                        weights+=[0]
                        boundary_node=copy.copy(boundary_node_update)

                    else:
                        boundary_node=copy.copy(b_index_t[0])


        elif stabilizer_type=="plaquette":
            for i in range(n_nodes_t):
                (pt,p0,p1)=n_list_t[i]
                (bt,b0,b1)=(t,-1 if p0<lattice_size else m,p1)
                boundary_node_positions_t+=[[bt,b0,b1]]                
                weight = weight_lookup[p0][b0]+weight_lookup[p1][b1]
 #               graphArray+=[[n_index_t[i],b_index_t[i],weight]]
                nodes1+=[n_index_t[i]]
                nodes2+=[b_index_t[i]]
                weights+=[int(weight*wB/wS)]

                if i==0:
                    if isinstance(boundary_node,int):
                        boundary_node_update=b_index_t[0]
#                        graphArray+=[[boundary_node_update,boundary_node,0]]
                        nodes1+=[boundary_node_update]
                        nodes2+=[boundary_node]
                        weights+=[0]

                        boundary_node=copy.copy(boundary_node_update)

                    else:
                        boundary_node=copy.copy(b_index_t[0])

        

        else:
            print "stabilizer_type must be either **star** or **plaquette**"
            return 0
            

    
        ## save one boundary node to connect to other layers

        all_boundary_nodes+=boundary_node_positions_t
        #boundary_nodes_positions_t=
        #[[pt,p0,-1 if p1<lattice_size else 2*lattice_size+1] for [pt,p0,p1] in node_list_t]
        #if stabilizer_type=="star" else [[pt,-1 if p0<lattice_size else 2*lattice_size,p1]]

    
       # tt2 = time.time()

        # fully connect boundary nodes with weight 0
        for i in range(n_nodes_t-1):
            for j in range(i+1,n_nodes_t):
                
#                graphArray+=[[b_index_t[i],b_index_t[i+j+1],0]]
                nodes1+=[b_index_t[i]]
                #nodes2+=[b_index_t[i+j+1]]
                nodes2+=[b_index_t[j]]
                weights+=[0]
#        t22 += time.time()-tt2

### ADD some extra inter-boundary links 
### 12/03/14

        
    for i in range(n_nodes -1):
        (pt,p0,p1)=all_boundary_nodes[i]

    for j in range(i+1,n_nodes):
        (qt,q0,q1)=all_boundary_nodes[j]
        wt=(qt-pt)
        if wt>=2: break
        
        weight = 0

        nodes1 +=[i+n_nodes]
        nodes2 +=[j+n_nodes]
        weights+=[weight]

#########

    if print_graph==True:
        print zip(nodes1,nodes2,weights)
#    print 't0 = ', t0
 #   print 't1 = ', time.time()-tt1
  #  print 't2 = ', t22
   # print 't3 = ', t3
    n_edges=len(nodes1)
    
################ MATCHING ###################
    #tt4 = time.time()    
#    matching=pm.getMatching(2*n_nodes,graphArray)
    matching = pm.getMatching_fast(2*n_nodes,nodes1,nodes2,weights)
   # print 'matching ', time.time()-tt4
#############################################
    
    if print_graph==True:
        print "Matching"
        print matching

    matching_pairs=[[i,matching[i]] for i in range(2*n_nodes) if matching[i]>i]
    
    
    all_positions=nodes_list+all_boundary_nodes
     

    points=[] if len(matching_pairs)==0 else [[all_positions[i] for i in x] for x in matching_pairs]

  
    return points






#########################



















def match_toric_2D(lattice_size,anyon_positions):

    
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

################ MATCHING ###################

    matching=pm.getMatching(n_nodes,graphArray)

#############################################

    matching_pairs=[[i,matching[i]] for i in range(n_nodes) if matching[i]>i]
    points=[] if len(matching_pairs)==0 else [[nodes_list[i] for i in x] for x in matching_pairs]
  
    return points

#########################














def match_toric_3D(lattice_size,anyon_positions,weights):

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
    for t in range(10):
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
            if wt>=8: break
            # the list of nodes is ordered by time so break as soon as difference between pt and qt is >=10


     #           w0=(q0-p0)%m
      #          w1=(q1-p1)%m
       #         weight=(min([w0,m-w0])+min([w1,m-w1]))*wS+wt*wT
                
            weight = weight_lookup[q0][p0]+weight_lookup[q1][p1]+time_lookup[wt]
            graphArray+=[[i,indexj,weight]]

    n_edges=len(graphArray)

 #   tp1 = time.time()
  #  print 'generate matching graph ',tp1-tp0
################ MATCHING ###################

    matching=pm.getMatching(n_nodes,graphArray)

    #############################################

    matching_pairs=[[i,matching[i]] for i in range(n_nodes) if matching[i]>i]
    points=[] if len(matching_pairs)==0 else [[nodes_list[i] for i in x] for x in matching_pairs]
   # tp2 = time.time()
    #print 'perfect matching ', tp2 - tp1

    return points

#########################













def match_planar_2D(lattice_size,stabilizer_type,anyon_positions):


    if anyon_positions==[]:
        matching=[]
        return matching
    
    N_nodes=len(anyon_positions)
    #N_edges=N_nodes*(N_nodes-1)/2


#    graphStr=str(N_nodes*2)+' '+str(N_edges*2+N_nodes)+'\n'

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


    






     

















