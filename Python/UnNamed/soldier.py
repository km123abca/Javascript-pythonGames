import pygame
from pygame.locals import *
from helpers import *
import os
import variableStore as v



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
		self.anim=0
		self.frame=0
		self.rotationSpeed=2
		self.vmax=5
		self.velMin=1
		self.velocity=CreateVector(self.velMin,0)	
		self.vel=self.velMin

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

	def update(self):
		if v.LEFTPRESSED:
			self.angle+=self.rotationSpeed
			if self.angle < 0:
				self.angle+=360
			self.updateVelocity()
		elif v.RIGHTPRESSED:
			self.angle-=self.rotationSpeed
			if self.angle > 360:
				self.angle=360-self.angle
			self.updateVelocity()

		if v.UPPRESSED:	
			self.ChangeAnimation("move")		
			self.ApplyVelocity()
		else:
			self.ChangeAnimation("idle")
			self.DeApplyVelocity()
		
			
		
	def updateVelocity(self):
		rangle=360-self.angle
		self.velocity.x=self.vel * math.cos(d2r(rangle))
		self.velocity.y=self.vel * math.sin(d2r(rangle))			

	def ApplyVelocity(self):
		if self.vel < self.vmax:
			self.vel+=1
			self.updateVelocity()
		self.position.add(self.velocity)

	def DeApplyVelocity(self):
		if self.vel <=self.velMin:
			return True
		self.vel-=1
		self.updateVelocity()
		self.position.add(self.velocity)


	def display(self,win):
		draw_translate_rotate(self.images[self.anim][self.frame],self.angle,self.position.x-self.width/2,self.position.y-self.height/2,win)
		self.updateAnimation()



		