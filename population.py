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
        best.indexesOfMultipleRoads = self.individuals[0].indexesOfMultipleRoads.copy()
        best.hadACollision = self.individuals[0].hadACollision
        best.possibleRoads = copy.deepcopy(self.individuals[0].possibleRoads)
        best.found = self.individuals[0].found

        return best

