import pygame
from pygame.locals import *
from helpers import *
import os
import variableStore as v
import time

class collisionBox:
	def __init__(self,x,y,width,height):
		self.width=width
		self.height=height
		self.position=CreateVector(x,y)
	def display(self,win):
		pygame.draw.rect(win,(255,0,0),
									(self.position.x-self.width/2-v.camera.position.x,
									 self.position.y-self.height/2-v.camera.position.y,self.width,self.height))
	def update(self,x,y,width,height):
		if self.position.x !=x or self.position.y != y or self.width !=width or self.height != height:
			self.position.x=x
			self.position.y=y
			self.width=width
			self.height=height

	def updateP(self,pos):
		if self.position.x != pos.x or self.position.y != pos.y:
			self.position.x=pos.x
			self.position.y=pos.y 

class positionBlock:
	def __init__(self,x,y,rx,ry,angle,width,height):
		self.width=width
		self.height=height
		self.angle=angle
		self.aposition=CreateVector(x,y)
		self.relPosition=CreateVector(rx,ry)		
		self.position=self.aposition.copy().add(vectorInrRotAx(self.relPosition,self.angle))
		
	def update(self,angle,position):
		if self.angle!=angle or not self.position.equals(position):
			self.aposition.setVec(position)
			self.angle=angle			
			self.position=self.aposition.copy().add(vectorInrRotAx(self.relPosition,self.angle))
	def display(self,win):
		pygame.draw.rect(win,(255,0,0),
									(self.position.x-self.width/2-v.camera.position.x,
									 self.position.y-self.height/2-v.camera.position.y,self.width,self.height))




class bullet:
	def __init__(self,x,y,angle):
		self.onScreen=True
		self.position=CreateVector(x,y)
		self.width=30
		self.height=30
		self.image=pygame.transform.scale(pygame.image.load('./sprites/redcube.png'),(self.width,self.height))
		self.angle=angle
		self.speed=10

		self.velocity=CreateVector(self.speed * math.cos(d2r(self.angle)),self.speed * math.sin(d2r(self.angle)))

	def display(self,win):
		draw_translate_rotate(self.image,
							  self.angle,self.position.x-self.width/2-v.camera.position.x,
							  self.position.y-self.height/2-v.camera.position.y,win)

	def update(self):
		self.position.add(self.velocity)
		self.checkCollisions()

	def checkCollisions(self):
		for x in v.pipesList:
			if not x.onScreen:
				continue
			if boxCollision(self,x):
				self.onScreen=False


class soldier:
	def __init__(self,x,y):
		self.onScreen=True
		self.width=200
		self.height=200
		self.position=CreateVector(x,y)
		self.boxCollider=collisionBox(x,y,self.width*0.5,self.height*0.5)
		self.shootPosition=positionBlock(x,y,100*v.xscale,40*v.yscale,0,self.width*0.05,self.height*0.05)
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
		self.bullets=[]
		self.lastShootTime=0
		self.shootGap=2

	def shoot(self):
		if time.time()-self.lastShootTime > self.shootGap:
			self.bullets.append(bullet(self.position.x,self.position.y,360-self.angle))
			self.lastShootTime=time.time()


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

	def updateRunBullets(self,win):
		for x in self.bullets:
			if not x.onScreen:
				continue
			x.display(win)
			x.update()
		flushList(self.bullets)

	def update(self,win):
		self.updateRunBullets(win)
		self.updateAndDrawShootPos(win)
		if v.SPACEPRESSED:
			self.shoot()
		if v.LEFTPRESSED:
			self.angle+=self.rotationSpeed
			if self.angle > 360:
				self.angle-=360
			self.updateVelocity()
		elif v.RIGHTPRESSED:
			self.angle-=self.rotationSpeed
			if self.angle < 0:
				self.angle+=360
			self.updateVelocity()

		if v.UPPRESSED:	
			self.ChangeAnimation("move")		
			self.ApplyVelocity()
		else:
			self.ChangeAnimation("idle")
			self.DeApplyVelocity()

		self.boxCollider.updateP(self.position)
		
	def updateAndDrawShootPos(self,win):
		self.shootPosition.update(360-self.angle,self.position)
		self.shootPosition.display(win)		
		
	def updateVelocity(self):
		rangle=360-self.angle
		self.velocity.x=self.vel * math.cos(d2r(rangle))
		self.velocity.y=self.vel * math.sin(d2r(rangle))			

	def ApplyVelocity(self):
		if self.vel < self.vmax:
			self.vel+=1
			self.updateVelocity()
		self.position.add(self.velocity)
		self.checkWithRoadBlocks()

	def DeApplyVelocity(self):
		if self.vel <=self.velMin:
			return True
		self.vel-=1
		self.updateVelocity()
		self.position.add(self.velocity)
		self.checkWithRoadBlocks()

	def checkWithRoadBlocks(self):
		for x in v.roadBlocks:
			if not x.onScreen:
				continue
			x.checkCollisions(self)

	def reelLeft(self):
		self.position.x-=abs(self.velocity.x)
	def reelRight(self):
		self.position.x+=abs(self.velocity.x)
	def reelDown(self):
		self.position.y+=abs(self.velocity.y)
	def reelUp(self):
		self.position.y-=abs(self.velocity.y)


	def display(self,win):
		draw_translate_rotate(self.images[self.anim][self.frame],
							  self.angle,self.position.x-self.width/2-v.camera.position.x,
							  self.position.y-self.height/2-v.camera.position.y,win)
		self.updateAnimation()
		#self.boxCollider.display(win)



class pipe:
	def __init__(self,x,y,width,height,hori=True,usercon=False):
		self.onScreen=True
		self.position=CreateVector(x,y)
		self.width=width
		self.height=height
		self.angle=0
		self.usercon=usercon
		self.hori=hori

		
		self.hdels=[1,0.5]
		self.wdels=[1,0.5]
		self.xdels=[1,0.5]
		self.ydels=[1,0.5]
		

		if hori:
			self.imagexOrig=pygame.image.load('./sprites/Pipes/pipeHori.png')
		else:
			self.imagexOrig=pygame.image.load('./sprites/Pipes/pipe.png')

		self.imagex=pygame.transform.scale(self.imagexOrig,(self.width,self.height))

		if hori:
			self.leftCollider= collisionBox(x-self.width*0.49,y                 ,0.005*self.width,self.height*0.8)
			self.rightCollider=collisionBox(x+self.width*0.49,y                 ,0.005*self.width,self.height*0.8)
			self.topCollider =collisionBox(x                 ,y-self.height*0.35,0.98*self.width ,0.05*self.height)
			self.bottomCollider =collisionBox(x              ,y+self.height*0.35,0.98*self.width ,0.05*self.height)
			self.colliders=[self.leftCollider,self.rightCollider,self.bottomCollider,self.topCollider]
		else:
			self.leftCollider= collisionBox(x-self.width*0.44,y+15*v.yscale       ,0.05*self.width,self.height*0.94)
			self.rightCollider=collisionBox(x+self.width*0.44,y+15*v.yscale       ,0.05*self.width,self.height*0.94)
			self.topCollider =collisionBox(x                 ,y-self.height*0.44,0.8*self.width ,0.005*self.height)
			self.bottomCollider =collisionBox(x              ,y+self.height*0.5,0.8*self.width ,0.005*self.height)
			self.colliders=[self.leftCollider,self.rightCollider,self.bottomCollider,self.topCollider]

	def checkCollisions(self,obj):
		if boxCollision(self.leftCollider,obj.boxCollider):
			obj.reelLeft()
		elif boxCollision(self.rightCollider,obj.boxCollider):
			obj.reelRight()
		elif boxCollision(self.bottomCollider,obj.boxCollider):
			obj.reelDown()
		elif boxCollision(self.topCollider,obj.boxCollider):
			obj.reelUp()



	def display(self,win):
		draw_translate_rotate(self.imagex,
							  self.angle,self.position.x-self.width/2-v.camera.position.x,
							  self.position.y-self.height/2-v.camera.position.y,win)
		'''
		for col in self.colliders:
			col.display(win)
		'''





	def update(self,win):
		# self.leftCollider.update(self.position.x-self.width*0.46 ,self.position.y                 ,0.05*self.width,self.height*0.8)
		# self.rightCollider.update(self.position.x+self.width*0.46,self.position.y                 ,0.05*self.width,self.height*0.8)
		# self.topCollider.update(self.position.x                  ,self.position.y-self.height*0.35,0.8*self.width ,0.05*self.height)
		# self.bottomCollider.update(self.position.x               ,self.position.y+self.height*0.35,0.8*self.width ,0.05*self.height)


		self.imagex=pygame.transform.scale(self.imagexOrig,(int(self.width),int(self.height)))
		if self.usercon:
			self.slideWithUser(win)

	def adjustSliderValues(self,pos,velacc,neg):
		if neg:
			pos-=velacc[0]
		else:
			pos+=velacc[0]
		velacc[0]+=velacc[1]
		if velacc[0] > 10:
			velacc[0]=10
		return pos



	def slideWithUser(self,win):
		w2screen(win,"width:"+str(round(self.width/v.xscale)),300,100)
		w2screen(win,"height:"+str(round(self.height/v.yscale)),300,150)
		w2screen(win,"xpos:"+str(round(self.position.x/v.xscale)),300,200)
		w2screen(win,"ypos:"+str(round(self.position.y/v.yscale)),300,250)
		if v.TPRESSED:
			self.height=self.adjustSliderValues(self.height,self.hdels,False)
		elif v.BPRESSED:
			self.height=self.adjustSliderValues(self.height,self.hdels,True)
		else:
			self.hdels[0]=1
		if v.HPRESSED:
			self.width=self.adjustSliderValues(self.width,self.wdels,False)
		elif v.FPRESSED:
			self.width=self.adjustSliderValues(self.width,self.wdels,True)
		else:
			self.wdels[0]=1
		

		if v.IPRESSED:
			self.position.y=self.adjustSliderValues(self.position.y,self.ydels,False)
		elif v.MPRESSED:
			self.position.y=self.adjustSliderValues(self.position.y,self.ydels,True)
		else:
			self.ydels[0]=1
		if v.LPRESSED:
			self.position.x=self.adjustSliderValues(self.position.x,self.xdels,False)
		elif v.JPRESSED:
			self.position.x=self.adjustSliderValues(self.position.x,self.xdels,True)
		else:
			self.xdels[0]=1
	

			




		