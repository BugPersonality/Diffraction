import numpy as np 
from scipy.stats import norm
import matplotlib.pyplot as plt
import math
from main import * 

constPlank = 1.054 * 10 ** (-34)    # Дж / c
deltaX = 5.5 * 10 ** (-10)          # м 
deltaPhi = 50                       # В 
massE = 9.1093837015 * 10 ** (-31)  # кг
e = 1.60217662 * 10 ** (-19)        # Кл

def getPx(k):
    return ((2 * k - 1) * math.pi * 2 * constPlank) / (12 * deltaX)

def getPhiX(px, p):
    return np.arcsin(px / p)

def getP():
    return math.sqrt(e * deltaPhi * massE * 2)

arrK = [i for i in range(1, 11)]

arrPxk = []
arrPhiK = []

for k in arrK:
    pxk = getPx(k)
    phixK = getPhiX(pxk, getP())
    arrPxk.append(pxk)
    arrPhiK.append(phixK)

print(f"Имульсы сука = \n {arrPxk} \n")
print(f"Углы сука = \n {arrPhiK} \n")

print(getDistribution(arrPxk, 10))