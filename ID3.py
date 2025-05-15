import pandas as pd
import numpy as np
import random
random.seed(0)

from collections import Counter

#calcula a entropia de um dataset
def entropy(database):
    labels = database[:, -1] #obtem o nome dos atributos
    _, counts = np.unique(labels, return_counts=True) #numero de atributos
    probs = counts / counts.sum()
    return -np.sum(probs * np.log2(probs + 1e-9))

#se coluna for numinal:
def is_categorical_col(col, max_unique=10):
    if col.dtype.kind in {"U", "S", "O"}:
        return True
    return np.unique(col).size <= max_unique

#calculaa information gain de um split qualquer
def information_gain(parent, children):
    n_parent = len(parent) #calculada só uma vez
   
    #ganha nada num nó vazio
    if n_parent == 0:
        return 0.0
    
    total_parent = entropy(parent) #entropia do pai,ou seja, valor de partida
    

    weighted_entropy = 0.0
    for c in children:
        n_children = len(c)
        if n_children == 0:
            continue #evita log(0) ou div por zero
        weighted_entropy += (n_children/n_parent) * entropy(c) 
        
    return total_parent - weighted_entropy

#retorna o melhor theshold para um dado atribuuto
def best_split(database,index):
    #organiza os dados pelo valor do atributo index
    sorted = database[database[:,index].argsort()]
    values = sorted[:,index].astype(float)
    types = sorted[:,-1] #classes correspondentes na mesma ordem

    bestgain = -1
    bestthresh = None
    totalentropy = entropy(database)
    for i in range(1, len(values)):
        if types[i] != types[i-1]: #se na esqueda temos uma classe e a direita outra vale tentar um corte
            thresh = (values[i] + values[i - 1]) / 2 #para cada par calcula-se o ponto médio
            #avalia cada candidato e escolhe o melhor
            left = database[database[:, index].astype(float) <= thresh]
            right = database[database[:, index].astype(float) > thresh] 
            if len(left) == 0 or len(right) == 0:
                continue

            gain = totalentropy
            gain -= (len(left) / len(database)) * entropy(left)
            gain -= (len(right) / len(database)) * entropy(right)
            if gain > bestgain: #escolhe o threshold com melhor ganho
                bestgain = gain
                bestthresh = thresh
    
    return bestgain, bestthresh

#encontra o atributo com maior information gain:
def best_attribute(database, attribute_indices):
    bestgain = -1
    best_attribute  = None #indice do attr 
    best_thresh = None #caso contínuo
    best_cat = False #flag do cat

    for i in attribute_indices: #loop para encontrar o que gera maior redução de incerteza
        col = database[:,i] #valores do atributo avaliado

        #se categórico faz um split multi-ramo(um ramo por valor)
        if is_categorical_col(col):
            values = np.unique(col) #todos possíveis
            subsets = [database[col == v] for v in values] #subconjunto para cada valor
            gain = information_gain(database, subsets) 
            if gain > bestgain:
                bestgain = gain
                best_attribute  = i
                best_thresh = None
                best_cat = True
            continue

        #se contínuo faz por binário(usando best_split)
        gain_num, thresh = best_split(database, i)
        if gain_num > bestgain:
            bestgain = gain_num
            best_attribute = i
            best_thresh = thresh
            best_cat = False 

    return best_attribute, best_thresh, best_cat

#descobre atributo mais frequente (mecanismo de fallback em id3)
def majority_atribute(data):
    attributes = data[:,-1]
    return Counter(attributes).most_common(1)[0][0]

#cria a decision tree
def id3(data, attribute_indices, attribute_names, min_sample, max_depth, counter):
    
    # ---base case
    types = data[:, -1] #ultima coluna
    
    #pre-prunning
    if (len(data) < min_sample) or (counter == max_depth):
        return majority_atribute(data)
    
    #caso todos os atributos forem iguais
    if np.all(types == types[0]):
        return types[0]
    
    #se não houver mais atributos para fazer split
    if not attribute_indices:
        return majority_atribute(data)
    
    best, p, is_cat = best_attribute(data, attribute_indices)
    
    #---split categórico---
    if is_cat:
        tree = {f"{attribute_names[best]} =": {}}
        col = data[:,best]  
        values = np.unique(col)

        for v in values: #cria um ramo para cada valor
            subset = data[col == v]
            new_idx = [i for i in attribute_indices if i != best]  #remove atributo usado
            tree[f"{attribute_names[best]} ="][str(v)] = id3(subset, new_idx, attribute_names,
                                                            min_sample, max_depth, counter+1)
        return tree
    
    #---split contínuo(binário)---
    thresh = p
    if thresh is None: #flag se não encontrar
        return majority_atribute(data)

    #cria a arvore
    left = data[data[:, best].astype(float) <= thresh]
    right = data[data[:, best].astype(float) > thresh]

    subtree_left = id3(left, attribute_indices, attribute_names,min_sample, max_depth, counter+1)
    subtree_right = id3(right, attribute_indices, attribute_names,min_sample, max_depth, counter+1)
    
    node_name = f"{attribute_names[best]} <= {thresh:.2f}"
    tree = {node_name: {"yes": subtree_left, "no": subtree_right}}
    return tree
 
#conta classes nas folhas de multi-ramos(mecanismo de fallback em classify)
def majority_branches(branches): #entrada de um dict de ramos de um nó categórico
    types = []
    for s in branches.values():
        if isinstance(s, str): #se for folha adiciona diretamente a lista
            types.append(s)
        else:
            types.append(majority_branches(s)) #se for subarvore faz recusividade a escolher folha no ramo
    return Counter(types).most_common(1)[0][0] # o que aparece mais vezes entre os rótulos é escolhido

#dado um novo exemplo, classica-o se é é categórico ou contínuo
def classify(example, tree):
    if isinstance(tree, str):
        return tree  # caso base: folha da árvore
    
    # pega no atributo de decisão neste nível
    node = next(iter(tree))  

    #---categórico(multi-ramo)---
    if node.endswith(" ="):
        attr = node[:-2].strip() #remove o " ="
        branch = tree[node]
        val = str(example[attr])

        if val in branch:
            return classify(example, branch[val])
        #devolve classe majoritária nos ramos do nó de um valor se não existir
        return majority_branches(branch)
    
    #---contínuo(binário)---
    # separar o nome e o threshold
    attr_name, condition = node.split(" <= ")
    threshold = float(condition)
    # valor real do exemplo para esse atributo
    value = float(example[attr_name])
    branch = "yes" if value <= threshold else "no"
    return classify(example, tree[node][branch])

# treinar/testar split
def train_test_split(df, test_size):
    if isinstance(test_size, float): #vê se o test_size é percentagem ou a qtd de linhas
        test_size = round(test_size * len(df))

    indices = df.index.tolist()
    test_indices = random.sample(population=indices, k=test_size)

    test_df = df.loc[test_indices] #acesso somente aos índices de test  
    train_df = df.drop(test_indices)
        
    return train_df, test_df

