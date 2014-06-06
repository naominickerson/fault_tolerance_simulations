from planar_lattice import *
import arrayMaker




class SpinLattice(PlanarLattice):

    def __init__(self,size):

        PlanarLattice.__init__(self,size)
        self.errorArray=None

    
    def generateArray(self,sdInPlane=0.01,sdInZ=0.01,Pj=0.0016,prX=0.01/3,prY=0.01/3,prZ=0.01/3,initStateError=0.01,measureError=0.01):
        """ function to generation a random array of spins"""
        self.errorArray=arrayMaker.generateArray(2*self.size+3,sdInPlane,sdInZ,Pj,prX,prY,prZ,initStateError,measureError)




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



    def stabilizer(self,channel,pos,sType):

        if channel in ["plaquette","P"]: c=0
        elif channel in ["star","Star","S"]:c=1
        else: raise ValueError('%s is not a valid channel for the stabilizer'%(channel))


        p=pos
        p0,p1=pos
        stabQubits=((p0-1,p1),(p0,p1+1),(p0+1,p1),(p0,p1-1))        

        if sType=="F":   order=[0,1,2,3]
        elif sType=="L": order=[0,1,2]
        elif sType=="R": order=[0,2,3]
        elif sType=="T": order=[1,2,3]
        elif sType=="B": order=[0,1,3]
        else: raise ValueError('%s is not a valid stabilizer type'%(sType,))

        
    # Measure true value of stabilizer
        stab = 1
        for i in order:
            q=stabQubits[i]
            stab*=self.array[q[0]][q[1]][c]
            
        stabc= 0 if stab==1 else 1


        E,O,I,X,Y,Z=1,-1,[1,1],[-1,1],[-1,-1],[1,-1]
        errorList = [[E, I, I, I, I],[E, I ,I, I, Z],[E, I, I, Z, I],[E, I, I, Z, Z],
                     [E, I, Z, I, I],[E, I, Z, I, Z ],[E, I, Z, Z, I],[E, Z, I, I, I],
                     [O, I, I, I, I],[O, I, I, I, Z],[O, I, I, Z, I],[O, I, I, Z, Z],
                     [O, I, Z, I, I],[O, I, Z, I, Z],[O, I, Z, Z, I ],[O, Z, I, I, I ]]

        # set the error vector
        errorVector = self.errorArray[p[0]][p[1]][stabc]

        errorList4=sorted(zip(errorVector,errorList),reverse=True)
        error_prob,errorSort=zip(*errorList4)           
        cum_prob=np.cumsum(np.array(error_prob)).tolist()   # sum up cumulative probability lists


        # Select error from the error Vector
        rand=random.random()                            
        for j in range(16):
            if rand<cum_prob[j]:
                error =errorSort[j]
                break;
            if j==19: 
                error=[1,[1,1],[1,1],[1,1],[1,1]]

#        if stabc==1: print error
        # Apply the error and record the stabilizer 

        for i in order:
            err = error[i+1]
            if err==[1,1]: continue
            q=stabQubits[i]
            
            self.array[q[0]][q[1]][0]*=err[0]
            self.array[q[0]][q[1]][1]*=err[1]

        # Set the stabilizer value
        self.array[p0][p1]=error[0]




          

    def measureNoisyStabilizers(self,sType):

        if sType not in ["plaquette","star"]: raise ValueError(' channel must be either "plaquette" or "star" ')

## IDENTIFY STABILIZER POSITIONS 

        stabilizerType=sType
        edge1="L" if sType=="plaquette" else "T"
        edge2="R" if sType=="plaquette" else "B"

        full_positions= self.positions_full_P if sType=="plaquette" else self.positions_full_S
        edge_positions_1 = self.positions_edge_P_L if sType =="plaquette" else self.positions_edge_S_T
        edge_positions_2 = self.positions_edge_P_R if sType =="plaquette" else self.positions_edge_S_B


## MEASURE THE STABILIZERS 

        for p in full_positions:
            self.stabilizer(sType,p,"F")

        for p in edge_positions_1:
            self.stabilizer(sType,p,edge1)

        for p in edge_positions_2:
            self.stabilizer(sType,p,edge2)
            






