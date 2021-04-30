import csv
from copy import deepcopy
import time

nodosEnPila = 0
matriz = []
dicPosiciones = {}
grafo = {}


matriz = []

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


def crearGrafo():  # profundidad
    vecg = []
    vecP = []
    i = 0
    for x in range(9):
        if x % 2 == 0:
            for y in range(9):
                if matriz[y][x] == '':
                    vertices = posibles(matriz, x, y)
                    vecP.append((str(i), [y, x]))
                    vecg.append((str(y) + "," + str(x), vertices))
                    i += 1
        if x % 2 == 1:
            for num in range(8, -1, -1):
                if matriz[num][x] == '':
                    vertices = posibles(matriz, x, num)
                    vecP.append((str(i), [num, x]))
                    vecg.append((str(num) + "," + str(x), vertices))
                    i += 1
    dicPosiciones.update(vecP)
    grafo.update(vecg)

"""
def display(grid):
    """"""
    funcion mostrar cuadricula
    """"""
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
    global nodosEnPila
    queue = [(0, -1, deepcopy(matriz))]
    while queue:
        (node, nivel, grid) = queue.pop(0)
        if queue:
            nodosEnPila += 1
        if nivel + 1 == len(dicPosiciones):
            print("Solucion DFS: ")
            for row in grid:
                salida = []
                for col in row:
                    if col == '':
                        salida.append(0)
                    else:
                        salida.append(int(col))
                print(salida)
            print('Total nodos en la Pila: ', nodosEnPila)
            fin = time.time() - inicio
            print('El tiempo de resolución fue: ', fin, ' segundos')
            print('la solución se encontró en el nivel: ', nivel)
            break
        pos = dicPosiciones.get(str(nivel + 1))
        newM = deepcopy(posibles(grid, pos[0], pos[1], ))
        if len(newM) > 0:
            for next in sorted(newM, reverse=True):
                copi = deepcopy(grid)
                copi[pos[0]][pos[1]] = next
                queue.append((next, (nivel + 1), copi))


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