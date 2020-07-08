from sudoku import *
from board import *
from keyPad import *
from scene import *
from menu import *
from adjustColor import *
import math

def muchLarger(x,y):
	return x > y*1.2

class sudokuGui(Scene):
	
	def setup(self):
		#build board
		self.color = 'white'
		self.hex = '#1768ff'
		self.background_color = self.hex
		self.fitScreen()
		self.board = Board((9,9),self.hex,self.square,stroke_color=self.color,parent=self,position=self.boardPos)
		#build keypad
		self.keyPad = KeyPad(self.hex,self.rect,stroke_color=self.color,fill_color='clear',parent=self,position=self.keyPadPos)
		#build menu
		self.menuItems = "easy medium hard".split(" ")
		self.prompt = 'Play Again?'
		self.dims = [400,300,250,50]
		self.menu = Menu(adjustColor(self.hex,1.2),self.prompt,self.menuItems,self.dims,stroke_color='white')
		self.placeMenu()
		
	def placeMenu(self):
		(w,h) = self.size
		self.add_child(self.menu)
		self.menu.position = (w/2,h/2)
		self.menu.placeMenuItems()
		
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
		if self.menu.isActive:
			button = self.menu.isButtonPressed(touch)
			if button:
				self.initializeBoard(button.id)
				self.menu.isActive = False
				self.menu.remove_from_parent()
				button.deactivate()
		else:
			self.keyPad.isModeButtonPressed(touch)
			if self.board.isSpacePressed(touch) and self.keyPad.activeButton and self.keyPad.activeButton.id == 'erase':
				self.board.eraseSpaceContents()
			elif self.keyPad.activeButton and self.board.activeSpace:
				numberButton = self.keyPad.isNumberButtonPressed(touch)
				if numberButton:
					if self.keyPad.activeButton.id == 'write':
						self.board.placeGuess(numberButton)
						self.checkSolution()
					elif self.keyPad.activeButton.id == 'note':
						self.board.placeNote(numberButton)
		
	def touch_ended(self,touch):
		self.keyPad.isNotPressed()
		
	def initializeBoard(self,difficulty):
		self.board.clearSpaces()
		self.sudoku = Sudoku(difficulty)
		self.board.fillSpaces(self.sudoku.grid)
		
	def checkSolution(self):
		isSolved = True
		for space in self.board.spaces:
			(j,i) = space.index
			if self.sudoku.grandSolution[j][i] != int(space.charactar.text):
				isSolved = False
				break
		if isSolved:
			self.placeMenu()
		
run(sudokuGui())
