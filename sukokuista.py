from sudoku import *
from board import *
from keyPad import *
from scene import *
import math

def muchLarger(x,y):
	return x > y*1.2

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
		self.keyPad = KeyPad(hex,self.rect,stroke_color=self.color,fill_color='clear',parent=self,position=self.keyPadPos)
		self.winText = LabelNode()
		
	def did_change_size(self):
		self.fitScreen()
		self.board.path = self.square
		self.board.position = self.boardPos
		self.board.placeSpaces()
		self.board.placeBorders()
		self.keyPad.path = self.rect
		self.keyPad.position = self.keyPadPos
		self.keyPad.placeButtons()
		
	def fitScreen(self):
		#calc dimensions for board
		margin = 40
		largeSide = max(self.size.w,self.size.h)
		smallSide = min(self.size.w,self.size.h)
		sideDiff = largeSide - smallSide
		if muchLarger(largeSide,smallSide):
			availableSize = smallSide
		else:
			availableSize = 2/3 * smallSide
		self.boardPos = (availableSize/2, self.size.h - availableSize/2)	
		size = availableSize - 2*margin
		self.square = ui.Path.rect(0,0,size,size)
		
		#calc dimensions for keypad
		#needs some work
		if muchLarger(self.size.h,self.size.w):
			height = math.floor(0.9 * sideDiff)
			width = 4*height/3
			self.keyPadPos=(self.size.w/2, self.size.h - availableSize - sideDiff/2 + margin/2)
		else:
			width = math.floor(0.9 * sideDiff)
			height = 4*width/3
			self.keyPadPos=(self.size.w - sideDiff/2 - margin/2, self.size.h - availableSize/2)
		self.rect = ui.Path.rect(0,0,width,height)		
		
		#calc font size
		#self.mainFont = ('Helvetica', 	
	
	def touch_began(self,touch):
		self.keyPad.isModeButtonPressed(touch)
		if self.board.isSpacePressed(touch) and self.keyPad.activeButton and self.keyPad.activeButton.id == 'erase':
			self.board.eraseSpaceContents()
		elif self.keyPad.activeButton and self.board.activeSpace:
			numberButton = self.keyPad.isNumberButtonPressed(touch)
			if numberButton:
				if self.keyPad.activeButton.id == 'write':
					self.board.placeGuess(numberButton)
				elif self.keyPad.activeButton.id == 'note':
					self.board.placeNote(numberButton)
		
	def touch_ended(self,touch):
		self.keyPad.isNotPressed()
		
	def initializeBoard(self):
		self.board.fillSpaces(self.sudoku.grid)
		
run(sudokuGui())
