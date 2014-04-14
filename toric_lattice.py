import random
import math
import copy
import itertools
import numpy as np

#import matplotlib.pyplot as plt


##INFO:
##   Errors stored in an array, each entry represents either 
##   a qubit: [xError?,zError?] with xError,zError in {1,-1}
##   a stabiliser: star or plaquette depending on location with S in {1,-1}



### PlanarLattice

### Associated Methods:

# 	constructArray()
#	constructLists()	information is stored in two ways in the lattice and these operations convert between the two

#	showArray(arrayType="stabilizers" or "errors", channel ="X" or "Z")

#	measurePlaquettes(pLie)
#	measureStars(pLie)
#	measureNoisyPlaquettes()
#	measureNoisyStars()

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

class PlanarLattice:

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

       
        ## Initialise empty lists to contain qubit and stabilizer values       

        self.qubits=[[1]*2 for _ in range(self.N_Q)]
        self.plaq=[0]*self.N_P
        self.star=[0]*self.N_P
       
        ## Initialise array

        self.array=[[[1,1]]*(2*self.size) for _ in range(2*self.size)]

       

    def __constructArray(self):

        for i in range(self.N_Q):
            self.array[self.positions_Q[i][0]][self.positions_Q[i][1]]=self.qubits[i]

        for i in range(self.N_P):
            self.array[self.positions_P[i][0]][self.positions_P[i][1]]=self.plaq[i]
            self.array[self.positions_S[i][0]][self.positions_S[i][1]]=self.star[i]
            
    def __constructLists(self):

        self.star=[]
        for pos in self.positions_S:
            self.star+=[self.array[pos[0]][pos[1]]]

        self.plaq=[]
        for pos in self.positions_P:
            self.plaq+=[self.array[pos[0]][pos[1]]]

        self.qubits=[]
        for pos in self.positions_Q:
            self.qubits+=[self.array[pos[0]][pos[1]]]
       
               

    def showArray(self,arrayType,channel=0):

        c=0 if channel=="X" else 1
        
        if arrayType=="errors":            
            
            print_array=[[x[c] if isinstance(x,list) else 0 for x in row]for row in self.array]

        if arrayType=="stabilizers":

            print_array=[[x if isinstance(x,int) else 0 for x in row] for row in self.array]

        
        plt.imshow(print_array)
        plt.show()


##########################################################################      
##################                       #################################
##################     BASIC TOOLS       #################################
##################                       #################################
##########################################################################



    def measurePlaquettes(self,pLie=0):
                 
        for i in range(self.N_P):

            pos=self.positions_P[i]
            m=2*self.size
            stabQubits=((pos[0],(pos[1]-1)%m),(pos[0],(pos[1]+1)%m),((pos[0]-1)%m,pos[1]),((pos[0]+1)%m,pos[1]))

            stab=1
            for j in range(4):    
                stab*=self.array[stabQubits[j][0]][stabQubits[j][1]][0]

            rand=random.random()
            stab*=1 if rand>pLie else -1
               
            self.plaq[i]=stab
  
        self.__constructArray()


    def measureStars(self,pLie=0):      
       
        for i in range(self.N_P):

            pos=self.positions_S[i]
            m=2*self.size
            stabQubits=((pos[0],(pos[1]-1)%m),(pos[0],(pos[1]+1)%m),((pos[0]-1)%m,pos[1]),((pos[0]+1)%m,pos[1]))

            stab=1
            for j in range(4):    
                stab*=self.array[stabQubits[j][0]][stabQubits[j][1]][1]

            rand=random.random()
            stab*=1 if rand>pLie else -1
                        
            self.star[i]=stab


        self.__constructArray()



    def apply_matching(self,error_type,matching):


        channel=0 if error_type=="X" else 1
        
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

        self.__constructLists()
            

                
    def apply_flip_array(self,channel,flip_array):

        c=0 if channel=="X" else 1

        for (x0,x1) in self.positions_Q:
            self.array[x0][x1][c]*=flip_array[x0][x1]       

        self.__constructArray()


    def applyRandomErrors(self,pX,pZ):

        for i in range(self.N_Q):

            rand1=random.random()
            rand2=random.random()

            if rand1<pX:
                self.qubits[i][0]=-self.qubits[i][0]
            if rand2<pZ:
                self.qubits[i][1]=-self.qubits[i][1]

        self.__constructArray()


  
        


    def findAnyons(self):

        anyon_positions_S=[]
        anyon_positions_P=[]
        
        for i in range(self.N_P):
            if self.star[i]==-1:
                anyon_positions_S+=[self.positions_S[i]]
            if self.plaq[i]==-1:
                anyon_positions_P+=[self.positions_P[i]]
                 
        self.positions_anyons_P=anyon_positions_P
        self.positions_anyons_S=anyon_positions_S
        



    def measure_logical(self):


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


    # note to change: pass only an error 'number' to this function and then 
    # use the lookup tables at the top. Eg. error = 13 -> [1,[-1,-1],[1,1]] 

    def stabilizer(self,channel,pos,error,round12):

 #       if channel!="plaquette" and channel!="star":
#            print "ERROR: channel must be either star or plaquette"
  #      if round12!=1 and round12!=2:
   #         print "ERROR: round must be either 1 or 2 "            
        c=0 if channel=="plaquette" else 1
        
          
        p=pos
        m=2*self.size  
        stabQubits=((p[0],(p[1]-1)%m),(p[0],(p[1]+1)%m),((p[0]-1)%m,p[1]),((p[0]+1)%m,p[1]))

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
        
        #alternative version: 
        #random.shuffle(stabQubits)
        #errQubits = stabQubits[0:2]

 #       random.shuffle(order)

        errQubits = [stabQubits[order[0]],stabQubits[order[1]]]
#            errQubits=[stabQubits[order[0]],stabQubits[order[1]]]            
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
#                stab*=self.array[q[0]][q[1]][c]
            self.array[p[0]][p[1]]=stab







          

    def measureNoisyStabilizers(self,channel,errorVector4):

        ## error vectors corrected 17/07/13
        
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
        
        #print [round(x,2) for x in c_probs1  ] 

        #print c_probs1
        
        self.errors_P1=[]                                # generate lists of errors and lies to be applied
        self.errors_P2=[]
        for i in range(self.N_P/2):                      # Select random error for each stabilizer to 
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
            
                
## SET PARAMETERS BASED ON CHANNEL TYPE

        #stabilizerType=channel
        positions_1= self.positions_P1 if channel=="plaquette" else self.positions_S1
        positions_2= self.positions_P2 if channel=="plaquette" else self.positions_S2

########################################################
######              ROUND ONE               ############
########################################################
        for i in range(len(positions_1)):
            pos=positions_1[i]
            error_p=self.errors_P1[i]                        
            self.stabilizer(channel,pos,error_p,1)
#        self.__constructLists()
                                
########################################################
######              ROUND TWO               ############
########################################################
        for i in range(len(positions_2)):  
            pos=positions_2[i]
            error_p=self.errors_P2[i]                     
            self.stabilizer(channel,pos,error_p,2)

              
        ### Update array etc.
        self.__constructLists()
    
        



#######################################################################

    










    
        

              
    

        
        
        
    
    

            


            

        











######################################################################
######################################################################
######################################################################            
######################################################################
######################################################################






class Lattice3D:

    def __init__(self,size):

        self.size=size        
        self.N=size*size # number of stabilizers
        
        self.syndrome_P=[1]*self.N
        self.syndrome_S=[1]*self.N
        
        self.parity_array_P=[]
        self.parity_array_S=[]
        
        self.time=len(self.parity_array_P)
                
        self.definite_array_P=[[1]*self.N]
     
##        self.positions_full_S=()
##        self.positions_edge_S_T=()
##        self.positions_edge_S_B=()
##        self.positions_full_P=()
##        self.positions_edge_P_L=()
##        self.positions_edge_P_R=()
## 
##        for j in range(size):
##            self.positions_edge_S_T+=((0,2*j+1),)
##            self.positions_edge_S_B+=((2*size,2*j+1),)
##            for i in range(size-1):
##                self.positions_full_S+=((2*i+2,2*j+1),)
##      
##        for i in range(size):
##            self.positions_edge_P_L+=((2*i+1,0),)
##            self.positions_edge_P_R+=((2*i+1,2*size),)
##            for j in range(size-1):
##                self.positions_full_P+=((2*i+1,2*j+2),)
          
        #self.positions_P=self.positions_edge_P_L+self.positions_full_P+self.positions_edge_P_R
        #self.positions_S=self.positions_edge_S_T+self.positions_full_S+self.positions_edge_S_B

        self.positions_S=[(x,y) for x in range(0,2*size,2) for y in range(0,2*size,2)];
        self.positions_P=[(x,y) for x in range(1,2*size,2) for y in range(1,2*size,2)]
        
    def getTime(self):
        self.time=len(self.parity_array_P)

            
        
#P_edge_R,P_edge_L,P_full,S_edge_T,S_edge_B,S_full


    def showTopLayer(self):

        print_array=[[0 for x in range(2*self.size)] for y in range(2*self.size)]
        
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


            

##    This is no longer used, after changing to a final round
##    Of stabilizer measurements which are PERFECT
        
##    def closeLattice(self):
##        
##        plaquette_layer= [1]*self.N
##        star_layer     = [1]*self.N
##
##        new_syndrome_P=copy.copy(plaquette_layer)
##        new_syndrome_S=copy.copy(star_layer)
##
##        
##        for i in range(self.N):
##            plaquette_layer[i]*=self.syndrome_P[i]
##            star_layer[i]*=self.syndrome_S[i]
##       
##        self.parity_array_S+=[star_layer]
##        self.parity_array_P+=[plaquette_layer]
##
##        self.syndrome_P=new_syndrome_P
##        self.syndrome_S=new_syndrome_S
##
##
        



         


       

        
