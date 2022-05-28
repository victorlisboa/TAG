# Universidade de Brasília - Departamento de Ciências da Computação
# Teoria e Aplicação de Grafos
# Professor: Dibio Leandro Borges
# Aluno: Victor Hugo França Lisboa
# Projeto 3
# Data: 25/04/2022
# 
# Modelagem de um jogo de Sudoku 9x9 como um grafo e a solução é feita
# utilizando algoritmo de coloração de grafos
#
# Fontes utilizadas para o desenvolvimento deste projeto:
# - https://medium.com/code-science/sudoku-solver-graph-coloring-8f1b4df47072

from random import randint, sample

def geraProposta():
    tabelaSudoku = [0 for x in range(81)]  # tabela do sudoku iniciada sem cores
    idx = randint(0, 81)  # Escolhe um indice aleatorio pra receber uma cor aleatoria
    tabelaSudoku[idx] = randint(1, 10) # Atribui uma cor aleatoria pra um unico vertice
    
    coloreGrafo(listaAdjacencias, 0, tabelaSudoku, False) # Resolve o problema inicial

    # Gera uma lista com 17 numeros diferentes para usar como proposta inicial
    proposta = sample(range(81), 17)  # indices dos vertices ja coloridos
    
    # descolore todos os outros vertices
    tabelaSudoku = [0 if x not in proposta else tabelaSudoku[x] for x in range(81)]
    
    return tabelaSudoku


def montaGrafo():
    """ O grafo eh montado através de lista de adjacencias """

    listaAdjacencias = []
    linhas = [[] for i in range(9)]
    colunas = [[] for i in range(9)]
    blocos = [[[] for i in range(3)] for j in range(3)]

    # listas que armazenam valores na mesma linha, coluna e bloco
    for linha in range(9):
        for coluna in range(9):
            num = coluna + 9*(linha)
            linhas[linha].append(num)
            colunas[coluna].append(num)
            blocos[num//27][num%9//3].append(num)
    
    # Para cada vertice adiciona os vertices adjacentes a ele
    # isto eh, todos os vertices na mesma linha, coluna e bloco
    for vertice in range(81):
        adjacentes = []
        for celula in linhas[vertice//9]:
            if celula != vertice:
                adjacentes.append(celula)
        for celula in colunas[vertice%9]:
            if celula != vertice:
                adjacentes.append(celula)
        for celula in blocos[vertice//27][vertice%9//3]:
            if celula != vertice and celula not in adjacentes:
                adjacentes.append(celula)
        listaAdjacencias.append(adjacentes)
    
    return listaAdjacencias


def mostraTabela(tabelaSudoku):
    """ Exibe a configuracao da tabela de sudoku passada como parametro """
    
    espaco = '  '
    largura = 37
    print('-'*largura)
    for linha in range(0, 9, 3):
        for x in range(3):
            print('|', end=espaco)
            for coluna in range(0, 9, 3):
                for y in range(3):
                    print(tabelaSudoku[(linha+x)*9 + coluna+y], end=espaco)
                print('|'+espaco, end='')
            print()
        print('-'*largura)


def ehPossivelColorir(tabelaSudoku, cor, vertice, listaAdjacencias):
    """ Retorna se eh possivel colorir o vertice com a cor passada """
    
    for vertice in listaAdjacencias[vertice]:
        if tabelaSudoku[vertice] == cor:
            return False
    
    return True


def coloreGrafo(listaAdjacencias, vertice, tabelaSudoku, mostrar):
    """ Funcao recursiva que colore o grafo resolvendo o problema do sudoku """
    
    # Caso base:
    # Se os vertices foram coloridos, retorna verdadeiro
    if vertice == 81:
        if(mostrar):  # flag pra determinar se a tabela deve ser mostrada
            print('\n' + '-'*40 + '\n' + '\nSolucao da proposta:\n')
            mostraTabela(tabelaSudoku)
        return True

    # Saidas intermediarias
    if vertice%50 == 0 and mostrar:
        qntColoridos = 0
        for v in tabelaSudoku:
            if v:
                qntColoridos += 1  # Conta a quantidade de vertices ja foram coloridos

        print(f'\nTabela com {qntColoridos} vertices coloridos:')
        mostraTabela(tabelaSudoku)

    # Tenta colorir o vertice com a menor cor
    # que nao esteja sendo usada pelos vertices adjacentes
    for cor in range(1, 10):
        if(ehPossivelColorir(tabelaSudoku, cor, vertice, listaAdjacencias)):
            estaColorido = True  # Assume que o vertice ja esta colorido
            if tabelaSudoku[vertice] == 0:
                estaColorido = False  # Se o valor da tabela for 0, nao esta colorido
                tabelaSudoku[vertice] = cor  # entao colore o vertice

            # Chamada recursiva com o proximo vertice
            # Se nao for possivel colorir com essa coloracao o
            # algoritmo faz backtracking e tenta colorir de outra forma
            if coloreGrafo(listaAdjacencias, vertice+1, tabelaSudoku, mostrar):
                return True

            if not estaColorido:  # Se nao estava colorido, retira a cor novamente
                tabelaSudoku[vertice] = 0
    
    # se nenhuma coloracao no estado atual der certo faz backtracking pra mudar de cor    
    return False


print("--- SUDOKU ---\n")
listaAdjacencias = montaGrafo()  # O grafo com seus respectivos indices sempre eh o mesmo
while(True):
    print('MENU:\n')
    print('1 - Gera nova proposta e a soluciona.\n' +
          '2 - Encerra programa.\n')
    entrada = input('Escolha uma opcao: ')
    if entrada == '2':
        break
    elif entrada == '1':
        print('\n' + '-'*40 + '\n' + '\nProposta Inicial:\n')
        tabelaSudoku = geraProposta()
        mostraTabela(tabelaSudoku)
        print('\n' + '-'*40 + '\n' + '\nSaidas Intermediarias:\n')
        coloreGrafo(listaAdjacencias, 0, tabelaSudoku, True)
        print('\n')
    else:
        print('\nEntrada invalida!\n')
