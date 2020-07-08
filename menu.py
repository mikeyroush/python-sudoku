from button import *

class Menu(ShapeNode):
	def __init__(self,hex,prompt,menuItems,dimensions,*args,**kwargs):
		ShapeNode.__init__(self,*args,**kwargs)
		#save values from parameters
		self.fill_color = hex
		self.promptMessage = prompt
		menuItems.reverse()
		self.menuItems = menuItems
		(self.menuWidth,self.menuHeight,self.buttonWidth,self.buttonHeight) = dimensions
		#make prompt and buttons
		self.prompt = LabelNode(prompt,parent=self)
		self.buttons = [Button(id,hex,fontSize=self.buttonHeight*0.9,stroke_color='white',parent=self) for id in menuItems]
		#make menu shape
		self.path = ui.Path.rect(0,0,self.menuWidth,self.menuHeight)
		self.isActive = True
	
	def placeMenuItems(self):
		#place buttons
		(w,h) = self.size
		divs = len(self.menuItems)+1
		divHeight = h/divs
		shape = ui.Path.rect(0,0,self.buttonWidth,self.buttonHeight)
		for i, button in enumerate(self.buttons):
			button.path = shape
			button.position = (0,-h/2+(1/2+i)*divHeight)
		#place prompt
		self.prompt.font = ('Helvetica',min(divHeight*0.9,1.5*w/len(self.promptMessage)))
		self.prompt.position=(0,h/2-6*self.prompt.font[1]/10)
		
	def isButtonPressed(self,touch):
		point = self.point_from_scene(touch.location)
		for button in self.buttons:
			if button.isPressed(point):
				return button
		
	def isNotPressed(self):
		for button in self.buttons:
			if button.active:
				button.deactivate()
				return button.id
		return None
