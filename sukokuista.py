from sudoku import *
from board import *
from scene import *

class sudokuGui(Scene):
	
	def setup(self):
		#build board
		self.color = 'white'
		hex = '#1768ff'
		self.background_color = hex
		self.sudoku = Sudoku()
		self.fitScreen()
		self.board = Board((9,9),hex,self.square,stroke_color=self.color,parent=self,position=self.boardPos)
		self.initializeBoard()
		
	def did_change_size(self):
		self.fitScreen()
		self.board.path = self.square
		self.board.position = self.boardPos
		self.board.placeSpaces()
		
	def fitScreen(self):
		#calc dimensions
		margin = 40
		if self.size.w > self.size.h:
			self.boardPos = (self.size.h/2, self.size.h/2 )
			available_size = self.size.h
		else:
			self.boardPos = (self.size.w/2, self.size.h - self.size.w/2 )
			available_size = self.size.w
		size = available_size - 2*margin
		self.square = ui.Path.rect(0,0,size,size)
		
	def touch_began(self,touch):
		self.board.isSpaceTouched(touch)
		
	def initializeBoard(self):
		self.board.fillSpaces(self.sudoku.grid)
		
run(sudokuGui())
