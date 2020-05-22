from scene import *
from adjustColor import *
from touch import *

class Button(ShapeNode):
	def __init__(self,id,hex,*args,**kwargs):
		ShapeNode.__init__(self,*args,**kwargs)
		self.id = id
		self.hex = hex
		self.active = False
		font = ('Helvetica', self.size.w/len(str(id)))
		self.text = LabelNode(str(id),font=font,parent=self)
		
	def isPressed(self,point):
		pressed = isTouched(self,point)
		if pressed:
			self.active = True
			self.fill_color = adjustColor(self.hex,0.75)
		return pressed
			
	def deactivate(self):
		self.fill_color = self.hex
		self.active = False
		
