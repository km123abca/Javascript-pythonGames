import pygame
from pygame.locals import *
from helpers import *
import os


class soldier:
	def __init__(self,x,y):
		self.width=200
		self.height=200
		self.position=CreateVector(x,y)
		self.idle_images,self.move_images,self.shoot_images=[],[],[]		
		self.images=[]	
		self.angle=0
		self.animInQueue=None
		for i in range(19):
			imagex=pygame.transform.scale(pygame.image.load(os.path.join('sprites',
				f'soldier/idle/survivor-idle_handgun_{i}.png')),(self.width,self.height))
			self.idle_images.append(imagex)
		for i in range(19):
			imagex=pygame.transform.scale(pygame.image.load(os.path.join('sprites',
				f'soldier/move/survivor-move_handgun_{i}.png')),(self.width,self.height))
			self.move_images.append(imagex)
		for i in range(3):
			imagex=pygame.transform.scale(pygame.image.load(os.path.join('sprites',
				f'soldier/shoot/survivor-shoot_handgun_{i}.png')),(self.width,self.height))
			self.shoot_images.append(imagex)
		self.images=[self.idle_images,self.move_images,self.shoot_images]
		self.animTimers=[0,0,0]
		self.animTimerMax=[1,1,1]
		self.anim=1
		self.frame=0
		self.rotationSpeed=2
		self.velocity=CreateVector(0,0)
		self.acceleration=CreateVector(0,0)
		self.amax=2
		self.vmax=5

	def animUpdateAllowed(self):
		self.animTimers[self.anim]+=1
		if self.animTimers[self.anim] >= self.animTimerMax[self.anim]:
			self.animTimers[self.anim]=0
			return True
		return False

	def updateAnimation(self):
		if not self.animUpdateAllowed():
			return False
		self.frame+=1		
		if self.frame >= len(self.images[self.anim]):
			if not self.animInQueue:
				self.frame=0
			else:
				self.ChangeAnimation(self.animInQueue)

	def ChangeAnimation(self,animName):
		if animName=='idle' and self.anim!=0:
			self.anim=0
			self.frame=0
		elif animName=='move' and self.anim!=1:
			self.anim=1
			self.frame=0
		elif animName=="shoot" and self.anim!=2:
			self.anim=2
			self.frame=0

	def update(self,leftPressed,rightPressed,upPressed,downPressed):
		if leftPressed:
			self.angle-=self.rotationSpeed
			if self.angle < 0:
				self.angle+=360
			self.updateAcceleration()
		elif rightPressed:
			self.angle+=self.rotationSpeed
			if self.angle > 360:
				self.angle=360-self.angle
			self.updateAcceleration()

		if upPressed:			
			self.ApplyAcceleration()
		else:
			self.ApplyDecceleration()
		self.ApplyVelocity()
			
		
	def updateAcceleration(self):
		self.acceleration.x=self.amax * math.cos(d2r(self.angle))
		self.acceleration.y=self.amax * math.sin(d2r(self.angle))

	def ApplyAcceleration(self):
		self.velocity.add(self.acceleration)
		if self.velocity.mag() > self.vmax:
			self.velocity.sub(self.acceleration)
	def ApplyDecceleration(self):
		if self.velocity.x==0 and self.velocity.y==0:
			return False
		self.velocity.div(2)
		if self.velocity.mag() < 0.5:
			self.velocity.set(0,0)

	def ApplyVelocity(self):
		self.position.add(self.velocity)
		







	def display(self,win):
		draw_translate_rotate(self.images[self.anim][self.frame],self.angle,self.position.x-self.width/2,self.position.y-self.height/2,win)
		self.updateAnimation()



		