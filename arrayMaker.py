## Python implementation of Simon Benjamin's 'array Maker'

import math
import random
import sys
import time
import numpy as np

 
def RandomReal(X):
    random.random(0,X)

def TwoNormals():
    u=math.sqrt(-2*math.log(random.random()))
    v=2*math.pi*random.random()
    return [u*math.sin(v),u*math.cos(v)]
                 

def displayStab(stab):

    ## remaining code below is simply to collate and present the probabilities as a printout -- comment out in final version

    ## Define Labels
    label6Darray = [[[[[[[0 for i1 in range(6)] for i2 in range(2)] for i3 in range(2)] for i4 in range(2)] for i5 in range(2)] for i6 in range(2)] for i7 in range(2)]
            
    for p in [0,1]:
        for q in [0,1]:
            for r in [0,1]:
                for s in [0,1]:
                    for t in [0,1]:
                        for u in [0,1]:
                            label6Darray[p][q][r][s][t][u][0] = 'E' if p==0 else 'O'
                            label6Darray[p][q][r][s][t][u][1] = 'e' if q==0 else 'o'
                            label6Darray[p][q][r][s][t][u][2] = 'I' if r==0 else 'Z'
                            label6Darray[p][q][r][s][t][u][3] = 'I' if s==0 else 'Z'
                            label6Darray[p][q][r][s][t][u][4] = 'I' if t==0 else 'Z'
                            label6Darray[p][q][r][s][t][u][5] = 'I' if u==0 else 'Z'

    fn=[[[[[[0 for i1 in range(2)] for i2 in range(2)] for i3 in range(2)] for i4 in range(2)] for i5 in range(2)] for i6 in range(2)]

    withPrepMeas=stab

    for p in [0,1]:
        for q in [0,1]:                  
        
            fn[p][q][0][0][0][1] = withPrepMeas[p][q][0][0][0][1] + withPrepMeas[p][q][1][1][1][0]
            fn[p][q][0][0][1][0] = withPrepMeas[p][q][0][0][1][0] + withPrepMeas[p][q][1][1][0][1]
            fn[p][q][0][1][0][0] = withPrepMeas[p][q][0][1][0][0] + withPrepMeas[p][q][1][0][1][1]
            fn[p][q][1][0][0][0] = withPrepMeas[p][q][1][0][0][0] + withPrepMeas[p][q][0][1][1][1]
            fn[p][q][0][0][1][1] = withPrepMeas[p][q][0][0][1][1] + withPrepMeas[p][q][1][1][0][0]
            fn[p][q][0][1][1][0] = withPrepMeas[p][q][0][1][1][0] + withPrepMeas[p][q][1][0][0][1]
            fn[p][q][0][1][0][1] = withPrepMeas[p][q][0][1][0][1] + withPrepMeas[p][q][1][0][1][0]
            fn[p][q][0][0][0][0] = withPrepMeas[p][q][0][0][0][0] + withPrepMeas[p][q][1][1][1][1]
    
    theTots = [0 for _ in range(2)]
    for p in [0,1]: 
        for r in [0,1]:
            for s in [0,1]:
                for t in [0,1]:
                    for u in [0,1]:
                        
                        theTots[0]+=fn[0][p][r][s][t][u];
                        theTots[1]+=fn[1][p][r][s][t][u];

    print "Total probability for the (real) even and odd projectors, respectively, is %f and %f\n"%(theTots[0],theTots[1])
  
    for p in [0,1]: 
        for q in [0,1]:
            for r in [0,1]:
                for s in [0,1]:
                    for t in [0,1]:
                        for u in [0,1]:
                            if (fn[p][q][r][s][t][u]!=0):
                                for v in range(6):
                                    print "%c"%label6Darray[p][q][r][s][t][u][v],
                                print ": %.9lf, "%fn[p][q][r][s][t][u]                        
    print "\n\n"              



def errorVector(stab):

    ## remaining code below is simply to collate and present the probabilities as a printout -- comment out in final version

    fn=[[[[[[0 for i1 in range(2)] for i2 in range(2)] for i3 in range(2)] for i4 in range(2)] for i5 in range(2)] for i6 in range(2)]

    withPrepMeas=stab

    errorVec=[[],[]]

    for p in [0,1]:
        for q in [0,1]:                  
        
            fn[p][q][0][0][0][1] = withPrepMeas[p][q][0][0][0][1] + withPrepMeas[p][q][1][1][1][0]
            fn[p][q][0][0][1][0] = withPrepMeas[p][q][0][0][1][0] + withPrepMeas[p][q][1][1][0][1]
            fn[p][q][0][1][0][0] = withPrepMeas[p][q][0][1][0][0] + withPrepMeas[p][q][1][0][1][1]
            fn[p][q][1][0][0][0] = withPrepMeas[p][q][1][0][0][0] + withPrepMeas[p][q][0][1][1][1]
            fn[p][q][0][0][1][1] = withPrepMeas[p][q][0][0][1][1] + withPrepMeas[p][q][1][1][0][0]
            fn[p][q][0][1][1][0] = withPrepMeas[p][q][0][1][1][0] + withPrepMeas[p][q][1][0][0][1]
            fn[p][q][0][1][0][1] = withPrepMeas[p][q][0][1][0][1] + withPrepMeas[p][q][1][0][1][0]
            fn[p][q][0][0][0][0] = withPrepMeas[p][q][0][0][0][0] + withPrepMeas[p][q][1][1][1][1]
    

    for p in [0,1]: 
        for q in [0,1]:
            for r in [0,1]:
                for s in [0,1]:
                    for t in [0,1]:
                        for u in [0,1]:
                            if (fn[p][q][r][s][t][u]!=0):
                                errorVec[p] +=[ fn[p][q][r][s][t][u] ]                              
   
    return errorVec



    




def generateArray(arraySize=29,sdInPlane=0.01,sdInZ=0.01,Pj=0.00,prX=0,prY=0,prZ=0,initStateError=0.01,measureError=0.01):
    
#    print "in arrayMaker.py sdInZ = ",sdInZ

             ### set parameters

    #Pj = 0.0016 # phase jitter ACTUALLY (jitter)^2/4 so should be a small number here!
    #prX = 0.01/3
    #prY = 0.01/3
    #prZ = 0.01/3 #// three components of the probe flip error

    #initStateError = 0.01
    #measureError = 0.01

    #sdInPlane = 0.01
    #sdInZ = 0.02  #//note: PHYSICAL LOCATION ERRORS where the average distance from probe to data qubit is unity

    #arraySize = 15     #//atom array size, should be an odd total, actual max num atoms in a given row/col is ( (this)+1 )/2

    MAXphysicalArrayWidth = 100
    
    if arraySize>MAXphysicalArrayWidth:
        print "Atom array size exceeds presumed max! Stopping!"
        sys.exit(0)

#    print "Using standard deviation in plane=%f, and in z-dir sd is=%f, and array size=%i\n"%(sdInPlane,sdInZ,arraySize)
    
    rSeed = time.time();
    random.seed(rSeed)
 #   print "Random seed=%i\n"%(rSeed,)

   
    # Pick the random phase shifts 
    phaseShifts=[[0 for x in range(arraySize)] for y in range(arraySize)]
    for i in range(arraySize):
        for j in range(arraySize):
            if (i+j)%2==0:
                twoRnds = TwoNormals()
    
                beeLine=math.sqrt( (sdInPlane*twoRnds[0])**2 + (1+sdInZ*twoRnds[1])**2)
                
                phaseShifts[i][j]=1.57079632679*((beeLine**-3)-1);


    ## get the stabErrors

    stabErrors=[[0 for x in range(arraySize-2)] for y in range(arraySize-2)] 

    for xLoc in range(arraySize-2):
        for yLoc in range(arraySize-2):

            if (xLoc+yLoc)%2!=1: continue
            #stabErrors[xLoc][yLoc]=[[[[[[0 for i1 in range(2)] for i2 in range(2)] for i3 in range(2)] for i4 in range(2)] for i5 in range(2)] for i6 in range(2)]
            
            #print "Evaluating stabiliser at coords %i %i\n"%(xLoc,yLoc)
    
            shift1=phaseShifts[xLoc+1][yLoc+0]; ##north    in atom coords, centre of stab would be i+1, j+1
            shift2=phaseShifts[xLoc+2][yLoc+1]; ##east
            shift3=phaseShifts[xLoc+1][yLoc+2]; ##south
            shift4=phaseShifts[xLoc+0][yLoc+1]; ##west



            #shift1,shift2,shift3,shift4=[-0.025092, -0.143628, 0.056573, -0.055322]
            #print "the phase shifts are ", shift1, shift2, shift3, shift4


                            
            probeFlipPattern=((0, 0, 0, 0, 0),(0, 1, 1, 1, 0),(0, 1, 0, 1, 0),(0, 0, 1, 0, 0));
            numTwirlCases=4;
            if (shift1==0 and shift2==0 and shift3==0 and shift4==0): numTwirlCases=1  ##if there are no defects, we need not bother with twirling
  
            #rSeed=time.time()
            #random.seed(rSeed)

            ## initialise arrays


            f6D=np.zeros(64).reshape((2,2,2,2,2,2)).tolist()
            wJ=np.zeros(64).reshape((2,2,2,2,2,2)).tolist()
            PrEr=np.zeros(64).reshape((2,2,2,2,2,2)).tolist()
            withPrepMeas=np.zeros(64).reshape((2,2,2,2,2,2)).tolist()
            
            #f6D=[[[[[[0 for i1 in range(2)] for i2 in range(2)] for i3 in range(2)] for i4 in range(2)] for i5 in range(2)] for i6 in range(2)]
            #wJ=[[[[[[0 for i1 in range(2)] for i2 in range(2)] for i3 in range(2)] for i4 in range(2)] for i5 in range(2)] for i6 in range(2)]
            #PrEr=[[[[[[0 for i1 in range(2)] for i2 in range(2)] for i3 in range(2)] for i4 in range(2)] for i5 in range(2)] for i6 in range(2)]
            #withPrepMeas=[[[[[[0 for i1 in range(2)] for i2 in range(2)] for i3 in range(2)] for i4 in range(2)] for i5 in range(2)] for i6 in range(2)]

            ## Calculating the parameters

            ssum1=(shift1 + shift2 + shift3 + shift4)/2
            ssum2=(shift1 + shift2 - shift3 - shift4)/2
            ssum3=(shift1 - shift2 + shift3 - shift4)/2
            ssum4=(shift1 - shift2 - shift3 + shift4)/2
                        
            Ct = math.cos(ssum1);
            Ca = math.cos(ssum2);
            Cb = math.cos(ssum3);
            Cc = math.cos(ssum4);

            ST = math.sin(ssum1);
            SA = math.sin(ssum2);
            SB = math.sin(ssum3);
            SC = math.sin(ssum4);

            OmegaEven = ((Ct + Ca + Cb + Cc)**2)/16;
            Delta11zz = ((Ct + Ca - Cb - Cc)**2)/16;
            Delta1z1z = ((Ct - Ca + Cb - Cc)**2)/16;
            Delta1zz1 = ((Ct - Ca - Cb + Cc)**2)/16;

            ssum5 = (-shift1 + shift2 + shift3 + shift4)/2
            ssum6 = (+shift1 - shift2 + shift3 + shift4)/2
            ssum7 = (+shift1 + shift2 - shift3 + shift4)/2
            ssum8 = (+shift1 + shift2 + shift3 - shift4)/2
            
            S1 = math.sin(ssum5);
            S2 = math.sin(ssum6);
            S3 = math.sin(ssum7);
            S4 = math.sin(ssum8);

            cAlpha = math.cos(ssum5);
            cBeta =  math.cos(ssum6);
            cGamma = math.cos(ssum7);
            cDelta = math.cos(ssum8);
    
            gamma1 = ((-S1 + S2 + S3 + S4)**2)/16;
            gamma2 = ((S1 - S2 + S3 + S4)**2)/16;
            gamma3 = ((S1 + S2 - S3 + S4)**2)/16;
            gamma4 = ((S1 + S2 + S3 - S4)**2)/16;

    
            OmegaOdd   = ((cAlpha + cBeta + cGamma + cDelta)**2)/16;
            Lambda11zz = ((cAlpha + cBeta - cGamma - cDelta)**2)/16;
            Lambda1z1z = ((cAlpha - cBeta + cGamma - cDelta)**2)/16;
            Lambda1zz1 = ((cAlpha - cBeta - cGamma + cDelta)**2)/16;
    
            Gamma1 = ((+ST + SA + SB + SC)**2)/16;
            Gamma2 = ((+ST + SA - SB - SC)**2)/16;
            Gamma3 = ((+ST - SA + SB - SC)**2)/16;
            Gamma4 = ((+ST - SA - SB + SC)**2)/16;
            

            f6D[0][0][0][0][0][0] = OmegaEven;
            f6D[0][0][0][0][1][1] = Delta11zz/2;
            f6D[0][0][0][1][0][1] = Delta1z1z/2;
            f6D[0][0][0][1][1][0] = Delta1zz1/2;
            f6D[0][0][1][0][0][1] = Delta1zz1/2;
            f6D[0][0][1][0][1][0] = Delta1z1z/2;
            f6D[0][0][1][1][0][0] = Delta11zz/2;
    
            f6D[1][0][0][0][0][1] = gamma1;
            f6D[1][0][0][0][1][0] = gamma2;
            f6D[1][0][0][1][0][0] = gamma3;
            f6D[1][0][1][0][0][0] = gamma4;
    
            f6D[0][1][0][0][0][1] = Gamma1;
            f6D[0][1][0][0][1][0] = Gamma2;
            f6D[0][1][0][1][0][0] = Gamma3;
            f6D[0][1][1][0][0][0] = Gamma4;
        
            f6D[1][1][0][0][0][0] = OmegaOdd;
            f6D[1][1][0][0][1][1] = Lambda11zz/2;
            f6D[1][1][0][1][0][1] = Lambda1z1z/2;
            f6D[1][1][0][1][1][0] = Lambda1zz1/2;
            f6D[1][1][1][0][0][1] = Lambda1zz1/2;
            f6D[1][1][1][0][1][0] = Lambda1z1z/2;
            f6D[1][1][1][1][0][0] = Lambda11zz/2;
                

            
          
        
            Nj=1-Pj;
            
            wJ=(Nj*Nj*Nj*Nj*np.array(f6D)).tolist()
                      
            for p in [0,1]: 
                P=1-p
                for q in [0,1]:
                    Q=1-q
                    for r in [0,1]:
                        R=1-r
                        for s in [0,1]:
                            S=1-s
                            for t in [0,1]:
                                T=1-t
                                for u in [0,1]:
                                    U=1-u
                                    
                                    wJ[p][q][r][s][t][u] += Pj*Pj*(Nj*Nj*(f6D[p][q][r][s][T][U] + f6D[p][q][r][S][t][U] + f6D[p][q][r][S][T][u]+\
                                    f6D[p][q][R][S][t][u] + f6D[p][q][R][s][T][u] + f6D[p][q][R][s][t][U]) + Pj*Pj*f6D[p][q][R][S][T][U])+\
                                    Pj*Nj*(Nj*Nj*(f6D[p][Q][r][s][t][U] + f6D[p][Q][r][s][T][u] + f6D[p][Q][r][S][t][u] + f6D[p][Q][R][s][t][u])+\
                                    Pj*Pj*(f6D[p][Q][R][S][T][u] + f6D[p][Q][R][S][t][U] + f6D[p][Q][R][s][T][U] + f6D[p][Q][r][S][T][U]))
                                    
             
            
            

            prT = prX + prY + prZ
            nT = 1 - prT
            pfp=[0 for _ in range(5)]


            for p in [0,1]: 
                P=1-p
                for q in [0,1]:
                    Q=1-q
                    for r in [0,1]:
                        R=1-r
                        for s in [0,1]:
                            S=1-s
                            for t in [0,1]:
                                T=1-t
                                for u in [0,1]:
                                    U=1-u
                                    
                                    tmpEle = 0;

                                    for tw in range(numTwirlCases):
                                        for qk in range(0,5): pfp[qk]=probeFlipPattern[tw][qk]

                                        if ((pfp[0] != 0) or (pfp[4] != 0)):
                                            print ">>>>>>>> Error: had assumed we'd never flip probe for data qubit 1, or immediate prior to measurement %i %i <<<<<<<<\n"%(pfp[0],pfp[4])

                                        if (pfp[1]==0 and pfp[2]==0 and pfp[3]==0):
                                            tmpEle += wJ[p][q][r][s][t][u]
                                            

                                        elif (pfp[1]==0 and pfp[2]==1 and pfp[3]==0):
                                            tmpEle +=nT*wJ[p][q][r][s][t][u] + prX*wJ[p][q][R][S][t][u] + prY*wJ[p][Q][R][S][t][u] + prZ*wJ[p][Q][r][s][t][u]
                                            
                                        elif (pfp[1]==1 and pfp[2]==0 and pfp[3]==1):
                      
                                            tmpEle += (nT*nT + prZ*prZ)*wJ[p][q][r][s][t][u] + 2*nT*prZ*wJ[p][Q][r][s][t][u] +\
                                            (nT*prX + prY*prZ)*wJ[P][q][R][S][T][u] + \
                                            (nT*prY + prX*prZ)*wJ[P][Q][R][S][T][u] + \
                                            (nT*prX + prZ*prY)*wJ[P][q][R][s][t][u] + \
                                            (nT*prY + prZ*prX)*wJ[P][Q][R][s][t][u] + \
                                            (prX*prX + prY*prY)*wJ[p][q][r][S][T][u] + \
                                            2*prX*prY*wJ[p][Q][r][S][T][u]; 
                                            
                                            
 
                                        elif ( pfp[1]==1 and pfp[2]==1 and pfp[3]==1):
                                       
                                            tmpEle += (nT*nT*nT + 3*nT*prZ*prZ)*wJ[p][q][r][s][t][u] + \
                                                 (3*nT*nT*prZ + prZ*prZ*prZ)*wJ[p][Q][r][s][t][u] +\
                                                 (nT*nT*prX + 2*nT*prY*prZ + prX*prZ*prZ)*(wJ[P][q][R][S][T][u] + wJ[p][q][R][S][t][u] + wJ[P][q][R][s][t][u]) + \
                                                (nT*nT*prY + 2*nT*prX*prZ + prY*prZ*prZ)*(wJ[P][Q][R][S][T][u] + wJ[p][Q][R][S][t][u] + wJ[P][Q][R][s][t][u]) + \
                                                (nT*prX*prX+ nT*prY*prY + 2*prX*prY*prZ)*(wJ[P][q][r][S][t][u] + wJ[p][q][r][S][T][u] + wJ[P][q][r][s][T][u]) + \
                                                (prX*prX*prZ + prY*prY*prZ + 2*nT*prX*prY)*(wJ[P][Q][r][S][t][u] + wJ[p][Q][r][S][T][u] + wJ[P][Q][r][s][T][u]) + \
                                                  (prX*prX*prX + 3*prY*prY*prX)*wJ[p][q][R][s][T][u] +(prY*prY*prY + 3*prX*prX*prY)*wJ[p][Q][R][s][T][u] 
                                            
                                        else:
                                            print ">>>>>>> Error: twirl patten not coded for <<<<<<<"
                                            sys.exit(0)

                                        
                                    PrEr[p][q][r][s][t][u] = tmpEle/numTwirlCases;

                              

        
            coeff1 = (2*initStateError/3 + measureError - 4*initStateError*measureError/3)         

            for p in [0,1]:
                withPrepMeas[p][0]=((1-coeff1)*np.array(PrEr[p][0]) + coeff1*np.array(PrEr[p][1])).tolist()
                withPrepMeas[p][1]=((1-coeff1)*np.array(PrEr[p][1]) + coeff1*np.array(PrEr[p][0])).tolist()

            stabErrors[xLoc][yLoc]=errorVector(withPrepMeas)
#            print stabErrors[xLoc][yLoc]
            #displayStab(withPrepMeas)
#            break
#        break
 
    return stabErrors
#    return stabErrors



def timeGeneration(size=29):

    t0=time.time()
    generateArray(size)
    return time.time()-t0


'''

            for p in [0,1]: 
i                for q in [0,1]:
                    for r in [0,1]:
                        for s in [0,1]:
                            for t in [0,1]:
                                for u in [0,1]:
 
                                    withPrepMeas[p][0][r][s][t][u]=(1 - 2*initStateError/3 - measureError + 4*initStateError*measureError/3)*PrEr[p][0][r][s][t][u] +\
                                                        (2*initStateError/3 + measureError - 4*initStateError*measureError/3)*PrEr[p][1][r][s][t][u]
                                    withPrepMeas[p][1][r][s][t][u]=(1 - 2*initStateError/3 - measureError + 4*initStateError*measureError/3)*PrEr[p][1][r][s][t][u] +\
                                                        (2*initStateError/3 + measureError - 4*initStateError*measureError/3)*PrEr[p][0][r][s][t][u];
'''
