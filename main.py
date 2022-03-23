import pygame
import random
from threading import RLock
from opensimplex import OpenSimplex
import random
import string
import time
from timeit import default_timer as timer
import pygame
from pygame.locals import *
from statistics import mean
clock = pygame.time.Clock()
from Tiles import *
from timeit import default_timer as timer
from PIL import Image
from math import floor, 

ZOOM_LEVEL_0 = (32, 32)
ZOOM_LEVEL_1 = (63, 75)
ZOOM_LEVEL_2 = (127, 149)

TOP = "TOP"
DOWN = "DOWN"
LEFT = "LEFT"
RIGHT = "RIGHT"

list_move_keys = [K_DOWN, K_s, K_UP, K_z, K_RIGHT, K_d, K_LEFT, K_q]

def getOrientationFromTriangularSignal(x, periode):
	""" x = coordonée X du clic
	amplitudeMax = periode / 4
	periode = niveau de zoom
	"""
	periode -= 1
	AmplitudeMax = periode / 4
	nbReste = x/periode - x//periode

	if nbReste > 0.5:
		Amplitude = 1 - nbReste
		orientation = RIGHT
	else:
		Amplitude = nbReste
		orientation = LEFT

	Limite = Amplitude * AmplitudeMax / 0.5

	return floor(Limite), orientation


def getCoordinatesOfClick(coordinates, event, offset):
	gridWidth, gridHeight = coordinates
	#Y = int(event.pos[1]) - (self.offset_h * hexSizeX)
	#X = int(event.pos[0]) - (self.offset_v * hexSizeY)
	offset_v, offset_h = offset # offset étant de combien de pixel on est décalé sur la droite
	x, y = event.pos[0], event.pos[1] # X et Y représentant les clics de la souris
	#height, width = 19, 20
	"""
	height, width = round(gridHeight * (3/4)) - 1, gridWidth - 1
	columnY = y // height

	if (columnY % 2 == 0):
		x -= (width / 2)
	"""

	""" 
	On regarde si on est dans la partie supérieure de l'hexagone
	-> On calcule les coordonnées du sprite qu'on a choppé
	-> On regarde si notre x est compris entre x et x + (hauteur / 4)
	-> On regarde si on est à gauche ou à droite du milieu
	-> On fait la fonction triangulaire/affine 
	-> On regarde si on est en dessous ou au dessus
	-> si on est en dessosu tout va bien
	-> Si on est au dessus c'est l'hexagone en haut à gauche
	-> Ou l'hexagone en haut à droite qu'il faut qu'on prenne
	-> f(x) = 0.5 * (x) à gauche
	-> f(x) = hauteur / 4 - (0.5*x) à droite
	"""
	"""
	columnX = int(x // width)
	# We look if we are on th first quarter of the hexagon by calculating hexagon coordinates
	tileX = columnX * (gridWidth - 1) + (offset_v * (gridWidth - 1)) - gridWidth / 2
	tileY = columnY * (gridHeight - (gridHeight / 4) - 1) + (offset_h * gridHeight)
	print("TileX = ", tileX, columnX, columnY)
	newX, newY = x - tileX, y - tileY
	limite, orientation = getOrientationFromTriangularSignal(x, gridWidth)
	print(newX, newY)
	if (newY < (gridHeight / 4) - 1):
		print("We are on the first quarter of the hexagon", y, y - gridHeight)
		
		print("newY = ", newY)
		# This mean that we are at the first quarter of the hexagon
		# Are we in the left side or the left side?
		limite, orientation = getOrientationFromTriangularSignal(x, gridWidth)
		print("orientation = ", orientation, " limite = ", limite)
		if newY > limite:
			# On est au dessus.
			columnY -= 1
			if (orientation == RIGHT):
				columnX += 1
	"""

	print("Colonne X = ", columnX)
	print("Colonne Y = ", columnY)
	print(x)
	print("---------------")
	return (columnX, columnY)


class Map:
	def __init__(self):
		self.sizeX = 20
		self.sizeY = 20
		self.map = []
		self.width = 600
		self.height = 400
		self.window = pygame.display.set_mode((self.width, self.height))
		self.offset_h = 0
		self.offset_v = 0
		self.current_zoom_level = 0
		self.current_zoom = ZOOM_LEVEL_0
		self.tmp = OpenSimplex(round(time.time()))

		for x in range(self.sizeX + 1):
			self.map.append(list())
			for y in range(self.sizeY + 1):
				self.map[x].append(thevoid(0, 0, 0))

		self.generate()

	def getAdjacentCells(self, X, Y):
		result = []
		try:
			result.append(self.map[X-1][Y-1])
		except:
			pass
		try:
			result.append(self.map[X-1][Y])
		except:
			pass
		try:
			result.append(self.map[X-1][Y+1])
		except:
			pass
		try:
			result.append(self.map[X][Y-1])
		except:
			pass
		try:
			result.append(self.map[X][Y+1])
		except:
			pass
		try:
			result.append(self.map[X+1][Y-1])
		except:
			pass
		try:
			result.append(self.map[X+1][Y])
		except:
			pass
		try:
			result.append(self.map[X+1][Y+1])
		except:
			pass
		return (result)

	def isAtTheEdge(self, x, y):
		if (x == 0 or x == self.sizeX - 1):
			return True
		if (y == 0 or y == self.sizeY - 1):
			return True
		return False

	def doesTheAdjacentCaseIsWater(self, x, y):
		listOfCases = self.getAdjacentCells(x, y)
		for cases in listOfCases:
			if (cases.tileName in ["sea", "ocean", "iceberg", "island", "reef"]):
				return True
		return False

	def generate(self):
		x = 0
		start = timer()

		while x < self.sizeX:
			y = 0
			while y < self.sizeY:
				z1 = (x + y) / 2
				s = (x + y + z1) / 3
				j = self.tmp.noise2d((x+s) / 16, (y+s) / 16)
				gradient_chaleur = self.tmp.noise2d((y+s)/40, (x+s)/40)
				reef_time = self.tmp.noise2d((x + y) / 2, (x + s) / 2)
				wetness = self.tmp.noise2d((x + y) / 20, (x + s) / 20)
				disaster_random = self.tmp.noise2d ((x + y) / 3, (x + s) / 3)

				if disaster_random > 0.95:
					a = volcan(x, y, self.sizeX, j, random.randint(0, 1), random.randint(1, 5), "wood", self.map, random.randint(1, 5), random.randint(1, 5))
					self.map[x][y] = a
					self.disasters.append(a)

				elif (j < -0.3 and (self.isAtTheEdge(x, y) or self.doesTheAdjacentCaseIsWater(x, y))):
					""" Génération des océans """
					i = random.randint(10, 50)
					if (gradient_chaleur < -0.4):
						self.map[x][y] = iceberg(x, y, j)
					else:					
						if (i == 42):
							self.map[x][y] = island_ocean(x, y, j)
						else:
							self.map[x][y] = ocean(x, y, j)

				elif (j < -0.01) :
					""" Génération de la mer """
					i = random.randint(10, 50)
					if (i == 42):
						self.map[x][y] = island(x, y, j)
					else:
						if (reef_time < -0.20):
							self.map[x][y] = reef(x, y, j)
						else:
							self.map[x][y] = sea(x, y, j)

				elif (j < 0.20) and (gradient_chaleur > 0.5):
					self.map[x][y] = desert(x, y, j)		
				elif (j < 0.20) and (gradient_chaleur > 0.3):
					self.map[x][y] = savanah(x, y, j)		
				elif (j < 0.20) and (gradient_chaleur < -0.3):
					self.map[x][y] = tundra(x, y, j)		
				elif (j < 0.20 and wetness > 0.4):
					self.map[x][y] = swamp(x, y, j)
				elif (j < 0.20 ):
					self.map[x][y] = land(x, y, j)
				elif (j < 0.50) and (gradient_chaleur > 0.3) and wetness > 0.4:
					self.map[x][y] = jungle(x, y, j)
				elif (j < 0.50) and (gradient_chaleur < -0.3):
					self.map[x][y] = taiga(x, y, j)
				elif (j < 0.50):
					self.map[x][y] = forest(x, y, j)
				elif (j < 0.51) and (gradient_chaleur < -0.3):
					self.map[x][y] = snowy_hills(x, y, j)
				elif (j < 0.51):
					self.map[x][y] = hills(x, y, j)
				else:
					self.map[x][y] = mountain(x, y, j)
				y += 1
			x += 1
		duration = timer() - start
		print("Génération de la map = ", duration)


	def draw_tiles(self, hexSize = (63, 75)):
		hexSizeX, hexSizeY = hexSize
		for x in range(self.sizeX):
			for y in range(self.sizeY):
				if (hexSize == ZOOM_LEVEL_0):
					horizontalDeportation = 0
					if (y % 2 == 0):
						horizontalDeportation = -(hexSizeX - 1) / 2 # (hexsizeX - 1) / 2
					tiles = self.map[x][y]
					tileX = tiles.X * (hexSizeX - 1) + (self.offset_v * (hexSizeX - 1)) - horizontalDeportation
					tileY = tiles.Y * (hexSizeY - (hexSizeY / 4) - 1) + (self.offset_h * hexSizeY)
					if (tileX >= -hexSizeX and tileX < self.screenresW) and (tileY >= -hexSizeY and tileY < self.screenresH):
						self.window.blit(tiles.img_zoom_level_0, (tileX, tileY))
				elif (hexSize == ZOOM_LEVEL_1):
					horizontalDeportation = 0
					if (y % 2 == 0):
						horizontalDeportation = -(hexSizeX - 1) / 2
					tiles = self.map[x][y]
					tileX = tiles.X * (hexSizeX - 1) + (self.offset_v * (hexSizeX - 1)) - horizontalDeportation
					tileY = tiles.Y * (hexSizeY - 20) + (self.offset_h * hexSizeY)
					if (tileX >= -hexSizeX and tileX < self.screenresW) and (tileY >= -hexSizeY and tileY < self.screenresH):
						self.window.blit(tiles.img_zoom_level_1, (tileX, tileY))
				elif (hexSize == ZOOM_LEVEL_2):
					horizontalDeportation = 0
					if (y % 2 == 0):
						horizontalDeportation = -(hexSizeX - 1) / 2
					tiles = self.map[x][y]
					tileX = tiles.X * (hexSizeX - 1) + (self.offset_v * (hexSizeX - 1)) - horizontalDeportation
					tileY = tiles.Y * (hexSizeY - 38) + (self.offset_h * hexSizeY)
					if (tileX >= -hexSizeX and tileX < self.screenresW) and (tileY >= -hexSizeY and tileY < self.screenresH):
						self.window.blit(tiles.img_zoom_level_2, (tileX, tileY))

# X = L'AXE VERTICAL
# Y = L'AXE HORIZONTAL

	def handle_zoom(self, event):
		if (event.y > 0):
			self.current_zoom_level += 1
		if (event.y < 0):
			self.current_zoom_level -= 1
		if (self.current_zoom_level > 2):
			self.current_zoom = ZOOM_LEVEL_0
		if (self.current_zoom_level > 3):
			self.current_zoom = ZOOM_LEVEL_1
		if (self.current_zoom_level > 4):
			self.current_zoom = ZOOM_LEVEL_2
			self.current_zoom_level = 5
		if (self.current_zoom_level <= 0):
			self.current_zoom_level = 1

	def handle_movement(self, event):
		if event.type == KEYDOWN and (event.key == K_DOWN or event.key == K_s):
			self.offset_h -= 3
		elif event.type == KEYDOWN and (event.key == K_UP or event.key == K_z):
			self.offset_h += 3
		elif event.type == KEYDOWN and (event.key == K_RIGHT or event.key == K_d):
			self.offset_v -= 3
		elif event.type == KEYDOWN and (event.key == K_LEFT or event.key == K_q):
			self.offset_v += 3

	def handle_click(self, event):
		columnX, columnY = getCoordinatesOfClick(self.current_zoom, event, (self.offset_v, self.offset_h))
		try:
			self.map[columnX][columnY].changeTile()
		except Exception as E:
			print(columnX, columnY, E)

		#print(self.map[X][Y].tileName)

	def show(self):
		""" Main loop of the game"""
		continuer = True
		infoObject = pygame.display.Info()

		self.screenresW = infoObject.current_w
		self.screenresH = infoObject.current_h
		
		while continuer:
			pygame.draw.rect(self.window, (0, 0, 0), (0, 0, self.screenresW, self.screenresH))
			self.draw_tiles(self.current_zoom)
			clock.tick(60)

			pygame.display.flip()
			for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
				pygame.key.set_repeat(100)
				if event.type == QUIT:     #Si un de ces événements est de type QUIT
					continuer = False

				elif event.type == KEYDOWN and event.key == K_ESCAPE:
					continuer = False

				elif event.type == KEYDOWN and (event.key in list_move_keys):
					self.handle_movement(event)

				elif event.type == MOUSEBUTTONDOWN and event.button == 1:
					self.handle_click(event)

				elif event.type == MOUSEWHEEL:
					self.handle_zoom(event)


if __name__ == "__main__":
	a = Map()
	a.show()