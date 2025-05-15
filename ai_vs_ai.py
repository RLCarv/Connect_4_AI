from game_logic import *
from ai_mcts import *

"""Gameloop de uma AI contra outra AI"""
def gameLoop(c1,c2):
    print(f"\nNovo Jogo entre {c1} e {c2}")
    newGame = game() # gera um novo objeto jogo
    
    ai1 = MCTS(c1,100)
    aiName1 = "MCTS: c = " + str(c1)
    ai2 = MCTS(c2,100)
    aiName2 = "MCTS: c = " + str(c2)

    while newGame.gameWinner == EMPTY: #game loop
        
        if newGame.turn % 2 == 0:
            col = ai1.getMove(newGame,False) # type: ignore
            newGame.playOneTurn(col,newGame.player())
        else:
            col = ai2.getMove(newGame,False) # type: ignore
            newGame.playOneTurn(col,newGame.player())

        if newGame.gameOver(): # caso o jogo acabe
            if newGame.gameWinner == "Tie": # empate
                print("\n")
                newGame.drawBoard()
                print(f"\nIt's a Tie!")
                return 0,0
            elif newGame.gameWinner == "X":
                print("\n")
                newGame.drawBoard()
                print(f"\nX Won")
                return c1,c2
            else:
                print("\n")
                newGame.drawBoard()
                print(f"\nO Won")
                return c2,c1
            
        else: # o jogo não acabou
            newGame.turn += 1 # próximo turno
    
    return 0,0 #failsafe

"""realiza 2 jogos entre MCTSs com valores diferentes de c (c1 e c2) e retorna quem perdeu
caso resulte num empate, retorna o menor valor como perdedor"""
def worstC(c1,c2):
    result1 = gameLoop(c1,c2)
    result2 = gameLoop(c2,c1)

    if result1[0] == 0 and result2[0] != 0: #(0,vitoria)
        return result2[1]
    elif result2[0] == 0 and result1[0] != 0: #(vitoria,0)
        return result1[1]
    elif result1[0] == 0: #(0,0)
        return c1
    elif result1[0] == result2[0]: #(vitoria,vitoria)
        return result1[1]
    else: #(vitoria cx, vitoria cy)
        return c1

"""executa diversos jogos com os valores de C entre 0.2 e 2.0 e retorna o melhor valor"""
bestC = []
for i in range (2,21,2):
    bestC.append(i/10)

# primeiro round da chave
for i in range (2,20,4):
    c1 = i/10
    c2 = (i+2)/10
    bestC.remove(worstC(c1,c2))

bestC.remove(worstC(bestC[0],bestC[1])) # segundo round
bestC.remove(worstC(bestC[2], bestC[3]))
bestC.remove(worstC(bestC[0],bestC[2])) # terceiro round
bestC.remove(worstC(bestC[0],bestC[1])) # último round


bestC.append(((bestC[0]*10)-1)/10)
bestC.append(((bestC[0]*10)+1)/10)

bestC.remove(worstC(bestC[1],bestC[2])) # refinamento dos resultados
bestC.remove(worstC(bestC[0],bestC[1])) # resultado final

print(f"O melhor valor de C é: {bestC[0]}")    