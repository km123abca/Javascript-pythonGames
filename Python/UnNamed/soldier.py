import pygame
from pygame.locals import *
from helpers import *
import os
import variableStore as v

class collisionBox:
	def __init__(self,x,y,width,height):
		self.width=width
		self.height=height
		self.position=CreateVector(x,y)
	def display(self,win):
		pygame.draw.rect(win,(255,0,0),
									(self.position.x-self.width/2-v.camera.position.x,
									 self.position.y-self.height/2-v.camera.position.y,self.width,self.height))
	def update(self,pos):
		if self.position.x !=pos.x or self.position.y !=pos.y:
			self.position.x=pos.x
			self.position.y=pos.y



class soldier:
	def __init__(self,x,y):
		self.onScreen=True
		self.width=200
		self.height=200
		self.position=CreateVector(x,y)
		self.boxCollider=collisionBox(x,y,self.width*0.5,self.height*0.5)
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

		self.boxCollider.update(self.position)
		
			
		
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
		draw_translate_rotate(self.images[self.anim][self.frame],
							  self.angle,self.position.x-self.width/2-v.camera.position.x,
							  self.position.y-self.height/2-v.camera.position.y,win)
		self.updateAnimation()
		self.boxCollider.display(win)



class pipe:
	def __init__(self,x,y,width,height,hori=True):
		self.onScreen=True
		self.position=CreateVector(x,y)
		self.width=width
		self.height=height
		self.angle=0
		if hori:
			self.imagex=pygame.transform.scale(pygame.image.load('./sprites/Pipes/pipeHori.png'),(self.width,self.height))
		else:
			self.imagex=pygame.transform.scale(pygame.image.load('./sprites/Pipes/pipe.png'),(self.width,self.height))

		self.leftCollider= collisionBox(x-self.width*0.46,y,0.05*self.width,self.height*0.8)
		self.rightCollider=collisionBox(x+self.width*0.46,y,0.05*self.width,self.height*0.8)
		self.topCollider =collisionBox(x,y-self.height*0.35,0.8*self.width,0.05*self.height)
		self.bottomCollider =collisionBox(x,y+self.height*0.35,0.8*self.width,0.05*self.height)
		self.colliders=[self.leftCollider,self.rightCollider,self.bottomCollider,self.topCollider]

	def display(self,win):
		draw_translate_rotate(self.imagex,
							  self.angle,self.position.x-self.width/2-v.camera.position.x,
							  self.position.y-self.height/2-v.camera.position.y,win)
		for col in self.colliders:
			col.display(win)



		