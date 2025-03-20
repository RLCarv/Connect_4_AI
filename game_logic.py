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
        self.tops = [0] * NUM_COL

    """desenha a board"""
    def drawBoard(self):
        for i in range(7): print(i, end=" ") #imprime os numeros das colunas
        print() # coloca newline
        for line in self.board:
            for piece in line:
                print(piece, end=" ")
            print()# coloca newline
        return

    def verifyCol(self, col):
    #a coluna está disponível se o tamanho da pilha for menor que o total das linha 
        return self.tops[col] < NUM_ROW  
    
    """joga um turno"""
    def playOneTurn(self, col, piece): #joga um turno onde trata cada col como uma pilha
        if not self.verifyColumn(col):
            return False  # Col não está cheia
        
        #Coloca a coluna ceta desde a base usando lógica da pilha
        row_to_place = NUM_ROW - 1 - self.tops[col]
        
        # Coloca a peça 
        self.board[row_to_place][col] = piece
        
        # Adiciona ao contador da pilha nessa coluna
        self.tops[col] += 1
        return True

    """coloca a peça na board e atualiza ela"""
    def putGamePiece(self): 
        pass
    
    """verifica se um determinado estado é um estado final"""
    def gameOver(self):
        pass