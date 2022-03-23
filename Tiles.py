import random
import pygame

def rotation_random():
	a = [0, 90, 180, 270]
	return (random.choice(a))

class tiles():
	def __init__(self, X, Y, j):
		self.tileName = ""
		self.passable = True
		self.size = 3000
		self.ores = []
		self.X = X
		self.Y = Y
		self.radius = 30
		self.j = j
		self.ForestSize = 0
		self.MountainSize = 0
		self.FieldSize = 0
		self.img_zoom_level_0 = pygame.image.load("assets/30px/{}.png".format("void")).convert_alpha()
		self.img_zoom_level_1 = pygame.image.load("assets/60px/{}.png".format("void")).convert_alpha()
		self.img_zoom_level_2 = pygame.image.load("assets/120px/{}.png".format("void")).convert_alpha()
		self.typeOfMaterial = ["none"]
		self.isExtension = False
		self.weDoNotMix = [""]

	def changeTile(self):
		self.img_zoom_level_0 = pygame.image.load("assets/30px/{}.png".format("void")).convert_alpha()
		self.img_zoom_level_1 = pygame.image.load("assets/60px/{}.png".format("void")).convert_alpha()
		self.img_zoom_level_2 = pygame.image.load("assets/120px/{}.png".format("void")).convert_alpha()

	def getForestSize(self):
		return (self.ForestSize)

	def getMountainSize(self):
		return (self.MountainSize)

	def getFieldSize(self):
		return (self.FieldSize)

	def getName(self):
		return (self.tileName)

	def onClick(self):
		print(self.X, self.Y, "j = ", round(self.j, 3))

	def smoothMap(self, map, x, y):
		listAdjacentCells = []
		try:
			tileName = map[x - 1][y].tileName
			tile2 = self.tileName if tileName not in self.weDoNotMix else "void"
			listAdjacentCells.append(tile2)
		except Exception as E:
			listAdjacentCells.append("void")
		try:
			tileName = map[x][y - 1].tileName
			tile2 = self.tileName if tileName not in self.weDoNotMix else "void"
			listAdjacentCells.append(tile2)
		except Exception as E:
			listAdjacentCells.append("void")
		try:
			tileName = map[x + 1][y].tileName
			tile2 = self.tileName if tileName not in self.weDoNotMix else "void"
			listAdjacentCells.append(tile2)
		except Exception as E:
			listAdjacentCells.append("void")
		try:
			tileName = map[x][y + 1].tileName
			tile2 = self.tileName if tileName not in self.weDoNotMix else "void"
			listAdjacentCells.append(tile2)
		except Exception as E:
			listAdjacentCells.append("void")

		print(listAdjacentCells)

		howManyMountains = listAdjacentCells.count(self.tileName)
		if (howManyMountains == 4):
			self.img = pygame.image.load("tiles/{}_four_side.png".format(self.tileName)).convert_alpha()
			self.img = pygame.transform.rotate(self.img, rotation_random())
		if (howManyMountains == 3):
			self.img = pygame.image.load("tiles/{}_three_side.png".format(self.tileName)).convert_alpha()
			positionAdjacentMountain = listAdjacentCells.index("void")
			listAngles = [90, 0, 270, 180, 270]
			self.img = pygame.transform.rotate(self.img, listAngles[positionAdjacentMountain])

		if (howManyMountains == 2):
			if ((listAdjacentCells[0] == "void" and listAdjacentCells[2] == "void") or 
				(listAdjacentCells[1] == "void" and listAdjacentCells[3] == "void")):
				self.img = pygame.image.load("tiles/{}_two_sides_alternative.png".format(self.tileName)).convert_alpha()
				if (listAdjacentCells[2] == self.tileName):
					self.img = pygame.transform.rotate(self.img, 90)
			else:
				self.img = pygame.image.load("tiles/{}_two_side.png".format(self.tileName)).convert_alpha()

				if (listAdjacentCells[0] == self.tileName and listAdjacentCells[1] == self.tileName):
					self.img = pygame.transform.rotate(self.img, 270)
				if (listAdjacentCells[3] == self.tileName and listAdjacentCells[0] == self.tileName):
					self.img = pygame.transform.rotate(self.img, 0)
				if (listAdjacentCells[3] == self.tileName and listAdjacentCells[2] == self.tileName):
					self.img = pygame.transform.rotate(self.img, 90)
				if (listAdjacentCells[1] == self.tileName and listAdjacentCells[2] == self.tileName):
					self.img = pygame.transform.rotate(self.img, 180)

		if (howManyMountains == 1):
			positionAdjacentMountain = listAdjacentCells.index(self.tileName)
			listAngles = [270, 180, 90, 0, 270]
			self.img = pygame.image.load("tiles/{}_one_side.png".format(self.tileName)).convert_alpha()
			self.img = pygame.transform.rotate(self.img, listAngles[positionAdjacentMountain])


class thevoid(tiles):
	def __init__(self, X, Y, j):
		tiles.__init__(self,  X, Y, j)
		self.tileName = "void"
		self.passable = False
		self.img_zoom_level_0 = pygame.image.load("assets/30px/{}.png".format("void")).convert_alpha()
		self.img_zoom_level_1 = pygame.image.load("assets/60px/{}.png".format("void")).convert_alpha()
		self.img_zoom_level_2 = pygame.image.load("assets/120px/{}.png".format("void")).convert_alpha()
		self.j = j
		self.weDoNotMix = [""]



class sea(tiles):
	def __init__(self, X, Y, j):
		tiles.__init__(self,  X, Y, j)
		self.tileName = "sea"
		self.passable = False
		self.img_zoom_level_0 = pygame.image.load("assets/30px/{}.png".format("sea")).convert_alpha()
		self.img_zoom_level_1 = pygame.image.load("assets/60px/{}.png".format("sea")).convert_alpha()
		self.img_zoom_level_2 = pygame.image.load("assets/120px/{}.png".format("sea")).convert_alpha()
		self.j = j
		self.typeOfMaterial = ["water"]
		self.weDoNotMix = ["land", "desert", "savanah"]

class reef(tiles):
	def __init__(self, X, Y, j):
		tiles.__init__(self,  X, Y, j)
		self.tileName = "reef"
		self.passable = False
		self.img_zoom_level_0 = pygame.image.load("assets/30px/{}.png".format("sea")).convert_alpha()
		self.img_zoom_level_1 = pygame.image.load("assets/60px/{}.png".format("sea")).convert_alpha()
		self.img_zoom_level_2 = pygame.image.load("assets/120px/{}.png".format("sea")).convert_alpha()
		self.j = j
		self.typeOfMaterial = ["water", "stone"]
		self.weDoNotMix = []

class island(tiles):
	def __init__(self, X, Y, j):
		tiles.__init__(self,  X, Y, j)
		self.tileName = "island"
		self.passable = True
		self.img_zoom_level_0 = pygame.image.load("assets/30px/{}.png".format("sea")).convert_alpha()
		self.img_zoom_level_1 = pygame.image.load("assets/60px/{}.png".format("sea")).convert_alpha()
		self.img_zoom_level_2 = pygame.image.load("assets/120px/{}.png".format("sea")).convert_alpha()
		self.j = j
		self.ForestSize = random.randint(15, 50)
		self.MountainSize = random.randint(15, 50)
		self.FieldSize = 100 - self.ForestSize - self.MountainSize
		self.typeOfMaterial = ["wood", "stone"]
		self.weDoNotMix = [""]

class island_ocean(tiles):
	def __init__(self, X, Y, j):
		tiles.__init__(self,  X, Y, j)
		self.tileName = "island_ocean"
		self.passable = True
		self.img_zoom_level_0 = pygame.image.load("assets/30px/{}.png".format("sea")).convert_alpha()
		self.img_zoom_level_1 = pygame.image.load("assets/60px/{}.png".format("sea")).convert_alpha()
		self.img_zoom_level_2 = pygame.image.load("assets/120px/{}.png".format("sea")).convert_alpha()
		self.j = j
		self.ForestSize = random.randint(15, 50)
		self.MountainSize = random.randint(15, 50)
		self.FieldSize = 100 - self.ForestSize - self.MountainSize
		self.typeOfMaterial = ["wood", "stone"]
		self.weDoNotMix = [""]


class ocean(tiles):
	def __init__(self, X, Y, j):
		tiles.__init__(self,  X, Y, j)
		self.tileName = "ocean"
		self.passable = False
		self.img_zoom_level_0 = pygame.image.load("assets/30px/{}.png".format("ocean")).convert_alpha()
		self.img_zoom_level_1 = pygame.image.load("assets/60px/{}.png".format("ocean")).convert_alpha()
		self.img_zoom_level_2 = pygame.image.load("assets/120px/{}.png".format("ocean")).convert_alpha()
		self.j = j
		self.typeOfMaterial = ["water"]
		self.weDoNotMix = [""]


class iceberg(tiles):
	def __init__(self,  X, Y, j):
		tiles.__init__(self,  X, Y, j)
		self.tileName = "iceberg"
		self.passable = False
		self.img_zoom_level_0 = pygame.image.load("assets/30px/{}.png".format("ocean")).convert_alpha()
		self.img_zoom_level_1 = pygame.image.load("assets/60px/{}.png".format("ocean")).convert_alpha()
		self.img_zoom_level_2 = pygame.image.load("assets/120px/{}.png".format("ocean")).convert_alpha()
		self.j = j
		self.typeOfMaterial = ["water", "ice"]
		self.weDoNotMix = ["land", "tundra", "desert", "savanah"]

class hills(tiles):
	def __init__(self,  X, Y, j):
		tiles.__init__(self,  X, Y, j)
		self.tileName = "hills"
		self.passable = True
		self.ForestSize = random.randint(15, 50)
		self.FieldSize = 100 - self.ForestSize
		self.img_zoom_level_0 = pygame.image.load("assets/30px/{}.png".format("hills")).convert_alpha()
		self.img_zoom_level_1 = pygame.image.load("assets/60px/{}.png".format("hills")).convert_alpha()
		self.img_zoom_level_2 = pygame.image.load("assets/120px/{}.png".format("hills")).convert_alpha()
		self.j = j
		self.typeOfMaterial = ["stone"]
		self.weDoNotMix = [""]


class forest(tiles):
	def __init__(self,  X, Y, j):
		tiles.__init__(self,  X, Y, j)
		self.tileName = "forest"
		self.ForestSize = random.randint(80, 100)
		self.FieldSize = 100 - self.ForestSize
		self.img_zoom_level_0 = pygame.image.load("assets/30px/{}.png".format("forest")).convert_alpha()
		self.img_zoom_level_1 = pygame.image.load("assets/60px/{}.png".format("forest")).convert_alpha()
		self.img_zoom_level_2 = pygame.image.load("assets/120px/{}.png".format("forest")).convert_alpha()
		self.j = j
		self.typeOfMaterial = ["wood", "land"]
		self.weDoNotMix = [""]

class jungle(tiles):
	def __init__(self,  X, Y, j):
		tiles.__init__(self,  X, Y, j)
		self.tileName = "jungle"
		self.ForestSize = random.randint(80, 100)
		self.FieldSize = 100 - self.ForestSize
		self.img_zoom_level_0 = pygame.image.load("assets/30px/{}.png".format("jungle")).convert_alpha()
		self.img_zoom_level_1 = pygame.image.load("assets/60px/{}.png".format("jungle")).convert_alpha()
		self.img_zoom_level_2 = pygame.image.load("assets/120px/{}.png".format("jungle")).convert_alpha()
		self.j = j
		self.typeOfMaterial = ["water", "wood", "land"]

class tundra(tiles):
	def __init__(self,  X, Y, j):
		tiles.__init__(self,  X, Y, j)
		self.tileName = "tundra"
		self.ForestSize = random.randint(80, 100)
		self.FieldSize = 100 - self.ForestSize
		self.img_zoom_level_0 = pygame.image.load("assets/30px/{}.png".format("forest")).convert_alpha()
		self.img_zoom_level_1 = pygame.image.load("assets/60px/{}.png".format("forest")).convert_alpha()
		self.img_zoom_level_2 = pygame.image.load("assets/120px/{}.png".format("forest")).convert_alpha()
		self.j = j
		self.typeOfMaterial = ["land", "ice", "land"]

class taiga(tiles):
	def __init__(self,  X, Y, j):
		tiles.__init__(self,  X, Y, j)
		self.tileName = "taiga"
		self.ForestSize = random.randint(80, 100)
		self.FieldSize = 100 - self.ForestSize
		self.img_zoom_level_0 = pygame.image.load("assets/30px/{}.png".format("forest")).convert_alpha()
		self.img_zoom_level_1 = pygame.image.load("assets/60px/{}.png".format("forest")).convert_alpha()
		self.img_zoom_level_2 = pygame.image.load("assets/120px/{}.png".format("forest")).convert_alpha()
		self.j = j
		self.typeOfMaterial = ["wood", "ice", "land"]

class swamp(tiles):
	def __init__(self,  X, Y, j):
		tiles.__init__(self,  X, Y, j)
		self.tileName = "swamp"
		self.ForestSize = random.randint(0, 10)
		self.FieldSize = random.randint(0, 10)
		self.img_zoom_level_0 = pygame.image.load("assets/30px/{}.png".format("swamp")).convert_alpha()
		self.img_zoom_level_1 = pygame.image.load("assets/60px/{}.png".format("swamp")).convert_alpha()
		self.img_zoom_level_2 = pygame.image.load("assets/120px/{}.png".format("swamp")).convert_alpha()
		self.j = j
		self.typeOfMaterial = ["water", "wood"]

class desert(tiles):
	def __init__(self,  X, Y, j):
		tiles.__init__(self,  X, Y, j)
		self.tileName = "desert"
		self.ForestSize = 0
		self.FieldSize = 100 - self.ForestSize
		self.img_zoom_level_0 = pygame.image.load("assets/30px/{}.png".format("desert")).convert_alpha()
		self.img_zoom_level_1 = pygame.image.load("assets/60px/{}.png".format("desert")).convert_alpha()
		self.img_zoom_level_2 = pygame.image.load("assets/120px/{}.png".format("desert")).convert_alpha()
		self.j = j
		self.typeOfMaterial = ["desert"]
		self.weDoNotMix = ["sea", "ocean", "reef", "iceberg"]

class savanah(tiles):
	def __init__(self,  X, Y, j):
		tiles.__init__(self,  X, Y, j)
		self.tileName = "savanah"
		self.ForestSize = random.randint(0, 10)
		self.FieldSize = 100 - self.ForestSize
		self.color = "#"
		self.img_zoom_level_0 = pygame.image.load("assets/30px/{}.png".format("savanah")).convert_alpha()
		self.img_zoom_level_1 = pygame.image.load("assets/60px/{}.png".format("savanah")).convert_alpha()
		self.img_zoom_level_2 = pygame.image.load("assets/120px/{}.png".format("savanah")).convert_alpha()
		self.j = j
		self.typeOfMaterial = ["wood", "desert"]
		self.weDoNotMix = ["sea", "ocean", "reef", "iceberg"]



class lake(tiles):
	def __init__(self,  X, Y, j):
		tiles.__init__(self,  X, Y, j)
		self.tileName = "lake"
		self.ForestSize = random.randint(0, 20)
		self.FieldSize = 100 - self.ForestSize
		self.color = "#"
		self.img_zoom_level_0 = pygame.image.load("assets/30px/{}.png".format("lake")).convert_alpha()
		self.img_zoom_level_1 = pygame.image.load("assets/60px/{}.png".format("lake")).convert_alpha()
		self.img_zoom_level_2 = pygame.image.load("assets/120px/{}.png".format("lake")).convert_alpha()
		self.j = j
		self.typeOfMaterial = ["water"]

class land(tiles):
	def __init__(self,  X, Y, j):
		tiles.__init__(self,  X, Y, j)
		self.tileName = "land"
		self.ForestSize = random.randint(0, 20)
		self.FieldSize = 100 - self.ForestSize
		self.color = "#"
		self.img_zoom_level_0 = pygame.image.load("assets/30px/{}.png".format("land")).convert_alpha()
		self.img_zoom_level_1 = pygame.image.load("assets/60px/{}.png".format("land")).convert_alpha()
		self.img_zoom_level_2 = pygame.image.load("assets/120px/{}.png".format("land")).convert_alpha()
		self.j = j
		self.typeOfMaterial = ["land"]
		self.weDoNotMix = ["sea", "ocean", "reef", "iceberg"]

class snowy_hills(tiles):
	def __init__(self,  X, Y, j):
		tiles.__init__(self,  X, Y, j)
		self.tileName = "snowy_hills"
		self.ForestSize = 0
		self._fieldSize = 10
		self.img_zoom_level_0 = pygame.image.load("assets/30px/{}.png".format("hills")).convert_alpha()
		self.img_zoom_level_1 = pygame.image.load("assets/60px/{}.png".format("hills")).convert_alpha()
		self.img_zoom_level_2 = pygame.image.load("assets/120px/{}.png".format("hills")).convert_alpha()
		self.j = j
		self.typeOfMaterial = ["stone", "ice"]

class mountain(tiles):
	def __init__(self, X, Y, j):
		tiles.__init__(self,  X, Y, j)
		self.tileName = "mountain"
		self.ForestSize = 0
		self.passable = False

		self.img_zoom_level_0 = pygame.image.load("assets/30px/{}.png".format("mountain")).convert_alpha()
		self.img_zoom_level_1 = pygame.image.load("assets/60px/{}.png".format("mountain")).convert_alpha()
		self.img_zoom_level_2 = pygame.image.load("assets/120px/{}.png".format("mountain")).convert_alpha()
	
		self.j = j
		self.typeOfMaterial = ["stone", "ice"]
		self.weDoNotMix = ["snowy_hills", "land", "lake", "savanah", "tundra", "desert", "swamp", "taiga", "jungle", "forest", "colline", "iceberg"]

