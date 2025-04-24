import math 
import numpy as np
import random
import copy
import time

"""limite de tempo arbitrário para parar a execuçao dos rollouts, o número de
simulações aumenta consideravelmente com o passar do jogo"""

MCTS_TIME = 5.0
MAX_ITER = 50000

"""valor de C aleatório, no futuro testaremos diversos valores para definir
qual o melhor balanço entre exploration e exploitation para este problema"""

MCTS_C = 7.0

class Node:

    def __init__(self, state, parent=None):
        self.visits = 0
        self.value = 0
        self.state = state
        self.parent = parent
        self.children = []
        self.children_move = []

    def full_explored(self):
        return len(self.children) == len(self.state.availableCollumns())

    def update(self, v):
        self.value = self.value + v
        self.visits +=1
    
    def add_child(self, child, move):
        self.children.append(Node(child.state, parent=self))
        self.children_move.append(move)
    


class MCTS:
    def __init__(self):
        self.processing_time = MCTS_TIME
        self.exploring_rate = MCTS_C

    """Função principal que retorna o movimento Final"""
    def getMove(self, state):
        self.aiPiece = state.player() # define a peça da AI
        #print(f"\n{state.player()}")

        new_state = copy.deepcopy(state) #cria copias do estado inicial
        node = Node(copy.deepcopy(new_state))

        start_time = time.process_time()
        rolloutsCounter = 0
        run_time = 0

        """
        while time.process_time() - start_time < self.processing_time: # loop principal
            nextNode = self.choose(node) # escolhe o próximo Node
            simValue = self.rollout(nextNode) # faz a simulação da partida e retorna o resultado
            self.backpropagation(nextNode, simValue) # faz a backpropagation até o node escolhido
            #self.backpropagationAlt(nextNode, simValue)
            rolloutsCounter += 1 """

        for i in range(MAX_ITER):  # loop principal
            nextNode = self.choose(node) # escolhe o próximo Node
            simValue = self.rollout(nextNode) # faz a simulação da partida e retorna o resultado
            self.backpropagationAlt(nextNode, simValue) # faz a backpropagation até o node escolhido
            rolloutsCounter += 1 
    
        run_time = int(time.process_time() - start_time)
        
        """retorna a child com a maior razão entre vitórias e números de visitas, no entanto não
        leva em conta quem tem o maior valor de visitas, isso é: uma child com 1/1 seria escolhido
        ao invés de uma com 99/100"""
        melhorValor = float('-inf')
        for child in node.children: # itera sobre todas as children
            if child.visits == 0: # eliminar children que não foram visitadas, apesar de ser pouco provável
                continue
            elif child.value/child.visits > melhorValor:
                melhorValor = child.value/child.visits
                melhorChild = child
            print(f"---> move: {child.state.last_move} value: {child.value} visits:{child.visits} ratio: {child.value/child.visits}")
        print(f"{rolloutsCounter} simulations in {run_time} seconds")
        
        # toda vez que um movimento é feito ele é salvo em last move, então é só ir ao lastmove da melhor child
        return melhorChild.state.last_move 

    """Seleciona o próximo node para fazer rollout"""
    def choose(self, node):
        while not node.state.gameOver():
            if not node.full_explored():
                return self.expand (node)
            else:
                node = self.bestChild(node)
        return node
    
    """Calcula a UCBT para cada child e retorna a melhor"""
    def bestChild(self, node):
        bestScore = float('-inf')
        bestChild = []

        for child in node.children:
            score = child.value/child.visits + self.exploring_rate * math.sqrt(2*math.log(node.visits)/child.visits) #UCBT
            if score == bestScore:
                bestChild.append(child)
            if score > bestScore:
                bestChild = [child]
                bestScore = score

        return random.choice(bestChild) # escolhe aleatóriamente entre as que tem o maior valor
    
    """expande o nó escolhido"""
    def expand(self, node):
        possible_actions = node.state.availableCollumns() # lista de ações possíveis
        #print(f"\npossible: {possible_actions}")
        #print(f"\n available: {node.state.availableCollumns()}")
        notTaken = [] # lista de ações não tomadas

        for action in possible_actions:
            if action not in node.children_move:
                notTaken.append(action)
        #print(f"\nnot taken: {notTaken}")
        action = random.choice(notTaken)

        new = copy.deepcopy(node.state)
        
        #print(f"\nnext expand\: {new.player()}")
        new.playOneTurn(action,new.player())
        new.turn += 1
        #print(f"{new.drawBoard()}")

        node.add_child(Node(new), action)
        return node.children[-1]
    
    """realiza as simulações com jogadas aleatórias"""
    def rollout(self, node):
        new = node.state

        while not new.gameOver(): # enquanto o jogo não acabar continua o rollout
            new = copy.deepcopy(new)
            possible_actions = new.availableCollumns()

            if len(possible_actions) > 0:
                #print(f"\nnext: {new.player()}")
                new.playOneTurn(random.choice(possible_actions), new.player())
                new.turn += 1
                #print(f"{new.drawBoard()}")
        #return new.gameWinner

        #new.turn += 1
        #print(f"\nfinal {new.player()}")
        #print(f"winner: {new.gameWinner}")
        #print(f"ai: {self.aiPiece}")
        #print(f"{new.drawBoard()}")

        if new.gameWinner == self.aiPiece: # se a ai vencer
            return 1
        elif new.gameWinner != self.aiPiece:
            return 0 # derrota da ai
        else:
            return -1 # empate

    """faz a backpropagation
    -- por algum motivo fazer de forma alternada é pior (???)
    isso não tem muito sentido pois ele soma a pontuação seja pos ou neg para
    ambos os players... ainda tenho que testar mais"""

    def backpropagation(self, node, value):

        while node != None: # node inicial tem valor None em parent
            node.value += value
            node.visits += 1
            node = node.parent

        return


    def backpropagationAlt(self, node, value):
        node.state.turn +=1
        #print("\n\nbackprop:\n")
        #print(f"value: {value}; winner: {node.state.player()}; turn: {node.state.turn} ")

        if value == -1: # empate
            while node != None:
                node.visits += 1
                node = node.parent

        elif value == 0: # derrota
            while node != None:
                node.value += value
                node.visits += 1
                #print(f"{node.value}; {node.state.player()} ")
                node = node.parent
                value = 1 - value

        else: # vitória
            while node != None:
                node.value += value
                node.visits += 1
                #print(f"{node.value}; {node.state.player()} ")
                node = node.parent