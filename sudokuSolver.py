import numpy as np

#test grid
grid = [[5,3,0,0,7,0,0,0,0],
		[6,0,0,1,9,5,0,0,0],
		[0,9,8,0,0,0,0,6,0],
		[8,0,0,0,6,0,0,0,3],
		[4,0,0,8,0,3,0,0,1],
		[7,0,0,0,2,0,0,0,6],
		[0,6,0,0,0,0,2,8,0],
		[0,0,0,4,1,9,0,0,5],
		[0,0,0,0,8,0,0,7,9]]
		
#see if a number is possible at a given position
def possible(y, x, n):
	global grid
	#see if the number already exists in the row
	for i in range(9):
		if grid[y][i] == n:
			return False
	#see if the number already exists in the column
	for i in range(9):
		if grid[i][x] == n:
			return False
	#find the base position of a given square
	x0 = (x//3) * 3
	y0 = (y//3) * 3
	#see if the number already exists in the square
	for i in range(3):
		for j in range(3):
			if grid[y0 + i][x0 + j] == n:
				return False
	return True

#test all spots with all possible numbers and backtrack if need be
def solve():
	global grid
	for y in range(9):
		for x in range(9):
			if grid[y][x] == 0:
				for n in range(1,10):
					if possible(y,x,n):
						grid[y][x] = n
						solve()
						grid[y][x] = 0
				return #backtrack if nothing is possible
	print(np.matrix(grid))
	input("More?")
	
#Main
solve()
