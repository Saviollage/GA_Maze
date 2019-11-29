import random
import copy


class Chromosome:

    #   O individuo desta população é o cromossomo, este contém
    # uma nota referente a sua classificação (aptidão), e o caminho
    # que ele realiza no labirinto.

    def __init__(self, rating, road):

        #   Sua nota varia de 1 até lado² e diz respeito
        #   a classificação do caminho, quanto maior esta avaliação maior a
        #   chance do individuo resolver o labirinto.
        self.rating = rating

    #   Já o caminho é um vetor de movimentos realizados pelo individuo
    #   sendo estes:
    #
    #   1 -> Esquerda
    #   2 -> Cima
    #   3 -> Direita
    #   4 -> Baixo

        self.road = road

    #   Variável que verifica se houve colisão
        self.hadACollision = False

    #   Variável que verifica se houve conclusao da matriz
        self.found = False

    #   Vetor com os índices do vetor road onde há multiplos caminhos
        self.indexesOfMultipleRoads = []

    #   Vetor com vetores de possiveis indices baseados no valor acima
        self.possibleRoads = []

    #   Valor de sua geração atual
        self.generation = 0

    def wightedChoice(self, elements):
        #   Recebe uma lista e escolhe um valor aleatório com peso baseado na posição de cada elemento, tendendo a escolha para o final da lista

        if len(elements) == 1:
            return elements[0]
        
        else:
            sum = 0
            for _ in range(len(elements)):
                sum += _

            choice = random.randint(1, sum)
            newSum = 0
            for _ in range(len(elements)):
                newSum += _
                if choice <= newSum:
                    return elements[_]

    def mutation(self,  mutationChance, mutationChanceForCollision):
        #   A função mutacão recebe um individio e realiza sua mutação
        # baseada em uma porcentagem enviada pelo parametro `mutationChance`
        if self.hadACollision:
            if random.random()*100 < mutationChanceForCollision:

                index = self.wightedChoice(self.indexesOfMultipleRoads)

                self.possibleRoads = self.possibleRoads[:index]
                self.road = self.road[:index]
                self.indexesOfMultipleRoads = self.indexesOfMultipleRoads[:self.indexesOfMultipleRoads.index(
                    index)]
                self.hadACollision = False

    def getPossibleRoad(self, maze, point):
        possible = []

        #   VERIFICA SE O PONTO NÃO ULTRAPASSA OS LIMITES DA MATRIZ E SE A POSIÇÃO É VÁLIDA PARA O USUÁRIO
        if point[1]-1 >= 0 and maze[point[0]][point[1]-1] == 0:
            #   ESQUERDA
            possible.append(1)

        #   VERIFICA SE O PONTO NÃO ULTRAPASSA OS LIMITES DA MATRIZ E SE A POSIÇÃO É VÁLIDA PARA O USUÁRIO
        if point[1]+1 <= (len(maze[0]) - 1) and maze[point[0]][point[1]+1] == 0:
            #   DIREITA
            possible.append(3)

        #   VERIFICA SE O PONTO NÃO ULTRAPASSA OS LIMITES DA MATRIZ E SE A POSIÇÃO É VÁLIDA PARA O USUÁRIO
        if point[0]-1 >= 0 and maze[point[0]-1][point[1]] == 0:
            #   CIMA
            possible.append(2)

        #   VERIFICA SE O PONTO NÃO ULTRAPASSA OS LIMITES DA MATRIZ E SE A POSIÇÃO É VÁLIDA PARA O USUÁRIO
        if point[0]+1 <= (len(maze) - 1) and maze[point[0]+1][point[1]] == 0:
            #   BAIXO
            possible.append(4)

        return possible

    def fitness(self, initialCoordinates, matrix):
        # A funcao fitness define a pontuação de cada individuo
        maze = copy.deepcopy(matrix)
        actualPoint = initialCoordinates

        rate = 0
        for element in self.road:
            #   Relembrando que cada elemento do road varia de 1 a 4, sendo:
            #   1 -> Esquerda
            #   2 -> Cima
            #   3 -> Direita
            #   4 -> Baixo
            if element == 1 and actualPoint[1] > 0:
                #   Andar para ESQUERDA
                actualPoint = (actualPoint[0], actualPoint[1]-1)
            elif element == 2 and actualPoint[0] > 0:
                #   Andar para CIMA
                actualPoint = (actualPoint[0] - 1, actualPoint[1])
            elif element == 3 and actualPoint[1] < (len(maze[0]) - 1):
                #   Andar para DIREITA
                actualPoint = (actualPoint[0], actualPoint[1] + 1)
            elif element == 4 and actualPoint[0] < (len(maze) - 1):
                #   Andar para BAIXO
                actualPoint = (actualPoint[0]+1, actualPoint[1])

            if maze[actualPoint[0]][actualPoint[1]] == 0:
                #   Relembrando a codificação de cada elemento da matriz, sendo
                #   0 -> Espaço disponível
                #   1 -> Parede
                #   2 -> Ponto inicial
                #   3 -> Ponto final
                #   4 -> Usuário
                rate += 1

            elif maze[actualPoint[0]][actualPoint[1]] == 1 or maze[actualPoint[0]][actualPoint[1]] == 4:
                #   Se o usuário encontrar uma parede ou voltar para o caminho
                # anterior, seu caminho encerra
                break

            elif maze[actualPoint[0]][actualPoint[1]] == 3:
                self.found = True
                break

            # Define caminho ja percorrido pelo usuário
            maze[actualPoint[0]][actualPoint[1]] = 4

        self.rating = rate

    def generateIndexesArrays(self, initialCoordinates, matrix):
        maze = copy.deepcopy(matrix)
        actualPoint = initialCoordinates

        #   ANDA COM O INDIVIDUO PELO LABIRINTO ATÉ SEU ULTIMO PONTO
        for element in self.road:

            if maze[actualPoint[0]][actualPoint[1]] == 1 or maze[actualPoint[0]][actualPoint[1]] == 4:
                #   Se o usuário encontrar uma parede ou voltar para o caminho
                # anterior, seu caminho encerra
                self.hadACollision = True
                break

            if maze[actualPoint[0]][actualPoint[1]] == 3:
                self.found = True
                break

            # Define caminho ja percorrido pelo usuário
            maze[actualPoint[0]][actualPoint[1]] = 4

            if element == 1 and actualPoint[1] > 0:
                #   Andar para ESQUERDA
                actualPoint = (actualPoint[0], actualPoint[1]-1)
            elif element == 2 and actualPoint[0] > 0:
                #   Andar para CIMA
                actualPoint = (actualPoint[0] - 1, actualPoint[1])
            elif element == 3 and actualPoint[1] < (len(maze[0]) - 1):
                #   Andar para DIREITA
                actualPoint = (actualPoint[0], actualPoint[1] + 1)
            elif element == 4 and actualPoint[0] < (len(maze) - 1):
                #   Andar para BAIXO
                actualPoint = (actualPoint[0]+1, actualPoint[1])

        # Se não houve uma colisão
        if not self.hadACollision and not self.found:
            possible = self.getPossibleRoad(
                maze, actualPoint)

            currentIndex = len(self.possibleRoads)

            if len(possible) > 1:
                self.indexesOfMultipleRoads.append(currentIndex)
                self.possibleRoads.append(possible)
            elif len(possible) == 1:
                self.possibleRoads.append(possible)

    def moveChromossome(self, initialCoordinates, matrix):

        maze = matrix
        actualPoint = initialCoordinates
        road = self.road

        for index, element in enumerate(road):
            #   Relembrando que cada elemento do road varia de 1 a 4, sendo:
            #   1 -> Esquerda
            #   2 -> Cima
            #   3 -> Direita
            #   4 -> Baixo

            if element == 1 and actualPoint[1] > 0:
                #   Andar para ESQUERDA
                actualPoint = (actualPoint[0], actualPoint[1]-1)
            elif element == 2 and actualPoint[0] > 0:
                #   Andar para CIMA
                actualPoint = (actualPoint[0] - 1, actualPoint[1])
            elif element == 3 and actualPoint[1] < (len(maze[0]) - 1):
                #   Andar para DIREITA
                actualPoint = (actualPoint[0], actualPoint[1] + 1)
            elif element == 4 and actualPoint[0] < (len(maze) - 1):
                #   Andar para BAIXO
                actualPoint = (actualPoint[0]+1, actualPoint[1])

                #   Apenas para coloris mais claro os pontos de cruzamento
            if(index+1 in self.indexesOfMultipleRoads):
                maze[actualPoint[0]][actualPoint[1]] = 5
            elif maze[actualPoint[0]][actualPoint[1]] != 3:
                maze[actualPoint[0]][actualPoint[1]] = 4

    def appendRoad(self, possible):

        self.road.append(random.choice(possible))

    def setGeneration(self, generation):
        self.generation = generation

    def saveIndividual(self, individual):

        self.generation = individual.generation
        self.rating = individual.rating
        self.road = individual.road.copy()
        self.indexesOfMultipleRoads = individual.indexesOfMultipleRoads.copy(
        )
        self.hadACollision = individual.hadACollision
        self.possibleRoads = copy.deepcopy(individual.possibleRoads)
        self.found = individual.found
