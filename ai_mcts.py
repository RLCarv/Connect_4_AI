import math 
import numpy as np
import random
import copy
import time

"""limite de tempo arbitrário para parar a execuçao dos rollouts, o número de
simulações aumenta consideravelmente com o passar do jogo"""

MCTS_TIME = 5.0
MAX_ITER = 5000

"""valor de C aleatório, no futuro testaremos diversos valores para definir
qual o melhor balanço entre exploration e exploitation para este problema"""

MCTS_C = 2.0

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
    def __init__(self, c=MCTS_C, max_iterations=MAX_ITER):
        self.processing_time = MCTS_TIME
        self.exploring_rate = c
        self.max_iterations = max_iterations

    """Função principal que retorna o movimento Final"""
    def getMove(self, state, statistics = True):
        self.aiPiece = state.player() # define a peça da AI

        new_state = copy.deepcopy(state) # cria copias do estado inicial
        node = Node(copy.deepcopy(new_state))

        self.root = node 
        start_time = time.process_time() # começa o timer do jogo
        iterations = 0
        run_time = 0
        
        # o loop continuar até o tempo acabar ou a quantidade máxima de iterações
        #while time.process_time() - start_time < self.processing_time:
        while iterations < self.max_iterations:
            nextNode = self.choose(node) # escolhe o próximo Node
            
            if (nextNode[1]): # se o node for uma vitória imediata, retorna esse node
                return node.children[-1].state.last_move # os movimentos feitos são salvos em last move, então é só ir ao last move da ultima child adicionada
            elif (nextNode[2]): # se o node do player for uma vitória imediata, retorna esse node, bloqueando o player
                return node.children[-1].state.last_move

            simValue = self.rollout(nextNode[0]) # faz a simulação da partida e retorna o resultado
            self.backpropagation(nextNode[0], simValue) # faz a backpropagation até a child escolhida
            iterations += 1
    
        run_time = int(time.process_time() - start_time)
        
        """Retorna a child com a maior razão entre vitórias e números de visitas"""
        melhorValor = float('-inf')
        for child in node.children: # itera sobre todas as children e escolhe a com melhor razão
            if child.visits == 0: # eliminar children que não foram visitadas, apesar de ser pouco provável
                continue
            elif child.value/child.visits > melhorValor:
                melhorValor = child.value/child.visits
                melhorChild = child
            if statistics:
                print(f"---> move: {child.state.last_move} value: {child.value} visits:{child.visits} ratio: {child.value/child.visits}") # estatísticas
        if statistics:
            print(f"{iterations} iterations in {run_time} seconds")
        
        return melhorChild.state.last_move # toda vez que um movimento é feito ele é salvo em last move, então é só ir ao lastmove da melhor child

    """Seleciona o próximo node para fazer rollout, retorna o node,True/False que diz se a proxima jogada é vitória imediata"""
    def choose(self, node):  
        if not node.full_explored(): # se todas as children do node não foram exploradas, retorna uma delas
            return self.expand(node)
        else: # se todas foram exploradas uma vez, retorna a melhor de acordo com UCBT
            node = self.bestChild(node) 
        return node
    
    """expande o nó inicial"""
    def expand(self, node):
        possible_actions = node.state.availableCollumns() # lista de ações possíveis
        notTaken = [] # lista de ações não tomadas

        for action in possible_actions: 
            if action not in node.children_move: # children_move lista as ações já tomadas
                notTaken.append(action)

        action = random.choice(notTaken) # escolhe aleatóriamente uma ação não tomada

        newchild = copy.deepcopy(node.state) # gera uma nova child baseado nas ações não tomadas
        newchild.playOneTurn(action,newchild.player()) # faz essa jogadaa
        newchild.turn += 1
        immediateAIWin = newchild.gameOver() # verifica se a AI vai ganhar nessa jogada

        testplayer = copy.deepcopy(node.state) # gera uma child teste que joga como o player e sera descartada
        testplayer.turn += 1 # incrementa o turno, jogando como o player
        testplayer.playOneTurn(action,testplayer.player()) # faz essa jogada como o player
        immediatePlayerWin = testplayer.gameOver()

        node.add_child(Node(newchild), action) # adiciona ao node inicial essa nova child
        return node.children[-1],immediateAIWin,immediatePlayerWin # retorna essa child para fazer o rollout e se ela é uma vitória imediata
    
    """Calcula a UCBT para cada child e retorna a melhor,
    o False serve para manter o output da função choose consistente e não altera nada em bestChild"""
    def bestChild(self, node):
        bestScore = float('-inf')
        bestChild = []

        for child in node.children:
            score = child.value/child.visits + self.exploring_rate * math.sqrt(2*math.log(node.visits)/child.visits) # UCBT
            if score == bestScore:
                bestChild.append(child)
            if score > bestScore:
                bestChild = [child]
                bestScore = score

        return random.choice(bestChild), False, False # escolhe aleatóriamente entre as que tem o maior valor
    
    """Realiza as simulações com jogadas aleatórias"""
    def rollout(self, node):
        new = node.state

        while not new.gameOver(): # enquanto o jogo não acabar continua o rollout
            new = copy.deepcopy(new)
            possible_actions = new.availableCollumns()

            if len(possible_actions) > 0:
                new.playOneTurn(random.choice(possible_actions), new.player())
                new.turn += 1

        if new.gameWinner == self.aiPiece: # se a ai vencer
            return 1
        elif new.gameWinner != self.aiPiece:
            return 0 # derrota da ai
        else:
            return -1 # empate

    """Faz a backpropagation"""
    def backpropagation(self, node, value):
        #node.state.turn +=1

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

    """def backpropagationOld(self, node, value):

        while node != None: # node inicial tem valor None em parent
            node.value += value
            node.visits += 1
            node = node.parent

        return"""