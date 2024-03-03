from copy import deepcopy
from random import randint
import random
import math
import numpy as np

constepslist = [-3, -2, -1, 0, 1, 2, 3]
constepslistabc = [-1, 0, 1]
def szimulaltLehutes(dim, numofdays, hutes, itmax):#dim = nurse num
    k = 1 #number of iterations
    t0 = 100
    t = t0
    S=[]
    SAll = np.array([])
    numOfShiftsInARowAll = np.array([])
    numOfShiftsInARow = np.array([])
    
    for i in range(0, dim):
      randnum = 0
      numOfShiftsInARow = np.append(numOfShiftsInARow, randnum)

    for i in range(dim):
        randnum = random.randint(0,3)
        S.append(randnum)
        if(randnum !=0):
          numOfShiftsInARow[i] = numOfShiftsInARow[i] + 1
    
    for i in numOfShiftsInARow:
        numOfShiftsInARowAll = np.append(numOfShiftsInARowAll, i)
    
    for i in S:
        SAll = np.append(SAll, i)
    
    #print(S)
    #Legjobb = S.copy()
    
    Slast = np.array([])
    for i in range(0, dim):
      randnum = 0
      Slast = np.append(Slast, randnum)
    #Legjobb = Slast
    
    while True:
        S2 = S.copy()
        ratios = []
        W=[]
        bestminW = 9999999
        bestminWShift = []
        for its in range(itmax):
            W = []
            #print("it = ", its, " S = ", S)
            for i in range(dim):
                randgen = random.choice(constepslist)
                while(abs(S2[i] + randgen) > 3 or (S2[i] + randgen) < 0):
                    randgen = random.choice(constepslist)
                W.append(S2[i] + randgen)
            
            r = random.random()
            minW = shiftMinoseg(W,S2,numOfShiftsInARow)
            if(minW < bestminW):
                bestminW = minW
                bestminWShift = W
        #print("S = ", S)
        #print("W = ", bestminWShift)
        minS = shiftMinoseg(S,Slast,numOfShiftsInARow)
        #print(minS, bestminW)
        eHatvany = (minS-bestminW)/t #volt minW-minS, felcsereltem
        if(bestminW <= minS or r < math.e ** eHatvany): # <
            S = bestminWShift.copy()
            #print("w copied into s")
        match hutes:
            case "exponential":
                alpha = 0.85
                t = t0 * (alpha ** k)
            case "linear":
                #alpha = 0.01
                alpha = 0.5
                t = t0 / (1 + alpha * k)
            case "quadratic":
                alpha = 0.00001
                t = t0 / (1 + alpha * (k ** 2))
            case _:
                #print("Add meg a hutes tipusat (exponencialis/linearis/kvadratikus)")
                print("Specify annealing type (exponential/linear/quadratic)")
                return -1
       
        minS = shiftMinoseg(S,Slast,numOfShiftsInARow)
        #minL = shiftMinoseg(Legjobb,dim)
        Slast = S.copy()
        #if(minS < minL):
        #    Legjobb = S.copy()
        k = k + 1
        SAll = np.append(SAll, S)
        
        slen = len(S)
        for i in range(slen):
            if(S[i] != 0):
                numOfShiftsInARow[i] = numOfShiftsInARow[i] + 1
            else:
                numOfShiftsInARow[i] = 0
        
        for i in numOfShiftsInARow:
            numOfShiftsInARowAll = np.append(numOfShiftsInARowAll, i)
        
        if(k >= numofdays or t <= 0):
            break
    
    #return Legjobb
    #print(minS)
    SAllReshape = SAll.reshape(k, dim)
    SAllInt = SAllReshape.astype(int)
    numOfShiftsInARowAllReshape = numOfShiftsInARowAll.reshape(k, dim)
    numOfShiftsInARowAllInt = numOfShiftsInARowAllReshape.astype(int)
    fullshiftminoseg = 0
    #print(len(SAllInt))
    #print(len(numOfShiftsInARowAllInt))
    #print(k)
    #print(SAllInt)
    #print("WOOO")
    #print(numOfShiftsInARowAllInt)
    for i in range(1, numofdays):
        fullshiftminoseg = fullshiftminoseg + shiftMinoseg(SAllInt[i],SAllInt[i-1],numOfShiftsInARowAllInt[i-1])
    #print(fullshiftminoseg)
    return fullshiftminoseg, SAllInt

#megkotesek (restrictions):
# HARD: egy nurse egy nap csak egy shiftben dolgozhat (a nurse can only take one shift per day)
# HARD: egy nurse nem dolgozhat egymasutan egy nap ejszaka, masik nap reggel (a nurse cannot work a night shift followed by a morning shift)
# SOFT: egy nurse nem dolgozhat egymasutan 7 napnal tobbet (a nurse cannot work for more than 7 days in a row)

def shiftMinoseg(currentShifts, lastShifts, numOfShiftsInARow):
  #shifts can be 0 for no shift, 1 for morning, 2 for afternoon, 3 for night
  shiftslen = len(currentShifts)
  violations = 0
  numOfShiftsTemp = deepcopy(numOfShiftsInARow)
  for i in range(shiftslen):
    if(currentShifts[i] == 1 and lastShifts[i] == 3):
      return 999999
    if(currentShifts[i] != 0):
      numOfShiftsTemp[i] = numOfShiftsTemp[i] + 1
    if(numOfShiftsTemp[i] >= 7):
      violations = violations + 1
  return violations

def abc(nursenum, numofdays, gennum):
    k = 1 #number of iterations
    gennum2 = gennum
    S=[]
    SAll = np.array([])
    numOfShiftsInARowAll = np.array([])
    numOfShiftsInARow = np.array([])
    WFinal = np.array([])
    WFinalbaRakott = np.array([])

    for i in range(0, nursenum):
      randnum = 0
      numOfShiftsInARow = np.append(numOfShiftsInARow, randnum)

    for i in range(nursenum):
        randnum = random.randint(0,3)
        S.append(randnum)
        if(randnum !=0):
          numOfShiftsInARow[i] = numOfShiftsInARow[i] + 1
    
    for i in numOfShiftsInARow:
        numOfShiftsInARowAll = np.append(numOfShiftsInARowAll, i)
    
    for i in S:
        SAll = np.append(SAll, i)
    
    #print(S)
    #Legjobb = S.copy()
    
    Slast = np.array([])
    for i in range(0, nursenum):
      #randnum = 0
      Slast = np.append(Slast, S[i])
    Slast = Slast.astype(int)
    Wcummulative = np.array([])
    minWcummulative = np.array([])
    minWShiftArray = np.array([])
    #W = np.array([])
    #WAll = np.array([])
    #WShiftMinoseg = np.array([])
    while True:
        S2 = Slast.copy()
        #print("S2 ", S2)
        ratios = []
        W=np.array([])
        WAll = np.array([])
        WShiftMinoseg = np.array([])
        #Wcummulative = np.array([])
        minWcummulative = np.array([])
        #scouter bees here?
        employedS = np.array([])
        if(gennum > gennum2):
            WShiftMinoseg = np.array([])
            for elem in Wcummulative:#ha uj nap van, a meglevo 50% W-nek uj shift minosege lesz, mas arrayhez viszonyitjuk
                #print("wcum elem is", elem)
                minW = shiftMinoseg(elem,S2,numOfShiftsInARow)
                #print("and shiftmin is ", minW)
                WShiftMinoseg = np.append(WShiftMinoseg, minW)
            for gennum2i in range(gennum2):
                employedS = np.array([])
                for i in range(nursenum):
                    randgen = random.choice(constepslistabc)
                    toappend = WFinalbaRakott[i] + randgen #minWshift[0][i] volt / minWShiftArray[i] volt
                    if (WFinalbaRakott[i] + randgen) > 3: 
                        toappend = 0
                    elif (WFinalbaRakott[i] + randgen) < 0:
                        toappend = 3
                    employedS=np.append(employedS,toappend)
                employedSInt = employedS.astype(int)
                #print(employedSInt)
                #print(S2)
                #print(numOfShiftsInARow)
                minEmp = shiftMinoseg(employedSInt,S2,numOfShiftsInARow)
                WAll = np.append(WAll, employedSInt)
                WShiftMinoseg = np.append(WShiftMinoseg, minEmp)
                #print("empw", WAll)
        if(gennum == gennum2):
            for its in range(gennum2):
                W = np.array([])
                for i in range(nursenum):
                    toappend = random.randint(0,3)
                    W=np.append(W,toappend)
       
                Wint = W.astype(int)
                minW = shiftMinoseg(Wint,S2,numOfShiftsInARow)
                WAll = np.append(WAll, Wint)
                WShiftMinoseg = np.append(WShiftMinoseg, minW)
        
            #minS = shiftMinoseg(S,Slast,numOfShiftsInARow)
            #if(minW < minS): # <
            #    S = W.copy()
        WAllReshape = WAll.reshape(gennum2, nursenum)
        WAllReshapeInt = WAllReshape.astype(int)
        WShiftMinosegInt = WShiftMinoseg.astype(int)
        #WShiftMinoseg = WShiftMinoseg.reshape(gennum, nursenum)
        #print(S2)
        #print(WAllReshapeInt)
        #print(WShiftMinosegInt)
        #break

        Wcummulative = np.append(Wcummulative, WAllReshapeInt)
        minWcummulative = np.append(minWcummulative, WShiftMinosegInt)
        Wcummulative = Wcummulative.astype(int)
        minWcummulative = minWcummulative.astype(int)
        #print("wcum after generating", Wcummulative)
        WcumReshape = Wcummulative.reshape(gennum, nursenum)
        WcumReshapeInt = WcumReshape.astype(int)
        #print("wcum after generating and reshaping", WcumReshapeInt)
        #print(minWcummulative)
        ##minWShiftMinoseg = min(WShiftMinosegInt)
        #minWShiftMinosegPos = WShiftMinosegInt.index(minWShiftMinoseg)
        ##minWShiftMinosegPos = np.where(WShiftMinosegInt == minWShiftMinoseg)
        ##minWShift = WAllReshapeInt[minWShiftMinosegPos]
        Wnext = np.array([])
        WFinalbaRakott = np.array([])
        for halfi in range(0, int(gennum/2) + 1):#+1!!!
            minWShiftMinoseg = min(minWcummulative)
            #print("forban min in minwcum ", minWShiftMinoseg)
            #print("all min in minwcum", minWcummulative)
        #minWShiftMinosegPos = np.where(minWcummulative == minWShiftMinoseg)
            minWShiftMinosegPos = -1
            for Windex in range(0, len(minWcummulative)):
                if minWcummulative[Windex] == minWShiftMinoseg:
                    minWShiftMinosegPos = Windex
                    minWcummulative[Windex] = 10000000
                    break
            minWShift = Wcummulative[minWShiftMinosegPos]
            minWShift = minWShift.astype(int)
            minWShiftArray = np.array([])
            for minposi in range(minWShiftMinosegPos * nursenum, (minWShiftMinosegPos + 1) * nursenum):
                minWShiftArray = np.append(minWShiftArray, Wcummulative[minposi])
        #print(minWShiftMinoseg)
        #print(S2)
        #print("wcum", Wcummulative)
        #print(minWcummulative)
        #print(minWShiftMinoseg)
        #print(minWShiftMinosegPos) 
        #print(minWShift)#arraylength != nursenum neha for some reason, look into it
        #break
            minWShiftArray = minWShiftArray.astype(int)
        #print(minWShiftArray)
            if(halfi == 0):
                WFinalbaRakott = minWShiftArray
                WFinal = np.append(WFinal, minWShiftArray)
            else:
                Wnext = np.append(Wnext, minWShiftArray)
        #print("wnext", Wnext)
        #top 50% maradjon meg a W-bol, bottom 50% szevasz efolott
        WnextInt = Wnext.astype(int)
        WnextReshape = WnextInt.reshape(int(gennum/2), nursenum)
        WnextReshapeInt = WnextReshape.astype(int)
        Wcummulative = WnextReshapeInt

        gennum2 = int(gennum / 2)

        k = k + 1

        Slast = WFinalbaRakott
        #print("finalba rakott: ", WFinalbaRakott)
        minWShiftArrayLen = len(WFinalbaRakott)
        for i in range(minWShiftArrayLen):
            #if(minWShiftArray[i] != 0):
            if(WFinalbaRakott[i] != 0):
                numOfShiftsInARow[i] = numOfShiftsInARow[i] + 1
            else:
                numOfShiftsInARow[i] = 0
        
        for i in numOfShiftsInARow:
            numOfShiftsInARowAll = np.append(numOfShiftsInARowAll, i)

        if(k > numofdays):
            fullshiftminoseg = 0
            #print(numOfShiftsInARowAll)
            numOfShiftsInARowAllReshape = numOfShiftsInARowAll.reshape(numofdays+1, nursenum)
            #numOfShiftsInARowAllInt = numOfShiftsInARowAllReshape.astype(int)
            numOfShiftsInARowAllInt = numOfShiftsInARowAllReshape.astype(int)
            #SAllReshape = SAll.reshape(k, dim)
            #print(Wcummulative)
            Wcummulative = WFinal.astype(int)
            Wcummulative = Wcummulative.reshape(numofdays, nursenum)
            #print(Wcummulative)
            for i in range(1, numofdays):
                #print(Wcummulative[i], Wcummulative[i-1],numOfShiftsInARowAllInt[i-1])
                fullshiftminoseg = fullshiftminoseg + shiftMinoseg(Wcummulative[i],Wcummulative[i-1],numOfShiftsInARowAllInt[i-1])
            return fullshiftminoseg, Wcummulative


nursenum = 200
numofdays = 50
iterations = 40
gennum = 40 #iterations but for abc instead

szimulaltnumresults = np.array([])
for i in range(0, 1):
    numresult, arrayresult = szimulaltLehutes(nursenum,numofdays,"exponential",iterations)
    szimulaltnumresults = np.append(szimulaltnumresults, numresult)
szimulaltnumresults = szimulaltnumresults.astype(int)
print("simulated annealing num results: ", szimulaltnumresults)
print("average of simulated annealing results: ", np.mean(szimulaltnumresults))
print("std deviation of simulated annealing num results: ", np.std(szimulaltnumresults))

abcnumresults = np.array([])
for i in range(0, 1):
    numresult, arrayresult = abc(nursenum, numofdays, gennum)
    abcnumresults = np.append(abcnumresults, numresult)
abcnumresults = abcnumresults.astype(int)
print("artificial bee colony num results: ", abcnumresults)
print("average of artificial bee colony results: ", np.mean(abcnumresults))
print("std deviation of artificial bee colony num results: ", np.std(abcnumresults))
#cs = [1, 2, 3, 0, 2, 3]
#ls = [2, 2, 0, 1, 1, 1]
#ns = [6, 6, 5, 6, 5, 5]
#print(shiftMinoseg(cs,ls,ns))