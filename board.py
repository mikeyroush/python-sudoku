from scene import *
from colorsys import rgb_to_hls, hls_to_rgb
from matplotlib.colors import hex2color
import math

class Space(ShapeNode):
	def __init__(self,index,hex,*args,**kwargs):
		ShapeNode.__init__(self,*args,**kwargs)
		self.fill_color = hex
		font = ('Helvetica', min(self.size.w,self.size.h)*0.9)
		startCharacter = ""
		self.charactar = LabelNode(startCharacter,font=font,parent=self)
		self.locked = False
		self.index = index
		self.hex = hex
		
	def isTouched(self,point):
		if not self.locked:
			(x,y) = point
			(X,Y) = self.position
			bound = self.size.w/2
			return X - bound < x and X + bound > x and Y - bound < y and Y + bound > y
		return False
		
	def fill(self, char):
		self.locked = True
		self.charactar.text = str(char)
		self.adjustColor(1.2)
		
	def activate(self):
		self.adjustColor(0.75)
		#self.fill_color = 'grey'
		
	def deactivate(self):
		self.fill_color = self.parent.fill_color
		
	def adjustColor(self,factor):
		#convert hex to hls
		(r,g,b) = hex2color(self.hex)
		(h,l,s) = rgb_to_hls(r,g,b)
		#adjust color
		l = max(min(l * factor, 1.0), 0.0)
		#convert back
		(r,g,b) = hls_to_rgb(h,l,s)
		(r,g,b) = int(r*255),int(g*255),int(b*255)
		hex = '#{:02x}{:02x}{:02x}'.format(r,g,b)
		self.fill_color = hex
		
class Border(ShapeNode):
	def __init__(self,dimensions,*args,**kwargs):
		ShapeNode.__init__(self,*args,**kwargs)
		(x,y,dx,dy) = dimensions
		#draw line and return ShapeNode
		line = ui.Path()
		line.line_width = 10
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
		self.rowSize = self.size.h/self.rows
		self.colSize = self.size.w/self.cols
		self.spaces = [Space((j,i),hex,stroke_color=self.stroke_color,parent=self) for i in range(self.cols) for j in range(self.rows)]
		self.activeSpace = None		
		self.placeSpaces()
		self.placeBorders()
		
	def placeSpaces(self):	
		for space in self.spaces:
			square = ui.Path.rect(0,0,self.rowSize,self.colSize)
			pos = self.calcDimensions(space.index)
			space.path = square
			space.position = pos
			
	def placeBorders(self):
		divsX = int(math.sqrt(self.cols))
		divsY = int(math.sqrt(self.rows))
		for i in range(1,divsX):
			x = i*self.size.w/divsX - self.size.w/2
			dimensions = (x,0,0,self.size.h)
			border = Border(dimensions,parent=self,stroke_color=self.stroke_color)
		for j in range(1,divsY):
			y = j*self.size.h/divsY - self.size.h/2
			dimensions = (0,y,self.size.w,0)
			border = Border(dimensions,parent=self,stroke_color=self.stroke_color)
				
	def calcDimensions(self,index):
		(j,i) = index
		x = -self.size.w/2 + self.rowSize/2 + i*self.rowSize
		y = +self.size.h/2 - self.colSize/2 - j*self.colSize
		return (x,y)
		
	def isSpaceTouched(self,touch):
		point = self.point_from_scene(touch.location)
		for space in self.spaces:
			if space.isTouched(point):
				self.makeActive(space)
				
	def makeActive(self, space):
		if self.activeSpace:
			self.activeSpace.deactivate()
		self.activeSpace = space
		self.activeSpace.activate()
		
	def fillSpaces(self,grid):
		for space in self.spaces:
			(j,i) = space.index
			if grid[j][i] != 0:
				space.fill(grid[j][i])
