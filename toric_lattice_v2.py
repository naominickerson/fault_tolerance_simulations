import random
import math
import copy
import itertools
import numpy as np

#For using .showArray() function uncomment this
import matplotlib.pyplot as plt



# generate a list of errors to apply from the two error vectors
I,X,Y,Z=[1,1],[-1,1],[-1,-1],[1,-1]

errorListP1=[[1,[I,I]],[1,[I,Z]],[1,[I,X]],[1,[I,Y]],
            [1,[X,X]],[1,[X,Y]],[1,[Y,Y]],[1,[X,Z]],
            [1,[Y,Z]],[1,[Z,Z]],[-1,[I,I]],[-1,[I,Z]],
            [-1,[I,X]],[-1,[I,Y]],[-1,[X,X]],[-1,[X,Y]],
            [-1,[Y,Y]],[-1,[X,Z]],[-1,[Y,Z]],[-1,[Z,Z]]]

errorListP2=[[1,[I,I]],[1,[I,Z]],[-1,[I,X]],[-1,[I,Y]],
            [1,[X,X]],[1,[X,Y]],[1,[Y,Y]],[-1,[X,Z]],
            [-1,[Y,Z]],[1,[Z,Z]],[-1,[I,I]],[-1,[I,Z]],
            [1,[I,X]],[1,[I,Y]],[-1,[X,X]],[-1,[X,Y]],
            [-1,[Y,Y]],[1,[X,Z]],[1,[Y,Z]],[-1,[Z,Z]]]

errorListS1=[[1,[I,I]],[1,[I,X]],[1,[I,Z]],[1,[I,Y]],
            [1,[Z,Z]],[1,[Z,Y]],[1,[Y,Y]],[1,[Z,X]],
            [1,[Y,X]],[1,[X,X]],[-1,[I,I]],[-1,[I,X]],
            [-1,[I,Z]],[-1,[I,Y]],[-1,[Z,Z]],[-1,[Z,Y]],
            [-1,[Y,Y]],[-1,[Z,X]],[-1,[Y,X]],[-1,[X,X]]]

errorListS2=[[1,[I,I]],[1,[I,X]],[-1,[I,Z]],[-1,[I,Y]],
            [1,[Z,Z]],[1,[Z,Y]],[1,[Y,Y]],[-1,[Z,X]],
            [-1,[Y,X]],[1,[X,X]],[-1,[I,I]],[-1,[I,X]],
            [1,[I,Z]],[1,[I,Y]],[-1,[Z,Z]],[-1,[Z,Y]],
            [-1,[Y,Y]],[1,[Z,X]],[1,[Y,X]],[-1,[X,X]]]

""" 2D version of the Toric Lattice
	
Input Parameters: 
-----------------
size --> dimension of the lattice
	
Data Array:
----------

STAR -- Q -- STAR -- Q -- STAR -- Q --
|            |            | 
|            |            |
Q    PLAQ    Q    PLAQ    Q    PLAQ
|            |            |
|            |            |
PLAQ -- Q -- STAR -- Q -- STAR -- Q --
|            |            | 
|            |            |
Q    PLAQ    Q    PLAQ    Q    PLAQ
|            |            |
|            |            |
PLAQ -- Q -- STAR -- Q -- STAR -- Q --
|            |            |
|            |            |

PLAQ and STAR positions store the value of the most recent
stabilizer measurement. They can take a value of 0 or 1. 

Q(ubit) positions store the state of a qubit, a list: [x,z] x,z in {1,-1} 
	
"""


    
class PlanarLattice:
    """2D version of the toric lattice"""

    def __init__(self,size):
    

        self.size=size
        
        self.N_Q=2*size*size
        self.N_P=size*size
       
        self.positions_x_anyons=None
        self.positions_z_anyons=None
        
        ## Define basic qubit and stabilizer positions

        self.positions_Q=[(x,y) for x in range(0,2*size) for y in range(((x+1)%2),2*size,2) ]
        self.positions_S=[(x,y) for x in range(0,2*size,2) for y in range(0,2*size,2)]        
        self.positions_P=[(x,y) for x in range(1,2*size,2) for y in range(1,2*size,2)]
        
        ## Defining list of positions for two interspersed round of plaquette measurement

        self.positions_P1=[(x,y) for x in range(1,2*size,2) for y in range(x%4,2*size,4)]
        self.positions_P2=[(x,y) for x in range(1,2*size,2) for y in range((x+2)%4,2*size,4)]
        self.positions_S1=[(x,y)  for x in range(0,2*size,2) for y in range(x%4,2*size,4)]
        self.positions_S2=[(x,y)  for x in range(0,2*size,2) for y in range((x+2)%4,2*size,4)]

        self.positions_anyons_P=None
        self.positions_anyons_S=None

       
        ## Initialise array

        self.array=[[0 for x in range(2*self.size)] for _ in range(2*self.size)]
        for i in range(self.N_Q):
            self.array[self.positions_Q[i][0]][self.positions_Q[i][1]]=[1,1]

        for i in range(self.N_P):
            self.array[self.positions_P[i][0]][self.positions_P[i][1]]=1
            self.array[self.positions_S[i][0]][self.positions_S[i][1]]=1



    def showArray(self,arrayType,channel=0):
        """ displays the current state as an array plot
        """
        c=0 if channel=="X" else 1
        
        if arrayType=="errors":            
            
            print_array=[[x[c] if isinstance(x,list) else 0 for x in row]for row in self.array]

        if arrayType=="stabilizers":

            print_array=[[x if isinstance(x,int) else 0 for x in row] for row in self.array]
        
        plt.imshow(print_array)
        plt.show()



    
    def showArrayText(self,arrayType="errors",channel=0):
        """ displays the current state in the given channel in text
        """


        if channel in ["X",0]: c=0
        elif channel in ["Z",1]: c=1
        else: 
            "channel = ",channel," is not supported. \"X\" and \"Z\" are the possible channels"

        
        if arrayType in ["error","errors","Errors","Error"]: 
            print_array = [[str(x[c]) if isinstance(x,list) else '.' for x in row] for row in self.array]
        
        elif arrayType in ["stabilizers","stabs","stabilisers","stabilizer","stabiliser"]:
            print_array = [[str(x) if isinstance(x,int) else '.' for x in row] for row in self.array]

        elif arrayType in ["all","both"]:
            print_array = [[str(x[c]) if isinstance(x,list) else ("#" if x==-1 else ".") for x in row] for row in self.array]

        else: 
            print 'arrayType = ',arrayType,'. This array type isn\'t supported by showArrayText.'
            print ' please choose  \'errors\' or \'stabilizers\''
        

        print '\n showing the ',arrayType,' array',
        if arrayType in ["error","errors","Errors","Error"]: print 'for the ',channel,' channel.\n'
        else: print '.\n'
        col_width = 3
        for row in print_array:
            print "".join(word.ljust(col_width) for word in row)



    #####
    #####
    #####       MEASURING STABILIZERS
    #####
    #####


    def measurePlaquettes(self,pLie=0,pMeasure=1):
        """ calculates the value of each plaquette stabilizer given a fixed probability of lying

        Parameters:
        -----------
        pLie --> lie probability. Default: 0

        Returns:
        --------
        self.array is updated with the new plaquette values
        """

        m=2*self.size

        for p0,p1 in self.positions_P:
            
            stabQubits=((p0,(p1-1)%m),(p0,(p1+1)%m),((p0-1)%m,p1),((p0+1)%m,p1))
            
#            print "(%d,%d) --> ("%(p0,p1),
            stab=1
            for s0,s1 in stabQubits:
                stab*=self.array[s0][s1][0]
#                print self.array[s0][s1][0],",",
            
#            print ") --> %d"%(stab,),            
                
            if random.random()<pLie: stab*=-1

            if random.random()<pMeasure: self.array[p0][p1]=stab
            


    def measureStars(self,pLie=0,pMeasure=1):      
        """ calculates the value of each star stabilizer given a fixed probability of lying

        Parameters:
        -----------
        pLie --> lie probability. Default: 0

        Returns:
        --------
        self.array is updated with the new star values
        """

        m=2*self.size

        for p0,p1 in self.positions_S:
            stabQubits=((p0,(p1-1)%m),(p0,(p1+1)%m),((p0-1)%m,p1),((p0+1)%m,p1))
            
            stab=1
            for s0,s1 in stabQubits:
                stab*=self.array[s0][s1][1]
            
            if random.random()<pLie: stab*=-1

            if random.random()<pMeasure: self.array[p0][p1]=stab


    def apply_matching(self,error_type,matching):
        """ For correction of a 2D array. Pauli X or Z flips applied to return state to the codespace according to the given matching.
        
        Params:
        ------
        error_type --> which channel should the matching be applied to, X or Z
        matching --> list of pairs of anyon positions
        """

        if error_type in ["X","x",0]: channel=0
        elif error_type in ["Z","z",1]: channel =1
        else: 
            raise ValueError('valid error types are "X" or "Z"')
        
        flips=[]
        for pair in matching:
            
            [p0,p1]=pair[0]
            [q0,q1]=pair[1]
            

            m=2*self.size
            
            d0=(q0-p0)%m
            d1=(q1-p1)%m

            
            if d0 < m-d0:
                end0=q0
                for x in range(1,d0,2):
                    flips+=[[(p0+x)%m,p1]]                
            else:
                end0=p0
                for x in range(1,m-d0,2):
                    flips+=[[(q0+x)%m,q1]]
                    
            if d1 < m-d1:
                for y in range(1,d1,2):
                    flips+=[[end0,(p1+y)%m]]
            else:
                for y in range(1,m-d1,2):
                    flips+=[[end0,(q1+y)%m]]
                    
        
        for flip in flips:
            self.array[flip[0]][flip[1]][channel]*=-1


            

                
    def apply_flip_array(self,channel,flip_array):
        
        if channel in ["X","x",0]: c=0
        elif channel in ["Z","z",1]: c=1
        else: 
            raise ValueError('channel must be X or Z')

        for (x0,x1) in self.positions_Q:
            self.array[x0][x1][c]*=flip_array[x0][x1]       

    def applyNCorrelatedErrors(self,pX,N):

        direction =(0,1)

        for q0,q1 in self.positions_Q:
            rand1 = random.random()

            if rand1<pX:
                d = random.choice(direction)
                if d==0 and q0%2==0:
                    positions = [[(q0+2*i)%(2*self.size),q1] for i in range(N)]
                elif d==1 and q0%2==0: 
                    positions = [[(q0-2*i)%(2*self.size),q1] for i in range(N)]
                elif d==0 and q0%2==1:
                    positions = [[q0,(q1+2*i)%(2*self.size)] for i in range(N)]
                elif d==1 and q0%2==1:
                    positions = [[q0,(q1-2*i)%(2*self.size)] for i in range(N)]

                for qq0,qq1 in positions:
                    self.array[qq0][qq1][0]*=-1



 

    def applyRandomErrors(self,pX,pZ):
        """ Applies random X and Z errors with the given probabilites to all qubits.
        
        The qubit values in self.array are updated.
        """
        for q0,q1 in self.positions_Q:
            rand1=random.random()
            rand2=random.random()
            
            if rand1<pX:
                self.array[q0][q1][0]*=-1
#                print "X error applied at position: ",q0,",",q1,"new value is ",self.array[q0][q1]
            if rand2<pZ:
                self.array[q0][q1][1]*=-1
  
        


    def findAnyons(self):
        """ Locates all the '-1' stabilizer outcomes in the 2D array
        
        Returns:
        -------
        No return value. The list of anyon positions is stored in the 
        variable self.positions_anyons_P(S).
 
        """
        anyon_positions_S=[]
        anyon_positions_P=[]
        
        for p0,p1 in self.positions_S:
            if self.array[p0][p1]==-1:
                anyon_positions_S += [(p0,p1)]
        for p0,p1 in self.positions_P:
            if self.array[p0][p1]==-1:
                anyon_positions_P += [(p0,p1)]

        # for i in range(self.N_P):
        #     if self.star[i]==-1:
        #         anyon_positions_S+=[self.positions_S[i]]
        #     if self.plaq[i]==-1:
        #         anyon_positions_P+=[self.positions_P[i]]
                 
        self.positions_anyons_P=anyon_positions_P
        self.positions_anyons_S=anyon_positions_S
        



    def measure_logical(self):
        """ measures the logical state of the array
        
        Assumes: 
        -------
        That the array is in the code space. That is, if all stabilizers
        were to be measured they should all return +1.

        Returns:
        -------
        A list of the form [[x1,z1],[x2,z2]] where all values in {1,-1}
        giving the logical state of the x and z components of the two 
        encoded qubits.
        
        """

        logical_x=[1,1]
        logical_z=[1,1]
        positions_z1=[[1,x] for x in range(0,2*self.size,2)]
        positions_z2=[[y,1] for y in range(0,2*self.size,2)]
        positions_x1=[[0,x] for x in range(1,2*self.size,2)]
        positions_x2=[[y,0] for y in range(1,2*self.size,2)]

        for pos in positions_z1:
            logical_z[0]*=self.array[pos[0]][pos[1]][1]
        for pos in positions_z2:
            logical_z[1]*=self.array[pos[0]][pos[1]][1]
        for pos in positions_x1:
            logical_x[0]*=self.array[pos[0]][pos[1]][0]
        for pos in positions_x2:
            logical_x[1]*=self.array[pos[0]][pos[1]][0]

        return [logical_x,logical_z]




#####################################################################
#####################################################################
#####################################################################


    def stabilizer(self,channel,pos,error,round12,stabilizersNotComplete=0):

        """ measures value of a stabilizer at a given position, and updates the stabilizer array

        Parameters:
        ----------
        channel -- "plaquette" or "star"
        pos -- array position of stabilizer to be measured
        error -- error induced by the stabilizer, e.g. [[1,-1],[1,1],-1]: one qubit gets Z error, and the stabilizer 'lies'
        round12 -- can take values 1 or 2 to indicate 1st or 2nd half-round of stabilizers
        stabilizersNotComplete -- fraction of stabilziers that aren't evaluated. Default: 0

        
        """

        if round12 not in [1,2]: raise ValueError("round12 must be either 1 or 2")

        if channel == "plaquette": c=0
        elif channel == "star": c=1
        else: raise ValueError("channel must be either \"plaquette\" or \"star\" ")

        
        # option that a stabilizer doesn't get measured. The stabilizer value stays the same as the previous round and no errors are applied
        
        if random.random()>stabilizersNotComplete: 
            

            p=pos
            m=2*self.size  
            stabQubits=((p[0],(p[1]-1)%m),(p[0],(p[1]+1)%m),((p[0]-1)%m,p[1]),((p[0]+1)%m,p[1]))
        
            # select random order for the qubits
            order=[0,1,2,3]
            random.shuffle(order)
        
            lie,err=error  
        
            ## measure stabilizers first for round 2
            if round12==2:
                stab=lie
                for q in stabQubits:
                #                stab*=self.array[q[0]][q[1]][c]
                    if self.array[q[0]][q[1]][c]==-1: stab = -stab
                    self.array[p[0]][p[1]]=stab
                
             ## apply the error
                
            errQubits = [stabQubits[order[0]],stabQubits[order[1]]]
            if err!=[[1,1],[1,1]]:
                for i in (0,1):
                    q=errQubits[i]
                    if err[i][0]==-1: self.array[q[0]][q[1]][0]=-self.array[q[0]][q[1]][0]
                    if err[i][1]==-1: self.array[q[0]][q[1]][1]=-self.array[q[0]][q[1]][1]
                
                
             ## measure stabilizers second for round1  
            if round12==1:
                stab=lie
                for q in stabQubits:
                    if self.array[q[0]][q[1]][c]==-1: stab=-stab
                    self.array[p[0]][p[1]]=stab







          

    def measureNoisyStabilizers(self,channel,errorVector4,stabilizersNotComplete=0):

        """ measures all the stabilizers of given channel according to the error vector.

        Parameters:
        ----------
        channel -- either "plaquette" or "star" 
        errorVector4 -- error vector describing 4 qubit stabilizer superoperator. 
        stabilizersNotComplete -- fraction of stabilizers not measured. 

        Returns: 
        --------
        No value returned. Stabilizer values updated in self.array
        """
        
	if channel=="plaquette":
        	errorList1=errorListP1
        	errorList2=errorListP2        	
	elif channel=="star":
        	errorList1=errorListS1
        	errorList2=errorListS2
        else: 
            print "USAGE: measureNoisyStabilizers(channel, errorVector4)\n channel must be *star* or *plaquette* \n"
            return 0

        sortList1=sorted(zip(errorVector4,errorList1),reverse=True)     # label the error probabilities list
        sortList2=sorted(zip(errorVector4,errorList2),reverse=True)     # label the error probabilities list
        
        probs1,errors1=zip(*sortList1)                        # separate ordered lists into lists of errors and their probs
        probs2,errors2=zip(*sortList2) 

        c_probs1=np.cumsum(np.array(probs1)).tolist()           # sum up cumulative probability lists
        c_probs2=np.cumsum(np.array(probs2)).tolist()


## SET PARAMETERS BASED ON CHANNEL TYPE

        #stabilizerType=channel
        positions_1= self.positions_P1 if channel=="plaquette" else self.positions_S1
        positions_2= self.positions_P2 if channel=="plaquette" else self.positions_S2
        
        
        self.errors_P1=[]                                # generate lists of errors and lies to be applied
        self.errors_P2=[]
        for i in range(len(positions_1)):                      # Select random error for each stabilizer to 
            rand1=random.random()
            rand2=random.random()                       # be measured
            
            for j in range(20):
                if rand1<c_probs1[j]:
                    self.errors_P1+=[errors1[j]]
                    break;
                if j==19:
                    self.errors_P1+=[errors1[0]]
                    
            #print i,round(rand1,2),(len(self.errors_P1)),self.errors_P1[-1]
                       
            for j in range(20):            
                if rand2<c_probs2[j]:
                    self.errors_P2+=[errors2[j]]
                    break;
                if j==19:
                    self.errors_P2+=[errors2[0]]
            
                


######              ROUND ONE               ############

        for i in range(len(positions_1)):
            pos=positions_1[i]
            error_p=self.errors_P1[i]                        
            self.stabilizer(channel,pos,error_p,1,stabilizersNotComplete)
                                

######              ROUND TWO               ############

        for i in range(len(positions_2)):  
            pos=positions_2[i]
            error_p=self.errors_P2[i]                     
            self.stabilizer(channel,pos,error_p,2,stabilizersNotComplete)

              




           











######################################################################
######################################################################
######################################################################            
######################################################################
######################################################################






class Lattice3D:
    """ 3D extension for the toric code """

    def __init__(self,size):

        self.size=size        
        self.N=size*size # number of stabilizers
        
        self.syndrome_P=[1]*self.N
        self.syndrome_S=[1]*self.N
        
        self.parity_array_P=[]
        self.parity_array_S=[]
        
        self.time=len(self.parity_array_P)
                
        self.definite_array_P=[[1]*self.N]
     
        self.positions_S=[(x,y) for x in range(0,2*size,2) for y in range(0,2*size,2)];
        self.positions_P=[(x,y) for x in range(1,2*size,2) for y in range(1,2*size,2)]
        
    def getTime(self):
        self.time=len(self.parity_array_P)

            
        

    def showTopLayer(self):
        """displays the most recent layer added to the lattice"""
       
        print_array=[[0 for x in range(2*self.size)] for y in range(2*self.size)]
        
        for i in range(len(self.positions_S)):
            Spos=self.positions_S[i]
            Ppos=self.positions_P[i]
            print_array[Spos[0]][Spos[1]]=self.parity_array_S[-1][i]
            print_array[Ppos[0]][Ppos[1]]=self.parity_array_P[-1][i]

        plt.imshow(print_array)
        plt.show()

        
    def addMeasurement(self,lat):
        """ adds a new layer to the 3D array"""

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
        """ identifies the positions of all the anyons in the parity lattice"""
        self.getTime()
        
        anyon_positions_P=()
        anyon_positions_S=()
                
        for t in range(self.time):

            anyon_positions_P_t=()
            anyon_positions_S_t=()
            
            for i in range(self.N):
                
                                
                if self.parity_array_P[t][i]==-1:
                    anyon_positions_P_t+=((t,)+(self.positions_P[i]),)
                    
                if self.parity_array_S[t][i]==-1:
                    anyon_positions_S_t+=((t,)+(self.positions_S[i]),)

            anyon_positions_S+=(anyon_positions_S_t,)
            anyon_positions_P+=(anyon_positions_P_t,)

        self.anyon_positions_S=anyon_positions_S
        self.anyon_positions_P=anyon_positions_P


            


       

        
