from helpers import *
import variableStore as v
class Camera:
	def __init__(self):
		self.position=CreateVector(0,0)
		self.target=None
		self.mouseLockX=0
		self.mouseLockY=0
		self.temp=0

	def runwithmouse(self):
		if v.mouseClicked:			
			if self.mouseLockX==0:
				self.mouseLockX=v.mousex
			if self.mouseLockY==0:
				self.mouseLockY=v.mousey 
			self.position.x-=(v.mousex-self.mouseLockX)/10
			self.position.y-=(v.mousey-self.mouseLockY)/10			
		else:
			if self.mouseLockX!=0:
				self.mouseLockX=0
			if self.mouseLockY!=0:
				self.mouseLockY=0





	


