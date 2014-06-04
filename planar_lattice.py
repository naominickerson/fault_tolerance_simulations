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

        ## Initialise lists to contain qubit and stabilizer values       

        self.qubits=[[1,1] for _ in range(self.N_Q)]
        self.full_P=[1]*self.N_full_P
        self.full_S=[1]*self.N_full_P
        self.edge_P_L=[1]*self.N_edge_P
        self.edge_P_R=[1]*self.N_edge_P       
        self.edge_S_T=[1]*self.N_edge_P
        self.edge_S_B=[1]*self.N_edge_P

        ## Initialise array

        self.array=[[1]*(2*self.size+1) for _ in range(2*self.size+1)]

        for i in range(self.N_Q):
            self.array[self.positions_Q[i][0]][self.positions_Q[i][1]]=self.qubits[i]

        for i in range(self.N_full_P):
            self.array[self.positions_full_P[i][0]][self.positions_full_P[i][1]]=self.full_P[i]
            self.array[self.positions_full_S[i][0]][self.positions_full_S[i][1]]=self.full_S[i]
            
        for i in range(self.N_edge_P):
            self.array[self.positions_edge_P_L[i][0]][self.positions_edge_P_L[i][1]]=self.edge_P_L[i]
            self.array[self.positions_edge_P_R[i][0]][self.positions_edge_P_R[i][1]]=self.edge_P_R[i]
            self.array[self.positions_edge_S_T[i][0]][self.positions_edge_S_T[i][1]]=self.edge_S_T[i]
            self.array[self.positions_edge_S_B[i][0]][self.positions_edge_S_B[i][1]]=self.edge_S_B[i]
     
 



##    def constructArray(self):
##
##        for i in range(self.N_Q):
##            self.array[self.positions_Q[i][0]][self.positions_Q[i][1]]=self.qubits[i]
##
##        for i in range(self.N_full_P):
##            self.array[self.positions_full_P[i][0]][self.positions_full_P[i][1]]=self.full_P[i]
##            self.array[self.positions_full_S[i][0]][self.positions_full_S[i][1]]=self.full_S[i]
##            
##        for i in range(self.N_edge_P):
##            self.array[self.positions_edge_P_L[i][0]][self.positions_edge_P_L[i][1]]=self.edge_P_L[i]
##            self.array[self.positions_edge_P_R[i][0]][self.positions_edge_P_R[i][1]]=self.edge_P_R[i]
##            self.array[self.positions_edge_S_T[i][0]][self.positions_edge_S_T[i][1]]=self.edge_S_T[i]
##            self.array[self.positions_edge_S_B[i][0]][self.positions_edge_S_B[i][1]]=self.edge_S_B[i]
##        
##    def constructLists(self):
##
##        self.full_S=[]
##        for pos in self.positions_full_S:
##            self.full_S+=[self.array[pos[0]][pos[1]]]
##
##        self.edge_S_T=[]
##        for pos in self.positions_edge_S_T:
##            self.edge_S_T+=[self.array[pos[0]][pos[1]]]
##
##        self.edge_S_B=[]
##        for pos in self.positions_edge_S_B:
##            self.edge_S_B+=[self.array[pos[0]][pos[1]]]
##
##        self.full_P=[]
##        for pos in self.positions_full_P:
##            self.full_P+=[self.array[pos[0]][pos[1]]]
##
##        self.edge_P_L=[]
##        for pos in self.positions_edge_P_L:
##            self.edge_P_L+=[self.array[pos[0]][pos[1]]]
##
##        self.edge_P_R=[]
##        for pos in self.positions_edge_P_R:
##            self.edge_P_R+=[self.array[pos[0]][pos[1]]]
##
##        self.qubits=[]
##        for pos in self.positions_Q:
##            self.qubits+=[self.array[pos[0]][pos[1]]]
##       
##               


    def showArray(self,arrayType,channel=0):

        c=0 if channel=="X" else 1
        
        if arrayType=="errors":                        
            print_array=[[x[c] if isinstance(x,list) else 0 for x in row]for row in self.array]

        if arrayType=="stabilizers":
            print_array=[[x if isinstance(x,int) else 0 for x in row] for row in self.array]

        
        plt.imshow(print_array)
        plt.show()


    def showArrayText(self,arrayType="errors",channel=0):

        c=0 if channel=="X" else 1
        if channel=="X": c=0
        elif channel=="Z": c=1
        else: 
            "channel = ",channel," is not supported. \"X\" and \"Z\" are the possible channels"

        if arrayType in ["error","errors","Errors","Error"]: 

            print_array = [[str(x[c]) if isinstance(x,list) else '.' for x in row] for row in self.array]
            print_array = [[channel if x=='-1' else x for x in row] for row in print_array]

        
        elif arrayType in ["stabilizers","stabs","stabilisers","stabilizer","stabiliser"]:
        
            print_array = [[str(x) if isinstance(x,int) else '.' for x in row] for row in self.array]

        else: 
            print 'arrayType = ',arrayType,'. This array type isn\'t supported by showArrayText.'
            print ' please choose  \'errors\' or \'stabilizers\''


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


    def findAnyons(self):
  
        anyon_positions_x=[]
        anyon_positions_z=[]
        
        for i in range(self.N_full_P):
            if self.full_S[i]==-1:
                anyon_positions_x+=[self.positions_full_S[i]]

        for i in range(self.N_edge_P):
            if self.edge_S_T[i]==-1:
                anyon_positions_x+=[self.positions_edge_S_T[i]]
            if self.edge_S_B[i]==-1:
                anyon_positions_x+=[self.positions_edge_S_B[i]]

        for i in range(self.N_full_P):
            if self.full_P[i]==-1:
                anyon_positions_z+=[self.positions_full_P[i]]

        for i in range(self.N_edge_P):
            if self.edge_P_L[i]==-1:
                anyon_positions_z+=[self.positions_edge_P_L[i]]
            if self.edge_P_R[i]==-1:
                anyon_positions_z+=[self.positions_edge_P_R[i]]
      
             
        self.positions_anyons_S=anyon_positions_x
        self.positions_anyons_P=anyon_positions_z

        
##################   MEASUREMENT #################################



    def measurePlaquettes(self,pLie=0):
        
         
        for i in range(self.N_full_P):

            pos=self.positions_full_P[i]            
            stabQubits=((pos[0],pos[1]-1),(pos[0],pos[1]+1),(pos[0]-1,pos[1]),(pos[0]+1,pos[1]))

            stab=1
            for j in range(4):    
                stab*=self.array[stabQubits[j][0]][stabQubits[j][1]][0]

            rand=random.random()
            stab*=1 if rand>pLie else -1
               
            self.full_P[i]=stab
  

        for i in range(self.N_edge_P):

            pos_L=self.positions_edge_P_L[i]
            pos_R=self.positions_edge_P_R[i]
            
            stabQubits_L=((pos_L[0],pos_L[1]+1),(pos_L[0]-1,pos_L[1]),(pos_L[0]+1,pos_L[1]))
            stabQubits_R=((pos_R[0],pos_R[1]-1),(pos_R[0]-1,pos_R[1]),(pos_R[0]+1,pos_R[1]))
            
            stab_L=1
            stab_R=1
            for j in range(3):    
                stab_L*=self.array[stabQubits_L[j][0]][stabQubits_L[j][1]][0]
                stab_R*=self.array[stabQubits_R[j][0]][stabQubits_R[j][1]][0]

            rand=random.random()
            stab_L*=1 if rand>pLie else -1

            rand=random.random()
            stab_R*=1 if rand>pLie else -1
               
            self.edge_P_L[i]=stab_L
            self.edge_P_R[i]=stab_R

        self.constructArray()


    def measureStars(self,pLie=0):      
        #print
        for i in range(self.N_full_P):

            pos=self.positions_full_S[i]            
            stabQubits=((pos[0],pos[1]-1),(pos[0],pos[1]+1),(pos[0]-1,pos[1]),(pos[0]+1,pos[1]))

            stab=1
            for j in range(4):    
                stab*=self.array[stabQubits[j][0]][stabQubits[j][1]][1]

            rand=random.random()
            stab*=1 if rand>pLie else -1
            #print '0' if rand>pLie else '1',
            
            self.full_S[i]=stab
  

        for i in range(self.N_edge_P):

            pos_T=self.positions_edge_S_T[i]
            pos_B=self.positions_edge_S_B[i]

           
            
            stabQubits_T=((pos_T[0],pos_T[1]-1),(pos_T[0],pos_T[1]+1),(pos_T[0]+1,pos_T[1]))
            stabQubits_B=((pos_B[0],pos_B[1]-1),(pos_B[0],pos_B[1]+1),(pos_B[0]-1,pos_B[1]))
            
            stab_T=1
            stab_B=1

     
            for j in range(3):

                stab_T*=self.array[stabQubits_T[j][0]][stabQubits_T[j][1]][1]
                stab_B*=self.array[stabQubits_B[j][0]][stabQubits_B[j][1]][1]
              
            rand=random.random()
            stab_T*=1 if rand>pLie else -1
            #print '0' if rand>pLie else '1',

            rand=random.random()
            stab_B*=1 if rand>pLie else -1
            #print '0' if rand>pLie else '1',
            
            self.edge_S_T[i]=stab_T
            self.edge_S_B[i]=stab_B

        self.constructArray()


#####################################################################


    def stabilizer(self,channel,pos,error,sType,round12,stabilizersNotComplete=0):

        if channel!="plaquette" and channel!="star":
            print "ERROR: channel must be either star or plaquette"

        if round12!=1 and round12!=2:
            print "ERROR: round must be either 1 or 2 "

            
        c=0 if channel=="plaquette" else 1
        
          
        p=pos
        if sType=="F":
            stabQubits=((p[0],p[1]-1),(p[0],p[1]+1),(p[0]-1,p[1]),(p[0]+1,p[1]))
            order=[0,1,2,3]
        elif sType=="L":
            stabQubits=((p[0],p[1]+1),(p[0]-1,p[1]),(p[0]+1,p[1]))
            order=[0,1,2]
        elif sType=="R":
            stabQubits=((p[0],p[1]-1),(p[0]-1,p[1]),(p[0]+1,p[1]))
            order=[0,1,2]
        elif sType=="T":
            stabQubits=((p[0],p[1]-1),(p[0],p[1]+1),(p[0]+1,p[1]))
            order=[0,1,2]
        elif sType=="B":
            stabQubits=((p[0],p[1]-1),(p[0],p[1]+1),(p[0]-1,p[1]))
            order=[0,1,2]
        else:
            print "ERROR: pType must be a valid plaquette type: F,R or L "

        
        # Add option that a stabilizer doesn't get measured. The stabilizer value stays the same as the previous round and no errors are applied
        
        if random.random()>stabilizersNotComplete: 

            lie,err=error  
                    
            if round12==2:
                stab=lie
                for q in stabQubits:
                    stab*=self.array[q[0]][q[1]][c]
                    self.array[p[0]][p[1]]=stab

            random.shuffle(order)
            errQubits=[stabQubits[order[0]],stabQubits[order[1]]]            
            

            if err!=[[1,1],[1,1]]:
                for i in range(len(errQubits)):
                    q=errQubits[i]
                    self.array[q[0]][q[1]][0]*=err[i][0]
                    self.array[q[0]][q[1]][1]*=err[i][1]
                
            if round12==1:
                stab=lie
                for q in stabQubits:
                    stab*=self.array[q[0]][q[1]][c]
                self.array[p[0]][p[1]]=stab







          

    def measureNoisyStabilizers(self,channel,errorVector3,errorVector4,stabilizersNotComplete=0):

        if channel!="plaquette" and channel!="star":
            print "ERROR!: channel must be either *plaquette* or *star*"
            return 0;

        # generate a list of errors to apply from the two error vectors
        I,X,Y,Z=[1,1],[-1,1],[-1,-1],[1,-1]

        ##note error lists are corrected here 17/07/13
        
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

                                                            # zip errors and the probability vector together
                                                            # and sort them into p descending order
        errorList4=sorted(zip(errorVector4,errorList),reverse=True)
        errorList3=sorted(zip(errorVector3,errorList),reverse=True)

        error_prob_4,errorSort4=zip(*errorList4)            # separate ordered lists into
        error_prob_3,errorSort3=zip(*errorList3)            # lists of errors and their probs

        cum_prob_4=np.cumsum(np.array(error_prob_4)).tolist()   # sum up cumulative probability lists
        cum_prob_3=np.cumsum(np.array(error_prob_3)).tolist()

#        if cum_prob_4[-1]<1:
 #           cum_prob_4[-1]=1
#        if cum_prob_3[-1]<1:
 #           cum_prob_3[-1]=1
        
  
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

#        if len(self.errors_full_P)!=self.N_full_P:
 #           print len(self.errors_full_P),
  #          print cum_prob_4
        
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



########################################################
######              ROUND ONE               ############
########################################################

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
            
                        
########################################################
######              ROUND TWO               ############
########################################################

            
        for p in full_positions_2:
            if errCount4 >= len(self.errors_full_P):
                print len(self.errors_full_P),"||",

##            if errCount4 >= len(self.errors_full_P):
##                print "errCount4 =", errCount4,
##                print "self.errors_full_P", len(self.errors_full_P),
##                print "self.N_full_P", self.N_full_P,
##                print "size = ",self.size
                
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


              
        ### Update array etc.

        self.constructLists()
    
        



#######################################################################

    def apply_matching(self,error_type,matching):


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
#        print "FLIPS ",error_type,"\n",flips,"\n"
                
        for flip in flips:
            self.array[flip[0]][flip[1]][channel]*=-1

        self.constructLists()
            
                
            




  
        













    
        

##    def measureNoisyStars(vec12,vec2):
##
##                self.errors_edge_S_T=[]
##        self.errors_edge_S_B=[]
##
##                    self.errors_full_S=[]       
##            rand=random.random()
##            for j in range(16):
##                if rand<cum_prob_4[j]:
##                    self.errors_full_S+=[errorSort4[j]]
##                    break;
##        for i in range(self.N_edge_P):
##            rand=random.random()
##            for j in range(16):
##                if rand<cum_prob_3[j]:
##                    self.errors_edge_S_T+=[errorSort3[j]]
##                    break;
##            rand=random.random()
##            for j in range(16):
##                if rand<cum_prob_3[j]:
##                    self.errors_edge_S_B+=[errorSort3[j]]
##                    break;
##                   
    
    def applyErrors_4Q(self,errorVector,stabilizerPosition):

        E=1
        O=-1
        I=[1,1]
        X=[-1,1]
        Z=[1,-1]
        Y=[-1,-1]

        N_errors=len(errorVector)
        
        errorList=[[E,I,I,I,I],[O,I,I,I],
                   [E,I,I,I,Z],[O,I,I,I,Z],
                   [E,I,I,I,X],[O,I,I,I,X],
                   [E,I,I,I,Y],[O,I,I,I,Z],
                   [E,I,I,Z,Z],[O,I,I,Z,Z],
                   [E,I,I,X,Z],[O,I,I,X,Z],
                   [E,I,I,Y,Z],[O,I,I,Y,Z],
                   [E,I,I,X,X],[O,I,I,X,X],
                   [E,I,I,Y,Y],[O,I,I,Y,Y],
                   [E,I,I,X,Y],[O,I,I,X,Y]]

        # CALCULATE CUMULATIVE PROBABILITY VECTOR
        cumulativeP=[0]
        for p in errorVector:
            pAdd=p+cumulativeP[-1]
            cumulativeP+=[pAdd]             
        cumulativeP=cumulativeP[1:N_errors+1]

        # SELECT ERROR FROM PROBABILITY VECTOR
        rand=random.random()
        for i in range(N_errors):

            if rand<cumulativeP[i]:
                pickError=errorList[i]
                break

        ## if error is [IIII] then break out of function

        # RANDOM QUBIT ORDER.
        qubitOrderList=list(itertools.permutations((0,1,2,3)))
        qubitOrder=random.choice(qubitOrderList)

        #APPLY ERRORS
        pos0=stabilizerPosition[0]
        pos1=stabilizerPosition[1]
        positionsList=((pos0+1,pos1),(pos0-1,pos1),(pos0,pos1+1),(pos0,pos1-1))

        for i in range(4):

            a=positionsList[i][0]
            b=positionsList[i][1]

            qubit=self.array[a][b]
            error=pickError[i+1]

            qX=qubit[0]*error[0]
            qZ=qubit[1]*error[1]
            self.array[a][b]=[qX,qZ]


 
    def applyErrors_3Q(self,errorVector,stabilizerPosition,stabilizerType):

        E=1
        O=-1
        I=[1,1]
        X=[-1,1]
        Z=[1,-1]
        Y=[-1,-1]

        a=stabilizerPosition[0]
        b=stabilizerPosition[1]
        posList={'left':  ((a+1,b),(a-1,b),(a,b+1)),
                 'right': ((a+1,b),(a-1,b),(a,b-1)),
                 'top':   ((a+1,b),(a,b-1),(a,b+1)),
                 'bottom':((a-1,b),(a,b-1),(a,b+1))}[stabilizerType]

        N_errors=len(errorVector)
        
        errorList=[[E,I,I,I],[O,I,I,I],
                   [E,I,I,Z],[O,I,I,Z],
                   [E,I,I,X],[O,I,I,X],
                   [E,I,I,Y],[O,I,I,Z],
                   [E,I,Z,Z],[O,I,Z,Z],
                   [E,I,X,Z],[O,I,X,Z],
                   [E,I,Y,Z],[O,I,Y,Z],
                   [E,I,X,X],[O,I,X,X],
                   [E,I,Y,Y],[O,I,Y,Y],
                   [E,I,X,Y],[O,I,X,Y]]

        # CALCULATE CUMULATIVE PROBABILITY VECTOR
        cumulativeP=[0]
        for p in errorVector:
            pAdd=p+cumulativeP[-1]
            cumulativeP+=[pAdd]             
        cumulativeP=cumulativeP[1:N_errors+1]

        # SELECT ERROR FROM PROBABILITY VECTOR
        rand=random.random()
        for i in range(N_errors):

            if rand<cumulativeP[i]:
                pickError=errorList[i]
                break

        ## if error is [IIII] then break out of function

        # RANDOM QUBIT ORDER.
        qubitOrderList=list(itertools.permutations((0,1,2,3)))
        qubitOrder=random.choice(qubitOrderList)

        #APPLY ERRORS
        pos0=stabilizerPosition[0]
        pos1=stabilizerPosition[1]
        positionsList=((pos0+1,pos1),(pos0-1,pos1),(pos0,pos1+1),(pos0,pos1-1))

        for i in range(4):

            a=positionsList[i][0]
            b=positionsList[i][1]

            qubit=self.array[a][b]
            error=pickError[i+1]

            qX=qubit[0]*error[0]
            qZ=qubit[1]*error[1]
            self.array[a][b]=[qX,qZ]




        
       
        
        
    
    def show_errors(self,error_type,filename):

        channel=0 if error_type=="X" else 1
        
        import matplotlib.pyplot as plt

        qubitArray=[[0]*(2*self.size+1) for _ in range(2*self.size+1)]



        for i in range(self.N_Q):
            [p0,p1]=self.positions_Q[i]            
            qubitArray[p0][p1]=self.qubits[i][channel]

        plt.imshow(qubitArray)
        plt.savefig(filename)            
        #plt.show()

    def show_stars(self):

        stabArray=[[0]*(2*self.size+1) for _ in range(2*self.size+1)]

        for i in range(self.N_full_P):
            [p0,p1]=self.positions_full_S[i]
            stabArray[p0][p1]=self.full_S[i]

        for i in range(self.N_edge_P):
            [p0,p1]=self.positions_edge_S_T[i]
            stabArray[p0][p1]=self.edge_S_T[i]

        for i in range(self.N_edge_P):
            [p0,p1]=self.positions_edge_S_B[i]
            stabArray[p0][p1]=self.edge_S_B[i]
            
        plt.imshow(stabArray)
        plt.savefig("fig2.png")            
        #plt.show()
            
       
            
            

    def apply_flip_array(self,channel,flip_array):

        c=0 if channel=="X" else 1

        for (x0,x1) in self.positions_Q:
            self.array[x0][x1][c]*=flip_array[x0][x1]

            
    def measure_logical(self):

        self.constructArray()

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
######################################################################
######################################################################            
######################################################################
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

        self.positions_S=[(x,y) for x in range(0,2*size+1,2) for y in range(1,2*size+1,2)];
        self.positions_P=[(x,y) for x in range(1,2*size+1,2) for y in range(0,2*size+1,2)]
        
    def getTime(self):
        self.time=len(self.parity_array_P)


            
        
#P_edge_R,P_edge_L,P_full,S_edge_T,S_edge_B,S_full


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

        #P_edge_R=lat.edge_P_R
        #P_edge_L=lat.edge_P_L
        #P_full=lat.full_P
        #S_edge_T=lat.edge_S_T
        #S_edge_B=lat.edge_S_B
        #S_full=lat.full_S

        plaquette_layer=[1 for x in range(self.N)]
        star_layer=[1 for x in range(self.N)]

        for i in range(self.N):

            Ppos=self.positions_P[i]
            Spos=self.positions_S[i]

            plaquette_layer[i]=lat.array[Ppos[0]][Ppos[1]]
            star_layer[i]=lat.array[Spos[0]][Spos[1]]
       
       # plaquette_layer= P_edge_L+P_full+P_edge_R
       # star_layer     = S_edge_T+S_full+S_edge_B

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
        



         


       

        
