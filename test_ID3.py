import pandas as pd
import numpy as np

from ID3 import train_test_split, id3, classify

# --- Treinar/testar split ---

#função de separação dos dados de treino e de teste:

def main():
    df = pd.read_csv("iris.csv")

    
    # --- Treinar/testar split ---
    train_df, test_df = train_test_split(df, test_size=0.4) #usa 30% como exemplo


    # --- Training ID3 ---
    train_np = train_df.values #linhas de df
    attributes = list(train_df.columns[:-1]) #nome dos atributos
    attribute_indices = list(range(len(attributes))) #indices dos atributos
    min_sample = 6
    max_depth  = 8
    tree = id3(train_np, attribute_indices, attributes,
            min_sample, max_depth, counter=0) #constroi a arvore

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

if __name__ == "__main__":
    main()