from game_logic import *

NEW_GAME = True

def playerMove(piece): #movimento do jogador
    print(f"Next to play: {piece}")
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
    newGame = game() #gera um novo jogo
    newGame.gameWinner = EMPTY #reseta o vencedor
    newGame.turn = 0 #reseta o turno 0

    while newGame.gameWinner == EMPTY: #game loop
        #controla de quem é a vez
        if newGame.turn % 2 == 0:
            newGame.playerTurn = PLAYER_1_PIECE
        else:
            newGame.playerTurn = PLAYER_2_PIECE

        print(f"\nTurn: {newGame.turn}")
        newGame.drawBoard()
        playerMove(newGame.playerTurn)

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