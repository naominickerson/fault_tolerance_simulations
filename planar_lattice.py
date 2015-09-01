import random
import math
import copy
import itertools
import numpy as np

# uncomment to be able to use the .showArray() function
#import matplotlib.pyplot as plt





"""

INFO:
   Errors stored in an array, each entry represents either 
   a qubit: [xError?,zError?] with xError,zError in {1,-1}
   a stabiliser: star or plaquette depending on location with S in {1,-1}


Data structure: 
       top          top
  Q -- STAR -- Q -- STAR -- Q -- 
        |            |
 left   |            |
 PLAQ   Q    PLAQ    Q    PLAQ
        |            |
        |            |
  Q -- STAR -- Q -- STAR -- Q --
        |            |
 left   |            |
 PLAQ   Q    PLAQ    Q    PLAQ
        |            |
        |            |
  Q -- STAR -- Q -- STAR -- Q --
        |            |
        |            |

 
"""

class PlanarLattice:
    
    """
    Planar lattice class
    """

    def __init__(self,size):

        self.size=size
        
        self.N_Q=2*size*size+2*size+1
        self.N_full_P=size*(size-1)
        self.N_edge_P=size

        self.positions_anyons_S=None
        self.positions_anyons_P=None
        
        ## Define basic qubit and stabilizer positions

        self.positions_Q=[(x,y) for x in range(2*size+1) for y in range((x%2),2*size+1,2) ]
        self.positions_P=[(x,y) for x in range(0,2*size+1,2) for y in range(1,2*size+1,2)]
        self.positions_S=[(x,y) for x in range(1,2*size+1,2) for y in range(0,2*size+1,2)]

        ## Define position lists by stabilizer type

        self.positions_full_S=[(x,y) for x in range(2,2*size-1,2) for y in range(1,2*size+1,2)]
        self.positions_edge_S_T=[(0,y) for y in range(1,2*size,2)]
        self.positions_edge_S_B=[(2*size,y) for y in range(1,2*size,2)]
        self.positions_full_P=[(x,y) for x in range(1,2*size,2) for y in range(2,2*size-1,2)]
        self.positions_edge_P_L=[(x,0) for x in range(1,2*size,2)]
        self.positions_edge_P_R=[(x,2*size) for x in range(1,2*size,2)]

        ## Defining list of positions for two interspersed round of plaquette measurement

        self.positions_full_P_1=[(x,y) for x in range(1,2*size,2) for y in range((x+1)%4+2,2*size,4)]
        self.positions_full_P_2=[(x,y) for x in range(1,2*size,2) for y in range((x-1)%4+2,2*size,4)]
        self.positions_edge_P_L_1=[(x,0) for x in range(1,2*size,4)]
        self.positions_edge_P_L_2=[(x,0) for x in range(3,2*size,4)]
        self.positions_edge_P_R_1= [(x,2*size) for x in range(2*(size%2)+1,2*size,4)]
        self.positions_edge_P_R_2=[(x,2*size) for x in range(2*((size+1)%2)+1,2*size,4)]

        self.positions_full_S_1=[(x,y)  for x in range(2,2*size-1,2) for y in range((x+2)%4+1,2*size,4)]
        self.positions_full_S_2=[(x,y)  for x in range(2,2*size-1,2) for y in range((x%4)+1,2*size,4)]
        self.positions_edge_S_T_1=[(0,y) for y in range(1,2*size,4)]
        self.positions_edge_S_T_2=[(0,y) for y in range(3,2*size,4)]
        self.positions_edge_S_B_1=[(2*size,y) for y in range(2*(size%2)+1,2*size,4)]
        self.positions_edge_S_B_2=[(2*size,y) for y in range(2*((size+1)%2)+1,2*size,4)]

        ## Initialise array

        self.array=[[1]*(2*self.size+1) for _ in range(2*self.size+1)]

        for p0,p1 in self.positions_Q: self.array[p0][p1]=[1,1]
        for p0,p1 in self.positions_P: self.array[p0][p1]=1
        for p0,p1 in self.positions_S: self.array[p0][p1]=1



    
    # Methods for Displaying the state of the array
    #==============================================


    def showArray(self,arrayType,channel=0):

        c=0 if channel=="X" else 1
        
        if arrayType=="errors":                        
            print_array=[[x[c] if isinstance(x,list) else 0 for x in row]for row in self.array]

        if arrayType=="stabilizers":
            print_array=[[x if isinstance(x,int) else 0 for x in row] for row in self.array]

        
        plt.imshow(print_array)
        plt.show()


    def showArrayText(self,arrayType="errors",channel=0):

        if channel in ["X","x",0]: c=0
        elif channel in ["Z","z",1]: c=1
        else: 
            raise ValueError('%s is not a valid channel for showArrayText(), channel must be "X" or "Z '%(channel,))

        if arrayType in ["error","errors","Errors","Error"]: 

            print_array = [[str(x[c]) if isinstance(x,list) else '.' for x in row] for row in self.array]
            print_array = [[channel if x=='-1' else x for x in row] for row in print_array]

        
        elif arrayType in ["stabilizers","stabs","stabilisers","stabilizer","stabiliser"]:
        
            print_array = [[str(x) if isinstance(x,int) else '.' for x in row] for row in self.array]

        elif arrayType in ["all","both"]:
            
            print_array = [[str(x[c]) if isinstance(x,list) else ('.' if x==1 else '#') for x in row] for row in self.array]
            
        else: 
            raise ValueError('%s is not a valid arrayType for showArrayText()'%(arrayType,))

        print_array = [['&' if (x=='#' and i%2==0)  else x for x in print_array[i]] for i in range(len(print_array))]


        print '\n showing the ',arrayType,' array',
        if arrayType in ["error","errors","Errors","Error"]: print 'for the ',channel,' channel.\n'
        else: print '.\n'
        col_width = 3
        for row in print_array:
            print "".join(word.ljust(col_width) for word in row)



    


    def applyRandomErrors(self,pX,pZ):
        """ applies random X and Z errors to every qubit in the array 

        Parameters:
        ----------
        pX -- probability of X error
        pZ -- probability of Z error

        """
        for q0,q1 in self.positions_Q:
            rand1=random.random()
            rand2=random.random()

            if rand1<pX:
                self.array[q0][q1][0]*=-1
            if rand2<pZ:
                self.array[q0][q1][1]*=-1


    def applyRandomErrorsXYZ(self,pX,pY,pZ):

        for p0,p1 in self.positions_Q:
            if random.random()<pX: 
                self.array[p0][p1][0]*=-1
            if random.random()<pY: 
                self.array[p0][p1][0]*=-1
                self.array[p0][p1][1]*=-1
            if random.random()<pZ:
                self.array[p0][p1][1]*=-1



    def findAnyons(self):
  
        anyon_positions_x=[]
        anyon_positions_z=[]
        
        for p0,p1 in self.positions_P:
            if self.array[p0][p1]==-1:
                anyon_positions_x+=[[p0,p1]]

        for p0,p1 in self.positions_S:
            if self.array[p0][p1]==-1:
                anyon_positions_z+=[[p0,p1]]

#        for i in range(self.N_full_P):
#            if self.full_S[i]==-1:
#                anyon_positions_x+=[self.positions_full_S[i]]

#        for i in range(self.N_edge_P):
#            if self.edge_S_T[i]==-1:
#                anyon_positions_x+=[self.positions_edge_S_T[i]]
#            if self.edge_S_B[i]==-1:
#                anyon_positions_x+=[self.positions_edge_S_B[i]]

#        for i in range(self.N_full_P):
#            if self.full_P[i]==-1:
#                anyon_positions_z+=[self.positions_full_P[i]]

#        for i in range(self.N_edge_P):
#            if self.edge_P_L[i]==-1:
#                anyon_positions_z+=[self.positions_edge_P_L[i]]
#            if self.edge_P_R[i]==-1:
#                anyon_positions_z+=[self.positions_edge_P_R[i]]
      
             
        self.positions_anyons_S=anyon_positions_x
        self.positions_anyons_P=anyon_positions_z

        

    # MEASUREMENT
    #============

    def updateStabilizer(self,p0,p1,stabQubits,channel,pLie):
        stab=1
        for s0,s1 in stabQubits:
            stab*=self.array[s0][s1][channel]
            
        rand = random.random()
        if rand<pLie: stab*=-1
        self.array[p0][p1]=stab


    def measurePlaquettes(self,pLie=0):
        

        for p0,p1 in self.positions_full_P:
            stabQubits=((p0,p1-1),(p0,p1+1),(p0-1,p1),(p0+1,p1))
            self.updateStabilizer(p0,p1,stabQubits,0,pLie)

        for p0,p1 in self.positions_edge_P_L:

             stabQubits = ((p0,p1+1),(p0-1,p1),(p0+1,p1))
             self.updateStabilizer(p0,p1,stabQubits,0,pLie)

        for p0,p1 in self.positions_edge_P_R:
             stabQubits = ((p0,p1-1),(p0-1,p1),(p0+1,p1))
             self.updateStabilizer(p0,p1,stabQubits,0,pLie)


    def measureStars(self,pLie=0):      

        for p0,p1 in self.positions_full_S:
            stabQubits=((p0,p1-1),(p0,p1+1),(p0-1,p1),(p0+1,p1))
            self.updateStabilizer(p0,p1,stabQubits,1,pLie)

        for p0,p1 in self.positions_edge_S_T:
            stabQubits = ((p0,p1-1),(p0,p1+1),(p0+1,p1))
            self.updateStabilizer(p0,p1,stabQubits,1,pLie)
        
        for p0,p1 in self.positions_edge_S_B:
            stabQubits = ((p0,p1-1),(p0,p1+1),(p0-1,p1))
            self.updateStabilizer(p0,p1,stabQubits,1,pLie)
            

    # MEASUREMENT ACCORDING TO AN ERROR VECTOR
    #=========================================

    def stabilizer(self,channel,pos,error,sType,round12,stabilizersNotComplete=0):

        if round12 not in [1,2]: raise ValueError('round12 must be either 1 or 2')
            
        if channel in ["plaquette","P"]: c=0
        elif channel in ["star","Star","S"]:c=1
        else: raise ValueError('%s is not a valid channel for the stabilizer'%(channel))
      
        
        p0,p1=pos
        
        [up,down,left,right] = [(p0-1,p1),(p0+1,p1),(p0,p1-1),(p0,p1+1)]

        if sType =="F": stabQubits = (left,right,up,down)
        elif sType =="L": stabQubits = (right,up,down)
        elif sType =="R": stabQubits = (left,up,down)
        elif sType =="T": stabQubits = (left,right,down)
        elif sType =="B": stabQubits = (left,right,up)
        else:
            raise ValueError(' pType must be a valid plaquette type: F,R,L,T or B ')
        
        order = range(len(stabQubits))

        
        # Add option that a stabilizer doesn't get measured. The stabilizer value stays the same as the previous round and no errors are applied
        
        if random.random()>stabilizersNotComplete: 

            lie,err=error  
                    
            if round12==2:
                stab=lie
                for q0,q1 in stabQubits:
                    stab*=self.array[q0][q1][c]
                    self.array[p0][p1]=stab

            random.shuffle(order)
            errQubits=[stabQubits[order[0]],stabQubits[order[1]]]            
            

            if err!=[[1,1],[1,1]]:
                for i in range(len(errQubits)):
                    q=errQubits[i]
                    self.array[q[0]][q[1]][0]*=err[i][0]
                    self.array[q[0]][q[1]][1]*=err[i][1]
                
            if round12==1:
                stab=lie
                for q0,q1 in stabQubits:
                    stab*=self.array[q0][q1][c]
                self.array[p0][p1]=stab







          

    def measureNoisyStabilizers(self,channel,errorVector3,errorVector4,stabilizersNotComplete=0):
        """ applies the stabilizer() function to each stabilizer position 

        Parameters: 
        ----------
        channel --> "star" or "plaquette" defining the type of stabilizer round
        errorVector3 --> error vector describing the errors for all 3 qubit stabilizers
        errorVector4 --> error vector describing the errors for all 4 qubit stabilizers
        stabilizersNotComplete --> probability of a given stabilizer not evaluating. Default: 0

        Action:
        -------
        For each stabilizer of the given channel this function picks an error probabilistically according
        to the error vectors given. 
        """


        I,X,Y,Z=[1,1],[-1,1],[-1,-1],[1,-1]

	if channel=="plaquette":
        	errorList=[[1,[I,I]],[1,[I,Z]],[1,[I,X]],[1,[I,Y]],
                  	 [1,[X,X]],[1,[X,Y]],[1,[Y,Y]],[1,[X,Z]],
                   	[1,[Y,Z]],[1,[Z,Z]],[-1,[I,I]],[-1,[I,Z]],
                   	[-1,[I,X]],[-1,[I,Y]],[-1,[X,X]],[-1,[X,Y]],
                   	[-1,[Y,Y]],[-1,[X,Z]],[-1,[Y,Z]],[-1,[Z,Z]]]
	elif channel=="star":
        	errorList=[[1,[I,I]],[1,[I,X]],[1,[I,Z]],[1,[I,Y]],
                  	 [1,[Z,Z]],[1,[Z,Y]],[1,[Y,Y]],[1,[Z,X]],
                   	[1,[Y,X]],[1,[X,X]],[-1,[I,I]],[-1,[I,X]],
                   	[-1,[I,Z]],[-1,[I,Y]],[-1,[Z,Z]],[-1,[Z,Y]],
                   	[-1,[Y,Y]],[-1,[Z,X]],[-1,[Y,Z]],[-1,[X,X]]]
        else: 
            raise ValueError('channel must be either "star" or "plaquette"')


        
                                                            # zip errors and the probability vector together
                                                            # and sort them into p descending order
        errorList4=sorted(zip(errorVector4,errorList),reverse=True)
        errorList3=sorted(zip(errorVector3,errorList),reverse=True)

        error_prob_4,errorSort4=zip(*errorList4)            # separate ordered lists into
        error_prob_3,errorSort3=zip(*errorList3)            # lists of errors and their probs

        cum_prob_4=np.cumsum(np.array(error_prob_4)).tolist()   # sum up cumulative probability lists
        cum_prob_3=np.cumsum(np.array(error_prob_3)).tolist()

        self.errors_full_P=[]                               # generate lists of errors and lies to be applied
        self.errors_edge_P=[]
        

        for i in range(self.N_full_P):                      # Select random error for each stabilizer to 

            rand=random.random()                            # be measured
            for j in range(20):
                if rand<cum_prob_4[j]:
                    self.errors_full_P+=[errorSort4[j]]
                    break;
                if j==19: 
                    self.errors_full_P+=[[1,[[1,1],[1,1]]]]

        
        for i in range(2*self.N_edge_P):
            rand=random.random()
            for j in range(20):
                if rand<cum_prob_3[j]:
                    self.errors_edge_P+=[errorSort3[j]]
                    break;
                if j==19: 
                    self.errors_edge_P+=[[1,[[1,1],[1,1]]]]

### DO THE STABILIZER MEASUREMENT IN TWO ROUNDS WITH ERRORS AND LIES

        errCount4=0
        errCount3=0
        order4=[0,1,2,3]
        order3=[0,1,2]

## SET PARAMETERS BASED ON CHANNEL TYPE

        stabilizerType=channel
        edge1="L" if channel=="plaquette" else "T"
        edge2="R" if channel=="plaquette" else "B"

        full_positions_1= self.positions_full_P_1 if channel=="plaquette" else self.positions_full_S_1
        full_positions_2= self.positions_full_P_2 if channel=="plaquette" else self.positions_full_S_2
        edge_positions_1_1 = self.positions_edge_P_L_1 if channel =="plaquette" else self.positions_edge_S_T_1

        edge_positions_1_2 = self.positions_edge_P_L_2 if channel =="plaquette" else self.positions_edge_S_T_2
        edge_positions_2_1 = self.positions_edge_P_R_1 if channel =="plaquette" else self.positions_edge_S_B_1
        edge_positions_2_2 = self.positions_edge_P_R_2 if channel =="plaquette" else self.positions_edge_S_B_2




######              ROUND ONE               ############


        for p in full_positions_1:

            error_p=self.errors_full_P[errCount4]
            errCount4+=1                        
            self.stabilizer(stabilizerType,p,error_p,"F",1,stabilizersNotComplete)

        for p in edge_positions_1_1:

            error_p=self.errors_edge_P[errCount3]
            errCount3+=1
            self.stabilizer(stabilizerType,p,error_p,edge1,1,stabilizersNotComplete)

        for p in edge_positions_2_1:

            error_p=self.errors_edge_P[errCount3]
            errCount3+=1
            self.stabilizer(stabilizerType,p,error_p,edge2,1,stabilizersNotComplete)
            
                        

######              ROUND TWO               ############


            
        for p in full_positions_2:
            error_p=self.errors_full_P[errCount4]
            errCount4+=1                        
            self.stabilizer(stabilizerType,p,error_p,"F",2,stabilizersNotComplete)

        for p in edge_positions_1_2:

            error_p=self.errors_edge_P[errCount3]
            errCount3+=1
            self.stabilizer(stabilizerType,p,error_p,edge1,2,stabilizersNotComplete)

        for p in edge_positions_2_2:

            error_p=self.errors_edge_P[errCount3]
            errCount3+=1
            self.stabilizer(stabilizerType,p,error_p,edge2,2,stabilizersNotComplete)


              





    def apply_matching(self,error_type,matching):
        """ applies appropriate flips to the array to bring it back to the codespace using the given matching """

        channel=0 if error_type=="X" else 1
        
        flips=[]
        
        for pair in matching:
            
            [p0,p1]=pair[0]
            [q0,q1]=pair[1]

            if channel==1 and (p1==-1 or p1==self.size*2+1)and(q1==-1 or q1==self.size*2+1):
                flips+=[]
            elif channel==0 and (p0==-1 or p0==self.size*2+1)and(q0==-1 or q0==self.size*2+1):
                flips+=[]
            else:

                s0=int(math.copysign(1,q0-p0))
                s1=int(math.copysign(1,q1-p1))

                range0=range(1,abs(q0-p0),2)
                range1=range(1,abs(q1-p1),2)
                       
                for x in range1:
                    flips+=[[p0,p1+s1*x]]
                for y in range0:
                    flips+=[[p0+s0*y,q1]]
                
        for flip in flips:
            self.array[flip[0]][flip[1]][channel]*=-1


    def apply_flip_array(self,channel,flip_array):

        c=0 if channel=="X" else 1

        for (x0,x1) in self.positions_Q:
            self.array[x0][x1][c]*=flip_array[x0][x1]

            
    def measure_logical(self):

        logical_x=1
        logical_z=1
        positions_x=[[0,x] for x in range(0,2*self.size+1,2)]
        positions_z=[[y,0] for y in range(0,2*self.size+1,2)]

        for pos in positions_x:
            logical_x*=self.array[pos[0]][pos[1]][0]
        for pos in positions_z:
            logical_z*=self.array[pos[0]][pos[1]][1]

        return [logical_x,logical_z]

            

        












######################################################################






class PlanarLattice3D:

    def __init__(self,size):

        self.size=size        
        self.N=size*(size+1) # number of stabilizers
        
        self.syndrome_P=[1]*self.N
        self.syndrome_S=[1]*self.N
        
        self.parity_array_P=[]
        self.parity_array_S=[]
        
        self.time=len(self.parity_array_P)
        
        self.definite_array_P=[[1]*self.N]

        self.positions_S=[(x,y) for x in range(0,2*size+1,2) for y in range(1,2*size+1,2)];
        self.positions_P=[(x,y) for x in range(1,2*size+1,2) for y in range(0,2*size+1,2)]
        
    def getTime(self):
        self.time=len(self.parity_array_P)


    def showTopLayer(self):

        print_array=[[0 for x in range(2*self.size+1)] for y in range(2*self.size+1)]


        for i in range(len(self.positions_S)):
            Spos=self.positions_S[i]
            Ppos=self.positions_P[i]
            print_array[Spos[0]][Spos[1]]=self.parity_array_S[-1][i]
            print_array[Ppos[0]][Ppos[1]]=self.parity_array_P[-1][i]

      
        plt.imshow(print_array)
        plt.show()

        
    def addMeasurement(self,lat):

        plaquette_layer=[1 for x in range(self.N)]
        star_layer=[1 for x in range(self.N)]

        for i in range(self.N):

            Ppos=self.positions_P[i]
            Spos=self.positions_S[i]

            plaquette_layer[i]=lat.array[Ppos[0]][Ppos[1]]
            star_layer[i]=lat.array[Spos[0]][Spos[1]]
       

        new_syndrome_P=copy.copy(plaquette_layer)
        new_syndrome_S=copy.copy(star_layer)

        
        for i in range(self.N):
            plaquette_layer[i]*=self.syndrome_P[i]
            star_layer[i]*=self.syndrome_S[i]
       
        self.parity_array_S+=[star_layer]
        self.parity_array_P+=[plaquette_layer]

        self.syndrome_P=new_syndrome_P
        self.syndrome_S=new_syndrome_S

    def findAnyons(self):

        self.getTime()
        
        anyon_positions_x=()
        anyon_positions_z=()
                
        for t in range(self.time):

            anyon_positions_x_t=()
            anyon_positions_z_t=()
            
            for i in range(self.N):
                
                                
                if self.parity_array_P[t][i]==-1:
                    anyon_positions_x_t+=((t,)+(self.positions_P[i]),)
                    
                if self.parity_array_S[t][i]==-1:
                    anyon_positions_z_t+=((t,)+(self.positions_S[i]),)

            anyon_positions_x+=(anyon_positions_x_t,)
            anyon_positions_z+=(anyon_positions_z_t,)

        self.anyon_positions_x=anyon_positions_x
        self.anyon_positions_z=anyon_positions_z
        
        self.anyon_positions_P = anyon_positions_x
        self.anyon_positions_S = anyon_positions_z 

       

        
