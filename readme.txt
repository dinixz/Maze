Bibliotecas usadas: numpy, copy, math, collections, time, heapq, pygame, sys, random

Para correr a interface basta correr o ficheiro interface.py. 
Selecione o modo player, se quiser jogar, ou modo ia, para ver a solução de um labirinto.
Selecione uma dificuldade e o computador vai encontrar a solução para o algoritmo, logo no inicio do jogo.
Na tela de jogo, use as teclas 'w', 'a', 's' e 'd' para mover, o botão azul para recomeçar, a lâmpada para o computador dar a dica e jogar e o botão vermelho para voltar à página anterior.
No modo de player, consideramos apenas uma solução possível que é gerada no inicio do jogo, daí a demora para passar da tela de menu para a tela de jogo. 
Fizemos isto porque seria muito pesado verificar se existe solução possivel a cada passo, ninguém quer jogar um jogo que trava para pensar constantemente.

Os algoritmos estão todos implementados no ficheiro algorithms.py assim como os labirintos pré-disponibilizados.