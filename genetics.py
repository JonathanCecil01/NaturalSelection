import random

import simulation
from brain import AllLayers
import math
import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-1 * x))



Age, Bdx, Bdy, Lmy, Lmx, Lx, Ly, Gen = 0, 0, 0, 0, 0, 0, 0, 0
S_Inputs = [Age, Lx, Ly, Lmx, Lmy, Gen, Bdx, Bdy]
Mvx, Mvy, Mrn, Mfd = 0, 0, 0, 0
A_Outputs = [Mvx, Mvy, Mrn, Mfd]

def bin_to_int(b):
    j =0
    sum =0
    for i in b:
        if i=='1':
            sum+= 2**j
        j+=1
    return sum



class Gene:
    def __init__(self):
        self.code = ""
        self.source_type = 0
        self.sourceNum = 0
        self.sink_type = 0
        self.sinkNum = 0
        self.weight = random.randrange(-4, 4, 1)

class Neuron:
    def __init__(self):
        self.output =0
        self.driven =0


class NeuralNet:
    def __init__(self):
        self.connections = []
        self.neurons = []



class Genome:
    def __init__(self):
        self.code = ""
        self.connections = []
        self.survival = 0
        self.inputs = [0, 0, 0, 0, 0, 0, 0, 0]
        self.outputs = [0, 0, 0, 0]
        self.weights = [0, 0, 0, 0, 0, 0, 0, 0]

class Evolution:
    @staticmethod
    def random_gene():
        g = Gene()
        gene = bin(random.getrandbits(14))
        if len(gene)<16:
            x = '0'*(16-len(gene))
            gene+=x
        g.code = gene[2:]
        g.source_type = gene[3]
        g.sourceNum = bin_to_int(gene[4:7])
        g.sink_type = gene[9]
        g.sinkNum = bin_to_int(gene[10:12])
        g.weight = bin_to_int(gene[12:])
        return g

    @staticmethod
    def generate_genome():
        length = random.randint(2, 6)
        genome = Genome()
        for i in range(length):
            genome.connections.append(Evolution.random_gene())
        for gene in genome.connections:
            genome.code+=str(gene.code)
            genome.inputs[gene.sourceNum]=1
            genome.outputs[gene.sinkNum]= 1
            genome.weights[gene.sourceNum]= gene.weight
        return genome

    @staticmethod
    def survivor(organisms):
        survivors = []
        for organism in organisms:
            if organism.survival==1:
                survivors.append(organism)
        return survivors

    #from simulation import Organism

    @staticmethod
    def cross(p1, p2):
        config = [(8, 6, sigmoid), (6, 4, sigmoid)]
        layers= []
        for layer in config:
            layers.append(AllLayers(*layer))
        c1 = simulation.Organism(layers)
        gc_in = p1.gene_code.inputs[:int(len(p1.gene_code.inputs)/2)]+p2.gene_code.inputs[int(len(p2.gene_code.inputs)/2):]
        while len(gc_in)>8:
            gc_in.pop(-1)
        gc_out = p1.gene_code.outputs[:int(len(p1.gene_code.outputs)/2)]+p2.gene_code.outputs[int(len(p2.gene_code.outputs)/2):]
        while len(gc_out)>4:
            gc_out.pop(-1)
        gc_w = p1.gene_code.weights[:int(len(p1.gene_code.weights) / 2)] + p2.gene_code.weights[
                                                                          int(len(p2.gene_code.weights) / 2):]
        while len(gc_w) > 8:
            gc_w.pop(-1)
        genome = Genome()
        genome.inputs = gc_in
        genome.outputs = gc_out
        genome.weights = gc_w
        for i in gc_in:
            genome.code+=str(i)
        c1.set_gene_code(genome)
        return c1


    @staticmethod
    def selection(organisms):
        survivors = Evolution.survivor(organisms)
        return survivors

    @staticmethod
    def crossover(organisms):
        offsprings = []
        for p1 in organisms:
            for p2 in organisms:
                if math.dist(p1.color,p2.color)<=200 and math.dist((p1.loc_x, p1.loc_y), (p2.loc_x, p2.loc_y))<=5:
                    c1 = Evolution.cross(p1,p2)
                    offsprings.append(c1)
        organisms.extend(offsprings)
        return organisms


    # def mutation(organisms):
    #     for organism in organisms:
    #         pass


    @staticmethod
    def evolve(fit_function, current_gen):
        print("New Generation")
        fit_function(current_gen)
        pop_size = len(current_gen.organisms)
        print(pop_size)
        genomes = Evolution.selection(current_gen.organisms)
        print(len(genomes))
        genomes = Evolution.crossover(genomes)
        print(len(genomes))
        #genomes = Evolution.mutation(genomes)
        for genome in genomes:
            genome.survival = 1
        return genomes


    # @staticmethod
    # def generate_population(pop_size):
    #     organisms = []
    #     for i in range(pop_size):
    #         organisms.append(Evolution.r)
    #     return organisms






