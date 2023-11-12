# Implementation of an integer linear program for L(2,1)-labeling of graphs
# Author: Atilio Gomes Luiz
# Date: 11-12-2023

from ortools.linear_solver import pywraplp
import numpy as np

# create a solver using CBC backend
msolver = pywraplp.Solver('L(2,1)-labeling', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

# read the file
f = open('edges.txt','r')
line = f.readline().split()
f.close()

# create the edges
edges = []
for i in range(0,len(line),2):
    edges.append([int(line[i]),int(line[i+1])])

# create the graph
G = dict()

for e in edges:
    if e[0] not in G:
        G[e[0]] = []
    if e[1] not in G:
        G[e[1]] = []
    G[e[0]].append(e[1])
    G[e[1]].append(e[0])

edges = []

# calculate maximum degree of the graph
maximum_degree = 0
for i in range(0,len(G)):
    if(len(G[i]) > maximum_degree):
        maximum_degree = len(G[i])

max_span = pow(maximum_degree,2) # upper bound for the span

# define two lists of variables
# x[i,j] variables will be true iff vertex i is assigned label j
# w[j] variables will be true if at least one node is assigned color j
x = dict()
w = []
for j in range(0, max_span + 1):
    w.append(msolver.IntVar(0, 1, f'w_{j}'))
for i in range(0, len(G)):
    x[i] = []
    for j in range(0, max_span + 1):
        x[i].append(msolver.IntVar(0, 1, f'x_{i}_{j}'))

# add constraints
# each vertex is assigned exactly one color
for vertex in range(0, len(G)):
    msolver.Add(sum(x[vertex])==1) 

# given a color and a pair of adjacent vertices, at most one of them may have that color assigned
for color in range(0, max_span + 1):
    for vertex in range(0,len(G)):
        for neighbor in G[vertex]:
            msolver.Add(x[vertex][color] + x[neighbor][color] <= 1)

 
# adjacent vertices must have colors at least two apart 
for color in range(0, max_span + 1):
    for vertex in range(0,len(G)):
        for neighbor in G[vertex]:                
            if(color > 0):
                msolver.Add(x[vertex][color] + x[neighbor][color-1] <= 1)
            if(color < max_span):
                msolver.Add(x[vertex][color] + x[neighbor][color+1] <= 1)


# vertices at distance two must have distinct colors
for color in range(0, max_span + 1):
    for vertex in range(0,len(G)):
        for neighbor in G[vertex]:
            for v in G[neighbor]:
                if(v != vertex):
                    msolver.Add(x[vertex][color] + x[v][color] <= 1)


# As for wj variables, one way to handle them is to simply make sure that if any node 
# is colored with color j then wj is set to true, by setting wj as an upper bound for every xij
for vertex in range(0, len(G)):
    for color in range(0, max_span + 1):
        msolver.Add(x[vertex][color] <= w[color])

# However, if the graph has no isolated nodes, we can take advantage of color conflict constraints 
# and reuse them to force wj variables to be true if one of the two adjacent nodes uses color j
for vertex in range(0,len(G)):
    for neighbor in G[vertex]:
        for color in range(0, max_span + 1):
            msolver.Add(x[vertex][color] + x[neighbor][color] <= w[color])

# objective function
used_labels = []
for j in range(0, max_span + 1):
    used_labels.append(j*w[j])
msolver.Minimize(sum(used_labels))

# calculate the optimal solution
mstatus = msolver.Solve()

# if an optimal solution has been found, print results
if mstatus == pywraplp.Solver.OPTIMAL:
    print(f'L(2,1)-labeling for the input graph')
    for j in range(max_span,-1,-1):
        if(w[j].solution_value() != 0):
            print(f'Optimal span = {j}')
            break
    print('Vertex Labels:')
    labeling = []
    for vertex in range(0,len(G)):
        for color in range(0,max_span+1):
            if x[vertex][color].solution_value() == 1:
                labeling.append(color)
                break
    print(labeling)
else:
    print('The solver could not find an optimal solution')