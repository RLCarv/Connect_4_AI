import numpy as np
NUM_ROW = 6
NUM_COL = 7
EMPTY = "-"
PLAYER_1_PIECE = "X"
PLAYER_2_PIECE = "O"

class game:
    def __init__(self):
        #variaveis iniciais
        self.first = PLAYER_1_PIECE #quem começa
        self.turn = 0 #contador do turno
        self.game_winner = EMPTY #variavel que controla quem ganhou
        self.board_is_full = False #retorna se a board esta cheia
        pass
        
    """desenha a board"""
    def drawBoard(self):
        pass

    """joga um turno"""
    def playOneTurn(self): #joga um turno
        pass

    """coloca a peça na board e atualiza ela"""
    def putGamePiece(self): 
        pass

    """Verifica se um determinado estado é um estado final"""
    def gameOver(self):
        pass