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
		
'''class Test(Scene):
	def setup(self):
		hex = '#ff527f'
		menuItems = "easy medium hard".split(" ")
		prompt = 'Play Again?'
		dims = [400,300,250,50]
		self.menu = Menu(hex,prompt,menuItems,dims,stroke_color='white',parent=self)
		self.placeMenu()
		
	def placeMenu(self):
		(w,h) = self.size
		self.menu.position = (w/2,h/2)
		self.menu.placeMenuItems()
		
	def did_change_size(self):
		self.placeMenu()
		
	def touch_began(self,touch):
		button = self.menu.isButtonPressed(touch)
		if button:
			#choose setting and delete menu
			pass
		
run(Test())'''
