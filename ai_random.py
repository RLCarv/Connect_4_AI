from game_logic import *
import random

# Sempre faz um movimento Random
class ai_random:
    def getMove(self, state):
        col = random.randrange(NUM_COL)
        while not state.verifyCol(col):
            col = random.randrange(NUM_COL)
        return col

    