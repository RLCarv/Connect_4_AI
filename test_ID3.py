import pandas as pd
import numpy as np

from ID3 import train_test_split, id3, classify
from ai_mcts import MCTS
from game_logic import game

# --- Gerar dataset ---
def gen_dataset(n_games: int, iterations: int = 500, c: float = 2.0) -> pd.DataFrame:
    records = [] #armazena um dict para cada estado jogado durante todas as partidas
     
    for g in range(n_games):
        env = game() 
        agents = {'X': MCTS(c, iterations), 'O': MCTS(c, iterations)}
        history = []  # lista de tuples (visits, player)
        #visits é um vector com 7 inteiros com n de visitas para cada coluna no estado

        #jogo até o fim
        while not env.gameOver():
            piece = env.player()
            agent = agents[piece]
            # Executa MCTS: a raiz é armazenada em agent.root
            best_col = agent.getMove(env, statistics=False)  # retorna coluna escolhida
            root = agent.root  # nó raiz com estatísticas de visitas

            #extrai número de visitas por coluna
            visits = [0] * 7
            for move, child in zip(root.children_move, root.children):
                visits[move] = child.visits
            history.append((visits, piece))

            # joga a coluna mais visitada
            env.playOneTurn(best_col, piece)
            env.turn += 1

        # resultado final
        winner = env.gameWinner  # 'X', 'O' ou 'Tie'
        for visits, piece in history:
            if winner == 'Tie':
                label = 'draw'
            elif piece == winner:
                label = 'win'
            else:
                label = 'loss'
            row = {f"visits_{i}": visits[i] for i in range(7)}
            row['result'] = label
            records.append(row)

        print(f"[{g+1}/{n_games}] Winner: {winner}")

    df = pd.DataFrame(records)
    df.to_csv('connect4_mcts_dataset.csv', index=False)
    print(f"Dataset salvo em 'connect4_mcts_dataset.csv' com {len(df)} linhas.")
    return df    

def main():
    print("Gerando dataset ia vs ia...")
    df = gen_dataset(n_games=100, iterations=500, c=2.0)

    # --- Treinar/testar separação ---
    train_df, test_df = train_test_split(df, test_size=0.4) #usa 40% como exemplo
    attributes = list(train_df.columns[:-1]) #nome dos atributos
    train_np = train_df.values #linhas de df
    attribute_indices = list(range(len(attributes))) #indices dos atributos
  
    # --- Treinar ID3 ---
    tree = id3(data = train_np, attribute_indices=attribute_indices,attribute_names=attributes,
            min_sample=5, max_depth=6, counter=0) 

    # --- Evaluation ---
    correct = 0
    #avalia com dados de teste
    for row in test_df.values:
        sample = dict(zip(attributes, row[:-1]))
        prediction = classify(sample, tree)
        if prediction == row[-1]:
            correct += 1

    accuracy = correct / len(test_df)
    print(f"Acurácia no dataset connect-4: {accuracy:.2f}")


if __name__ == "__main__":
    main()

