from proj_alum import alunos, projetos, participantes_projeto
from collections import defaultdict #Para manipular dicionarios de forma mais tranquila
"""Aqui usaremos o Gale-Shapley eu decidi usar como se os alunos fossem os homens que pedem as mãos das mulheres, e elas serem os projetos pq faz mais sentindo na lógica que alunos podem escolher mais de um projeto. Esse algoritmo é uma base, eh preciso que sejam selecionados o sprojeto e ver se a nota dos alunos é sulficiente e se ha vagas. Mas esse algoritmo faz uma seleção. Poemos construir o resto a partir dele."""

def asignacao(alunos, projetos, participantes_projeto):
    alunos_livres = list(alunos.keys())

    for aluno in alunos_livres:
        preferencias = alunos[aluno][:-1]  
        nota = alunos[aluno][-1]          

        for projeto in preferencias:
            if projeto not in projetos:
                continue
            else:
                capacidade, nota_minima = projetos[projeto]

            if capacidade > 0 and nota >= nota_minima:
                participantes_projeto[projeto].append(aluno)
                projetos[projeto] = (capacidade - 1, nota_minima)
                
                break  

    print(participantes_projeto, len(participantes_projeto))
    return participantes_projeto


resultado = asignacao(alunos, projetos, participantes_projeto)
print("Pares estáveis:")
for aluno, projeto in resultado.items():
    print(f"{aluno} - {projeto}")