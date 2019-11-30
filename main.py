import pygame
import random
from pygame.locals import *
from chromosome import Chromosome
from population import Population
from handleFile import HandleFile
from timeit import default_timer as timer
import sys
import copy
import os
import json
from time import sleep


def showWindow(matrix):
    #   A função showWindow recebe a matriz de posicoes dos objetos,
    # e a partir dela gera uma tela para melhor visualização do usuário
    # vale ressaltar que esta função faz uso da biblioteca pyGame para recursos
    # gráficos

    #   É definido a quantidade de linhas e colunas da matriz
    lines = len(matrix)
    columns = len(matrix[0])

    #   É definido uma taxa de proporção de tela, para melhor visualização dos
    # elementos, a screen ratio é definida baseada na quantidade de linhas do
    # arquivo
    screenRatio = (25, 25) if lines < 20 else (
        7, 7) if lines < 120 else (4, 4) if lines < 220 else (2, 2)

    #   Inicia a pyGame
    pygame.init()

    #   Define a tela baseada na proporção de tela e tamanho da matriz
    screen = pygame.display.set_mode(
        (columns*screenRatio[0], lines*screenRatio[1]))
    pygame.display.set_caption('Maze')

    #   Define o tamanho do pixel que representa a parede,
    #  conforme proporcao inicial com cor cinza
    #  #6b6b6b
    wallPixel = pygame.Surface(screenRatio)
    wallPixel.fill((107, 107, 107))

    #   Define o tamanho do pixel que representa o inicio,
    #  conforme proporcao inicial com cor vermelha
    #  #eb4034
    initPixel = pygame.Surface(screenRatio)
    initPixel.fill((235, 64, 52))

    #   Define o tamanho do pixel que representa o final,
    #  conforme proporcao inicial com cor azul
    #  #2bd6d3
    finishPixel = pygame.Surface(screenRatio)
    finishPixel.fill((43, 214, 211))

    #   Define o tamanho do pixel que representa o usuário,
    #  conforme proporcao inicial com cor amarela
    #  #ebba34
    userPixel = pygame.Surface(screenRatio)
    userPixel.fill((235, 186, 52))

    #   Define o tamanho do pixel que representa os pontos de colisao do usuário,  conforme proporcao inicial com cor amarela clara
    #  #f2d891
    userPixelonIndexesList = pygame.Surface(screenRatio)
    userPixelonIndexesList.fill((242, 216, 145))

    #   Define o fundo padrao como preto
    screen.fill((0, 0, 0))

    #   Percorre toda matriz para preencher a janela com pixels coloridos
    # baseados no valor de cada elemento da matriz
    for i, lines in enumerate(matrix):
        for j, element in enumerate(lines):
            if element == 1:
                screen.blit(wallPixel, (screenRatio[0]*j, screenRatio[1]*i))
            elif element == 2:
                screen.blit(initPixel, (screenRatio[0]*j, screenRatio[1]*i))
            elif element == 3:
                screen.blit(finishPixel, (screenRatio[0]*j, screenRatio[1]*i))
            elif element == 4:
                screen.blit(userPixel, (screenRatio[0]*j, screenRatio[1]*i))
            elif element == 5:
                screen.blit(userPixelonIndexesList,
                            (screenRatio[0]*j, screenRatio[1]*i))

    #   Exibe a tela
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

        pygame.display.update()


def getPoint(matrix, pointValue):
    (x, y) = (0, 0)
    for i, lines in enumerate(matrix):
        for j, item in enumerate(lines):
            if(item == pointValue):
                (x, y) = (i, j)

    return (x, y)


def showInformationDuringMoving(currentGeneration, bestGeneration, mutationChance, mutationWeight, bestIndividual, betterOnThatGeneration):
    os.system('cls')
    print('/////////////////////////////////////////////////////')
    print('Geração: {} | Melhor Geração: {} | Mutação: {}% | PesoDaMutação: {} '.format(
        currentGeneration, bestGeneration, mutationChance, mutationWeight))
    print('Melhor Individuo Geral: Fitness: {} | Pontos de colisao: {} | Prontos de cruzamento: {}'.format(
        bestIndividual.rating, bestIndividual.hadACollision, bestIndividual.indexesOfMultipleRoads))
    print('Possiveis caminhos: {}'.format(bestIndividual.possibleRoads))
    print('Melhor Individuo da Geração: Fitness: {} | Pontos de colisao: {} | Prontos de cruzamento: {}'.format(
        betterOnThatGeneration.rating, betterOnThatGeneration.hadACollision, betterOnThatGeneration.indexesOfMultipleRoads))
    print('Possiveis caminhos: {}'.format(
        betterOnThatGeneration.possibleRoads))
    print('Road: {}'.format(
        betterOnThatGeneration.road))
    print('/////////////////////////////////////////////////////')


def move(matrix, population, testMode, generations):

    initialCoordinates = getPoint(matrix, 2)
    maze = copy.deepcopy(matrix)
    start = timer()
    bestIndividual = Chromosome(0, [])
    individual = Chromosome(0, [])
    mutationWeight = 4
    mutationChance = 5

    #   Inicia o loop de gerações
    for currentGeneration in range(generations):
        for individual in population.individuals:

            individual.setGeneration(currentGeneration)

            individual.generateIndexesArrays(initialCoordinates, maze)
            # print('Possiveis caminhos: {}'.format(individual.possibleRoads))

            individual.appendRoad(individual.possibleRoads[-1])
            # print('Caminho: {}'.format(individual.road))

            individual.fitness(initialCoordinates, maze)

            individual.mutation(mutationChance, mutationChance*mutationWeight)

            if individual.found:
                bestIndividual.saveIndividual(individual)
                break

        os.system('cls')
        print('Geração: {}'.format(currentGeneration))
        print('Fitness: {}'.format(population.getBestIndividual().rating))
        print('Possivel: {}'.format(
            population.getBestIndividual().indexesOfMultipleRoads))


        if bestIndividual.found:
            break
        elif bestIndividual.rating < population.getBestIndividual().rating:
            bestIndividual.saveIndividual(population.getBestIndividual())

    os.system('\n\n\n')
    print('Aproximadamente: {}s'.format(timer() - start))
    if bestIndividual.found:
        print('Encontrou! {}'.format(len(bestIndividual.road)))
    print('/////////////////////////////////////////////////////')

    population.individuals = sorted(
        population.individuals, key=lambda item: (-item.found, -item.rating))

    content['Results'].append({
        "Fitness": bestIndividual.rating,
        "Geracao": bestIndividual.generation,
        "Encontrou": bestIndividual.found,
        "Tempo": timer() - start,
        "Qte Cruzamentos": len(bestIndividual.indexesOfMultipleRoads)
    })

    writeResults(resultsFileName, content)

    bestIndividual.moveChromossome(initialCoordinates, maze)
    showWindow(maze)


def writeResults(fileName, content):
    f = open('Results/' + fileName + '.json', 'w+')

    f.write(json.dumps(content))

    f.close()


#   Main
fileName = input('Entre com o nome do arquivo [M0/M1/M2/M3]: ')
handle = HandleFile(fileName)
matrix = handle.getMatrix()

generations = 10000
populationSize = 25
initialPoint = getPoint(matrix, 2)


resultsFileName = input(
    'Entre com o nome do arquivo para salvar os testes: [Ex: "Results"] \n Nome: ')



content = {
    "Arquivo Labirinto": fileName,
    "QtdMaxGeracoes": generations,
    "PopulationSize": populationSize,
    "Results": []
}


population = Population(initialPoint, matrix, populationSize)
move(matrix, population, content, generations)
