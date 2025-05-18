import pandas as pd
import random

from ID3 import id3, classify
from ai_mcts import MCTS
from game_logic import game

# --- Gerar dataset ---
#converte o board do jogo(array 2D) em uma lista de 42 caracteres ordenados de a - f
def board_to_row(board):
    row = []
    for r in range(6):
        for c in range(7):
            cell = board[r][c]
            if cell == 'X':
                row.append('x')
            elif cell == 'O':
                row.append('o')
            else:
                row.append('b')
    return row      

#cada linha é um estado do self-play MCTS vs MCTS
def gen_dataset(n_games: int, iterations: int = 500, c: float = 2.0) -> pd.DataFrame:
    records = [] #armazena um dict para cada estado jogado durante todas as partidas
    for game_id in range(n_games):
        env = game() 
        agents = {'X': MCTS(c, iterations), 'O': MCTS(c, iterations)}
        
        #histórico do board
        history = [] 
        while not env.gameOver():
            #snapshot (estado antes da jogada)
            row = board_to_row(env.board)
            piece = env.player()  # 'X' ou 'O'
            history.append((row,piece)) 
            
            # joga a coluna mais visitada
            best_col = agents[piece].getMove(env, statistics=False) #executa o MCTS
            env.playOneTurn(best_col, piece)
            env.turn += 1

        #determina resultado da partida
        winner = env.gameWinner  # 'X', 'O' ou 'Tie'
        #rotula cada snapshot com o resultado final e game_id
        for row, piece in history:
            if winner == 'Tie':
                label = 'draw'
            elif piece == winner: 
                label = 'win'
            else:
                label = 'loss'
        #inclui game_id para split por partida
            records.append(row + [label, game_id])

        print(f"[{game_id+1}/{n_games}] Winner: {winner}")

    #define os nomes da colunas: a1...a7,b1...b7,c1...c7,f1...f7 e o result
    cols = [f"{letter}{num}" for letter in ['a','b','c','d','e','f'] for num in range(1,8)]
    cols += ['result', 'game_id']

    df = pd.DataFrame(records, columns=cols)
    df.to_csv('connect4_dataset.csv', index=False)
    print(f"Dataset salvo em 'connect4_dataset.csv' com {len(df)} linhas.")
    return df    

def main():
    try:
        df = pd.read_csv('connect4_dataset2.csv')
    except FileNotFoundError:
        df = gen_dataset(n_games=100, iterations=500, c=2.0)

    # --- Treinar/testar separação ---
    #obtém todos os IDs de jogo e embaralha a lista
    game_ids = df['game_id'].unique().tolist()
    
    #define quantos jogos vão para o teste (40%)
    n_test   = round(0.4 * len(game_ids))

    #particona
    test_games  = random.sample(game_ids, k=n_test)
    train_games = [g for g in game_ids if g not in test_games]

    #faz o filtro
    train_df = df[df['game_id'].isin(train_games)]
    test_df  = df[df['game_id'].isin(test_games)]

     # --- Treinar ID3 ---
    #atributos sem 'result' e 'game_id'
    attributes = [c for c in train_df.columns if c not in ('result','game_id')]

    #transforma train_df num array para o ID3
    train_sub = train_df[attributes + ['result']]
    train_np  = train_sub.values
    attribute_indices = list(range(len(attributes)))

   
    tree = id3(data = train_np, attribute_indices=attribute_indices,attribute_names=attributes,
            min_sample=10, max_depth=6, counter=0) 

    # --- Avaliação ---
    correct = 0
    eval_cols = attributes + ['result']
    #avalia com dados de teste
    for row in test_df[eval_cols].values:
        sample = dict(zip(attributes, row[:-1]))
        prediction = classify(sample, tree)
        if prediction == row[-1]:
            correct += 1

    accuracy = correct / len(test_df)
    print(f"Acurácia no dataset connect-4: {accuracy:.2f}")


if __name__ == "__main__":
    main()

