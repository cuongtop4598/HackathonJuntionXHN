import random
from .parser import *
from .genetic import genotype, crossover, mutation, nextGeneration

def generator(target, POPULATION, GENERATION, match=None):
    g = 1
    result = []
    if match == None or match > len(target) :
        match = len(target)
    gene_count = len(genotype)
    pop = [random.sample(range(0,gene_count), gene_count) for _ in range(POPULATION)] 
    MAX_FITNESS = -1e9
    BEST_GENE = None
    BEST_REGEX = ""
    for i in range(GENERATION) :
        MAX_FITNESS = -1e9
        BEST_GENE = None
        BEST_REGEX = ""
        arr, filtered_set = preprocessor(random.sample(target,match))
        current_generation = []
        for idx, gene in enumerate(pop):
            g_res, fitness = parser(arr, filtered_set, gene)
            current_generation.append((fitness, ''.join(g_res)))
            if fitness > MAX_FITNESS:
                MAX_FITNESS = fitness
                BEST_GENE = gene
                BEST_REGEX = ''.join(g_res)
        fitness = [g[0] for g in current_generation]
        pop = nextGeneration(pop, fitness)
    result.append((MAX_FITNESS, BEST_REGEX))
    return result