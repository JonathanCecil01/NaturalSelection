import pygame
from pygame import *
import random as rd
from brain import *
from genetics import Evolution
import numpy as np

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
POPULATION_SIZE = 100

pygame.font.init()
init()
screen = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def sigmoid(x):
    return 1 / (1 + np.exp(-1 * x))


def bin_to_int(b):
    j = 0
    sum = 0
    for i in b:
        if i == '1':
            sum += 2 ** j
        j += 1
    return sum


class Species():
    def __init__(self, config):
        self.organisms = []
        self.generate_pop(config)

    def generate_pop(self, config):
        for i in range(POPULATION_SIZE):
            layers = []
            for layer in config:
                layers.append(AllLayers(*layer))
            self.organisms.append(Organism(layers))

    def update_members(self):
        for i in self.organisms:
            i.age += 1

    def run_generations(self):
        for organism in self.organisms:
            organism.draw()
            organism.move()


class Organism():
    SIZE = 5

    def __init__(self, network: list[AllLayers]) -> None:
        self.gene_code = Evolution.generate_genome()
        self.loc_x = rd.randint(10, SCREEN_WIDTH - 10)
        self.loc_y = rd.randint(10, SCREEN_HEIGHT - 10)
        self.color = find_color(self.gene_code)
        #print(self.color)
        self.age = 0
        self.survival = 1
        self.network = network

    def set_gene_code(self, gene_code):
        self.gene_code = gene_code
        self.color = find_color(self.gene_code)

    def draw(self):
        draw.circle(screen, self.color, (self.loc_x, self.loc_y), Organism.SIZE)

    def move(self, output):
        # print(output)
        if self.gene_code.outputs[0] != 0:
            if output[0] > 0.5:
                self.loc_x += 2
            else:
                self.loc_x -= 2
        if self.gene_code.outputs[1] != 0:
            if output[1] > 0.5:
                self.loc_y += 2
            else:
                self.loc_y -= 2
        if self.gene_code.outputs[2] != 0:
            if output[2] >= 0.5:
                self.loc_x += rd.randint(-2, 2)
                self.loc_y += rd.randint(-2, 2)
        if self.gene_code.outputs[3] != 0:
            if output[3] >= 0.5:
                if self.gene_code.inputs[3] == 1:
                    self.loc_x += rd.randint(-2, 2)
                else:
                    self.loc_y += rd.randint(-2, 2)


def find_color(gcode):
    n = len(gcode.code)
    one_third = (255/2**int(n/3))*bin_to_int(gcode.code[:int(n/3)])
    two_third = (255/2**(int(2*n/3)-int(n/3)))*bin_to_int(gcode.code[int(n/3):int(2*n/3)])
    last_third = (255/2**(n-int(2*n/3)))*bin_to_int(gcode.code[int(2*n/3):])
    r = int(one_third)
    g = int(two_third)
    b = int(last_third)
    return r, g, b


def fit(species: Species):
    nets = []
    organisms = species.organisms
    for organism in organisms:
        nn = NeuralNetwork(organism)
        nets.append(nn)
    run = True
    while run and len(organisms)>0:
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    run = False
                    break



        for x, organism in enumerate(organisms):
            organism.survival = 1
            output = nets[x].propogate(organism.gene_code.inputs, organism.gene_code.weights)
            organism.move(output)

        for organism in organisms:
            if organism.loc_x >= SCREEN_WIDTH - 10:
                organism.loc_x = SCREEN_WIDTH - 10
            elif organism.loc_x <= 10:
                organism.loc_x = 10

            if organism.loc_y >= SCREEN_HEIGHT - 10:
                organism.loc_y = SCREEN_HEIGHT - 10
            elif organism.loc_y <= 10:
                organism.loc_y = 10
            organism.age += 1

            if organism.survival==0:
                organisms.remove(organism)

            if organism.age >= 190:
                aging = rd.randint(0, 300)
                if aging == 1:
                    organisms.remove(organism)

            #SETTING THE NATURAL SELECTION CRITERIA

        for organism in organisms:
            if organism.loc_x>=2*SCREEN_WIDTH/3 :
                organism.survival = 0
            organism.draw()

        # species.run_generations()
        display.update()
        time.delay(1)  # Speed down


def run(gen):
    config = [(8, 6, sigmoid), (6, 4, sigmoid)]
    species = Species(config)
    #organisms = species.organisms
    for i in range(gen):
        organisms = Evolution.evolve(fit, species)
        species = Species(config)
        species.organisms = organisms


if __name__ == "__main__":
    run(10)
