import pandas as pd
import numpy as np

import math
from collections import Counter

import random
random.seed(0)

# --- Treinar/testar split ---

#função de separação dos dados de treino e de teste:
def train_test_split(df, test_size):
    if isinstance(test_size, float): #vê se o test_size é percentagem ou a qtd de linhas
        test_size = round(test_size * len(df))

    indices = df.index.tolist()
    test_indices = random.sample(population=indices, k=test_size)

    test_df = df.loc[test_indices] #acesso somente aos índices de test  
    train_df = df.drop(test_indices)
    
    return train_df, test_df

#leitura e separação dos dados:
df = pd.read_csv("iris.csv")
train_df, test_df = train_test_split(df, test_size=0.3) #usa 30% como exemplo

#Se coluna for numinal:
def is_categorical_col(col, max_unique=10):
    if col.dtype.kind in {"U", "S", "O"}:
        return True
    return np.unique(col).size <= max_unique

#calcula a entropia de um dataset
def entropy(database):
    labels = database[:, -1] #obtem o nome dos atributos
    _, counts = np.unique(labels, return_counts=True) #numero de atributos
    probs = counts / counts.sum()
    return -np.sum(probs * np.log2(probs + 1e-9))

#calculaa information gain dado uma lista de subconjuntos:
def information_gain(parent, children):
    total_parent = entropy(parent)
    weighted_entropy = sum(len(c)/len(parent) * entropy(c) for c in children)
    return total_parent - weighted_entropy

#retorna o melhor theshold para um dado atribuuto
def best_split(database,index):
    sorted = database[database[:,index].argsort()]#organiza os dados
    values = sorted[:,index].astype(float)
    types = sorted[:,-1]
    bestgain = -1
    bestthresh = None
    totalentropy = entropy(database)
    for i in range(1, len(values)):
        if types[i] != types[i-1]:
            thresh = (values[i] + values[i - 1]) / 2
            left = database[database[:, index].astype(float) <= thresh]
            right = database[database[:, index].astype(float) > thresh]
            if len(left) == 0 or len(right) == 0:
                continue
            gain = totalentropy
            gain -= (len(left) / len(database)) * entropy(left)
            gain -= (len(right) / len(database)) * entropy(right)
            if gain > bestgain:
                bestgain = gain
                bestthresh = thresh
    return bestgain, bestthresh

#encontra o atributo com maior information gain:
def best_attribute(database, attribute_indices):
    parent_entropy = entropy(database) #calcula entropia do conjunto completo de classes do nó pai,ou seja, valor de partida
    bestgain = -1
    best_attribute  = None #indice do attr 
    best_thresh = None #caso contínuo
    best_cat = False #flag do cat

    for i in attribute_indices: #loop para encontrar o que gera maior redução de incerteza
        col = database[:,i] #valores do atributo avaliado

        #---categórico(multi-ramo)---
        if is_categorical_col(col):
            values = np.unique(col) #todos possíveis
            subsets = [database[col == v] for v in values] #subconjunto para cada valor
            gain = information_gain(subsets, parent_entropy, len(database))
            if gain > bestgain:
                bestgain = gain
                best_attribute  = i
                best_thresh = None
                best_cat = True
            continue

        #---contínuo(binário)---
        gain, thresh = best_split(database, i)

        left  = database[database[:, idx].astype(float) <= thresh]
        right = database[database[:, idx].astype(float) >  thresh]

        gain = information_gain(database, [left, right])

        if gain > bestgain:
            bestgain = gain
            best_attribute = i
            best_thresh = thresh
            best_cat = False 

    return best_attribute, best_thresh, best_cat

#descobre atributo mais frequente 
def majority_atribute(data):
    attributes = data[:,-1]
    return Counter(attributes).most_common(1)[0][0]

#cria a decision tree
def id3(data, attribute_indices, attribute_names):
    # ---base case
    
    types = data[:, -1] #ultima coluna
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
            tree[f"{attribute_names[best]} ="][str(v)] = id3(subset, new_idx, attribute_names)
        return tree
    
    #---split contínuo(binário)---
    thresh = p
    if thresh is None: #flag se não encontrar
        return majority_atribute(data)

    #cria a arvore
    left = data[data[:, best].astype(float) <= thresh]
    right = data[data[:, best].astype(float) > thresh]

    subtree_left  = id3(left,  attribute_indices, attribute_names)
    subtree_right = id3(right, attribute_indices, attribute_names)
    
    node_name = f"{attribute_names[best]} <= {thresh:.2f}"
    tree = {node_name: {"yes": subtree_left, "no": subtree_right}}
    return tree
 

def majority_branches(branches):
    types = []
    for s in branches.values():
        if isinstance(s, str):
            types.append(s)
        else:
            types.append(majority_branches(s))
    return Counter(types).most_common(1)[0][0]

#dado um novo exemplo, classica-o
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
        #devolve classe majoritária nos ramos do nó de um valor nunca visto
        return majority_branches(branch)
    
    #---contínuo(binário)---
    # separar o nome e o threshold
    attr_name, condition = node.split(" <= ")
    threshold = float(condition)
    # valor real do exemplo para esse atributo
    value = float(example[attr_name])
    branch = "yes" if value <= threshold else "no"
    return classify(example, tree[node][branch])

# --- Training ID3 ---
train_np = train_df.values #linhas de df
attributes = list(train_df.columns[:-1]) #nome dos atributos
attribute_indices = list(range(len(attributes))) #indices dos atributos
tree = id3(train_np, attribute_indices, attributes) #constroi a arvore

# --- Evaluation ---
correct = 0
#avalia com dados de teste
test_data = test_df.values

for row in test_data:
    sample = dict(zip(attributes, row[:-1]))
    prediction = classify(sample, tree)
    if prediction == row[-1]:
        correct += 1

accuracy = correct / len(test_data)
print(f"Acurácia no dataset Iris: {accuracy:.2f}")
