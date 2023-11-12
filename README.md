# ILP_lambda21_labeling
Integer Linear Program for calculating an optimal L(2,1) labeling of a given graph G

## Antes de usar

Precisa instalar o solver de programação linear **ortools** do google.

Este link aqui ensina como instalar: https://developers.google.com/optimization/install?hl=pt-br

## Como funciona

O arquivo *edges.txt* possui somente uma linha, que contém todas as arestas do grafo para o qual
você quer determinar o número de dominação romana. Cada aresta é formada por um par de números. 
Dois números seguidos formam uma aresta.

Para executar o programa, digite no terminal o comando (aqui, estou supondo que você possui python3.8 ou superior instalado):

```
python3.10 PLI_ILP_L(2,1)labeling.py
```