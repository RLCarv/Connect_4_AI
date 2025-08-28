# **Adversarial search strategies and Decision Trees**
  
- Francisco Moreira
- Rodrigo Carvalho
- Verónica Azline

## Objetivo
O objetivo deste trabalho é implementar o algoritmo **Monte Carlo Tree Search (MCTS)** para jogar o jogo *Connect 4* utilizando o algoritmo *Upper Confidence Bound for Trees (UCT)* para a seleção do nó a ser expandido, e criar uma **Árvore de Decisões** através do procedimento *Iterative Dichotomiser 3 (ID3)*  para classificar 2 diferentes datasets.

## O jogo
**Connect Four** é um jogo de estratégia para dois jogadores. É jogado com 42 peças (21 de uma cor e 21 de outra) numa grade vertical com 7 colunas. Cada coluna pode conter no máximo 6 peças. Os dois jogadores jogam alternadamente colocando uma ficha numa das colunas. Quando uma ficha é colocada numa coluna, ela cai até atingir a parte inferior ou a ultima ficha nessa coluna. Um jogador vence quando pelo menos quatro de suas fichas estão alinhadas numa linha, coluna ou diagonal.

**É possível jogar o jogo entre dois players ou contra a AI do MCTS que desenvolvemos.**

## Nossa representação
A interface do nosso jogo é representada no terminal, onde os dois jogadores são representados através de "X" - sempre o primeiro jogador - e "O" - sempre o segundo jogador -, sendo que "-" significa uma casa vazia. 

 `Turn: 13`<br>
 `0 1 2 3 4 5 6`<br>
 `- - - - - - -`<br>
 `- - - - - - -`<br>
 `- - - - - - -`<br>
 `O - - - - - -`<br>
 `X - O O - - -`<br>
 `X - X O - - -`<br>
 `X O X X O - X`<br>
 `Next to play: Monte Carlo as O`

Além disto, após o algoritmo do Monte Carlo Tree Search fazer sua jogada, é representado para cada uma das jogadas possíveis o número de vezes em que uma vitória foi alcançada a partir daqueles nós ("value"), o número de visitas nestes nós ("visits"), e a ratio entre o numero de vitórias e o numero de visitas - que é usada para determinar a jogada a seguir.

`Thinking...`<br>
`---> move: 2 value: 665 visits:775 ratio: 0.8580645161290322`<br>
`---> move: 5 value: 550 visits:690 ratio: 0.7971014492753623`<br>
`---> move: 6 value: 581 visits:713 ratio: 0.814866760168303`<br>
`---> move: 1 value: 515 visits:664 ratio: 0.7756024096385542`<br>
`---> move: 3 value: 637 visits:754 ratio: 0.8448275862068966`<br>
`---> move: 0 value: 503 visits:655 ratio: 0.76793893129771`<br>
`---> move: 4 value: 630 visits:749 ratio: 0.8411214953271028`<br>
`5000 iterations in 6 seconds`<br>
`Monte Carlo played in col: 2`

## Instalação

**Pré-requisitos:**

- Python 3.x (https://www.python.org/downloads/)
- NumPy (https://numpy.org/install/)

**Rodando o jogo:**

- Abrir o terminal e navegar até a pasta *"Connect_4_AI/main"*
- Executar o comando:

```
python3 main.py
```

## Árvore de Decisões
Uma árvore de decisão é uma estrutura utilizada em treinamento de IAs, onde cada nó representa uma decisão e os seus ramos representam cada possibilidade dessa decisão. Para construir a nossa árvore de decisão utilizamos o algoritmo id3, que constrói a árvore recursivamente, dando prioridade aos atributos que dão maior ganho de informação.

A descrição completa do processo da criação das Árvore de Decisões e o processo de classificação dos dois datasetes encontra-se na segunda parte do arquivo ***"Adversarial search strategies and Decision Trees.ipynb"***. 
