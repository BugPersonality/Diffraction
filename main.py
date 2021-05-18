import numpy as np 
from scipy.stats import norm
import matplotlib.pyplot as plt
import math
import random

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
    phi = lambda p: math.sqrt(dx / (2 * math.pi * h) * ((math.sin(p * dx/ (2 * h)) )) / ((p * dx) / (2 * h) ))
    probabilityP = []
    for p in listP:
        probabilityP.append(phi(p))
    sum_ = sum(probabilityP)
    for p in probabilityP:
        p /= sum_
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

