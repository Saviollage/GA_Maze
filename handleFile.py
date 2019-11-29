import copy


class HandleFile:

    def __init__(self, filename):
        self.matrix = self.generateMatrix(self.getFileData(filename))

    def getFileData(self, name):
        #       A função fileData recebe um nome de um arquivo a ser
        #   aberto pelo usuário e mostra na tela a quantidade de linhas
        #   e colunas deste
        
        print('Analisando arquivo {}.txt'.format(name))
        file = open('Maze/{}.txt'.format(name), 'r')
        contents = file.read()

        lines = contents.split('\n')
        lines.pop()

        print('O arquivo em questão possui {} linhas'.format(len(lines)))
        print('O arquivo em questão possui {} colunas'.format(len(lines[0])))
        return lines

    def generateMatrix(self, fileLines):
        #       A função generateMatrix recebe o vetor de linhas do arquivo aberto
        #   a parir disso, é gerado uma matriz de inteiros (mat), onde:

        #   0 -> Espaço disponível
        #   1 -> Parede
        #   2 -> Ponto inicial
        #   3 -> Ponto final
        #   4 -> Usuário

        mat = []
        #   Convertendo matriz para inteiros
        for lineIndex, lineItems in enumerate(fileLines):
            mat.append([])
            for item in lineItems:
                mat[lineIndex].append(1 if item == '-' or item == '+' or item ==
                                      '|' else 0 if item == ' ' else
                                      2 if item == 'S' else 3 if item == 'E' else 4)

        newMat = []
        #   Gerando nova matriz removendo os espaços desnecessários
        for index, i in enumerate(mat):
            newMat.append([])
            for j in range(0, len(i), 2):
                newMat[index].append(mat[index][j])

        print('A matriz possui {} linhas'.format(len(newMat)))
        print('A matriz possui {} colunas'.format(len(newMat[0])))

        return newMat
    
    def getMatrix(self):
        #   Retorna a copia da matriz, para nao dar BO de referencias
        return copy.deepcopy(self.matrix)
