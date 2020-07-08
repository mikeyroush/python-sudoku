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
		self.calculate_dimensions()
		self.fit_board_to_screen()
		self.board = Board((9,9),self.hex,self.boardShape,stroke_color=self.color,parent=self,position=self.boardPos)
		#build keypad
		self.fit_keypad_to_screen()
		self.keyPad = KeyPad(self.hex,self.keyPadShape,stroke_color=self.color,fill_color='clear',parent=self,position=self.keyPadPos)
		#build menu
		self.menuItems = "easy medium hard".split(" ")
		self.prompt = 'Play Again?'
		self.dims = [400,300,250,50]
		self.menu = Menu(adjustColor(self.hex,1.2),self.prompt,self.menuItems,self.dims,stroke_color='white')
		self.place_menu()
		
	def place_menu(self):
		(w,h) = self.size
		self.add_child(self.menu)
		self.menu.isActive = True
		self.menu.position = (w/2,h/2)
		self.menu.placeMenuItems()
		
	def did_change_size(self):
		self.calculate_dimensions()
		self.fit_board_to_screen()
		self.board.path = self.boardShape
		self.board.position = self.boardPos
		self.board.placeSpaces()
		self.board.placeBorders()
		self.fit_keypad_to_screen()
		self.keyPad.path = self.keyPadShape
		self.keyPad.position = self.keyPadPos
		self.keyPad.placeButtons()
		
	def calculate_dimensions(self):
		self.margin = 40
		self.largeSide = max(self.size.w,self.size.h)
		self.smallSide = min(self.size.w,self.size.h)
		if muchLarger(self.largeSide,self.smallSide):
			self.availableSize = self.smallSide
		else:
			self.availableSize = 2/3 * self.smallSide
		self.sideDiff = max(self.largeSide - self.smallSide, self.largeSide - self.availableSize)
		
	def fit_board_to_screen(self):
		#size and placement for board
		self.boardPos = (self.availableSize/2, self.size.h - self.availableSize/2)	
		size = self.availableSize - 2*self.margin
		self.boardShape = ui.Path.rect(0,0,size,size)
		
	def fit_keypad_to_screen(self):
		#size and placement for keypad
		keyPadSize = min(math.floor(0.85 * self.sideDiff),self.availableSize - 2*self.margin)
		if muchLarger(self.size.h,self.size.w):
			self.keyPadPos=(self.size.w/2, self.size.h - self.availableSize - self.sideDiff/2 + self.margin/2)
		else:
			self.keyPadPos=(self.size.w - self.sideDiff/2 - self.margin/2, self.size.h - self.availableSize/2)
		self.keyPadShape = ui.Path.rect(0,0,keyPadSize,keyPadSize)		
	
	def touch_began(self,touch):
		#if the menu is active, check for menu button presses
		if self.menu.isActive:
			self.menu.isButtonPressed(touch)
			
		#otherwise, check for keypad and space presses
		else:
			self.keyPad.isSolveButtonPressed(touch)
			self.keyPad.isModeButtonPressed(touch)
			if self.board.isSpacePressed(touch) and self.keyPad.activeButton and self.keyPad.activeButton.id == 'erase':
				self.board.eraseSpaceContents()
			elif self.keyPad.activeButton and self.board.activeSpace:
				numberButton = self.keyPad.isNumberButtonPressed(touch)
				if numberButton:
					if self.keyPad.activeButton.id == 'write':
						self.board.placeGuess(numberButton)
						self.check_solution()
					elif self.keyPad.activeButton.id == 'note':
						self.board.placeNote(numberButton)
		
	def touch_ended(self,touch):
		#deactivate buttons and solve game if user gives up
		buttonID = self.keyPad.isNotPressed()
		if buttonID == 'Solve':
			self.solve_game()
		
		#start new game with selected difficulty
		difficulty = self.menu.isNotPressed()
		if difficulty != None:
				self.initialize_board(difficulty)
				self.menu.isActive = False
				self.menu.remove_from_parent()
		
	def initialize_board(self,difficulty):
		self.board.clearSpaces()
		self.sudoku = Sudoku(difficulty)
		self.board.fillSpaces(self.sudoku.grid)
		
	def check_solution(self):
		isSolved = True
		for space in self.board.spaces:
			(j,i) = space.index
			if str(self.sudoku.grandSolution[j][i]) != space.charactar.text:
				isSolved = False
				break
		if isSolved:
			self.place_menu()
			
	def solve_game(self):
		for space in self.board.spaces:
			(j,i) = space.index
			if str(self.sudoku.grandSolution[j][i]) != space.charactar.text:
				space.fillLocked(self.sudoku.grandSolution[j][i],'#8734f2')
		
run(sudokuGui())
