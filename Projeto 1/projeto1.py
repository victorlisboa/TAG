# Universidade de Brasília - Departamento de Ciências da Computação
# Teoria e Aplicação de Grafos
# Professor: Dibio Leandro Borges
# Aluno: Victor Hugo França Lisboa
# Projeto 1
# Data: 25/02/2022
# 
# Algoritmo de Bron-Kerbosch para encontrar todos os cliques maximais de um grafo com e sem pivoteamento
#
# Fontes utilizadas para o desenvolvimento deste projeto:
# - https://en.wikipedia.org/wiki/Bron–Kerbosch_algorithm
# - https://www.youtube.com/watch?v=j_uQChgo72I


from pathlib import Path

# Funções auxiliares

def montaGrafo():
    """ Entrada e criação da lista de adjacência """

    local_arquivo = Path(__file__).absolute().parent
    local_arquivo = local_arquivo / 'soc-dolphins.mtx'

    with open(local_arquivo) as arquivo:
        entrada = arquivo.readlines()
        qntGolfinhos, qntArestas = map(int, entrada.pop(0).split())
        listaAdjacencia = [[] for i in range(qntGolfinhos)]
        
        for i in range(qntArestas):
            verticeOrigem, verticeDestino = [int(j) for j in entrada[i].split()]
            listaAdjacencia[verticeOrigem - 1].append(verticeDestino)
            listaAdjacencia[verticeDestino - 1].append(verticeOrigem)  # Grafo não-direcionado
    
    return listaAdjacencia, qntGolfinhos


def VizinhosDe(vertice):
    """ Função que recebe um vértice e retorna seus vértices adjacentes """
    
    return listaAdjacencia[vertice - 1]


def intersec(lista1, lista2):
    """ Função que recebe duas listas e retorna a intersecção entre elas """
    
    return [item for item in lista1 if item in lista2]


# Implementações dos algoritmos de Bron-Kerbosch com e sem pivoteamento

def BronKerboschSemPivo(R, P, X):
    """ Algoritmo de Bron-Kerbosch sem pivoteamento """
    
    if(len(P) == 0 and len(X) == 0):  # R é reportada como um clique maximal
        print(f'Tamanho do clique = [{len(R)}] - Clique maximal = {{', end='')
        print(*R, sep=', ', end='')
        print('}')
        return

    Paux = P.copy()  # Lista auxiliar
    for vertice in P:
        vizinhos = VizinhosDe(vertice)
        BronKerboschSemPivo(R+[vertice], intersec(Paux, vizinhos), intersec(X, vizinhos))  # Chamada recursiva da função
        Paux.remove(vertice)
        X.append(vertice)


def BronKerboschComPivo(R, P, X):
    """ Algoritmo de Bron-Kerbosch com pivoteamento """

    if(len(P) == 0 and len(X) == 0):  # Se as listas P e X estão vazias, a lista R é reportada como um clique maximal
        print(f'Tamanho do clique = [{len(R)}] - Clique maximal = {{', end='')
        print(*R, sep=', ', end='')
        print('}')
        return

    Paux = P.copy()  # Lista auxiliar

    # Procura o vertice com maior grau no conjunto {P U X} pra melhorar a complexidade do algoritmo
    maiorGrau = -1
    for vertice in Paux + X:
        qntArestas = len(listaAdjacencia[vertice - 1])
        if(qntArestas > maiorGrau):
            maiorGrau = qntArestas
            vMaiorGrau = vertice  # Vértice de maior grau
    
    P = [i for i in P if i not in VizinhosDe(vMaiorGrau)]  # Lista com os vértices não adjacentes a vMaiorGrau

    for vertice in P:
        vizinhos = VizinhosDe(vertice)
        BronKerboschSemPivo(R+[vertice], intersec(Paux, vizinhos), intersec(X, vizinhos))  # Chamada recursiva da função
        Paux.remove(vertice)
        X.append(vertice)


def coeficienteMedio():
    """ Função que calcula e retorna coeficiente médio de arestas do grafo """

    somatorio = 0
    for vertice in listaVertices:
        vizinhos = VizinhosDe(vertice)
        qntVizinhos = len(vizinhos)
        triangulos = 0  # quantidade de cliques entre o vértice i e outros dois vizinhos de i
        for i in vizinhos:
            for j in vizinhos:
                if i != j and j in listaAdjacencia[i-1]:
                    triangulos += 1
        triangulos /= 2  # divide-se por dois pois cada triângulo é contado duas vezes
        triangulosPossiveis = (qntVizinhos * (qntVizinhos - 1))  # quantidade máxima possível de triângulos do vértice
        somatorio += ((2 * triangulos) / (triangulosPossiveis)) if triangulosPossiveis != 0 else 0  # condição pra evitar divisão por 0

    return somatorio / qntGolfinhos


# Leitura e criação da lista de adjacência

listaAdjacencia, qntGolfinhos = montaGrafo()
listaVertices = [i for i in range(1, qntGolfinhos+1)]

# Chamada do algoritmo de Bron-Kerbosch sem pivoteamento

print()
print('Executando o algoritmo de Bron-Kerbosch SEM pivoteamento para encontrar os cliques maximais:')
print()
BronKerboschSemPivo([], listaVertices, [])
print()
print('Executando o algoritmo de Bron-Kerbosch COM pivoteamento para encontrar os cliques maximais:')
print()
BronKerboschComPivo([], listaVertices, [])
print()
print(f'O coeficiente médio de arestas do grafo é {coeficienteMedio()}')
