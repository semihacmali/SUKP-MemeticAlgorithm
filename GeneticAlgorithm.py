# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 16:47:39 2023

@author: suhed
"""
import random
import numpy as np




class GeneticAlgorithm():
    def __init__(self, problem, pop_size, mutation_rate, maxFE):
        
        self.problem = problem
        self.pop_size = pop_size
        self.mutation_rate = mutation_rate
        self.num_generations = int(maxFE / (int(self.problem.dimension) * 0.04)) - self.pop_size
    
    def bitFlip(self, gen, point):
        gen[point] = not gen[point]
        return gen
    
    def run(self):
        
        self.population = [np.random.random(self.problem.dimension) > 0.5 for _ in range(self.pop_size)]
        self.fitness_values = np.zeros(self.pop_size)
        for i in range(self.pop_size):
            self.population[i], self.fitness_values[i] = self.problem.objective_function(self.population[i])
        
        self.bestValues = []
        for generation in range(self.num_generations):
            c1, f1, c2, f2 = self.childCreate()
            
            self.population.append(c1)
            self.population.append(c2)
            
            self.fitness_values = np.append(self.fitness_values, f1)
            self.fitness_values = np.append(self.fitness_values, f2)
            
            ids = np.argsort(self.fitness_values)[::-1][:20]
            nextGens = []
            for i in ids:
                nextGens.append(self.population[i])
            
            self.population = nextGens
            self.fitness_values = self.fitness_values[ids]
            
            self.bestValues.append(self.fitness_values[0])
        
        self.bestGen = self.population[0]
        
        #return self.bestValues, self.bestGen
        
    def Mutation(self, gen):
        mutation_point = random.randint(0, self.problem.dimension - 1)
        gen = self.bitFlip(gen, mutation_point)
        return gen
            
            
    def childCreate(self):
        rand1 = random.randint(0,self.pop_size - 1)
        rand2 = random.randint(0,self.pop_size - 1)
        
        while rand1 == rand2:
            rand2 = random.randint(0,self.pop_size - 1)
        
        parent1 = self.population[rand1]
        parent2 = self.population[rand2]
        
        crossover_point = random.randint(0, self.problem.dimension - 1)
        self.child1 = np.concatenate((parent1[:crossover_point], parent2[crossover_point:]), axis=0)
        self.child2 = np.concatenate((parent2[:crossover_point], parent1[crossover_point:]), axis=0)
        
        self.child1 = self.firstImproventRandomHillClimbing(self.child1)
        self.child2 = self.firstImproventRandomHillClimbing(self.child2)
        
        #child1 Mutation
        if(random.random() < self.mutation_rate):
            self.child1 = self.Mutation(self.child1)
            
        #child2 Mutation
        if(random.random() < self.mutation_rate):
            self.child2 = self.Mutation(self.child2)
        
        self.child1, self.fitness1 = self.problem.objective_function(self.child1)
        self.child2, self.fitness2 = self.problem.objective_function(self.child2)
        
        
        return self.child1,self.fitness1, self.child2, self.fitness2

    def firstImproventRandomHillClimbing(self, chrom):
        tmpChrom, bestEval = self.problem.objective_function(chrom)
        for i in range(0,int(self.problem.dimension * 0.2)):
            randomGen = random.randint(0, self.problem.dimension-1)
            tmpChrom = self.bitFlip(chrom, randomGen)
            tmpChrom, tmpEval = self.problem.objective_function(tmpChrom)
            if tmpEval > bestEval:
               chrom = tmpChrom
               bestEval = tmpEval
            else:
                tmpChrom = self.bitFlip(chrom, randomGen)                
                
        return tmpChrom





# problem = dataRead.SetUnionKnapsack('Data/SUKP',28)
# GN = GeneticAlgorithm(problem, 20, 0.1, 20 * max(problem.m, problem.n))
# len(GN.fitness_values)

# GN.run()
# GN.childCreate()
# GN.child1
# GN.child2
# GN.problem.objective_function(GN.child1)
# len(GN.fitness_values)
# GN.population.append(GN.child1)
# np.argsort(GN.fitness_values)

# c1, f1, c2, f2 = GN.childCreate()


# GN.population.append(c1)
# GN.population.append(c2)
# b = GN.population
# GN.fitness_values = np.append(GN.fitness_values, f1)
# GN.fitness_values = np.append(GN.fitness_values, f2)
# ids = np.argsort(GN.fitness_values)[::-1][:20]
# nextGens = []
# for i in ids:
#     nextGens.append(GN.population[i])
    
# GN.fitness_values = GN.fitness_values[ids]
# type(GN.fitness_values)
# len(GN.fitness_values)
# a = np.append(a, f1)
# a = GN.fitness_values
# a.append(f1)
# GN.fitness_values.append(f1)
# GN.fitness_values.append(f2)
# c = np.flip(np.argsort(GN.fitness_values)[::-1][:20] )

# np.unlist(ids)
# d = b.take(ids)
# np.squeeze(ids)[()]
# a = int(a)
# len(GN.population[int(a)])



