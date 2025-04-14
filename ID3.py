import math
from collections import Counter
import pandas as pd


#calcula a entropia de um dataset
def entropy(database):
    atribute = [row[-1] for row in database] #obtem o nome de atributos
    atribute_counts = Counter(atribute) #numero de atributos
    total = len(database)#numero de linhas
    ent = 0.0
    # calcula a entropia usandoa formula
    for count in atribute_counts.values():
        prob = count / total
        ent -= prob * math.log2(prob)
    return ent

#calcula a information gain de cada atributo
def information_gain(database, atribute_index):
    total_entropy = entropy(database)
    values = set(row[atribute_index] for row in database)
    weighted_entropy = 0.0

    for value in values:
        subset = [row for row in database if row[atribute_index] == value]
        weighted_entropy += (len(subset) / len(database)) * entropy(subset)

    return total_entropy - weighted_entropy

#encontra o atributo com maior information gain
def best_attribute(database, attribute_indices):
    gains = [(i, information_gain(database, i)) for i in attribute_indices]
    return max(gains, key=lambda x: x[1])[0]

#descobre atributo mais frequente
def majority_atribute(data):
    atribute = [row[-1] for row in data]
    return Counter(atribute).most_common(1)[0][0]

#cria a decision tree
def id3(data, attribute_indices, attribute_names):
    atribute = [row[-1] for row in data]
    
    #caso todos os atributos forem iguais
    if atribute.count(atribute[0]) == len(atribute):
        return atribute[0]
    
    #se não houver mais atributos para fazer split
    if not attribute_indices:
        return majority_atribute(data)

    best = best_attribute(data, attribute_indices) #melhor atributo para fazer split
    tree = {attribute_names[best]: {}}
    values = set(row[best] for row in data) #todos os valores do melhor atributo
    
    #ciclo que cria a arvore em si
    for value in values:
        subset = [row[:best] + row[best+1:] for row in data if row[best] == value]
        sub_attr_names = attribute_names[:best] + attribute_names[best+1:]
        sub_attr_indices = [i for i in range(len(sub_attr_names))]

        subtree = id3(subset, sub_attr_indices, sub_attr_names)
        tree[attribute_names[best]][value] = subtree

    return tree

#dado um novo exemplo, classica-o
def classify(example, tree):
    if isinstance(tree, str):
        return tree

    attribute = next(iter(tree))
    value = example.get(attribute)

    if value in tree[attribute]:
        return classify(example, tree[attribute][value])
    else:
        return "Unknown"




df = pd.read_csv("Connect_4_AI/iris.csv")
dataset = df.values.tolist()#linhas de df
attributes = list(df.columns[:-1])#nome dos atributos
attribute_indices = list(range(len(attributes)))#indices dos atributos
tree = id3(dataset, attribute_indices, attributes)#constroi a arvore

sample = { 'ID': 22, 'sepallength': 5.1, 'sepalwidth': 3.5, 'petallength': 1.4, 'petalwidth': 0.2}
print("Prediction:", classify(sample, tree))

