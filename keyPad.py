from scene import *
from button import *
from touch import *


class KeyPad(ShapeNode):
	def __init__(self,hex,*args,**kwargs):
		ShapeNode.__init__(self,*args,**kwargs)
		self.buttonSize = min(self.size.w,self.size.h)/3
		square = ui.Path.rect(0,0,self.buttonSize,self.buttonSize)
		self.numberButtons = [Button(i,hex,square,fill_color='clear',stroke_color='white',parent=self,position=(i*10,i*10)) for i in range(1,10)]
		buttonNames = "write note erase"
		buttonNames = buttonNames.split(" ")
		self.modeButtons = [Button(buttonNames[i],hex,square,fill_color='clear',stroke_color='white',parent=self,position=(i*10,i*10)) for i in range(len(buttonNames))]
		self.activeButton = None
		self.placeButtons()
		
	def placeButtons(self):
		if self.size.w > self.size.h:
			modeX = self.size.w/2
			modeOffsetX = -self.buttonSize/2
			modeFactorX = 0
			modeFactorY = 1
			numberOffsetY = 1/2
		else:
			modeX = -self.size.w/2
			modeOffsetX = self.buttonSize/2
			modeFactorX = 1
			modeFactorY = 0
			numberOffsetY = 3/2
			
		for i, button in enumerate(self.modeButtons):
			y = self.size.h/2 - self.buttonSize/2 - i%3*self.buttonSize*modeFactorY
			x = modeX + modeOffsetX + i%3*self.buttonSize*modeFactorX
			button.position = (x,y)
		for i, button in enumerate(self.numberButtons):
			y = self.size.h/2 - self.buttonSize*numberOffsetY - i//3*self.buttonSize
			x = -self.size.w/2 + self.buttonSize/2 + i%3*self.buttonSize
			button.position = (x,y)
			
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
				
	def isNotPressed(self):
		for button in self.numberButtons:
			if button.active:
				button.deactivate()
				
	def makeActive(self, button):
		if self.activeButton:
			self.activeButton.deactivate()
		self.activeButton = button
