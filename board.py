from scene import *
from adjustColor import *
from touch import *
import math

class Space(ShapeNode):
	def __init__(self,index,hex,*args,**kwargs):
		ShapeNode.__init__(self,*args,**kwargs)
		self.fill_color = hex
		mainFont = ('Helvetica', min(self.size.w,self.size.h)*0.9)
		noteFont = ('Helvetica', min(self.size.w,self.size.h)*0.25)
		startCharacter = ""
		self.charactar = LabelNode(startCharacter,font=mainFont,parent=self)
		self.locked = False
		self.index = index
		self.hex = hex
		self.notes = [LabelNode(startCharacter,font=noteFont,parent=self) for i in range(4)]
		self.placeNotes()
		self.noteIndex = 0
		
	def isPressed(self,point):
		if not self.locked:
			return isTouched(self,point)
		return False
		
	def adjustFont(self):
		mainFont = ('Helvetica', min(self.size.w,self.size.h)*0.9)
		noteFont = ('Helvetica', min(self.size.w,self.size.h)*0.25)
		self.charactar.font = mainFont
		for note in self.notes:
			note.font = noteFont
		self.placeNotes()
		
	def placeNotes(self):
		for i, note in enumerate(self.notes):
			note.position=(-self.size.w/2+(1/2+i%2)*note.font[1],self.size.h/2-(1/2+i//2)*note.font[1])
		
	def fillLocked(self, char, color=None):
		self.locked = True
		self.fill(char)
		if color == None:
			color = adjustColor(self.hex, 1.2)
		self.fill_color = color
		
	def fill(self, char):
		self.eraseNote()
		self.charactar.text = str(char)		
		
	def fillNote(self, char):
		self.eraseGuess()
		if self.noteIndex >= 4:
			self.noteIndex = 0
		self.notes[self.noteIndex].text = str(char)
		self.noteIndex += 1
		
	def clear(self):
		self.erase()
		self.locked = False
		self.fill_color = self.hex
		
	def erase(self):
		self.eraseGuess()
		self.eraseNote()
			
	def eraseGuess(self):
		self.charactar.text = ""		
		
	def eraseNote(self):
		for note in self.notes:
			note.text = ""		
		
	def activate(self):
		self.fill_color = adjustColor(self.hex, 0.75)
		
	def deactivate(self):
		self.fill_color = self.hex
		
class Border(ShapeNode):
	def __init__(self,*args,**kwargs):
		ShapeNode.__init__(self,*args,**kwargs)
		self.dimensions = tuple(None for _ in range(4))
		
	def draw(self):
		(x,y,dx,dy) = self.dimensions
		#draw line and return ShapeNode
		line = ui.Path()
		line.line_width = max(dx,dy)/80
		line.move_to(0,0)
		line.line_to(dx,dy)
		line.close()
		self.path = line
		self.position = (x,y)
		
class Board(ShapeNode):
	def __init__(self,layout,hex,*args,**kwargs):
		ShapeNode.__init__(self,*args,**kwargs)
		self.fill_color = hex
		(self.rows,self.cols) = layout
		self.divsX = int(math.sqrt(self.cols))
		self.divsY = int(math.sqrt(self.rows))
		self.spaces = [Space((j,i),hex,stroke_color=self.stroke_color,parent=self) for i in range(self.cols) for j in range(self.rows)]
		self.vertBorders = [Border(parent=self,stroke_color=self.stroke_color) for _ in range(1,self.divsX)]
		self.horzBorders = [Border(parent=self,stroke_color=self.stroke_color) for _ in range(1,self.divsY)]
		self.activeSpace = None		
		self.placeSpaces()
		self.placeBorders()
		
	def placeSpaces(self):	
		self.rowSize = self.size.h/self.rows
		self.colSize = self.size.w/self.cols
		for space in self.spaces:
			square = ui.Path.rect(0,0,self.rowSize,self.colSize)
			pos = self.calcDimensions(space.index)
			space.path = square
			space.position = pos
			space.adjustFont()
			
	def placeBorders(self):
		for i, border in enumerate(self.vertBorders,1):
			x = i*self.size.w/self.divsX - self.size.w/2
			dimensions = (x,0,0,self.size.h)
			border.dimensions = dimensions
			border.draw()
		for j, border in enumerate(self.horzBorders,1):
			y = j*self.size.h/self.divsY - self.size.h/2
			dimensions = (0,y,self.size.w,0)
			border.dimensions = dimensions
			border.draw()
							
	def calcDimensions(self,index):
		(j,i) = index
		x = -self.size.w/2 + self.rowSize/2 + i*self.rowSize
		y = +self.size.h/2 - self.colSize/2 - j*self.colSize
		return (x,y)
		
	def isSpacePressed(self,touch):
		point = self.point_from_scene(touch.location)
		for space in self.spaces:
			if space.isPressed(point):
				self.makeActive(space)
				return True
				
	def makeActive(self, space):
		if self.activeSpace:
			self.activeSpace.deactivate()
		self.activeSpace = space
		self.activeSpace.activate()
		
	def fillSpaces(self,grid):
		for space in self.spaces:
			(j,i) = space.index
			if grid[j][i] != 0:
				space.fillLocked(grid[j][i])
				
	def clearSpaces(self):
		for space in self.spaces:
			space.clear()
				
	def placeGuess(self, button):
		self.activeSpace.fill(button.id)
		
	def placeNote(self, button):
		self.activeSpace.fillNote(button.id)
		
	def eraseSpaceContents(self):
		self.activeSpace.erase()
