
import math
from collections import Counter
import pandas as pd
import numpy as np


#calcula a entropia de um dataset
def entropy(database):
    labels = database[:, -1]
    _, counts = np.unique(labels, return_counts=True)
    probs = counts / counts.sum()
    return -np.sum(probs * np.log2(probs + 1e-9))

#calcula a information gain de cada atributo
def information_gain(database, atribute_index):
    total_entropy = entropy(database)
    values = set(row[atribute_index] for row in database)
    weighted_entropy = 0.0

    for value in values:
        subset = [row for row in database if row[atribute_index] == value]
        weighted_entropy += (len(subset) / len(database)) * entropy(subset)

    return total_entropy - weighted_entropy

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


#encontra o atributo com maior information gain
def best_attribute(database, attribute_indices):
    bestgain = -1

    for i in attribute_indices:
        gain, thresh = best_split(database, i)
        if gain > bestgain:
            bestgain = gain
            best_attribute = i
            bestthresh = thresh
    return best_attribute, bestthresh

#descobre atributo mais frequente
def majority_atribute(data):
    atribute = [row[-1] for row in data]
    return Counter(atribute).most_common(1)[0][0]

#cria a decision tree
def id3(data, attribute_indices, attribute_names):
    tipos = data[:, -1] #ultima coluna
    
    #caso todos os tipos forem iguais
    if np.all(tipos == tipos[0]):
        return tipos[0]
    
    #se não houver mais atributos para fazer split
    if not attribute_indices:
        return majority_atribute(data)

    best , thresh = best_attribute(data, attribute_indices) #melhor atributo para fazer split e o threshold desse split
    if thresh is None:
        return majority_atribute(data)
    #cria a arvore
    tree = {f"{attribute_names[best]} <= {thresh:.2f}": {}}
    left = data[data[:, best].astype(float) <= thresh]
    right = data[data[:, best].astype(float) > thresh]
    subtree_left = id3(left, attribute_indices, attribute_names)
    subtree_right = id3(right, attribute_indices, attribute_names)
    
    tree[f"{attribute_names[best]} <= {thresh:.2f}"]["yes"] = subtree_left
    tree[f"{attribute_names[best]} <= {thresh:.2f}"]["no"] = subtree_right
    return tree


#dado um novo exemplo, classica-o
def classify(example, tree):
    if isinstance(tree, str):
        return tree  # caso base: folha da árvore
    # pega no atributo de decisão neste nível
    node = next(iter(tree))  
    # separar o nome e o threshold
    attr_name, condition = node.split(" <= ")
    threshold = float(condition)
    # valor real do exemplo para esse atributo
    value = float(example[attr_name])
    branch = "yes" if value <= threshold else "no"
    return classify(example, tree[node][branch])




df = pd.read_csv("Connect_4_AI/iris.csv")
df = df.drop(columns=["ID"])
dataset = df.values#linhas de df
attributes = list(df.columns[:-1])#nome dos atributos
attribute_indices = list(range(len(attributes)))#indices dos atributos
tree = id3(dataset, attribute_indices, attributes)#constroi a arvore

sample = { 'ID': 5, 'sepallength': 7.0, 'sepalwidth': 3.2, 'petallength': 4.7, 'petalwidth': 1.4}
print("Prediction:", classify(sample, tree))

