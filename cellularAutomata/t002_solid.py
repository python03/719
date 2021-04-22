import numpy as np
import matplotlib.pyplot as plt
from numba import experimental,float64,int64
import random

spec =(["dpi",int64],["state",float64[:,:]],["cells",float64[:,:]],["number",float64],["edge",float64[:,:]])
@experimental.jitclass(spec)

class Solid:
    def __init__(self,dpi):
        self.dpi = dpi
        self.state = np.zeros((dpi,dpi))
        self.cells = np.zeros((dpi,dpi))
        self.number = 1
        self.edge = np.zeros((dpi, dpi))

    def nuclear(self):
        for i in range(self.dpi):
            for j in range(self.dpi):
                self.state[i][j] = 1 if random.random() < 0.00005 else 0.0
                if self.state[i][j]:
                    self.cells[i][j] = self.number
                    self.number += 1

    def growth(self):
        cells = self.cells.copy()
        for i in range(1,self.dpi-1):
            for j in range(1,self.dpi-1):
                if self.state[i][j] == 0:
                    for indexi in [i-1,i,i+1]:
                        for indexj in [j-1,j,j+1]:
                            if indexi != i or indexj != j:
                                sign = abs(indexi-i)+abs(indexj-j)
                                if sign==1:
                                    if cells[indexi][indexj]:
                                        self.cells[i][j] = cells[indexi][indexj] if random.random() < 0.5 else self.cells[i][j]
                                else:
                                    if cells[indexi][indexj]:
                                        self.cells[i][j] = cells[indexi][indexj] if random.random() < 0.1 else self.cells[i][j]
                    if self.cells[i][j]:
                        self.state[i][j] = 1
                    else:
                        self.cells[i][j] = self.number if random.random() < 1/self.dpi**2 else self.cells[i][j]
                        if self.cells[i][j]:
                            self.number += 1
                            self.state[i][j] = 1

    def growth2(self):
        cells = self.cells.copy()
        for i in range(1, self.dpi-1):
            for j in range(1,self.dpi-1):
                if self.state[i][j] == 0:
                    if cells[i-1][j-1]:
                        self.cells[i][j] = cells[i-1][j-1] if random.random() < 0.01 else self.cells[i][j]
                    elif cells[i-1][j]:
                        self.cells[i][j] = cells[i - 1][j] if random.random() < 0.1 else self.cells[i][j]
                    elif cells[i - 1][j+1]:
                        self.cells[i][j] =cells[i-1][j+1] if random.random() < 0.01 else self.cells[i][j]
                    if cells[i][j-1]:
                        self.cells[i][j] = cells[i][j - 1] if random.random() < 0.8 else self.cells[i][j]
                    if cells[i][j + 1]:
                        self.cells[i][j] = cells[i][j + 1] if random.random() < 0.8 else self.cells[i][j]
                    if cells[i+1][j-1]:
                        self.cells[i][j] = cells[i + 1][j - 1] if random.random() < 0.01 else self.cells[i][j]
                    if cells[i+1][j]:
                        self.cells[i][j] = cells[i + 1][j] if random.random() < 0.1 else self.cells[i][j]
                    if cells[i + 1][j + 1]:
                        self.cells[i][j] = cells[i + 1][j + 1] if random.random() < 0.01 else self.cells[i][j]
                  # else:
                    #     pass

                    if self.cells[i][j]:
                        self.state[i][j] = 1

    def edgeCell(self):
        self.edge = np.zeros((self.dpi,self.dpi))
        for i in range(1,self.dpi-1):
            for j in range(1,self.dpi-1):
                sign = False
                for indexi in [i-1,i,i+1]:
                    for indexj in [j-1,j,j+1]:
                        if self.cells[i][j] != self.cells[indexi][indexj]:
                            sign = True
                            break
                    if sign:
                        break
                if sign:
                    self.edge[i][j] = 1

if __name__ == '__main__':
    solid = Solid(1000)
    solid.nuclear()
    # plt.imshow(solid.state,cmap="binary")
    for i in range(200):
        solid.growth()
        if i % 10 == 0:
            solid.edgeCell()
            # np.savetxt(r"./{}.txt".format(i),solid.cells,fmt="%5d")
            plt.imshow(solid.edge, cmap="binary")
            plt.pause(0.1)
    plt.show()

