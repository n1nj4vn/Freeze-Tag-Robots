import numpy as np
import matplotlib.pyplot as plt



def plotPoints(a):
    for i in range(len(a)):
        plt.scatter(a[i][0], a[i][1], color = 'g')
        #plt.pause(0.1)
    #plt.show()

def plotInitial(a):
    for i in range(len(a)):
        plt.scatter(a[i][0], a[i][1], color = 'r')
