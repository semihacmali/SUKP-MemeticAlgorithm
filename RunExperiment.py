# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 14:04:02 2023

@author: suhed
"""

import sys
import GeneticAlgorithm
import SetUnionKnapsack
import numpy as np
import statistics
import matplotlib.pyplot as plt
import pandas as pd


pNo = 28 #dosya numarasi (0-29)
pop_size = 20
mutation_rate = 0.1
penalty = False

# problem = SetUnionKnapsack.SetUnionKnapsack('Data/SUKP',pNo, True)

bestValues = []
bestGens = []
matrixBestValues = [[] for i in range(30)]
matrixBestGenes = [[] for i in range(30)]
df = pd.DataFrame()
for j in range(0,30):
    problem = SetUnionKnapsack.SetUnionKnapsack('Data/SUKP',j, penalty)
    for i in range(0,30):
        GN = GeneticAlgorithm.GeneticAlgorithm(problem, pop_size, mutation_rate, 20 * max(problem.m, problem.n))
        GN.run()
        bestValues.append(GN.bestValues[-1])
        bestGens.append(GN.bestGen)
    
    matrixBestValues[j].append(bestValues)
    matrixBestGenes[j].append(bestGens)
    df[problem.dosyaAdi] = [min(bestValues), max(bestValues), statistics.mean(bestValues), statistics.median(bestValues), statistics.stdev(bestValues)]
    print(df[problem.dosyaAdi])




