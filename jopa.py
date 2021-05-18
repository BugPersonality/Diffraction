import numpy as np
from scipy.stats import norm
import scipy.stats as st
import matplotlib.pyplot as plt
import math
from main import * 

constPlank = 1.054 * (10 ** (-34))      # Дж / c
deltaX = 5.5 * (10 ** (-10))            # м 
deltaPhi = 50                           # В 
massE = 9.1093837015 * (10 ** (-31))    # кг
e = 1.60217662 * (10 ** (-19))          # Кл

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

arrK = [i for i in range(1, 10)]

arrPxk = []
arrPhiK = []
dictKToPx = {}

for k in arrK:
    pxk = getPx(k)
    dictKToPx[k] = pxk
    phixK = getPhiX(pxk, getP())
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

for key in range(1, 10):
    if dict[dictKToPx[key]] is not None:
        arrCountPxForK.append(dict[dictKToPx[key]]/dict[dictKToPx[1]])
    else:
        raise Exception('Srat')

plt.bar(arrK, arrCountPxForK)
plt.show()

# y = [dict[x_] for x_ in x]
# plt.scatter(x, y)
# plt.show()

arrWaveFunc = []
arrYForWaveFunc = []

for px in dist:
    arrWaveFunc.append(waveFunctionAbsPow(px))
    arrYForWaveFunc.append((px * deltaX) / (2 * constPlank))

# plt.scatter(arrWaveFunc, arrYForWaveFunc)
# plt.show()

# dx = 0.55 * 10 ** (-34)
# h = 1.054 * 10 ** (-34)
# phi = lambda p: pow(abs(math.sqrt(dx / (2 * math.pi * h) * ((math.sin(p * dx/ (2 * h)) )) / ((p * dx) / (2 * h) ))), 2)
# x = []
# y = []

# for i in range(1, 5):
#     x.append(phi(i))
#     y.append(i)

# plt.plot(x, y)
# plt.show()

