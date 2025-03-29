import numpy as np
NUM_ROW = 6
NUM_COL = 7
EMPTY = "-"
PLAYER_1_PIECE = "X"
PLAYER_2_PIECE = "O"

class game:
    def __init__(self):
        #variaveis iniciais
        self.turn = 0 #contador do turno
        self.playerTurn = PLAYER_1_PIECE #quem começa
        self.gameWinner = EMPTY #variavel que controla quem ganhou
        self.boardIsFull = False #retorna se a board esta cheia
        self.board = np.full([NUM_ROW, NUM_COL], EMPTY) #gera a board vazia
        self.tops = [0] * NUM_COL #array unidimensional que guarda quantas peças em cada coluna

    """desenha a board"""
    def drawBoard(self):
        for i in range(7): print(i, end=" ") #imprime os numeros das colunas
        print() # coloca newline
        for line in self.board:
            for piece in line:
                print(piece, end=" ")
            print()# coloca newline
        return

    """verifica se a coluna está disponível"""
    def verifyCol(self, col):
    #a coluna está disponível se o tamanho da pilha for menor que o total das linha
        if col >= NUM_COL or col < 0: # error handling quando a coluna não existe
            return False
        else:
            return self.tops[col] < NUM_ROW
    
    """joga um turno"""
    def playOneTurn(self, col, piece): #joga um turno onde trata cada col como uma pilha
        if not self.verifyCol(col): #error handling ^2
            return False  # Col não está cheia
        
        # Coloca a coluna certa desde a base usando lógica da pilha
        row_to_place = NUM_ROW - 1 - self.tops[col]
        
        # Coloca a peça 
        self.board[row_to_place][col] = piece
        
        # Adiciona ao contador da pilha nessa coluna
        self.tops[col] += 1
        return True
    
    """verifica se um determinado estado é um estado final"""
    def gameOver(self):
        #retorna um boolean e altera o valor da variavel gameWinner
        for i in range(NUM_ROW):
            for j in range(NUM_COL):
                #verifica se a peça é X ou O
                piece = self.board[i, j]
                if piece == EMPTY:  
                    continue 
                #verifica em linha horizontal 
                if j <= NUM_COL - 4 and all(self.board[i, j + k] == piece for k in range(4)):
                    self.gameWinner = piece
                    return True
                #verifica em linha vertical 
                if i <= NUM_ROW - 4 and all(self.board[i + k, j] == piece for k in range(4)):
                    self.gameWinner = piece
                    return True
                #verifica a diagonal principal
                if i <= NUM_ROW - 4 and j <= NUM_COL - 4 and all(self.board[i + k, j + k] == piece for k in range(4)):
                    self.gameWinner = piece
                    return True
                #verifica a diagonal secundaria
                if i <= NUM_ROW - 4 and j >= 3 and all(self.board[i + k, j - k] == piece for k in range(4)):
                    self.gameWinner = piece
                    return True
        #verifica empate
        if all(not self.verifyCol(i) for i in range(NUM_COL)):  
            self.gameWinner = "Tie"
            return True

        return False