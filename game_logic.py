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
        self.gameWinner = EMPTY #variavel que controla quem ganhou
        self.boardIsFull = False #retorna se a board esta cheia
        self.board = np.full([NUM_ROW, NUM_COL], EMPTY) #gera a board vazia
        
    """desenha a board"""
    def drawBoard(self):
        for i in range(7): print(i, end=" ") #imprime os numeros das colunas
        print() # coloca newline
        for line in self.board:
            for piece in line:
                print(piece, end=" ")
            print()# coloca newline
        return

    """joga um turno e atualiza a board"""
    def playOneTurn(collumn, player): #joga um turno
        pass

    """Verifica se um determinado estado é um estado final"""
    def gameOver(self):
        pass