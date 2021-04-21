# int float bool
# list tuple dic

import numpy as np
import matplotlib.pyplot as plt
import random

from numba import experimental,float64
spec = [("dpi",float64),("cells",float64[:,:])]
@experimental.jitclass(spec)

class LifeOfGame:
    def __init__(self,dpi):
        self.dpi = dpi
        self.cells = np.zeros((dpi,dpi))


    def first(self):
        for i in range(self.dpi):
            for j in range(self.dpi):
                self.cells[i][j] = 1 if random.random() < 0.1 else 0.0

    def rule(self):
        cells = self.cells.copy()
        for i in range(1,self.dpi-1):
            for j in range(1,self.dpi-1):
                sign = 0
                for indexi in [i-1,i,i+1]:
                    for indexj in [j-1,j,j+1]:
                        if indexi != i or indexj !=j:
                            sign += cells[indexi][indexj]

                if sign == 3:
                    self.cells[i][j] = 1
                elif sign == 2:
                    pass
                elif sign>3 or sign<2:
                    self.cells[i][j] = 0

if __name__ == '__main__':
    life = LifeOfGame(100)
    life.first()
    plt.imshow(life.cells, cmap="binary")
    plt.pause(5)

    while True:
        life.rule()
        plt.imshow(life.cells, cmap="binary")
        plt.pause(0.1)




