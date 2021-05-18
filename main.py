import random
import numpy as np 
from scipy.stats import norm
import matplotlib.pyplot as plt

def draw_random_number_from_pdf(pdf, interval, pdfmax = 1, max_iterations = 100):
        for i in range(max_iterations):
            rand_x = (interval[1] - interval[0]) * np.random.random(1) + interval[0] 

            rand_y = pdfmax * np.random.random(1) 
            calc_y = pdf(rand_x)

            if(rand_y <= calc_y ):
                return rand_x

arr = []
x_axis = np.arange(0, 1, 0.1)

for i in range(10):
    arr.append(draw_random_number_from_pdf(norm.pdf, [0, 1])[0])

plt.plot(x_axis, arr)
plt.show()

print(arr)


