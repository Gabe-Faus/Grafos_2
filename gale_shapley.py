from proj_alum import alunos, projetos, participantes_projeto
from collections import defaultdict #Para manipular dicionarios de forma mais tranquila
import networkx as nx #Para fazer os grafos
import matplotlib.pyplot as plt #Para visualização

"""Aqui usaremos o Gale-Shapley eu decidi usar como se os alunos fossem os homens que pedem as mãos das mulheres, e elas serem os projetos pq faz mais sentindo na lógica que alunos podem escolher mais de um projeto. Esse algoritmo é uma base, eh preciso que sejam selecionados o sprojeto e ver se a nota dos alunos é sulficiente e se ha vagas. Mas esse algoritmo faz uma seleção. Poemos construir o resto a partir dele."""

def asignacao(alunos, projetos, participantes_projeto):
    alunos_livres = list(alunos.keys())
    cont = 0
    grafos = []

    for aluno in alunos_livres:
        preferencias = alunos[aluno][:-1]  
        nota = alunos[aluno][-1]          

        for projeto in preferencias:
            cont += 1
            #Aqui estamos settando o ultimo aluno que foi adicionado a lista e a sua nota
            try:
                ultimo_aluno = participantes_projeto[projeto][-1]
                nota_ultimo = alunos[ultimo_aluno][-1]
            except (KeyError, IndexError):
                ultimo_aluno = None
                nota_ultimo = None

            if projeto not in projetos:
                continue
            else:
                capacidade, nota_minima = projetos[projeto]

            if cont == 49:
                grafos.append(dict(participantes_projeto))
                cont = 0

            if capacidade > 0 and nota >= nota_minima:
                participantes_projeto[projeto].append(aluno)
                projetos[projeto] = (capacidade - 1, nota_minima)
                break
                
            if capacidade <= 0 and nota >= nota_ultimo:
                participantes_projeto[projeto].pop()
                participantes_projeto[projeto].append(aluno)
                break
        

    return participantes_projeto, grafos


resultado = asignacao(alunos, projetos, participantes_projeto)


cont_it = 0
for estados in resultado[1]:
    cont_it +=1
    print(f"ITERAÇÃO {cont_it}")
    for  projeto, alunos in estados.items():
        print(f"{projeto} - {alunos}")
    print()

G = nx.DiGraph()
projetos_cor = set()
alunos_cor = set()

print("PARES FINAIS:")
for projeto, alunos in resultado[0].items():
    print(f"{projeto} - {alunos}")
    projetos_cor.add(projeto)
    for aluno in alunos:
        alunos_cor.add(aluno)
        G.add_edge(projeto, aluno)

pos = nx.spring_layout(G)

node_colors = []
for node in G.nodes():
    if node in projetos_cor:
        node_colors.append('grey')  
    else:
        node_colors.append('skyblue')     

nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=1000, font_size=10) 
plt.show()

    
