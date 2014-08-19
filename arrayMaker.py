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



def ThreeNormDists():
    u=random.normalvariate(0,1)
    v=random.normalvariate(0,1)
    w=random.normalvariate(0,1)
    return [u,v,w]



def phaseDefectCircle(x=0.01,y=0.01,z=0.01):
    if((x<-0.6) or (x>0.6) or (y<-0.6) or (y>0.6) or (z<0.7) or (z>1.3)):
        print ('Out of bounds atoms coords %f , %f and %f',x,y,z)
    if((x<-0.5) or (x>0.5) or (y<-0.5) or (y>0.5) or (z<0.75) or (z>1.25)):
        return 28.101 - 0.0141163*x - 28.589*x*x - 0.00113518*x*x*x + 10.6178*x*x*x*x - 0.000230013*x*x*x*x*x - 0.78536*x*x*x*x*x*x - 0.000076882*x*x*x*x*x*x*x - 7.90929*y - 0.00333062*x*y - 2.59195*x*x*y + 0.000234097*x*x*x*y - 0.626942*x*x*x*x*y +    0.000115696*x*x*x*x*x*y + 0.0204305*x*x*x*x*x*x*y - 202.292*y*y - 0.000535206*x*y*y + 41.85*x*x*y*y -    0.000133602*x*x*x*y*y - 3.24516*x*x*x*x*y*y + 7.15795e-6*x*x*x*x*x*y*y + 36.9219*y*y*y +    0.000539753*x*y*y*y + 9.29434*x*x*y*y*y - 0.0000179842*x*x*x*y*y*y + 0.103162*x*x*x*x*y*y*y + 249.386*y*y*y*y + 0.00016051*x*y*y*y*y - 7.95474*x*x*y*y*y*y - 4.07454e-6*x*x*x*y*y*y*y - 27.5325*y*y*y*y*y +    0.000101114*x*y*y*y*y*y - 2.11391*x*x*y*y*y*y*y - 53.436*y*y*y*y*y*y + 0.0000286692*x*y*y*y*y*y*y + 2.11622*y*y*y*y*y*y*y - 85.8558*z +    0.0912228*x*z + 103.511*x*x*z + 0.00476716*x*x*x*z - 26.669*x*x*x*x*z + 0.000509806*x*x*x*x*x*z + 0.684711*x*x*x*x*x*x*z +    22.5539*y*z + 0.0170728*x*y*z - 0.599362*x*x*y*z - 0.000782605*x*x*x*y*z + 1.05142*x*x*x*x*y*z - 0.000107047*x*x*x*x*x*y*z +    598.419*y*y*z + 0.00203421*x*y*y*z - 105.952*x*x*y*y*z + 0.000246192*x*x*x*y*y*z +    2.84119*x*x*x*x*y*y*z - 102.102*y*y*y*z - 0.00171331*x*y*y*y*z - 11.8171*x*x*y*y*y*z +    0.0000238128*x*x*x*y*y*y*z - 566.456*y*y*y*y*z - 0.000332865*x*y*y*y*y*z + 6.81234*x*x*y*y*y*y*z +    45.8664*y*y*y*y*y*z - 0.0000892856*x*y*y*y*y*y*z + 45.5744*y*y*y*y*y*y*z + 104.291*z*z - 0.242919*x*z*z -    152.629*x*x*z*z - 0.0072424*x*x*x*z*z + 22.9364*x*x*x*x*z*z - 0.000232554*x*x*x*x*x*z*z -    22.8599*y*z*z - 0.0350188*x*y*z*z + 6.92807*x*x*y*z*z + 0.000781405*x*x*x*y*z*z - 0.457295*x*x*x*x*y*z*z - 741.071*y*y*z*z - 0.00283163*x*y*y*z*z +    91.5206*x*x*y*y*z*z - 0.000109545*x*x*x*y*y*z*z + 110.808*y*y*y*z*z +    0.00174259*x*y*y*y*z*z + 4.54192*x*x*y*y*y*z*z + 455.816*y*y*y*y*z*z +    0.00015672*x*y*y*y*y*z*z - 19.7941*y*y*y*y*y*z*z - 57.7634*z*z*z + 0.34136*x*z*z*z + 117.018*x*x*z*z*z +    0.00472463*x*x*x*z*z*z - 6.75234*x*x*x*x*z*z*z + 6.9091*y*z*z*z + 0.0359383*x*y*z*z*z -    5.89329*x*x*y*z*z*z - 0.000240904*x*x*x*y*z*z*z + 485.936*y*y*z*z*z + 0.00170802*x*y*y*z*z*z -    26.8706*x*x*y*y*z*z*z - 57.4266*y*y*y*z*z*z - 0.00057497*x*y*y*y*z*z*z - 130.271*y*y*y*y*z*z*z +  5.56918*z*z*z*z - 0.267135*x*z*z*z*z - 47.7596*x*x*z*z*z*z - 0.00112263*x*x*x*z*z*z*z + 3.37162*y*z*z*z*z -  0.0184447*x*y*z*z*z*z + 1.46474*x*x*y*z*z*z*z - 174.905*y*y*z*z*z*z - 0.000377384*x*y*y*z*z*z*z +  12.2262*y*y*y*z*z*z*z + 9.18049*z*z*z*z*z + 0.110456*x*z*z*z*z*z + 8.41571*x*x*z*z*z*z*z - 2.54602*y*z*z*z*z*z + 0.00378423*x*y*z*z*z*z*z + 29.0314*y*y*z*z*z*z*z - 3.90206*z*z*z*z*z*z - 0.0188661*x*z*z*z*z*z*z+ 0.379224*y*z*z*z*z*z*z + 0.377636*z*z*z*z*z*z*z;
    else:
        return 25.1269 - 0.019063*x + 0.0823438*x*x - 0.000614294*x*x*x - 0.165308*x*x*x*x - 0.0000749477*x*x*x*x*x - 0.000530201*x*x*x*x*x*x +    0.0000182594*x*x*x*x*x*x*x - 2.77031*y - 0.0123924*x*y - 17.4298*x*x*y + 0.000149602*x*x*x*y + 0.0437668*x*x*x*x*y +    0.0000472321*x*x*x*x*x*y + 0.00511155*x*x*x*x*x*x*y - 273.089*y*y - 0.000571823*x*y*y + 2.83432*x*x*y*y -    0.000785282*x*x*x*y*y + 0.831889*x*x*x*x*y*y - 0.0000579302*x*x*x*x*x*y*y + 22.0552*y*y*y -    0.000492414*x*y*y*y + 33.0481*x*x*y*y*y - 0.000706817*x*x*x*y*y*y - 0.0733405*x*x*x*x*y*y*y +    363.377*y*y*y*y - 0.000575967*x*y*y*y*y - 2.85214*x*x*y*y*y*y - 0.000213155*x*x*x*y*y*y*y - 18.2484*y*y*y*y*y -    0.0000821079*x*y*y*y*y*y - 4.07523*x*x*y*y*y*y*y - 76.8647*y*y*y*y*y*y + 0.000050478*x*y*y*y*y*y*y + 1.41555*y*y*y*y*y*y*y - 78.3524*z +    0.122568*x*z - 0.631604*x*x*z + 0.00267803*x*x*x*z + 0.213959*x*x*x*x*z + 0.000121944*x*x*x*x*x*z + 0.000505311*x*x*x*x*x*x*z +    8.06524*y*z + 0.0650971*x*y*z + 43.3409*x*x*y*z - 0.000288484*x*x*x*y*z - 0.0395758*x*x*x*x*y*z - 0.0000614502*x*x*x*x*x*y*z +    907.109*y*y*z + 0.00307445*x*y*y*z - 5.65779*x*x*y*y*z + 0.00171939*x*x*x*y*y*z -    0.680295*x*x*x*x*y*y*z - 66.1052*y*y*y*z + 0.00160632*x*y*y*y*z - 53.1399*x*x*y*y*y*z +    0.000636335*x*x*x*y*y*y*z - 870.234*y*y*y*y*z + 0.00120164*x*y*y*y*y*z + 2.36764*x*x*y*y*y*y*z + 30.8104*y*y*y*y*y*z +    0.0000608902*x*y*y*y*y*y*z + 65.9918*y*y*y*y*y*y*z + 98.6735*z*z - 0.325388*x*z*z + 1.37141*x*x*z*z -    0.00424974*x*x*x*z*z - 0.0909616*x*x*x*x*z*z - 0.0000563511*x*x*x*x*x*z*z - 8.97927*y*z*z -   0.13568*x*y*z*z - 43.3303*x*x*y*z*z + 0.00028757*x*x*x*y*z*z + 0.0120946*x*x*x*x*y*z*z -    1278.53*y*y*z*z - 0.00548046*x*y*y*z*z + 4.12104*x*x*y*y*z*z -    0.000819552*x*x*x*y*y*z*z + 77.9454*y*y*y*z*z - 0.00145364*x*y*y*y*z*z +    22.5179*x*x*y*y*y*z*z + 725.253*y*y*y*y*z*z - 0.000589325*x*y*y*y*y*z*z - 13.3082*y*y*y*y*y*z*z -    56.3212*z*z*z + 0.456596*x*z*z*z - 1.33431*x*x*z*z*z + 0.0029187*x*x*x*z*z*z + 0.018304*x*x*x*x*z*z*z +    3.68396*y*z*z*z + 0.140163*x*y*z*z*z + 21.0413*x*x*y*z*z*z - 0.00012881*x*x*x*y*z*z*z +    954.658*y*y*z*z*z + 0.00395139*x*y*y*z*z*z - 1.11051*x*x*y*y*z*z*z - 42.7322*y*y*y*z*z*z +    0.000370292*x*y*y*y*z*z*z - 209.678*y*y*y*y*z*z*z + 3.15635*z*z*z*z - 0.357244*x*z*z*z*z +    0.610639*x*x*z*z*z*z - 0.000736465*x*x*x*z*z*z*z + 0.506029*y*z*z*z*z - 0.0717953*x*y*z*z*z*z -    4.30219*x*x*y*z*z*z*z - 379.753*y*y*z*z*z*z - 0.00100007*x*y*y*z*z*z*z + 9.16793*y*y*y*z*z*z*z +    12.9084*z*z*z*z*z + 0.147807*x*z*z*z*z*z - 0.106564*x*x*z*z*z*z*z - 0.74886*y*z*z*z*z*z + 0.0146015*x*y*z*z*z*z*z +    64.8233*y*y*z*z*z*z*z - 6.00093*z*z*z*z*z*z - 0.0252726*x*z*z*z*z*z*z + 0.132446*y*z*z*z*z*z*z + 0.810164*z*z*z*z*z*z*z;



def phaseDefectAbrupt(x=0.01,z=0.01):
    if ((x>0.5) or (z<0.8) or (z>1.2)):
        print("Out of bounds atoms coords %f and %f",x,z)
    if ((x>0.25) or (z<0.93) or (z>1.07)): #then use the broad width function
        return 24.350 - 24.4430*x - 13.5715*x*x + 6.10644*x*x*x - 52.0085*z + 44.5051*x*z + 6.8577*x*x*z + 36.07222*z*z - 19.80326*x*z*z - 8.41386*z*z*z;
    else:                 #then use the narrow width function (more accurate for small values)
        return 27.2882 - 14.5097*x - 23.2735*x*x + 3.66809*x*x*x - 62.6*z + 28.3426*x*z + 17.9832*x*x*z + 48.0703*z*z - 13.7965*x*z*z - 12.7585*z*z*z;


def generateArray(arraySize=29,errortype='normal',orbit='abrupt',sdInX=0.01,sdInY=0.01,sdInZ=0.01,Pj=0.00,prX=0,prY=0,prZ=0,initStateError=0.01,measureError=0.01):
    
#    print "in arrayMaker.py sdInZ = ",sdInZ

             ### set parameters
    #errortype='normal' or 'pillbox' error distributions for position of spins
    #Pj = 0.0016 # phase jitter ACTUALLY (jitter)^2/4 so should be a small number here!
    #prX = 0.01/3
    #prY = 0.01/3
    #prZ = 0.01/3 #// three components of the probe flip error
    #orbit = 'abrupt' or 'circle' motion of probe: selects phase error interpolating function generated by mathematica simulations
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

    phaseErrors=[[[0 for z in range(4)] for y in range(arraySize)] for x in range(arraySize)]
    for i in range(arraySize):
        for j in range(arraySize):
            if (i+j)%2==0:
                if (errortype=='normal'):
                    threeRnds=ThreeNormDists()
                    for k in range(4):
                        if k==0:
                            position=[threeRnds[0]*sdInX,threeRnds[1]*sdInY,1+threeRnds[2]*sdInZ]
                        if k==1:
                            position=[threeRnds[1]*sdInY,threeRnds[0]*sdInX,1+threeRnds[2]*sdInZ]
                        if k==2:
                            position=[threeRnds[0]*sdInX,(-1.)*threeRnds[1]*sdInY,1+threeRnds[2]*sdInZ]
                        if k==3:
                            position=[(-1.)*threeRnds[1]*sdInY,threeRnds[0]*sdInX,1+threeRnds[2]*sdInZ]

                        if orbit=='circle':
                            phaseErrors[i][j][k]=phaseDefectCircle(position[0],position[1],position[2]);
                        if orbit=='abrupt':
                            phaseErrors[i][j][k]=phaseDefectAbrupt(np.sqrt(position[0]**2+position[1]**2),position[2]);

                if (errortype=='disc'):
                    randR=RandomReal(1.)
                    randtheta=RandomReal(2*np.pi)
                    randx=np.sqrt(randR)*np.cos(randtheta)
                    randy=np.sqrt(randR)*np.sin(randtheta)

                    for k in range(4):
                        if k==0:
                            position=[randx*sdInX,randy*sdInY,1]
                        if k==1:
                            position=[randy*sdInY,randx*sdInX,1]
                        if k==2:
                            position=[randx*sdInX,(-1.)*randy*sdInY,1]
                        if k==3:
                            position=[(-1.)*randy*sdInY,randx*sdInX,1]
                        
                        if orbit=='circle':
                            phaseErrors[i][j][k]=phaseDefectCircle(position[0],position[1],position[2]);
                        if orbit=='abrupt':
                            phaseErrors[i][j][k]=phaseDefectAbrupt(np.sqrt(position[0]**2+position[1]**2),position[2]);
                
                if (errortype=='pillbox'):
                    for k in range(4):
                        randR=random.random()
                        randtheta=2*np.pi*random.random()
                        randx=np.sqrt(randR)*np.cos(randtheta)
                        randy=np.sqrt(randR)*np.sin(randtheta)
                        randz=random.uniform(-1,1)
                        for k in range(4):
                            if k==0:
                                position=[randx*sdInX,randy*sdInY,1+randz*sdInZ]
                            if k==1:
                                position=[randy*sdInY,randx*sdInX,1+randz*sdInZ]
                            if k==2:
                                position=[randx*sdInX,(-1.)*randy*sdInY,1+randz*sdInZ]
                            if k==3:
                                position=[(-1.)*randy*sdInY,randx*sdInX,1+randz*sdInZ]

                            if orbit=='circle':
                                phaseErrors[i][j][k]=phaseDefectCircle(position[0],position[1],position[2]);
                            if orbit=='abrupt':
                                phaseErrors[i][j][k]=phaseDefectAbrupt(np.sqrt(position[0]**2+position[1]**2),position[2]);
                                    

    #convert to stabiliser errors#                                                                                                                  
    stabErrors=[[0 for x in range(arraySize-2)] for y in range(arraySize-2)]
    for xLoc in range(arraySize-2):
        for yLoc in range(arraySize-2):
            if (xLoc +yLoc)%2!=1: continue

            shift1=phaseErrors[xLoc+1][yLoc+0][0];  #north#                                                                                           
            shift2=phaseErrors[xLoc+2][yLoc+1][1];#east#                                                                                            
            shift3=phaseErrors[xLoc+1][yLoc+2][2];#south#                                                                                           
            shift4=phaseErrors[xLoc+0][yLoc+1][3];#west#            #stabilisers at i+1, j+1, even x,y are stars, odd x,y are plaquettes#   



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
                                    f6D[p][q][R][S][t][u] + f6D[p][q][R][s][T][u] + f6D[p][q][R][s][t][U]) + Pj*Pj*f6D[p][q][R][S][T][U]
                                                                   )+\
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
