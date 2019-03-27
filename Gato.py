import pygame
import sys
import time
from pygame.locals import *
from random import randint

numeral = [[0,0,0],[0,0,0],[0,0,0]] #Matriz de espacios libres en tablero
ListaposicionesX = [["x","x"],["x","x"],["x","x"],["x","x"],["x","x"]]
ListaposicionesO = [["x","x"],["x","x"],["x","x"],["x","x"],["x","x"]]

class equis(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self) #Clase base para mostrar objetos
		self.ImagenJugador = pygame.image.load("imagenes/X.jpg") #Cargar imagenes jugador

		self.rect = self.ImagenJugador.get_rect()
		self.rect.centerx = 0
		self.rect.centery = 0
		
		self.Turno = True
		self.Vida = True
		self.Velocidad = 205

	def obtenerpos(self):
		return self.rect.centerx, self.rect.centery

	def dibujar(self, superficie):
		superficie.blit(self.ImagenJugador, self.rect) #Posicionamiento de jugador en pantalla
		
	def movimientoH(self): #Movimiento horizontal jugador
		if self.Vida == True:
			if self.rect.left <= 0:
				self.rect.left = 0
			elif self.rect.right >= 610:
				self.rect.right = 610
			
	def movimientoV(self): #Movimiento vertical jugador
		if self.Vida == True:
			if self.rect.top <= 0:
				self.rect.top = 0
			elif self.rect.bottom >= 610:
				self.rect.bottom = 610

class posicion(pygame.sprite.Sprite): # Clase de posicionamiento de jugadas
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.indiceX = 0
		self.indiceO = 0
		self.prueba = False # Turno del jugador fue correcto o no

	def posicion(self, turno, x=0, y=0):
		if turno == True:
			self.prueba = False
			if x == 100:
				fila = 0
			elif x == 305:
				fila = 1
			elif x ==510:
				fila = 2

			if y == 100:
				colum = 0
			elif y == 305:
				colum = 1
			elif y == 510:
				colum = 2
						
		else: #Jugada conputadora mediante random
			aux = 0
			while aux == 0:

				fila = randint(0,2)
				colum = randint(0,2)

				if numeral[fila][colum] == 0:
					aux = 1

					if fila == 0:
						x = 100
					elif fila == 1:
						x = 305
					elif fila == 2:
						x = 510

					if colum == 0:
						y = 100
					elif colum == 1:
						y = 305
					elif colum == 2:
						y = 510
		
		self.__posicionlibre(fila,colum, x, y, turno)
				
	def __posicionlibre(self, x, y, posx, posy, turno): #Funcion para utilizar espacios vacios del gato
		if numeral[x][y] == 0:
			if turno == True:
				numeral[x][y] = 1
				ListaposicionesX[self.indiceX][0] = posx-100
				ListaposicionesX[self.indiceX][1] = posy-100
				self.indiceX = self.indiceX + 1
				self.prueba = True
			else:
				numeral[x][y] = 2
				ListaposicionesO[self.indiceO][0] = posx-100
				ListaposicionesO[self.indiceO][1] = posy-100
				self.indiceO = self.indiceO + 1
	
class veredicto(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.Triunfo = 0 # 0 no hay ganador; 1 gano usuario; 2 gano cpu y 3 empate
		self.ganados = 0
		self.perdidos = 0
		self.empatados = 0

	def triunfo(self):
		ExisteJuego = False
	
		for i in range(3):
			for j in range(3):
				if numeral[i][j] == 1 or numeral[i][j] == 2:
					ExisteJuego = True

		if ExisteJuego == True: #Busca si alguien a ganado solo si existen jugadas hechas
			self.__buscatriunfo()

	def __buscatriunfo(self):
		horX = self.__triunfoH(1) 
		verX = self.__triunfoV(1)
		diagX = self.__triunfoD(1)

		horO = self.__triunfoH(2) 
		verO = self.__triunfoV(2)
		diagO = self.__triunfoD(2)

		emp = self.__empate()

		if horX == 1 or verX == 1 or diagX == 1:
			self.Triunfo = 1
		elif horO == 2 or verO == 2 or diagO == 2:
			self.Triunfo = 2
		elif emp == 3:
			self.Triunfo = 3

	def __triunfoH(self, x): # Busca triunfos horizontales
		aux = 0
		for i in range(3):
			if numeral[0][i] == x and numeral[1][i] == x and numeral[2][i] == x:
				aux = x

		return aux

	def __triunfoV(self, x): # Busca triunfos vertical
		aux = 0
		for i in range(3):
			if numeral[i][0] == x and numeral[i][1] == x and numeral[i][2] == x:
				aux = x

		return aux

	def __triunfoD(self, x): # Busca triunfos diagonal
		aux = 0
		if numeral[0][0] == x and numeral[1][1] == x and numeral[2][2] == x:
			aux = x
		elif numeral[0][2] == x and numeral[1][1] == x and numeral[2][0] == x:
			aux = x

		return aux

	def __empate(self): #busca empates
		aux = 0
		for i in range(3):
			for j in range(3):
				if numeral[i][j] == 1 or numeral[i][j] == 2:
					aux = aux + 1

		if aux == 9:
			return 3
		else:
			return 0

def gato():
	pygame.init()
	ventana = pygame.display.set_mode((615,670)) #Creacion ventana
	pygame.display.set_caption("Cross & Circle")

	Color = (255,255,255)
	ColorLinea = (0,0,0)
	
	jugador = equis()
	cuadro = posicion()
	ganador = veredicto()
	aux = 0
	fuente = pygame.font.Font(None, 50)
	fuenteM = pygame.font.Font(None, 30)
	textoW = fuente.render("Ganaste",0,(0,0,0))
	textoP = fuente.render("Perdiste",0,(0,0,0))
	textoE = fuente.render("Empate",0,(0,0,0))

	SonidoW = pygame.mixer.Sound("sonidos/YouWin.wav")
	SonidoP = pygame.mixer.Sound("sonidos/YouLose.wav")
	SonidoMovimiento = pygame.mixer.Sound("sonidos/Movimiento.wav")
	SonidoPosicion = pygame.mixer.Sound("sonidos/Posicion.wav")

	while True:

		jugador.movimientoH()
		jugador.movimientoV()
		ganador.triunfo()

		for evento in pygame.event.get():
			if evento.type == QUIT:
				pygame.quit()
				sys.exit()
			
			elif ganador.Triunfo == 0:

				if jugador.Turno == True: #Movimientos y funcionamiento de botones
					if evento.type == pygame.KEYDOWN:

						if evento.key == K_LEFT:
							jugador.rect.left -= jugador.Velocidad
							SonidoMovimiento.play()
					
						elif evento.key == K_RIGHT:
							jugador.rect.right += jugador.Velocidad
							SonidoMovimiento.play()
					
						elif evento.key == K_UP:
							jugador.rect.top -= jugador.Velocidad
							SonidoMovimiento.play()
					
						elif evento.key == K_DOWN:
							jugador.rect.bottom += jugador.Velocidad
							SonidoMovimiento.play()

						elif evento.key == K_SPACE:
							x,y= jugador.obtenerpos()
							imagenX = pygame.image.load("imagenes/X.jpg")
							cuadro.posicion(jugador.Turno, x, y)
							aux = 1
							if cuadro.prueba == True:
								jugador.Turno = False
								SonidoPosicion.play()

				elif jugador.Turno == False: # Turno Computadora
						imagenO = pygame.image.load("imagenes/O.png")
						cuadro.posicion(jugador.Turno)
						jugador.Turno = True

			elif ganador.Triunfo == 1 or ganador.Triunfo == 2 or ganador.Triunfo == 3:
				if ganador.Triunfo == 1:
					ventana.blit(textoW,(250,635))
					ganador.ganados = ganador.ganados + 1
					SonidoW.play()
				elif ganador.Triunfo == 2:
					ventana.blit(textoP,(250,635))
					ganador.perdidos = ganador.perdidos + 1
					SonidoP.play()
				else:
					ventana.blit(textoE,(250,635))
					ganador.empatados = ganador.empatados + 1
					SonidoP.play()

				pygame.display.update()
				time.sleep(2)
				cuadro.indiceO = 0
				cuadro.indiceX = 0
				aux = 0
				ganador.Triunfo = 0
				jugador.Turno = True

				for i in range(3):
					for j in range(3):
						numeral[i][j] = 0
								
		ventana.fill(Color)
		pygame.draw.line(ventana,ColorLinea,(201,10),(201,600),5)
		pygame.draw.line(ventana,ColorLinea,(405,10),(405,600),5)
		pygame.draw.line(ventana,ColorLinea,(10,201),(600,201),5)
		pygame.draw.line(ventana,ColorLinea,(10,405),(600,405),5)
		marcador = fuenteM.render("Ganados: " + str(ganador.ganados) + " - Perdidos: " + str(ganador.perdidos) + " - Empatados: " + str(ganador.empatados),0,(0,0,0))
		ventana.blit(marcador,(100,615))

		if aux == 1:
			for i in range(cuadro.indiceX):
				ventana.blit(imagenX,(ListaposicionesX[i][0],ListaposicionesX[i][1]))

			for i in range(cuadro.indiceO):
				ventana.blit(imagenO,(ListaposicionesO[i][0],ListaposicionesO[i][1]))
	
		jugador.dibujar(ventana)
		pygame.display.update()

gato()