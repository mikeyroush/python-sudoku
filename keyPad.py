from scene import *
from button import *
from touch import *


class KeyPad(ShapeNode):
	def __init__(self,hex,*args,**kwargs):
		ShapeNode.__init__(self,*args,**kwargs)
		self.buttonHeight = self.size.h/4
		buttonShapeDefault = ui.Path.rect(0,0,self.buttonHeight,self.buttonHeight)
		buttonShapeSolve = ui.Path.rect(0,0,self.size.w,self.buttonHeight)
		self.numberButtons = [Button(i,hex,buttonShapeDefault,stroke_color='white',parent=self,position=(i*10,i*10)) for i in range(1,10)]
		buttonNames = "write note erase"
		buttonNames = buttonNames.split(" ")
		self.modeButtons = [Button(buttonNames[i],hex,buttonShapeDefault,stroke_color='white',parent=self,position=(i*10,i*10)) for i in range(len(buttonNames))]
		self.activeButton = None
		self.solveButton = Button('Solve',hex,buttonShapeSolve,stroke_color='white',parent=self,position=(0,0))
		self.placeButtons()
		
	def placeButtons(self):
		modeX = self.size.w/2
		modeOffsetX = -self.buttonHeight/2
		modeFactorX = 0
		modeFactorY = 1
		numberOffsetY = 1/2
		
		#place mode buttons
		for i, button in enumerate(self.modeButtons):
			y = self.size.h/2 - self.buttonHeight/2 - i%3*self.buttonHeight*modeFactorY
			x = modeX + modeOffsetX + i%3*self.buttonHeight*modeFactorX
			button.position = (x,y)
			
		#place number buttons
		for i, button in enumerate(self.numberButtons):
			y = self.size.h/2 - self.buttonHeight*numberOffsetY - i//3*self.buttonHeight
			x = -self.size.w/2 + self.buttonHeight/2 + i%3*self.buttonHeight
			button.position = (x,y)
			
		#place solve button
		self.solveButton.position = (0,-self.size.h/2 + self.buttonHeight/2)	
			
	def isNumberButtonPressed(self,touch):
		point = self.point_from_scene(touch.location)
		for button in self.numberButtons:
			if button.isPressed(point):
				return button
		
	def isModeButtonPressed(self,touch):
		point = self.point_from_scene(touch.location)
		for button in self.modeButtons:
			if button.isPressed(point) and button != self.activeButton:
				self.makeActive(button)
				
	def isSolveButtonPressed(self,touch):
		point = self.point_from_scene(touch.location)
		return self.solveButton.isPressed(point)
				
	def isNotPressed(self):
		for button in self.numberButtons:
			if button.active:
				button.deactivate()
				return button.id
		if self.solveButton.active:
			self.solveButton.deactivate()
			return self.solveButton.id
		return None
				
	def makeActive(self, button):
		if self.activeButton:
			self.activeButton.deactivate()
		self.activeButton = button
