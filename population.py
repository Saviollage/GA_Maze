import random
import copy
from chromosome import Chromosome


class Population:
    #   População contém um valor para armazenar seu tamanho máximo e uma lista
    #   de individuos gerados inicialmente de forma aleatória

    def __init__(self, initialCoordinates, matrix, maxPopulationSize):
        #   Size representa o tamanho total da população
        self.size = maxPopulationSize
        #   Lista de individuos
        self.individuals = self.generateIndividuals(
            initialCoordinates, matrix)

    def generateIndividuals(self, initialCoordinates, matrix):
        #   A função generateIndividuals() realiza a geração de N individuos
        # sendo N o tamanho máximo da população
        individuals = []

        for _ in range(self.size):
            individuals.append(Chromosome(0, []))

        return individuals

    def crossover(self,  chromosome1, chromosome2):
        #   A função crossover recebe um individuo como parametro e modifica
        # o individuo atual para o crossover entre ambos

        r1 = chromosome1.road.copy()
        r2 = chromosome2.road.copy()

        if chromosome1.rating > chromosome2.rating and len(chromosome1.indexesOfCollision) > 0:
            index_r1 = chromosome1.indexesOfCollision[0]

        elif chromosome1.rating < chromosome2.rating and len(
                chromosome2.indexesOfCollision) > 0:
            index_r1 = chromosome2.indexesOfCollision[0]

        else:
            index_r1 = len(r1) - 1

        #   Aqui ja temos ambos com o mesmo tamanho de road (caminho),
        # sendo assim é possível relizar o crossover entre estes. Para isto
        # seleciona uma posicao aleatoria da lista e realiza a troca
        # position = int((len(r1) - (chromosome1.rating + chromosome2.rating)/2))

        position = index_r1

        chromosome1.road = (
            r1[:position] + r2[position:])

        chromosome2.road = (
            r2[:position] + r1[position:])

        return chromosome1, chromosome2

    def sortByRate(self, element):
        return element.rating

    def getBestIndividual(self):
        # Ordena a população por nota
        self.individuals = sorted(
            self.individuals, key=lambda item: (-item.found, -item.rating))
        best = Chromosome(0, [])

        best.generation = self.individuals[0].generation
        best.rating = self.individuals[0].rating
        best.road = self.individuals[0].road.copy()
        best.indexesOfMultipleRoads = self.individuals[0].indexesOfMultipleRoads.copy(
        )
        best.hadACollision = self.individuals[0].hadACollision
        best.possibleRoads = copy.deepcopy(self.individuals[0].possibleRoads)
        best.found = self.individuals[0].found

        return best

    def addRoad(self, initialCoordinates, matrix):
        self.size = len(self.individuals) - 1
        for _ in range(self.size):
            self.individuals[_].generateIndexesArrays(
                initialCoordinates, matrix)
            self.individuals[_].appendRoad(
                self.individuals[_].possibleRoads[-1])

    def updatePopulation(self, newPopulation):
        self.individuals = []
        for ind in newPopulation:
            self.individuals.append(ind)

    def updateGeneration(self, generation):
        for ind in self.individuals:
            ind.setGeneration(generation)
