import numpy as np
from random import choice, randrange
from copy import deepcopy

class Sudoku:
	
	def __init__(self):
		#test grid
		"""self.grid = [[5,3,0,0,7,0,0,0,0],
					[6,0,0,1,9,5,0,0,0],
					[0,9,8,0,0,0,0,6,0],
					[8,0,0,0,6,0,0,0,3],
					[4,0,0,8,0,3,0,0,1],
					[7,0,0,0,2,0,0,0,6],
					[0,6,0,0,0,0,2,8,0],
					[0,0,0,4,1,9,0,0,5],
					[0,0,0,0,8,0,0,7,9]]"""
		self.blanks = randrange(40,50)
		self.solutions = []
		self.grandSolution = None
		self.grid = None
		self.generateGrid()
		
	def generateGrid(self):
		#initialize grid with 0s
		self.grid = [[0 for _ in range(9)] for _ in range(9)]
		#fill in diagonal squares
		for i in range(0,9,3):
			self.fillSquare(i,i)
		#find possible solutions
		self.solve()
		#pick a solution
		self.grid = deepcopy(choice(self.solutions))
		self.grandSolution = deepcopy(self.grid)
		self.solutions = []
		#remove spots from grid
		self.removeSpots(self.blanks)
		
	def fillSquare(self, y, x):
		x0 = (x//3) * 3
		y0 = (y//3) * 3
		choices = [i for i in range(1,10)]
		for i in range(3):
			for j in range(3):
				num = choice(choices)
				self.grid[y0 + i][x0 + j] = num
				choices.remove(num)
		
	#test all spots with all possible numbers and backtrack if need be
	def solve(self):
		if len(self.solutions) == 3:
			return 
		for y in range(9):
			for x in range(9):
				if self.grid[y][x] == 0:
					for n in range(1,10):
						if self.possible(y,x,n):
							self.grid[y][x] = n
							self.solve()
							self.grid[y][x] = 0
					return #backtrack if nothing is possible
		self.solutions.append(deepcopy(self.grid))
		
	def removeSpots(self, depth):
		if depth == 0:
			return
		depth -= 1
		y = randrange(9)
		x = randrange(9)
		while(self.grid[y][x]==0):
			y = randrange(9)
			x = randrange(9)
		backup = self.grid[y][x]
		self.grid[y][x] = 0
		self.solve()
		if len(self.solutions) > 1:
			self.grid[y][x] = backup
			depth += 1
		self.solutions = []
		self.removeSpots(depth)
			
	#see if a number is possible at a given position
	def possible(self, y, x, n):
		#see if the number already exists in the row
		if self.inRow(y, n):
			return False
		#see if the number already exists in the column
		if self.inCol(x, n):
			return False
		#see if the number already exists in the square
		if self.inSquare(y, x, n):
			return False
		#otherwise the number is possible
		return True
		
	def inRow(self, y, n):
		for i in range(9):
			if self.grid[y][i] == n:
				return True
		
	def inCol(self, x, n):
		for i in range(9):
			if self.grid[i][x] == n:
				return True
		
	def inSquare(self, y, x, n):
		#find the base position of a given square
		x0 = (x//3) * 3
		y0 = (y//3) * 3
		for i in range(3):
			for j in range(3):
				if self.grid[y0 + i][x0 + j] == n:
					return True
					
	def checkSolution(self):
		for y in range(len(self.grid)):
			for x in range(len(self.grid)):
				if self.grid[y][x] != self.grandSolution[y][x]:
					return False
		return True
		
#Main
#sudoku = Sudoku()
#print(np.matrix(sudoku.grid))
#print(np.matrix(sudoku.grandSolution))
