from game_logic import *

NEW_GAME = True

while NEW_GAME:
    newGame = game() #gera um novo jogo
    newGame.drawBoard() #desenha a board inicial
    NEW_GAME = False