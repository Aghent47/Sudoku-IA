import csv
from copy import deepcopy
import time

nodosEnCola = 0
matriz = []
dicPosiciones = {}  # orden del recorrido
grafo = {}

with open('sudoku_ejemplo.csv', 'r') as File:
    reader = csv.reader(File)
    for row in reader:
        fila = []
        for item in row:
            fila.append(str(item))
        matriz.append(deepcopy(fila))

original = matriz


def esPosible(grid, y, x, n):
    for i in range(0, 9):
        if grid[y][i] == n:
            return False
    for i in range(0, 9):
        if grid[i][x] == n:
            return False
    x0 = (x//3)*3  # 6 -> // 3 = 2 * 3 = '6'
    y0 = (y//3)*3  # 4 -> // 3 = 1 * 3 = '3'
    for i in range(0, 3):
        for j in range(0, 3):
            if grid[y0 + i][x0 + j] == n:
                return False
    return True


def posibles(grid, y, x):
    auxGrid = deepcopy(grid)
    numeros = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    posibles = []
    for num in range(len(numeros)):
        if esPosible(auxGrid, y, x, numeros[num]):
            posibles.append(numeros[num])
    return posibles


def crearGrafo():  # anchura
    vecg = []
    vecP = []
    i = 0
    for x in range(9):
        for y in range(x + 1):  # triangulo superior
            if matriz[x - y][y] == '':
                vertices = posibles(matriz, x - y, y)  # {0,0} -> [3 , 4]
                vecP.append((str(i), [x - y, y]))  # guarda posicion y posibilidades al encontrar un '0'
                vecg.append((str(x - y) + "," + str(y), vertices))  # guarda las coordenadas y los valores posibles ""
                i += 1
    for X in range(9):
        for Y in range(9 - X - 1):  # triangulo inferior
            if matriz[9 - Y - 1][Y + X + 1] == '':
                vertices = posibles(matriz, 9 - Y - 1, Y + X + 1)
                vecP.append((str(i), [9 - Y - 1, Y + X + 1]))
                vecg.append((str(9 - Y - 1) + "," + str(Y + X + 1), vertices))
                i += 1
    dicPosiciones.update(vecP)
    grafo.update(vecg)
    # print(dicPosiciones)
    # print(grafo)


"""
def display(grid):
    
    funcion mostrar cuadricula
    
    width = 1 + max(len(grid[s]) for s in range(9))
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in range(9):
        print(''.join(grid[r + c].center(width) + ('|' if c in '36' else '')
                      for c in range(9)))
        if r in 'CF': print(line)
    return
"""

def solver():
    inicio = time.time()
    global nodosEnCola
    cola = [(0, -1, deepcopy(matriz))]
    while cola:
        (node, nivel, m) = cola.pop(0)
        pos = dicPosiciones.get(str(nivel + 1))
        if cola:
            nodosEnCola += 1
        if nivel + 1 == len(dicPosiciones):
            print("\nSolución BFS: ")
            for x in m:
                salida = []
                for y in x:
                    if y == '':
                        salida.append(0)
                    else:
                        salida.append(int(y))
                print(salida)
            print('Total nodos en la cola: ', nodosEnCola)
            fin = time.time() - inicio
            print('El tiempo de resolución fue: ', fin, ' segundos')
            print('La solución se encontró en el nivel: ', nivel)
            break
        newM = deepcopy(posibles(m, pos[0], pos[1]))  # copia de matriz, coordenadas, lista de posibilidades
        if len(newM) > 0:
            for next in newM:
                copy = deepcopy(m)
                copy[pos[0]][pos[1]] = next
                cola.append((next, (nivel + 1), copy))


print('Original: ')
for x in original:
    salida = []
    for y in x:
        if y == '':
            salida.append(0)
        else:
            salida.append(int(y))
    print(salida)


crearGrafo()
solver()
print(grafo)
print(dicPosiciones)
