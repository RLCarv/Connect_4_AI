from game_logic import *
from ai_random import *
from ai_mcts import *

NEW_GAME = True

def playerMove(piece): # movimento do jogador
    print(f"Next to play: Player as {piece}")
    try:  # error handling
        col = int(
            input("Choose in which col do you wanna play or press 9 to quit: ")
        )
    except:
        col = -1

    while not newGame.verifyCol(col):
        if col == 9:
            quit()  # opção para quitar
        try:  # error handling
            col = int(
                input(
                    "The col you selected is either full or invalid, choose another one or press 9 to quit: "
                )
            )
        except:
            col = -1
    newGame.playOneTurn(col,piece)


def aiMove(piece): # movimento da AI
    print(f"Next to play: {aiName} as {piece}")

    if aiName == "Monte Carlo":
        print("Thinking...")
        col = ai.getMove(newGame)

    else: 
        col = ai.getMove(newGame)
    
    print(f"{aiName} played in col: {col}")
    newGame.playOneTurn(col,piece)

def gameMode(): # seleciona o modo de jogo e inicializa a AI
    start = -1 # error handling
    while start not in range(3):
        try:  
            start = int(input("\nChoose the Game Mode\n0 => Player vs Player\n1 => AI Random\n2 => Monte Carlo\n: "))
        except:
            continue
    match start:
        case 0:
            ai = None
            aiName = None
        case 1:
            ai = ai_random()
            aiName = "Random"
        case 2:
            ai = MCTS()
            aiName = "Monte Carlo"
    return ai,aiName

def PlayOrder(): #decide quem vai primeiro
    try:  # error handling
        first = int(input("\nChoose 0 to go first or 1 to go second: "))
    except:
        first = -1
    if first not in range(2):
        PlayOrder()
    return first

def requestNewGame():
    bol = -1
    while bol < 0 or bol > 1:
        try:  # error handling
            bol = int(input("\nType 0 to quit or 1 to play again: "))
        except:
            bol = -1
    return (bol == 1) # retorna True se houver novo jogo


# GAME LOOP
while NEW_GAME:
    print("\nNew Game")
    newGame = game() # gera um novo objeto jogo
    
    start = gameMode() # seleciona o modo de jogo
    ai = start[0] # inicializa a AI
    aiName = start[1]

    if aiName != None:
        order = PlayOrder() # seleciona se começa ou não    
    else: 
        order = -1 # pvp não tem quem começa

    while newGame.gameWinner == EMPTY: #game loop
        print(f"\nTurn: {newGame.turn}")
        newGame.drawBoard()
        

        if order == -1: # controla de quem é a vez e faz o movimento
                playerMove(newGame.player())
        elif order == 0: # player joga primeiro
            if newGame.turn % 2 == 0:
                playerMove(newGame.player())
            else:
                aiMove(newGame.player())
        else: # player joga segundo
            if newGame.turn % 2 == 0:
                aiMove(newGame.player())
            else:
                playerMove(newGame.player())


        if newGame.gameOver(): # caso o jogo acabe
            if newGame.gameWinner == "Tie": # empate
                newGame.drawBoard()
                print(f"\nIt's a Tie!")
            else: # vitória
                newGame.drawBoard()
                print(f"\n{newGame.gameWinner} Won!")    
            NEW_GAME = requestNewGame() # define se haverá outro jogo

        else: # o jogo não acabou
            newGame.turn += 1 # próximo turno