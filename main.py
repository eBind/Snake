import os
import time
import random
from colorama import Fore, Style


lefts = {
	"right": "top",
	"top": "left",
	"left": "bottom",
	"bottom": "right"
}

rights = {
	"right": "bottom",
	"top": "right",
	"left": "top",
	"bottom": "left"
}

directions = {
	"right": 0,
	"top": 1,
	"left": 2,
	"bottom": 3
}


def main():
	worm = Worm(2, "██", Fore.CYAN + "██" + Style.RESET_ALL)
	stadion = Stadion(40, 20, Fore.RED + "██" + Style.RESET_ALL)
	
	stadion.setworm(worm)
	stadion.genfood()
	stadion.update()

	while True:
		direct = input("[A|D] ")

		if direct in ["ф", "a", "^[[D"]:
			stadion.moveworm(lefts[worm.direction])

		elif direct in ["в", "d", "^[[C"]:
			stadion.moveworm(rights[worm.direction])

		else:
			stadion.moveworm(worm.direction)


class Worm:
	def __init__(self, length, body, head):
		self.length = length
		self.body = body
		self.head = head

		self.coords = []
		self.direction = "right"


class Stadion:
	def __init__(self, width, height, foodblock="██", field="  "):
		self.width = width
		self.height = height
		self.field = field

		self.foodcoord = None
		self.foodblock = foodblock
	
	
	def update(self):
		os.system("clear")
		print("▐▛" + "▀▀" * self.width + "▜▌")
		
		for y in range(0, self.height):
			print("▐▌", end='')
			
			for x in range(0, self.width):
				if self.worm.coords[-1] == (x, y):
					print(self.worm.head, end='')

				elif (x, y) in self.worm.coords:
					print(self.worm.body, end='')

				elif self.foodcoord == (x, y):
					print(self.foodblock, end='')

				else:
					print(self.field, end='')
			
			print("▐▌")
		
		print("▐▙" + "▄▄" * self.width + "▟▌")
	
	
	def setworm(self, worm):
		self.worm = worm
		
		for coord in range(1, self.worm.length + 2):
			self.worm.coords.append((coord, 1))
			
		return self.worm.coords
	
	
	def moveworm(self, direction="right"):
		self.worm.direction = direction

		firstcoord = None
		food = False


		def action(number, types="-", axis="x"):
			if types == "-": result = number - 1
			else: result = number + 1

			if axis == "x": maximal = self.width - 1
			else: maximal = self.height - 1

			if result < 0: return maximal
			elif result > maximal: return 0

			return result

		
		for index, coord in enumerate(self.worm.coords):
			if index == 0:
				firstcoord = coord

			try:
				self.worm.coords[index] = self.worm.coords[index + 1]

			except:
				if self.worm.direction == "right":
					new = (action(coord[0], '+', 'x'), coord[1])
				
				elif self.worm.direction == "left":
					new = (action(coord[0], '-', 'x'), coord[1])
				
				elif self.worm.direction == "top":
					new = (coord[0], action(coord[1], '-', 'y'))
				
				elif self.worm.direction == "bottom":
					new = (coord[0], action(coord[1], '+', 'y'))


				if new in self.worm.coords:
					raise SystemExit

				elif self.foodcoord == new:
					food = True

				self.worm.coords[index] = new

		if food:
			self.genfood()
			self.worm.length += 1
			self.worm.coords.insert(0, firstcoord)
			
		self.update()
	
	
	def genfood(self):
		randx = random.randint(0, self.width - 1)
		randy = random.randint(0, self.height - 1)

		if (randx, randy) not in self.worm.coords:
			self.foodcoord = (randx, randy)
			return self.foodcoord

		else:
			return self.genfood()


if __name__ == "__main__":
	main()