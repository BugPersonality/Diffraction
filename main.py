import numpy as np 
from scipy.stats import norm
import matplotlib.pyplot as plt
import math
import random

constPlank = 1.054 * (10 ** (-34))      # Дж / c
deltaX = 5.5 * (10 ** (-10))            # м 
deltaPhi = 50                           # В 
massE = 9.1093837015 * (10 ** (-31))    # кг
e = 1.60217662 * (10 ** (-19))          # Кл

def waveFunction(px):
    return math.sqrt(deltaX / (2 * math.pi * constPlank)) * (math.sin((px * deltaX) / (2 * constPlank)) / ((px * deltaX) / (2 * constPlank)))

def waveFunctionAbsPow(px):
    return math.pow(abs(waveFunction(px)), 2)

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
    phi = waveFunctionAbsPow #lambda p: pow(abs(math.sqrt(dx / (2 * math.pi * h) * ((math.sin(p * dx/ (2 * h)) )) / ((p * dx) / (2 * h) ))), 2)
    probabilityP = []
    for p in listP:
        probabilityP.append(phi(p))
    sum_ = sum(probabilityP)
    # for p in probabilityP:
    #     p /= sum_
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
