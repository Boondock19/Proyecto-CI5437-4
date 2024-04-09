import pygame
import sys
import random
import math
import numpy as np
from time import perf_counter

clock = pygame.time.Clock() #Para ver los eventos a velocidad normal

#Inicializacion de pygame
pygame.init()

position = ()

#Tamano de la ventana de juego
width = 1000
height = 1000

#Colores de las fichas y del fondo del tablero de juego
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FOREST_GREEN = (34, 139, 34)
PLAYER = 1
IA = 2


#Nombre de la ventana de juego
pygame.display.set_caption("Connect 4")
#Inicializacion de la ventana de juego
window = pygame.display.set_mode((width, height))

#Matriz asociada al tablero de juego
tablero = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0]])

#Funciones para poder jugar
def boardPos(mouseX, mouseY):
	#Numero de fila dado por la posicion de click
	if (mouseY < 100):
		row = -1 
	elif (mouseY < 200):
		row = 0
	elif (mouseY < 300):
		row = 1
	elif (mouseY < 400):
		row = 2
	elif (mouseY < 500):
		row = 3
	elif (mouseY < 600):
		row = 4
	elif (mouseY < 700):
		row = 5
	elif (mouseY < 800):
		row = 6
	elif (mouseY < 900):
		row = 7 
	elif (mouseY < 1000):
		row = -1

	#Numero de columna dado por la posicion de click
	if (mouseX < 100):
		col = -1
	elif (mouseX < 200):
		col = 0
	elif (mouseX < 300):
		col = 1
	elif (mouseX < 400):
		col = 2
	elif (mouseX < 500):
		col = 3
	elif (mouseX < 600):
		col = 4
	elif (mouseX < 700):
		col = 5
	elif (mouseX < 800):
		col = 6
	elif (mouseX < 900):
		col = 7 
	elif (mouseX<1000):
		col = -1
	return (row, col)


def estado_ganador(tablero, piece):
	# Constantes para la cantidad de columnas y filas
	COL_ROW = 8

	# Chequea si hay ganadores horizontales
	for r in range(COL_ROW):
		for c in range(COL_ROW - 3):
			if all(tablero[r][c + i] == piece for i in range(4)):
				return True

    # Chequea si hay ganadores verticales
	for c in range(COL_ROW):
		for r in range(COL_ROW - 3):
			if all(tablero[r + i][c] == piece for i in range(4)):
				return True

	# Chequea si hay ganadores diagonales de froma ascendente
	for c in range(COL_ROW - 3):
		for r in range(COL_ROW - 3):
			if all(tablero[r + i][c + i] == piece for i in range(4)):
				return True

    # Chequea si hay ganadores diagonales de forma descendente
	for c in range(COL_ROW - 3):
		for r in range(3, COL_ROW):
			if all(tablero[r - i][c + i] == piece for i in range(4)):
				return True

	return False

def esValida(A:[int], i:int, j:int) -> bool:
	return A[i][j] == 0

def cambiarJugador(turn:int) -> 'void':
	if turn == PLAYER:
		return IA
	else:
		return PLAYER

def reflejarJugada(A: [int], j: int, turno: int):
	for row in range(7, -1, -1):
			if A[row][j] == 0:
				A[row][j] = turno
				break
	return A

def obtenerMovimientosValidos(tablero):
	jugadas = []
	for col in range(8):
		for row in range(8-1, -1, -1):
			if tablero[row][col] == 0:
				jugadas.append(col)
				break
	return jugadas

def es_estado_final(tablero):
	return estado_ganador(tablero, PLAYER) or estado_ganador(tablero, IA) or (len(obtenerMovimientosValidos(tablero)) == 0)

def filaLibre(tablero,col):
	for row in range(8-1, -1, -1):
		if tablero[row][col] == 0:
			return row

def evaluate_window(window, piece):
	valor = 0
	opp_piece = PLAYER
	if piece == PLAYER:
		opp_piece = IA

	if window.count(piece) == 4:
		valor += 100 
	elif window.count(piece) == 3 and window.count(0) == 1:
		valor += 5
	elif window.count(piece) == 2 and window.count(0) == 2:
		valor += 2

	if window.count(opp_piece) == 3 and window.count(0) == 1:
		valor -= 4

	return valor

def valor_posicion(tablero, piece):

	COL_ROW = 8
	valor = 0

	center_array = [int(i) for i in list(tablero[:, 3])]
	center_count = center_array.count(piece)
	valor += center_count * 1.5

	center_array = [int(i) for i in list(tablero[:, 4])]
	center_count = center_array.count(piece)
	valor += center_count * 1.5

	for r in range(COL_ROW):
		row_array = [int(i) for i in list(tablero[r,:])]
		for c in range(COL_ROW-3):
			window = row_array[c:c+8]
			valor += evaluate_window(window, piece)

	for c in range(COL_ROW):
		col_array = [int(i) for i in list(tablero[:,c])]
		for r in range(COL_ROW-3):
			window = col_array[r:r+4]
			valor += evaluate_window(window, piece)

	for r in range(COL_ROW-3):
		for c in range(COL_ROW-3):
			window = [tablero[r+i][c+i] for i in range(4)]
			valor += evaluate_window(window, piece)

	for r in range(COL_ROW-3):
		for c in range(COL_ROW-3):
			window = [tablero[r+3-i][c+i] for i in range(4)]
			valor += evaluate_window(window, piece)

	return valor

def minimax(tablero, depth, alpha, beta, maximizingPlayer):
	valid_locations = obtenerMovimientosValidos(tablero)
	is_terminal = es_estado_final(tablero)
	if depth == 0 or is_terminal:
		if is_terminal:
			if estado_ganador(tablero, IA):
				return (None, 100000000000000)
			elif estado_ganador(tablero, PLAYER):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, valor_posicion(tablero, IA))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			b_copy = tablero.copy()
			b_copy = reflejarJugada(b_copy, col, IA)
			new_valor = minimax(b_copy, depth-1, alpha, beta, False)[1]
			if new_valor > value:
				value = new_valor
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: # Minimizing player
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			b_copy = tablero.copy()
			b_copy = reflejarJugada(b_copy, col, PLAYER)
			new_valor = minimax(b_copy, depth-1, alpha, beta, True)[1]
			if new_valor < value:
				value = new_valor
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value

turno = PLAYER
ia_depth = int(input("Introduzca la profundidad del algoritmo minmax (Recomendado: 4): "))
game_over = False
ronda = 0

#Dibujo de fondo del tablero
pygame.draw.rect(window, FOREST_GREEN, (100,100, 800,800))

#Dibujo de lineas del tablero, horizontales y verticales
pygame.draw.line(window, (0,0,0), (200,900), (200,100), 2)
pygame.draw.line(window, (0,0,0), (300,900), (300,100), 2)
pygame.draw.line(window, (0,0,0), (400,900), (400,100), 2)
pygame.draw.line(window, (0,0,0), (500,900), (500,100), 2)
pygame.draw.line(window, (0,0,0), (600,900), (600,100), 2)
pygame.draw.line(window, (0,0,0), (700,900), (700,100), 2)
pygame.draw.line(window, (0,0,0), (800,900), (800,100), 2)

pygame.draw.line(window, (0,0,0), (100,200), (900,200), 2)
pygame.draw.line(window, (0,0,0), (100,300), (900,300), 2)
pygame.draw.line(window, (0,0,0), (100,400), (900,400), 2)
pygame.draw.line(window, (0,0,0), (100,500), (900,500), 2)
pygame.draw.line(window, (0,0,0), (100,600), (900,600), 2)
pygame.draw.line(window, (0,0,0), (100,700), (900,700), 2)
pygame.draw.line(window, (0,0,0), (100,800), (900,800), 2)


while not game_over:
	startTime = perf_counter()

	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			sys.exit()
		
		if ronda <= 64:
			print("IA 1 pensando...")
			col, minimax_valor = minimax(tablero, ia_depth, -math.inf, math.inf, False)
			color = WHITE
			if esValida(tablero, filaLibre(tablero,col), col):
				tablero = reflejarJugada(tablero, col, turno)
				turno = cambiarJugador(turno)
				ronda += 1
				print('El siguiente jugador es: IA 2')
				for i in range(0,8):
					for j in range(0,8):
						if tablero[i][j] == PLAYER:
							color = BLACK
							row = i 
							col = j
							centerX = ((col) * 100) + 150
							centerY = ((row) * 100) + 150
							pygame.draw.circle(window, color, (centerX,centerY), 40)
						elif tablero[i][j] == IA:
							color = WHITE
							row = i 
							col = j
							centerX = ((col) * 100) + 150
							centerY = ((row) * 100) + 150
							pygame.draw.circle(window, color, (centerX,centerY), 40)
						else: 
							pass
				
			elif turno == IA:
				
				print("IA 2 pensando...")
				
				col, minimax_valor = minimax(tablero, ia_depth, -math.inf, math.inf, True)
				color = WHITE
				if esValida(tablero, filaLibre(tablero,col), col):
					tablero = reflejarJugada(tablero, col, turno)
					turno = cambiarJugador(turno)
					ronda += 1
					print('El siguiente jugador es: IA 1')
					for i in range(0,8):
						for j in range(0,8):
							if tablero[i][j] == PLAYER:
								color = BLACK
								row = i 
								col = j
								centerX = ((col) * 100) + 150
								centerY = ((row) * 100) + 150
								pygame.draw.circle(window, color, (centerX,centerY), 40)
							elif tablero[i][j] == IA:
								color = WHITE
								row = i 
								col = j
								centerX = ((col) * 100) + 150
								centerY = ((row) * 100) + 150
								pygame.draw.circle(window, color, (centerX,centerY), 40)
							else: 
								pass
					endTime = perf_counter()

			if estado_ganador(tablero, IA):
				print("El ganador es La IA 2, mas suerte la proxima!")
				endTime = perf_counter()
				solutionTime = endTime - startTime
				print(f"Tiempo de ejecución: {solutionTime:.3f}, segundos en la ronda {ronda}")
				sys.exit()
			if estado_ganador(tablero, PLAYER):
				print("El ganador es la IA 1! Felicidades!")
				endTime = perf_counter()
				solutionTime = endTime - startTime
				print(f"Tiempo de ejecución: {solutionTime:.3f} segundos, en la ronda {ronda}")
				sys.exit()
		else: 
			print("No quedan jugadas, el juego ha terminado en un empate.")
			endTime = perf_counter()
			solutionTime = endTime - startTime
			print(f"Tiempo de ejecución: {solutionTime:.3f} segundos, en la ronda {ronda}")
			sys.exit()

		pygame.display.update()

	clock.tick(5)