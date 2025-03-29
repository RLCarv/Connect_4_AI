from game_logic import *

# Sempre faz um movimento Random
class ai_random:
    def __init__(self):
        pass

    def AIMove(self,state):
        col = range(8)
        while not state.verifyCol(col):
            col = range(8)
        return col

    