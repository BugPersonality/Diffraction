import numpy as np
from scipy.stats import norm
import scipy.stats as st
import matplotlib.pyplot as plt
import math
import random 

constPlank = 1.054 * (10 ** (-34))      # Дж / c
deltaX = 5.5 * (10 ** (-10))            # м 
deltaPhi = 50                           # В 
massE = 9.1093837015 * (10 ** (-31))    # кг
e = 1.60217662 * (10 ** (-19))          # Кл
COUNT1 = 15
COUNT2 = -15

def getPx(k):
    return ((2 * k - 1) * math.pi * 2 * constPlank) / (12 * deltaX)

def getPhiX(px, p):
    return np.arcsin(px / p)

def getP():
    return math.sqrt(e * deltaPhi * massE * 2)

def waveFunction(px):
    return math.sqrt(deltaX / (2 * math.pi * constPlank)) * (math.sin((px * deltaX) / (2 * constPlank)) / ((px * deltaX) / (2 * constPlank)))

def waveFunctionAbsPow(px):
    return math.pow(abs(waveFunction(px)), 2)

def getDeBroglieWavelength(p, mode):
    if mode == "angle":
        return deltaX * math.sin(p)
    elif mode == "pulse":
        return (2 * constPlank) / p

def getDistribution(listP, amount):
    class Section:
        start = 0
        end = 0
        value = 0
        def __init__(self, start, end):
            self.start = start
            self.end = end

    dx = 0.55 * 10 ** (-34)
    h = 1.054 * 10 ** (-34)
    phi = waveFunctionAbsPow 
    probabilityP = []
    for p in listP:
        probabilityP.append(phi(p))
    sum_ = sum(probabilityP)
    for p in range(len(probabilityP)):
        probabilityP[p] /= sum_
    start = 0
    probabilitySection = []
    for p, val in zip(probabilityP, listP):
        section = Section(start, start + p)
        section.value = val
        start += p
        probabilitySection.append(section)

    distribution = []
    for _ in range(amount):
        randVal = random.uniform(0, 1)
        for section in probabilitySection:
            if  section.start <= randVal <= section.end:
                distribution.append(section.value)
                break
   
    return distribution

arrK = [i for i in range(COUNT2, COUNT1)]

arrPxk = []
arrPhiK = []
dictKToPx = {}
dictKToPhi = {}

for k in arrK:
    pxk = getPx(k)
    dictKToPx[k] = pxk
    phixK = getPhiX(pxk, getP())
    dictKToPhi[k] = phixK
    arrPxk.append(pxk)
    arrPhiK.append(phixK)

dist = np.array(getDistribution(arrPxk, 10000))
x = list(dist)
x.sort()
dict = {}

for x_ in x:
    if dict.get(x_) is not None:
        dict[x_] += 1
    else:
        dict[x_] = 1

arrCountPxForK = []

for key in range(COUNT2, COUNT1):
    if dict.get(dictKToPx[key]) is not None:
        arrCountPxForK.append(dict[dictKToPx[key]]/dict[dictKToPx[1]])
    else:
        arrCountPxForK.append(0)

arrForMainCpp = []

for px in x:
    for key in range(COUNT2, COUNT1):
        if px == dictKToPx[key]:
            arrForMainCpp.append(key)
            break

random.shuffle(arrForMainCpp)

f = open('resources/keys.txt', 'w')
f.write(f"{len(arrForMainCpp)} {len(dictKToPx)} \n")
for i in arrForMainCpp:
    f.write(str(i) + " \n")
f.close()

barlist = plt.bar(arrK, arrCountPxForK)
firstMin = 1

for i in range(1, len(arrCountPxForK) - 1):
    if (arrCountPxForK[i] < arrCountPxForK[i - 1]) and (arrCountPxForK[i] <= arrCountPxForK[i + 1]):
        barlist[i].set_color('r')
        firstMin = (i, arrCountPxForK[i])
        break
    elif (arrCountPxForK[i] < arrCountPxForK[i - 1]) and (arrCountPxForK[i] < arrCountPxForK[i + 1]):
        barlist[i].set_color('r')
        firstMin = (i, arrCountPxForK[i])
        break

plt.show()

# deBroglieWavelengthByPulse = getDeBroglieWavelength(firstMin[1], "pulse")
# deBroglieWavelengthByAngle = getDeBroglieWavelength(dictKToPhi[firstMin[0]], "angle")

# print(f"De Broglie wavelength by angle and pulse: {deBroglieWavelengthByAngle} ?= {deBroglieWavelengthByPulse}")


# arrWaveFunc = []
# arrYForWaveFunc = []

# for px in dist:
#     arrWaveFunc.append(waveFunctionAbsPow(px))
#     arrYForWaveFunc.append((px * deltaX) / (2 * constPlank))

# plt.scatter(arrWaveFunc, arrYForWaveFunc)
# plt.show()