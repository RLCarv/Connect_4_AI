import pandas as pd
import numpy as np

import math
from collections import Counter

import random
random.seed(0)

# --- Treinar/testar split ---

#função de separação dos dados de treino e de teste
def train_test_split(df, test_size):
    if isinstance(test_size, float): #vê se o test_size é percentagem ou a qtd de linhas
        test_size = round(test_size * len(df))

    indices = df.index.tolist()
    test_indices = random.sample(population=indices, k=test_size)

    test_df = df.loc[test_indices] #acesso somente aos índices de test  
    train_df = df.drop(test_indices)
    
    return train_df, test_df

#leitura e separação dos dados
df = pd.read_csv("iris.csv")
train_df, test_df = train_test_split(df, test_size=0.3) #usa 30% como exemplo

#calcula a entropia de um dataset
def entropy(database):
    labels = database[:, -1] #obtem o nome dos atributos
    _, counts = np.unique(labels, return_counts=True) #numero de atributos
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
    #column_label = data[:,-1]
    atribute = [row[-1] for row in data]  
    return Counter(atribute).most_common(1)[0][0]

#cria a decision tree
def id3(data, attribute_indices, attribute_names):
    tipos = data[:, -1] #ultima coluna
    
    #caso todos os atributos forem iguais
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



# --- Training ID3 ---
train_dataset = train_df.values.tolist() #linhas de df
attributes = list(train_df.columns[:-1]) #nome dos atributos
attribute_indices = list(range(len(attributes))) #indices dos atributos
tree = id3(train_dataset, attribute_indices, attributes) #constroi a arvore

"""
df = pd.read_csv("iris.csv")
dataset = df.values.tolist()#linhas de df
attributes = list(df.columns[:-1])#nome dos atributos
attribute_indices = list(range(len(attributes)))#indices dos atributos
tree = id3(dataset, attribute_indices, attributes)#constroi a arvore

sample = { 'ID': 22, 'sepallength': 5.1, 'sepalwidth': 3.5, 'petallength': 1.4, 'petalwidth': 0.2}
print("Prediction:", classify(sample, tree))
"""

# --- Evaluation ---

#avalia com dados de teste
test_data = test_df.values.tolist()
correct = 0

for row in test_data:
    sample = dict(zip(attributes, row[:-1]))
    prediction = classify(sample, tree)
    if prediction == row[-1]:
        correct += 1

accuracy = correct / len(test_data)
print(f"Acurácia no dataset Iris: {accuracy:.2f}")