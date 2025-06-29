from proj_alum import alunos, projetos
from collections import defaultdict #Para manipular dicionarios de forma mais tranquila
import networkx as nx #Para fazer os grafos
import matplotlib.pyplot as plt #Para visualização

"""Aqui usaremos o Gale-Shapley decidimos organizar como o exemplo do casamento entre homens e mulheres. Os alunos são os homens que pedem as mãos das mulheres, e as mulheres são os projetos que aceitam os homens (projetos)."""

def gale_shapley(alunos, projetos):
    participantes_projeto = defaultdict(list) # Aqui é onde guardamos a relação Projeto - alunos, quais alunos participarão de cada projeto
    capacidade_restante = projetos.copy()
    alunos_livres = list(alunos.keys())
    propostas_feitas = {aluno: 0 for aluno in alunos}

    while alunos_livres:
        aluno = alunos_livres.pop(0)
        preferencias_proj = alunos[aluno][:-1]
        nota_aluno = alunos[aluno][-1]
        
        #Aqui verificamos se ainda existem projetos na lista de preferencias
        if propostas_feitas[aluno] >= len(preferencias_proj):
            continue

        projeto = preferencias_proj[propostas_feitas[aluno]]
        propostas_feitas[aluno] += 1
        
        #Se o projeto não existir no dicionario de projetos 
        if projeto not in projetos:
            alunos_livres.append(aluno)
            continue

        capacidade, nota_minima = projetos[projeto]

        #Se a nota do aluno for insulficiente ele fica livre outra vez
        if nota_aluno < nota_minima:
            alunos_livres.append(aluno)
            continue

        alunos_alocados = participantes_projeto[projeto]

        if len(alunos_alocados) < capacidade:
            #Se ainda houverem vagas o aluno é adicionado ao projeto
            participantes_projeto[projeto].append(aluno)
        else:
            #Se nao vamos ver quem e o aluno com a pior nota
            notas_alunos_alocados = [(a, alunos[a][-1]) for a in alunos_alocados]
            pior_aluno, pior_nota = min(notas_alunos_alocados, key=lambda x: x[1])

            if nota_aluno > pior_nota:
                #Se o aluno tiver nota maior que o pior aluno então ele assume o lugar
                participantes_projeto[projeto].remove(pior_aluno)
                participantes_projeto[projeto].append(aluno)
                alunos_livres.append(pior_aluno)
            else:
                #Se nao ele é rejeitado
                alunos_livres.append(aluno) 



    return participantes_projeto



def apresentacao():
    """Aqui nesta função estamos apresentando os pares tanto no terminal quanto na criação do grafo"""
    resultado = gale_shapley(alunos, projetos)
    G = nx.DiGraph()
    projetos_cor = set()
    alunos_cor = set()

    print("PARES ESTÁVEIS:")
    for projeto, alunnos in resultado.items():
        print(f"{projeto} - {alunnos}")
        projetos_cor.add(projeto)
        for aluno in alunnos:
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

    return G

apresentacao()
