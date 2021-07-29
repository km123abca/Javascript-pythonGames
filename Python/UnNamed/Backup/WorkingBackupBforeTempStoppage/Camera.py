from helpers import *
import variableStore as v
class Camera:
	def __init__(self):
		self.position=CreateVector(0,0)
		self.target=None
		self.mouseLockX=0
		self.mouseLockY=0
		self.temp=0
		self.maxAllowedXRoaming=v.WIN_WIDTH*0.3
		self.maxAllowedYRoaming=v.WIN_HEIGHT*0.3

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

	def followTarget(self):
		if not self.target:
			return
		roamingDistX=self.target.position.x-(v.WIN_WIDTH/2+self.position.x)
		if abs(roamingDistX) > self.maxAllowedXRoaming:			
			if roamingDistX > 0:
				self.position.x+=roamingDistX-self.maxAllowedXRoaming
			else:
				self.position.x+=roamingDistX+self.maxAllowedXRoaming

		roamingDistY=self.target.position.y-(v.WIN_HEIGHT/2+self.position.y)
		if abs(roamingDistY) > self.maxAllowedYRoaming:
			if roamingDistY > 0:
				self.position.y+=roamingDistY-self.maxAllowedYRoaming
			else:
				self.position.y+=roamingDistY+self.maxAllowedYRoaming
			

			





	


