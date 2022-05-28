# Universidade de Brasília - Departamento de Ciências da Computação
# Teoria e Aplicação de Grafos
# Professor: Dibio Leandro Borges
# Aluno: Victor Hugo França Lisboa
# Projeto 2
# Data: 11/04/2022
# 
# Algoritmo de Gale-Shapley para encontrar um emparelhamento estável
#
# Fontes utilizadas para o desenvolvimento deste projeto:
# - https://www.geeksforgeeks.org/stable-marriage-problem/

from pathlib import Path

def montaGrafo():
    """ Entrada e criação da lista de adjacência """

    local_arquivo = Path(__file__).absolute().parent
    local_arquivo = local_arquivo / 'entrada.txt'

    with open(local_arquivo) as arquivo:
        entrada = [x for x in arquivo.readlines() if x[0] == '(']
    
    projetos = {}   # projetos[projeto] = ([alunos], vagas, nota_minima)
    alunos = {}     # alunos[aluno]     = ([projetos], nota)

    for linha in entrada:   
        # Tratamento da entrada     
        if(linha[1] == 'A'):
            linha = linha.replace(' (', '*')
            linha = linha.replace('(', '')
            linha = linha.replace(')', '')
            aux, nota = linha.split('*')
            aluno, projs = aux.split(':')
            projs = projs.replace('P', '')
            nota = int(nota)
            projs = list(map(int, projs.split(', ')))

            alunos[aluno] = (projs, nota)
    
    for linha in entrada:
        # Tratamento da entrada
        if(linha[1] == 'P'):
            linha = linha[:-1].replace('(', '')
            linha = linha.replace(')', '')
            projeto, *aux = linha.split(', ')
            aux = list(map(int, aux))

            vagas, nota_minima = aux

        # Cria uma lista de preferencia de cada projeto
            aluns = []
            for aluno in alunos:
                # O aluno so entra na lista de preferencia se ele tiver interesse no
                # projeto e tiver nota maior ou igual a nota requerida pelo projeto
                if int(projeto[1:]) in alunos[aluno][0] and alunos[aluno][1] >= aux[1]:
                    aluns.append(aluno)

            # Ordena a lista de preferencia do projeto pelas maiores notas
            aluns.sort(key=lambda x: alunos[x][1], reverse=True)

            projetos[projeto] = (aluns, vagas, nota_minima)

    return projetos, alunos


def prefereProjAtual(alunos, aluno, projetoAtual, projetoAluno):
    ''' Retorna se o aluno prefere o projeto analisado atualmente ao que ele esta '''
    return alunos[aluno][0].index(int(projetoAtual[1:])) < alunos[aluno][0].index(int(projetoAluno[1:]))


def validaImpressao(contador):
    ''' Valida se a string sera impressa na tela dependendo '''
    return 45 <= contador < 55


def galeShapley(projetos, alunos):
    # Dicionários auxiliares
    projetoPraAlunos = {}       # Chave: str Px; Valor: [lista de alunos no projeto]
    alunoPraProjeto = {}        # Chave: str Ax; Valor: str Px
    fila = []                   # Fila de projetos que contenham vagas livres

    for projeto in projetos:
        # Preenche o dicionário auxiliar e a fila inicialmente com todos os projetos
        projetoPraAlunos[projeto] = []
        fila.append(projeto)

    for aluno in alunos:
        alunoPraProjeto[aluno] = None # Inicialmente nenhum aluno esta em nenhum projeto

    contadorAuxiliar = 0

    # Enquanto tem projetos com alunos candidatáveis
    while fila:
        projetoAtual = fila.pop(0)  # Retira o proximo projeto da fila

        # Itera por cada aluno candidato do projeto
        for aluno in projetos[projetoAtual][0]:
            strIteracao = ''  # String auxiliar
            # Se o aluno nao esta em nenhum projeto, adiciona ele ao projeto
            if alunoPraProjeto[aluno] == None:
                strIteracao = f'O aluno {aluno} foi adicionado ao projeto {projetoAtual}.'
                projetoPraAlunos[projetoAtual].append(aluno)
                alunoPraProjeto[aluno] = projetoAtual
            else:
                # Se o aluno ja esta em algum projeto, verifica se ele prefere o projeto atual
                projetoAluno = alunoPraProjeto[aluno]  # Projeto que o aluno ja esta
                
                strIteracao = (f'O aluno {aluno} preferiu continuar no projeto {projetoAluno}' +
                                f' do que mudar para o projeto {projetoAtual}.')
                
                # Se o aluno prefere o projeto atual, remove o aluno do projeto anterior
                # e adiciona no projeto atual
                if prefereProjAtual(alunos, aluno, projetoAtual, projetoAluno):
                    projetoPraAlunos[projetoAluno].remove(aluno)
                    projetoPraAlunos[projetoAtual].append(aluno)
                    alunoPraProjeto[aluno] = projetoAtual

                    strIteracao = (f'O aluno {aluno} preferiu trocar do projeto {projetoAluno} para' +
                                    f' o projeto {projetoAtual}.')
                    
                    # Como o projeto que o aluno estava anteriormente ficou com uma vaga
                    # sobrando, ele eh colocado de volta na fila, mas apenas se ele ja
                    # nao estiver nela
                    if not projetoAluno in fila:
                        fila.append(projetoAluno)

            # Impressao de iteracoes na tela
            contadorAuxiliar += 1
            if validaImpressao(contadorAuxiliar):
                print(f'Iteracao {contadorAuxiliar}: ' + strIteracao)
            
            # Se o projeto chegou ao limite maximo de vagas quebra o laco
            if len(projetoPraAlunos[projetoAtual]) == projetos[projetoAtual][1]:
                break

    return projetoPraAlunos


projetos, alunos = montaGrafo()
print("10 iteracoes:\n")
resultado = galeShapley(projetos, alunos)
print()
print("Resultado final do emparelhamento maximo:")
print()

# Numeros finais
qntIncompleto = 0
qntSemAlunos = 0

for projeto in resultado.items():
    if len(projeto[1]) == 0:
        print(f'O projeto {projeto[0]} nao tem nenhum aluno participante.')
    else:
        s = ', '.join(projeto[1])
        print(f'O projeto {projeto[0]} tem como participantes o(s) aluno(s) ' + s + '.')
    
    if len(projeto[1]) == 0:
        qntSemAlunos += 1
    elif projetos[projeto[0]][1] != len(projeto[1]):
        qntIncompleto += 1

print()
print("Valores finais:")
print()
print(f'{qntIncompleto} projetos nao tiveram todas as suas vagas preenchidas.')
print(f'{qntSemAlunos} projetos nao tiveram nenhum aluno inscrito.')
print(f'{30 - (qntIncompleto+qntSemAlunos)} projetos tiveram suas vagas completamente preenchidas.')