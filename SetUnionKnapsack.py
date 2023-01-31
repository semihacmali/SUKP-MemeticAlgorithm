# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 19:38:38 2023

@author: suhed
"""
from os import listdir
from os.path import isfile, join
import numpy as np
from copy import deepcopy

class SetUnionKnapsack():
    def __init__(self, folderName, fileNo, penalty = False):
        mypath = folderName
        filenames = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        self.ID = filenames[fileNo]
        self.dosyaAdi = filenames[fileNo]
        f = open("{}/{}".format(folderName, self.dosyaAdi), "r")
        print("{}/{}".format(folderName, filenames[fileNo]))
        f.readline()
        f.readline()
        line1 = f.readline()
        start = line1.index('=')
        stop = line1.index(' ', start)
        self.m = int(line1[start + 1:stop])
        self.dimension = self.m
        start = line1.index('=', stop)
        stop = line1.index(' ', start)
        self.n = int(line1[start + 1:stop])
        start = line1.index('=', stop)
        iseof = line1.find(' ', start)
        if iseof == -1:
            stop = len(line1) - 1
        else:
            stop = line1.index(' ', start)

        self.C = int(line1[start + 1:stop])

        f.readline()
        f.readline()
        self.p = list(map(int, f.readline().split()))

        f.readline()
        f.readline()
        self.w = list(map(int, f.readline().split()))

        f.readline()
        f.readline()
        self.rmatrix = np.zeros((self.m, self.n), dtype=bool)
        self.items = []
        for i in range(self.m):
            self.items.append([])
            rm = list(map(int, f.readline().split()))
            self.rmatrix[i, :] = deepcopy(rm[:])
            self.items[i] = np.where(self.rmatrix[i][:] == True)
        self.R = np.zeros(self.m)
        self.freqs = np.sum(self.rmatrix, axis=0)
        for i in range(self.m):
            self.R[i] = self.p[i] / np.sum(self.w[j] / self.freqs[j] for j in range(self.n) if self.rmatrix[i][j])

        self.H = np.argsort(self.R)[::-1][:self.m] # en cok tekrar eden degerlerin siralamasi
        self.penalty = penalty
        f.close()

    def optimizing_stage(self, solution, temp):
        trial = temp.copy()
        for i in range(self.m):
            a = self.H[i]
            if solution[a] == 0:
                b = self.items[a]
                trial[b] = 1
                cap_val = np.sum(self.w, where=trial)
                if cap_val <= self.C:
                    temp[b] = True
                    solution[a] = True
                else:
                    trial = temp.copy()
        return solution

    def repair(self, solution):
        temp_sol = np.zeros(self.m, dtype=bool)
        temp = np.zeros((self.n), dtype=bool)
        trial = np.array(temp, copy=True)

        for i in range(self.m):
            a = self.H[i]
            if solution[a]:
                b = self.items[a]
                trial[b] = True
                cap_val = np.sum(self.w, where=trial)
                if cap_val <= self.C:
                    temp[b] = True
                    temp_sol[a] = True
                else:
                    trial = temp.copy()
        return temp_sol, temp

    def objective_function(self, solution):
        temp = np.zeros((self.n), dtype=bool)
        for i in range(self.m):
            if solution[i]:
                temp[self.items[i]] = True
        cap_val = np.sum(self.w, where=temp)
        runPenalty = False
        if cap_val > self.C:
            if self.penalty:
                runPenalty = True
                sum_val = min(self.p) / ( 2 * cap_val - self.C)
            else:
                solution, temp = self.repair(solution)
                solution = self.optimizing_stage(solution, temp)
        else:
            solution = self.optimizing_stage(solution, temp)
        if not runPenalty:    
            sum_val = np.sum(self.p[i] for i, val in enumerate(solution) if val)
        return solution, sum_val
    
# problem = SetUnionKnapsack('Data/SUKP',28)

# problem.items[0]
# problem.rmatrix[0]
# mypath = 'Data/SUKP'
# filenames = [f for f in listdir(mypath) if isfile(join(mypath, f))]
# solution = np.random.random(85) > 0.5
# for i, val in enumerate(solution):
#     print(i , val)