import pygame
from pygame.locals import *
from helpers import *
import os
import variableStore as v
import time,random
import re

######### Global Variables ##################
CLOUDIMAGE=pygame.image.load('./sprites/cloud-1.png')
REDCUBEIMAGE =pygame.image.load('./sprites/redcube.png')
REDSPHEREIMAGE=pygame.image.load('./sprites/redSphere.png')
FIREBALLIMAGE=pygame.image.load('./sprites/fireball.png')
HORIZONTAL_PIPE=pygame.image.load('./sprites/Pipes/pipeHori.png')
VERTICAL_PIPE=pygame.image.load('./sprites/Pipes/pipe.png')
HAZE=pygame.image.load('./sprites/haze.png')
GATE=pygame.image.load('./sprites/gate.png')
global BULLETIMAGE,BULLETSIZEFAC
BULLETIMAGE=REDSPHEREIMAGE
BULLETSIZEFAC=0.05
BEETLE_IDLE=pygame.image.load('./sprites/beetles/idle1.png')
BEETLE_MOVE1=pygame.image.load('./sprites/beetles/move1.png')
BEETLE_MOVE2=pygame.image.load('./sprites/beetles/move2.png')
CAVEENTRANCEIMAGE=pygame.image.load('./sprites/caveEntrance.png')
CIRCLEIMAGE=pygame.image.load('./sprites/circle.png')

# BEETLE_IDLE=pygame.transform.scale(BEETLE_IDLE,(100,100))
# BEETLE_MOVE1=pygame.transform.scale(BEETLE_MOVE1,(100,100))
# BEETLE_MOVE2=pygame.transform.scale(BEETLE_MOVE2,(100,100))


#############################################
def changeBullet(gun):	
	global BULLETIMAGE,BULLETSIZEFAC
	if gun=='handgun':					
		BULLETSIZEFAC=0.05
		BULLETIMAGE=REDSPHEREIMAGE
	elif gun=='rifle':						
		BULLETSIZEFAC=0.2
		BULLETIMAGE=FIREBALLIMAGE
	elif gun=='shotgun':					
		BULLETSIZEFAC=0.3
		BULLETIMAGE=FIREBALLIMAGE
def SpawnCloudGroup(pos):
	for i in range(30):
		v.cloudsList.append(cloudBurst(pos.x,pos.y))
class userSlider:
	def __init__(self):
		self.vel=1
		self.acc=0.5
		
	def adjustSliderValues(self,vec,win):
		if v.TPRESSED:
			vec.y-=self.vel
		if v.BPRESSED:
			vec.y+=self.vel
		if v.HPRESSED:
			vec.x+=self.vel
		if v.FPRESSED:
			vec.x-=self.vel
		
		w2screen(win,"xpos:"+str(round(vec.x/v.xscale)),300,200)
		w2screen(win,"ypos:"+str(round(vec.y/v.yscale)),300,250)

class MadCircle:
	def __init__(self,x,y,diameter,gateIndex):
		self.onScreen=True
		self.gateIndex=gateIndex
		self.position=CreateVector(x,y)
		self.width,self.height=diameter,diameter
		self.imagexOrig=CIRCLEIMAGE
		self.imagex=pygame.transform.scale(CIRCLEIMAGE,(self.width,self.height))
		self.angle=random.randint(0,80)
		self.velMax=10
		self.velocity=CreateVector(self.velMax * math.cos(d2r(self.angle)),self.velMax * math.sin(d2r(self.angle)))
		self.dirChangeClk,self.fireClk=0,0
		self.dirChangeGap,self.fireGap=6,5
		self.bullets=[]
		self.maxHealth=10
		self.health=self.maxHealth
		self.healthBar=healthBar(x,y,0,-80*v.yscale,-40*v.xscale,200*v.xscale,10*v.yscale,self.health)
		self.healthBarHidden=True
		self.healthBarOffTime=0
		self.healthBarOffGap=2
		self.boxCollider=collisionBox(x,y,self.width*0.8,self.height*0.8)

	def UpdateAndShowBoxCollider(self,win):
		self.boxCollider.updateP(self.position)
		# self.boxCollider.display(win)

	def ShowHealthBar(self):
		if self.healthBarHidden:
			self.healthBarHidden=False
			self.healthBarOffTime=time.time()

	def ManageHealthBarVisibility(self):
		if self.healthBarHidden:
			return
		if time.time()-self.healthBarOffTime > self.healthBarOffGap:
			self.healthBarHidden=True

	def updateHealthBar(self,win):
		self.ManageHealthBarVisibility()
		if not self.healthBarHidden:
			self.healthBar.display(win)
			self.healthBar.update(-self.angle,self.position)

	def TakeDamage(self,dmg):
		self.health-=dmg
		self.healthBar.reduceHealth(dmg)
		self.ShowHealthBar()
		if self.health < 0:
			self.onScreen=False
			v.gatesList[self.gateIndex].active=False
			v.gatesList[self.gateIndex].RemoveSelfFromHindranceList()

	def drawAndDisplayBullets(self,win):
		for b in self.bullets:
			if not b.onScreen:
				continue
			b.display(win)
			b.update()
		flushList(self.bullets)

	def DirectAtPlayer(self):
		if len(v.soldiersList) == 0 or not v.soldiersList[0].onScreen:
			return
		if time.time()-self.dirChangeClk > self.dirChangeGap:
			self.dirChangeClk=time.time()
			targetDir=v.soldiersList[0].position.copy().sub(self.position).normalized()
			self.velocity=targetDir.mult(self.velMax)
			self.angle=self.velocity.heading()

	def display(self,win):
		myrect=self.imagex.get_rect()
		myrect.centerx,myrect.centery=self.position.x-v.camera.position.x,self.position.y-v.camera.position.y
		win.blit(pygame.transform.rotate(self.imagex,-self.angle),myrect)
	def lightUp(self):
		if time.time()-self.fireClk > self.fireGap:
			self.fireClk=time.time()
			randomAngle=random.randint(0,89)
			for i in range(4):
				self.bullets.append(bullet(self.position.x,self.position.y,randomAngle,self,'enemy',4))
				randomAngle+=90
	def update(self,win):
		self.UpdateAndShowBoxCollider(win)
		self.updateHealthBar(win)
		self.lightUp()
		self.drawAndDisplayBullets(win)
		self.DirectAtPlayer()
		self.CollidedWithPlayer()
		self.DidCollideWithWall()
		self.position.add(self.velocity)
	def DidCollideWithWall(self):
		for wall in v.roadBlocks:
			if not wall.onScreen:
				continue
			if boxCollision(self,wall.topCollider):
				self.velocity.y=-abs(self.velocity.y)
				self.angle=self.velocity.heading()
			elif boxCollision(self,wall.bottomCollider):
				self.velocity.y=abs(self.velocity.y)
				self.angle=self.velocity.heading()
			elif boxCollision(self,wall.rightCollider):
				self.velocity.x=abs(self.velocity.x)
				self.angle=self.velocity.heading()
			elif boxCollision(self,wall.leftCollider):
				self.velocity.x=-abs(self.velocity.x)
				self.angle=self.velocity.heading()
	def CollidedWithPlayer(self):
		if len(v.soldiersList) == 0 or not v.soldiersList[0].onScreen:
			return
		if not v.soldiersList[0].InvincibleMode and boxCollision(self,v.soldiersList[0].boxCollider):
			v.soldiersList[0].TakeDamage(20)
		

class doorTrigger:
	def __init__(self,x,y,wid,hei,doorName):
		self.onScreen=True
		self.doorName=doorName
		self.position=CreateVector(x,y)
		self.width=wid
		self.height=hei 
		self.imagexOrig=BULLETIMAGE
		self.imagex=pygame.transform.scale(BULLETIMAGE,(self.width,self.height))

	def checkCollisionWithPlayer(self):
		if boxCollision(v.soldiersList[0].boxCollider,self):
			self.openHazes()

	def update(self):
		self.checkCollisionWithPlayer()

	def openHazes(self):
		hazesx=re.search('[0-9]+',self.doorName).group(0)
		for x in v.hazesList:
			if x.doorName in  ['door'+hazesx[0],'door'+hazesx[1]]:
				x.goOut()

	def display(self,win):
		myrect=self.imagex.get_rect()
		myrect.centerx,myrect.centery=self.position.x- v.camera.position.x,self.position.y- v.camera.position.y 
		win.blit(self.imagex,myrect)

class cloudBurst:
	def __init__(self,x,y):
		self.onScreen=True
		self.position=CreateVector(x,y)
		self.width=30*v.xscale
		self.height=30*v.yscale
		self.origWidth=self.width
		self.image=pygame.transform.scale(CLOUDIMAGE,(self.width,self.height))
		self.startTime=time.time()
		self.age=0.2
		self.velocity=CreateVector(random.randint(0,4),random.randint(0,4))
	def display(self,win):		
		draw_translate_rotate(self.image,
							  0,self.position.x-self.width/2-v.camera.position.x,
							  self.position.y-self.height/2-v.camera.position.y,win)
	def update(self):
		self.position.add(self.velocity)
		'''
		if time.time()-self.startTime > self.age:
			self.onScreen=False
		'''		
		self.width=int(self.width*0.95)
		self.height=int(self.height*0.95)
		self.image=pygame.transform.scale(CLOUDIMAGE,(self.width,self.height))
		if self.width/self.origWidth < 0.05:
			self.onScreen=False


class gratedGate:
	def __init__(self,x,y,width,height,active=0):
		self.position=CreateVector(x,y)
		self.width=width
		self.height=height
		self.imagexOrig=GATE
		self.imagex=pygame.transform.scale(self.imagexOrig,(self.width,self.height))
		self.onScreen=True
		self.active=False if active==0 else True
		self.leftCollider=collisionBox(self.position.x-0.36*self.width,self.position.y,0.2*self.width,self.height)
		self.rightCollider=collisionBox(self.position.x+0.36*self.width,self.position.y,0.2*self.width,self.height)
		self.topCollider=collisionBox(self.position.x,self.position.y-0.45*self.height,self.width,0.1*self.height)
		self.bottomCollider=collisionBox(self.position.x,self.position.y+0.45*self.height,self.width,0.1*self.height)
		self.colliders=[self.leftCollider,self.rightCollider,self.topCollider,self.bottomCollider]
		self.passedThrough=False
		self.bug=None

		if self.active:
			v.roadBlocks.append(self)

	def RemoveSelfFromHindranceList(self):
		v.roadBlocks.remove(self)

	def enterBug(self,bg):
		self.bug=bg

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
		if not self.active:
			return
		myrect=self.imagex.get_rect()
		myrect.centerx=self.position.x-v.camera.position.x
		myrect.centery=self.position.y-v.camera.position.y
		win.blit(self.imagex,myrect)
		# self.displayAndUpdateColliders(win)

	def displayAndUpdateColliders(self,win):
		if not self.active:
			return
		for x in self.colliders:
			x.display(win)

	def activate(self):
		if self.active:
			return
		if self.bug:
			self.bug.active=True
			pygame.mixer.music.load(f'./music/Capra.mp3')
			pygame.mixer.music.play(-1,0.0)
			self.active=True
		v.roadBlocks.append(self)


	def update(self):
		if not self.active:
			if boxCollision(v.soldiersList[0].boxCollider,self):
				if not self.passedThrough:
					self.passedThrough=True
			elif self.passedThrough and self.position.x < v.soldiersList[0].position.x:
				self.activate()

		
class GameManager:
	def __init__(self):
		self.scenesLoaded=[False,False,False,False,False,False,False,False]
		self.scenesReady=[True,False,False,False,False,False,False,False]
		self.loadingObjects=False
		self.loadingType=None
		self.currentScene=-1
		self.reloading=False
		self.gameStopTime=0
		self.maxReloadGap=3
		self.readyForNextLevel=False

		
	def checkScenes(self):
		#if self.sceneLoadingInProgress:
			#self.loadScene(i)
		for i,scene in enumerate(self.scenesLoaded):
			if self.scenesReady[i] and not scene:
				self.loadScene(i)

	def reloadLevel(self):
		self.reloading=True	
		self.gameStopTime=time.time()	
	def LoadNextLevel(self):
		if not self.readyForNextLevel:
			self.readyForNextLevel=True	
			self.gameStopTime=time.time()
	def loadScene(self,i):
		print('loading scene:'+str(i))
		filex=open('./SceneData.txt','r')
		for line in filex.readlines():
			if line[0]=='#':
				continue

			if 'scene'+str(i) in line:
				self.loadingObjects=True
			elif self.loadingObjects and 'sceneend' in line:
				self.scenesLoaded[i]=True
				self.loadingObjects=False
				self.currentScene=i				
				return
			elif self.loadingObjects:
				self.LoadObjects(line)
		filex.close()

	def LoadObjects(self,line):
		if not re.search(r'[0-9]',line):
			self.loadingType=re.findall(r'[a-z]+',line)[0]			
		else:
			nums=re.findall(r'[0-9\-]+',line)
			if self.loadingType=='pipe':
				v.pipesList.append(pipe(int(nums[0])*v.xscale,
					                    int(nums[1])*v.yscale,
					                    int(nums[2])*v.xscale,
					                    int(nums[3])*v.yscale,
					                    int(nums[4])==1 if True else False,
					                    int(nums[5])==1 if True else False
					               ))
				v.roadBlocks.append(v.pipesList[-1])
			elif self.loadingType=='haze':
				v.hazesList.append(haze(int(nums[0])*v.xscale,
										int(nums[1])*v.yscale,
										int(nums[2])*v.xscale,
										int(nums[3])*v.yscale,
										'door'+nums[4]
									))
			elif self.loadingType=='doortrigger':
				v.doorTriggersList.append(doorTrigger(
													  int(nums[0])*v.xscale,
													  int(nums[1])*v.yscale,
													  int(nums[2])*v.xscale,
													  int(nums[3])*v.yscale,
													  'door'+nums[4]
													  )
										  )
			elif self.loadingType=='gratedgate':
				v.gatesList.append(gratedGate(
											 int(nums[0])*v.xscale,
											 int(nums[1])*v.yscale,
											 int(nums[2])*v.xscale,
											 int(nums[3])*v.yscale,
											 int(nums[4])
											 ))				
			elif self.loadingType=='player':
				v.soldiersList.append(soldier(int(nums[0])*v.xscale,
											  int(nums[1])*v.yscale))
				v.camera.target=v.soldiersList[0]			
			elif self.loadingType=='beetle':
				v.beetlesList.append(beetle(int(nums[0]*v.xscale),
										    int(nums[1]*v.yscale),
										    int(nums[2])  
										   ) 
									)				
				v.enemiesList.append(v.beetlesList[-1])
			elif self.loadingType=='cave':
				v.cavesList.append(caveEntrance(
												int(nums[0]*v.xscale),
										    	int(nums[1]*v.yscale)
											   )
								  )
			elif self.loadingType=='circle':
				v.circlesList.append(MadCircle(
												int(nums[0]*v.xscale),
										    	int(nums[1]*v.yscale),
										    	int(nums[2]*v.xscale),
										    	int(nums[3])
											   )
								  )
				v.enemiesList.append(v.circlesList[-1])
				# v.pChanger=posChanger(v.gatesList[-1])


	def update(self):
		self.checkScenes()
		if self.reloading:
			if time.time()-self.gameStopTime > self.maxReloadGap:
				self.reloading=False
				self.unloadComponents()
				self.scenesLoaded[self.currentScene]=False
		elif self.readyForNextLevel:
			if time.time()-self.gameStopTime > self.maxReloadGap:
				self.readyForNextLevel=False
				self.unloadComponents()
				self.scenesReady[self.currentScene+1]=True


	def unloadComponents(self):
		v.beetlesList=[]
		v.enemiesList=[]
		v.soldiersList=[]
		v.gatesList=[]
		v.doorTriggersList=[]
		v.hazesList=[]
		v.roadBlocks=[]
		v.pipesList=[]
		v.cavesList=[]	
		v.circlesList=[]	
		pygame.mixer.music.load(f'./music/majula.mp3')
		pygame.mixer.music.play(-1,0.0)



class collisionBox:
	def __init__(self,x,y,width,height,col='red'):
		self.width=width
		self.height=height
		self.position=CreateVector(x,y)
		self.col=(255,0,0) if col=='red' else (0,0,255)
	def display(self,win):
		pygame.draw.rect(win,self.col,
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
	def __init__(self,x,y,rx,ry,angle,width,height,col=(255,0,0),centered=True):
		self.width=width
		self.height=height
		self.angle=angle
		self.aposition=CreateVector(x,y)
		self.relPosition=CreateVector(rx,ry)		
		self.position=self.aposition.copy().add(vectorInrRotAx(self.relPosition,self.angle))
		self.col=col
		self.centered=centered
		
	def update(self,angle,position):
		if self.angle!=angle or not self.position.equals(position):
			self.aposition.setVec(position)
			self.angle=angle			
			self.position=self.aposition.copy().add(vectorInrRotAx(self.relPosition,self.angle))
	def display(self,win):
		if self.centered:
			pygame.draw.rect(win,self.col,
									(self.position.x-self.width/2-v.camera.position.x,
									 self.position.y-self.height/2-v.camera.position.y,self.width,self.height))
		else:
			pygame.draw.rect(win,self.col,
									(self.position.x-v.camera.position.x,
									 self.position.y-self.height/2-v.camera.position.y,self.width,self.height))

class healthBar:
	def __init__(self,x,y,rx,ry,angle,width,height,maxHealth):		
		self.greenBar=positionBlock(x,y,rx,ry,angle,width,height,(26,255,209),False)
		self.redBar=positionBlock(x,y,rx,ry,angle,width,height,(163,163,194),False)
		self.maxHealth=maxHealth
		self.health=maxHealth
		self.width=width
		self.height=height
	def reduceHealth(self,dmg):
		self.health-=dmg
		self.health=0 if self.health < 0 else self.health
		self.greenBar.width=self.health/self.maxHealth * self.width
		
	def update(self,angle,position):
		self.redBar.update(0,position)
		self.greenBar.update(0,position)		
	def display(self,win):
		self.redBar.display(win)
		self.greenBar.display(win)
		



class haze:
	def __init__(self,x,y,wid,hei,doorName):
		self.position=CreateVector(x,y)
		self.doorName=doorName
		self.width=wid
		self.height=hei
		self.imagexOrig=HAZE
		self.imagex=pygame.transform.scale(HAZE,(self.width,self.height))
		self.onScreen=True
		self.basicFont=pygame.font.Font('freesansbold.ttf',32)

	def displayName(self,win):
		#w2screen(win,self.doorName,self.position.x,self.position.y)
		writeSurf=self.basicFont.render(self.doorName,1,(0,0,0))
		writeRect=writeSurf.get_rect()
		writeRect.centerx,writeRect.centery=self.position.x-v.camera.position.x,self.position.y-v.camera.position.y 
		win.blit(writeSurf,writeRect)

	def display(self,win):
		myrect=self.imagex.get_rect()
		myrect.centerx=int(self.position.x-v.camera.position.x)
		myrect.centery=int(self.position.y-v.camera.position.y)
		win.blit(self.imagex,myrect)
		self.displayName(win)
	def goOut(self):
		if self.onScreen:
			self.onScreen=False
			v.fogGateSound.play()


class bullet:
	def __init__(self,x,y,angle,parent,bulletType,lifeTime=0):
		self.onScreen=True
		self.bulletType=bulletType
		self.parent=parent
		self.position=CreateVector(x,y)
		# self.width=int(self.parent.width*BULLETSIZEFAC)
		# self.height=int(self.parent.width*BULLETSIZEFAC)
		self.width=30*v.xscale;
		self.height=30*v.xscale;
		self.image=pygame.transform.scale(BULLETIMAGE,(self.width,self.height))
		self.angle=angle
		self.speed=20*v.xscale
		self.velocity=CreateVector(self.speed * math.cos(d2r(self.angle)),self.speed * math.sin(d2r(self.angle)))

		self.lifeTime=lifeTime
		self.timeOfBirth=time.time()


	def checkLife(self):
		if self.lifeTime!=0:
			if time.time()-self.timeOfBirth > self.lifeTime:
				self.onScreen=False
	def display(self,win):
		draw_translate_rotate(self.image,
							  360-self.angle,self.position.x-self.width/2-v.camera.position.x,
							  self.position.y-self.height/2-v.camera.position.y,win)

	def update(self):
		self.checkLife()
		self.position.add(self.velocity)
		self.checkCollisions()
		self.OutOfBoundsCheck()

	def checkCollisions(self):
		for x in v.pipesList:
			if not x.onScreen:
				continue
			if boxCollision(self,x):
				self.onScreen=False
				SpawnCloudGroup(self.position)
				v.shootingSound.play()
		if self.bulletType=="player":
			for x in v.enemiesList:
				if not x.onScreen:
					continue
				if boxCollision(self,x.boxCollider):
					self.onScreen=False
					SpawnCloudGroup(self.position)
					v.shootingSound.play()
					x.TakeDamage(5)
		elif self.bulletType=="enemy":
			for x in v.soldiersList:
				if not x.onScreen or x.InvincibleMode:
					continue
				if boxCollision(self,x.boxCollider):
					self.onScreen=False
					SpawnCloudGroup(self.position)
					v.shootingSound.play()
					x.TakeDamage(5)


	def OutOfBoundsCheck(self):
		if self.position.x - v.camera.position.x > v.WIN_WIDTH or self.position.x - v.camera.position.x < 0:
			self.onScreen=False
		if self.position.y - v.camera.position.y > v.WIN_HEIGHT or self.position.y - v.camera.position.y < 0:
			self.onScreen = False 

class caveEntrance:
	def __init__(self,x,y):
		self.onScreen=True
		self.active=False
		self.position=CreateVector(x,y)
		self.imagexOrig=CAVEENTRANCEIMAGE
		self.width=100*v.xscale
		self.height=200*v.yscale
		self.imagex=pygame.transform.scale(self.imagexOrig,(self.width,self.height))
	def update(self):
		if not self.active:
			return
		if boxCollision(self,v.soldiersList[0]):
			v.gameManager.LoadNextLevel()
	def display(self,win):
		if not self.active:
			return
		myrect=self.imagex.get_rect()
		myrect.centerx,myrect.centery=self.position.x-v.camera.position.x,self.position.y-v.camera.position.y
		win.blit(self.imagex,myrect)

class beetle:
	def __init__(self,x,y,gateIndex):
		self.onScreen=True
		self.active=False	
		self.maxHealth=5
		self.health=5
		self.healthBar=healthBar(x,y,0,-80*v.yscale,-40*v.xscale,200*v.xscale,10*v.yscale,self.health)	
		v.gatesList[gateIndex].enterBug(self)
		self.width=300*v.xscale
		self.height=300*v.yscale
		self.boxCollider=collisionBox(x,y,self.width*0.8,self.height*0.8)
		self.hornCollider=positionBlock(x,y,90*v.xscale,0,0,30*v.xscale,30*v.xscale)
		self.position=CreateVector(x,y)
		self.idle_images,self.move_images=[BEETLE_IDLE],[BEETLE_MOVE1,BEETLE_MOVE2]
		
		for i,x in enumerate(self.idle_images):			
			self.idle_images[i]=pygame.transform.scale(self.idle_images[i],(self.width,self.height))
		for i,x in enumerate(self.move_images):
			self.move_images[i]=pygame.transform.scale(self.move_images[i],(self.width,self.height))
				
		
		self.animations=[self.idle_images,self.move_images]
		self.animTimers=[0,0]
		self.animTimersMax=[1,5]
		self.animFrame=0
		self.anim=1
		self.animInQueue=None
		self.angle=30
		self.velMax=8
		self.velocity=CreateVector(self.velMax,0)
		self.state="attack"
		self.enemy=v.soldiersList[0]
		self.enemyProximity=250*v.xscale

		self.lastShootTime=0
		self.shootGap=1

		self.shootAttackMax=6
		self.shootAttackTimer=0	
		self.lastAttackTime=0
		self.maxAttackGap=3
		self.bullets=[]
		self.angleGap=15

		self.plungeVelocity=CreateVector(self.velMax*4,0)
		self.focussed=False

		self.healthBarHidden=False
		self.healthBarClock=0
		self.healthBarMaxTime=3

		self.vicinity=160*v.xscale

	def ShowHealthBar(self):
		self.healthBarHidden=False
		self.healthBarClock=time.time()
	def HideHealthBar(self):
		if not self.healthBarHidden:			
			if time.time()-self.healthBarClock > self.healthBarMaxTime:
				self.healthBarHidden=True

	def updateAndDrawHealthBar(self,win):
		self.healthBar.update(-self.angle,self.position)
		if not self.healthBarHidden:
			self.healthBar.display(win)

	def updateAndDisplayHC(self,win):
		self.hornCollider.update(self.angle,self.position)
		# self.hornCollider.display(win)

	def updateRunBullets(self,win):
		for x in self.bullets:
			if not x.onScreen:
				continue
			x.display(win)
			x.update()
		flushList(self.bullets)

	def shoot(self):
		if time.time()-self.lastShootTime > self.shootGap:						
			self.bullets.append(bullet(self.hornCollider.position.x,self.hornCollider.position.y,self.angle,self,'enemy'))				
			v.shootingSound.play()		
			self.lastShootTime=time.time()


	def shootWild(self):
		if time.time()-self.lastShootTime > self.shootGap:
			angTemp=0
			for j in range(int(360/self.angleGap)):		
				angTemp+=self.angleGap				
				self.bullets.append(bullet(self.position.x,self.position.y,angTemp,self,'enemy',0.5))				
			v.shootingSound.play()		
			self.lastShootTime=time.time()

	def TakeDamage(self,dmg):
		self.health-=dmg
		self.healthBar.reduceHealth(dmg)
		self.ShowHealthBar()
		if self.health < 0:
			self.health=0
			SpawnCloudGroup(self.position)
			self.onScreen=False
			pygame.mixer.music.load('./music/majula.mp3')
			pygame.mixer.music.play(-1,0.0)
			v.cavesList[0].active=True


	def clearToShowNextImg(self):
		self.animTimers[self.animFrame]+=1
		if self.animTimers[self.animFrame] >= self.animTimersMax[self.animFrame]:
			self.animTimers[self.animFrame]=0
			return True
		return False

	def changeAnimation(self,animName):
		if animName=="idle" and self.anim!=0:
			self.anim=0
			self.animFrame=0
		elif animName=="move" and self.anim!=1:
			self.anim=1
			self.animFrame=0
	def getRunningAnimation(self):
		if self.anim==0:
			return "idle"
		elif self.anim==1:
			return "move"
		return "unknown"

	def display(self,win):		
		if self.clearToShowNextImg():
			self.animFrame+=1
			if self.animFrame >= len(self.animations[self.anim]):
				self.animFrame=0
		myrect=self.animations[self.anim][self.animFrame].get_rect()
		myrect.centerx,myrect.centery=self.position.x-v.camera.position.x,self.position.y-v.camera.position.y
		win.blit(pygame.transform.rotate(self.animations[self.anim][self.animFrame],-self.angle-90),myrect)
		'''
		pygame.draw.line(win,(255,0,255),
			(self.hornCollider.position.x-v.camera.position.x,self.hornCollider.position.y-v.camera.position.y),
			(self.hornCollider.position.x+self.vicinity-v.camera.position.x,self.hornCollider.position.y-v.camera.position.y))
		'''
		self.updateAndDisplayHC(win)	

	def moveForward(self):
		self.changeAnimation("move")
		self.velocity.pointToAngle(self.angle)
		self.position.add(self.velocity)

	def update(self,win):
		# self.manualControls()
		# return
		self.HideHealthBar()		
		self.updateRunBullets(win)
		self.updateAndDrawHealthBar(win)
		self.boxCollider.updateP(self.position)	
		if not self.active:
			return
		if self.state=="pursue":
			self.pursueEnemy()
		elif self.state=="attack":
			self.attackEnemy()
		elif self.state=="doingShootAttack":
			self.DoShootingAttack()
		elif self.state=="plungingAttack":
			self.plungeOnEnemy()
		elif self.state=="rainingBullets":
			self.RainBullets()

	def manualControls(self):
		if v.LEFTPRESSED:
			self.angle-=5
		if v.RIGHTPRESSED:
			self.angle+=5


	def DoShootingAttack(self):
		self.shootAttackTimer+=1/v.FRAME_RATE
		if self.shootAttackTimer > self.shootAttackMax:
			self.shootAttackTimer=0
			self.state="attack"
			self.lastAttackTime=time.time()
		self.focusOnEnemy()
		self.shoot()

	def RainBullets(self):
		self.shootWild()
		if self.position.copy().sub(self.enemy.position).mag() > self.vicinity:
			self.state="attack"
			# self.lastAttackTime=time.time()	
			

	def pursueEnemy(self):
		self.focusOnEnemy()
		if self.enemy.position.copy().sub(self.position).mag() > self.enemyProximity:
			self.moveForward()			
		else:
			self.state="attack"


	def attackEnemy(self):
		self.changeAnimation("idle")
		if self.position.copy().sub(self.enemy.position).mag() < self.vicinity:
			self.state="rainingBullets"
			return
		atkStates=["plungingAttack","doingShootAttack"]
		if time.time()- self.lastAttackTime > self.maxAttackGap:
			self.state=atkStates[random.randint(0,len(atkStates)-1)]
			




	def plungeOnEnemy(self):
		if not self.focussed:
			self.focusOnEnemy()
			dirVec=self.enemy.position.copy().sub(self.position).normalized()
			if dirVec.dot(getUnitVector(self.angle)) > 0.9995:
				self.focussed=True
				self.plungeVelocity.pointToAngle(self.angle)
			return
		self.changeAnimation("move")
		self.position.add(self.plungeVelocity)
		if not self.enemy.InvincibleMode and  boxCollision(self.hornCollider,self.enemy.boxCollider):
			self.enemy.TakeDamage(20,self.plungeVelocity)
			self.comeOutOfPlunge()
		for x in v.roadBlocks:			
			if boxCollision(x,self.hornCollider):
				self.comeOutOfPlunge()

	def comeOutOfPlunge(self):
		self.state="attack"
		self.focussed=False
		self.lastAttackTime=time.time()



	def focusOnEnemy(self):
		enemyAngle=self.enemy.position.copy().sub(self.position).heading()
		
		if abs(enemyAngle-self.angle) > 360+enemyAngle-self.angle:
			enemyAngle+=360
		elif abs(self.angle+360-enemyAngle) < abs(enemyAngle-self.angle):
			self.angle+=360
		
		self.angle=Lerp(self.angle,enemyAngle,9)
		if(self.angle > 360):
			self.angle-=360		


class soldier:
	def __init__(self,x,y):
		self.onScreen=True
		self.width=200*v.xscale
		self.height=200*v.yscale
		self.position=CreateVector(x,y)
		self.boxCollider=collisionBox(x,y,self.width*0.5,self.height*0.5)
		self.shootPosition=positionBlock(x,y,91*v.xscale,49*v.yscale,0,self.width*0.05,self.height*0.05)
		self.idle_images,self.move_images,self.shoot_images,self.reload_images,self.melee_images=[],[],[],[],[]		
		self.images=[]	
		self.angle=0
		self.animInQueue=None
		self.weaponIndex=0
		self.health=100
		self.maxHealth=100
		self.healthBar=healthBar(x,y,0,-80*v.yscale,-40*v.xscale,200*v.xscale,10*v.yscale,self.maxHealth)
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
		for i in range(15):
			imagex=pygame.transform.scale(pygame.image.load(os.path.join('sprites',
				f'soldier/reload/survivor-reload_handgun_{i}.png')),(self.width,self.height))
			self.reload_images.append(imagex)
		for i in range(15):
			imagex=pygame.transform.scale(pygame.image.load(os.path.join('sprites',
				f'soldier/meleeattack/survivor-meleeattack_handgun_{i}.png')),(self.width,self.height))
			self.melee_images.append(imagex)
		
		#flashlight images
		self.flashlight_idle_images,self.flashlight_melee_images,self.flashlight_move_images=[],[],[]
		for i in range(20):
			imagex=pygame.transform.scale(pygame.image.load(os.path.join('sprites',
				f'flashlight/idle/survivor-idle_flashlight_{i}.png')),(self.width,self.height))
			self.flashlight_idle_images.append(imagex)
		for i in range(15):
			imagex=pygame.transform.scale(pygame.image.load(os.path.join('sprites',
				f'flashlight/meleeattack/survivor-meleeattack_flashlight_{i}.png')),(self.width,self.height))
			self.flashlight_melee_images.append(imagex)
		for i in range(20):
			imagex=pygame.transform.scale(pygame.image.load(os.path.join('sprites',
				f'flashlight/move/survivor-move_flashlight_{i}.png')),(self.width,self.height))
			self.flashlight_move_images.append(imagex)

		#knife images
		self.knife_idle_images,self.knife_melee_images,self.knife_move_images=[],[],[]
		for i in range(20):
			imagex=pygame.transform.scale(pygame.image.load(os.path.join('sprites',
				f'knife/idle/survivor-idle_knife_{i}.png')),(self.width,self.height))
			self.knife_idle_images.append(imagex)
		for i in range(15):
			imagex=pygame.transform.scale(pygame.image.load(os.path.join('sprites',
				f'knife/meleeattack/survivor-meleeattack_knife_{i}.png')),(self.width,self.height))
			self.knife_melee_images.append(imagex)
		for i in range(20):
			imagex=pygame.transform.scale(pygame.image.load(os.path.join('sprites',
				f'knife/move/survivor-move_knife_{i}.png')),(self.width,self.height))
			self.knife_move_images.append(imagex)

		#rifle images
		self.rifle_idle_images,self.rifle_melee_images,self.rifle_move_images,self.rifle_reload_images,self.rifle_shoot_images=[],[],[],[],[]
		for i in range(20):
			imagex=pygame.transform.scale(pygame.image.load(os.path.join('sprites',
				f'rifle/idle/survivor-idle_rifle_{i}.png')),(self.width,self.height))
			self.rifle_idle_images.append(imagex)
		for i in range(15):
			imagex=pygame.transform.scale(pygame.image.load(os.path.join('sprites',
				f'rifle/meleeattack/survivor-meleeattack_rifle_{i}.png')),(self.width,self.height))
			self.rifle_melee_images.append(imagex)
		for i in range(20):
			imagex=pygame.transform.scale(pygame.image.load(os.path.join('sprites',
				f'rifle/move/survivor-move_rifle_{i}.png')),(self.width,self.height))
			self.rifle_move_images.append(imagex)
		for i in range(20):
			imagex=pygame.transform.scale(pygame.image.load(os.path.join('sprites',
				f'rifle/reload/survivor-reload_rifle_{i}.png')),(self.width,self.height))
			self.rifle_reload_images.append(imagex)
		for i in range(3):
			imagex=pygame.transform.scale(pygame.image.load(os.path.join('sprites',
				f'rifle/shoot/survivor-shoot_rifle_{i}.png')),(self.width,self.height))
			self.rifle_shoot_images.append(imagex)

		#shotgun images
		self.shotgun_idle_images,self.shotgun_melee_images,self.shotgun_move_images,self.shotgun_reload_images,self.shotgun_shoot_images=[],[],[],[],[]
		for i in range(20):
			imagex=pygame.transform.scale(pygame.image.load(os.path.join('sprites',
				f'shotgun/idle/survivor-idle_shotgun_{i}.png')),(self.width,self.height))
			self.shotgun_idle_images.append(imagex)
		for i in range(15):
			imagex=pygame.transform.scale(pygame.image.load(os.path.join('sprites',
				f'shotgun/meleeattack/survivor-meleeattack_shotgun_{i}.png')),(self.width,self.height))
			self.shotgun_melee_images.append(imagex)
		for i in range(20):
			imagex=pygame.transform.scale(pygame.image.load(os.path.join('sprites',
				f'shotgun/move/survivor-move_shotgun_{i}.png')),(self.width,self.height))
			self.shotgun_move_images.append(imagex)
		for i in range(20):
			imagex=pygame.transform.scale(pygame.image.load(os.path.join('sprites',
				f'shotgun/reload/survivor-reload_shotgun_{i}.png')),(self.width,self.height))
			self.shotgun_reload_images.append(imagex)
		for i in range(3):
			imagex=pygame.transform.scale(pygame.image.load(os.path.join('sprites',
				f'shotgun/shoot/survivor-shoot_shotgun_{i}.png')),(self.width,self.height))
			self.shotgun_shoot_images.append(imagex)

		self.weaponAnims=[[self.idle_images,self.move_images,self.shoot_images,self.reload_images,self.melee_images],
						  [self.flashlight_idle_images,self.flashlight_move_images,self.flashlight_melee_images,self.flashlight_melee_images,
						   self.flashlight_melee_images],
						  [self.knife_idle_images,self.knife_move_images,self.knife_melee_images,self.knife_melee_images,
						   self.knife_melee_images],
						  [self.rifle_idle_images,self.rifle_move_images,self.rifle_shoot_images,self.rifle_reload_images,
						   self.rifle_melee_images],
						  [self.shotgun_idle_images,self.shotgun_move_images,self.shotgun_shoot_images,self.shotgun_reload_images,
						   self.shotgun_melee_images],
		                  ]


		self.images=[self.idle_images,self.move_images,self.shoot_images,self.reload_images,self.melee_images]
		self.animTimers=[0,0,0,0,0]
		self.animTimerMax=[1,1,1,1,1]
		self.anim=0
		self.frame=0
		
		self.rotationSpeedMin=2
		self.rotationSpeed=self.rotationSpeedMin
		self.rotationSpeedAcc=0.25
		self.rotationSpeedMax=8

		self.vmax=10
		self.velMin=1
		self.velocity=CreateVector(self.velMin,0)	
		self.vel=self.velMin
		self.bullets=[]
		self.lastShootTime=0
		self.shootGap=1
		self.us=userSlider()
		self.weaponChangeAuthorized=True

		self.InvincibleMode=False
		self.invincibleStartTime=0
		self.invincibleMaxGap=2
		self.flickerCounter=0

		self.healthBarHidden=False
		self.healthBarClock=0
		self.healthBarMaxTime=3

		self.staggerDir=None
		self.staggerVel=16
		self.stoppedMovement=False
		self.staggering=False
		self.staggerStartTime=0
		self.maxStaggerTime=0.25

	def ShowHealthBar(self):
		self.healthBarHidden=False
		self.healthBarClock=time.time()
	def HideHealthBar(self):
		if not self.healthBarHidden:			
			if time.time()-self.healthBarClock > self.healthBarMaxTime:
				self.healthBarHidden=True
	def IncreaseRotationSpeed(self):
		if self.rotationSpeed < self.rotationSpeedMax:
			self.rotationSpeed+=self.rotationSpeedAcc


	def ManageInvincibility(self):
		if not self.InvincibleMode:
			return
		if time.time()-self.invincibleStartTime > self.invincibleMaxGap:
			self.InvincibleMode=False
	def TakeDamage(self,dmg,enemyVel=None):		
		self.health-=dmg
		self.healthBar.reduceHealth(dmg)
		self.ShowHealthBar()
		if enemyVel:
			self.startStagger(enemyVel)
		self.InvincibleMode=True
		self.invincibleStartTime=time.time()
		if self.health < 0:
			self.health=0
			self.onScreen=False
			SpawnCloudGroup(self.position)
			v.gameManager.reloadLevel()
			v.glassBreak.play()
	def changeWeapon(self):
		self.weaponIndex+=1
		if self.weaponIndex >= len(self.weaponAnims):
			self.weaponIndex=0
		self.images=self.weaponAnims[self.weaponIndex]
	def changeWeapons(self):
		if v.TPRESSED:
			if self.weaponChangeAuthorized:
				self.weaponChangeAuthorized=False
				self.changeWeapon()
				changeBullet(self.presentWeapon())
		elif not self.weaponChangeAuthorized:
			self.weaponChangeAuthorized=True

	def shoot(self):
		if time.time()-self.lastShootTime > self.shootGap:
			self.animInQueue=self.runningAnimation()
			if self.presentWeapon() not in ['flashlight','knife']:
				self.bullets.append(bullet(self.shootPosition.position.x,self.shootPosition.position.y,360-self.angle,self,'player'))
				# print("changed animation to shoot")
				self.ChangeAnimation("shoot")
				v.shootingSound.play()
			else:
				# print("changed animation to melee")
				self.ChangeAnimation("melee")
			self.lastShootTime=time.time()

	def animUpdateAllowed(self):

		self.animTimers[self.anim]+=1
		if self.animTimers[self.anim] >= self.animTimerMax[self.anim]:
			self.animTimers[self.anim]=0
			return True
		return False

	def FlickerManagerCleared(self):
		if not self.InvincibleMode:
			return True
		self.flickerCounter+=1
		if self.flickerCounter > 100:
			self.flickerCounter=0
		if self.flickerCounter % 3 == 0:
			return True
		return False

	def updateAnimation(self):
		if not self.animUpdateAllowed():
			return False
		
		self.frame+=1		
		if self.frame >= len(self.images[self.anim]):
			if not self.animInQueue:
				self.frame=0
			elif self.runningAnimation()=='shoot':
				self.ChangeAnimation('reload')
			else:
				self.ChangeAnimation(self.animInQueue)
				self.animInQueue=None

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
		elif animName=="reload" and self.anim!=3:			
			self.anim=3
			self.frame=0
		elif animName=="melee" and self.anim!=4:
			self.anim=4
			self.frame=0

	def presentWeapon(self):
		if self.weaponIndex==0:
			return 'handgun'
		elif self.weaponIndex==1:
			return 'flashlight'
		elif self.weaponIndex==2:
			return 'knife'
		elif self.weaponIndex==3:
			return 'rifle'
		elif self.weaponIndex==4:
			return 'shotgun'

	def runningAnimation(self):
		if self.anim==0:
			return 'idle'
		elif self.anim==1:
			return 'move'
		elif self.anim==2:
			return 'shoot'
		elif self.anim==3:
			return 'reload'
		elif self.anim==4:
			return 'melee'


	def updateRunBullets(self,win):
		for x in self.bullets:
			if not x.onScreen:
				continue
			x.display(win)
			x.update()
		flushList(self.bullets)
############Stagger starts################
	def staggerBack(self):
		if not self.stoppedMovement:
			self.position.add(self.staggerDir.copy().mult(self.staggerVel))
			for elem in v.roadBlocks:
				if not elem.onScreen:
					continue				
				if boxCollision(self,elem):					
					self.position.add(self.staggerDir.copy().mult(self.staggerVel*-1))
					self.stoppedMovement=True
		if time.time()-self.staggerStartTime > self.maxStaggerTime:
			self.staggering=False
			self.stoppedMovement=False
			self.staggerStartTime=time.time()
	def startStagger(self,enemyVel):		
		self.staggerDir=enemyVel.normalized()
		self.staggering=True
		self.staggerStartTime=time.time()
############Stagger ends##################


	def update(self,win):
		self.HideHealthBar()
		self.ManageInvincibility()
		self.updateRunBullets(win)
		self.updateAndDrawShootPos(win)
		self.updateAndDrawHealthBar(win)
		self.changeWeapons()

		if self.staggering:
			self.staggerBack()
		else:
			if v.SPACEPRESSED:
				self.shoot()
			if v.LEFTPRESSED:
				self.angle+=self.rotationSpeed
				self.IncreaseRotationSpeed()
				if self.angle > 360:
					self.angle-=360
				self.updateVelocity()
			elif v.RIGHTPRESSED:
				self.angle-=self.rotationSpeed
				self.IncreaseRotationSpeed()
				if self.angle < 0:
					self.angle+=360
				self.updateVelocity()
			else:
				self.rotationSpeed=self.rotationSpeedMin

			if v.UPPRESSED:	
				if self.runningAnimation()=="idle":
					self.ChangeAnimation("move")		
				self.ApplyVelocity()
			else:
				if self.runningAnimation()=="move":
					self.ChangeAnimation("idle")
				self.DeApplyVelocity()

		self.boxCollider.updateP(self.position)

	def updateAndDrawHealthBar(self,win):
		self.healthBar.update(-self.angle,self.position)
		if not self.healthBarHidden:
			self.healthBar.display(win)
		
	def updateAndDrawShootPos(self,win):
		self.shootPosition.update(360-self.angle,self.position)
		# self.shootPosition.display(win)	
		# self.us.adjustSliderValues(self.shootPosition.relPosition,win)	
		
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
		if not self.FlickerManagerCleared():
			return
		draw_translate_rotate(self.images[self.anim][self.frame],
							  self.angle,self.position.x-self.width/2-v.camera.position.x,
							  self.position.y-self.height/2-v.camera.position.y,win)
		self.updateAnimation()
		#self.boxCollider.display(win)

################### Position changer starts #################################
class posChanger:
	def __init__(self,obj):
		self.onScreen=True
		self.obj=obj
		self.hdels=[1,0.5]
		self.wdels=[1,0.5]
		self.xdels=[1,0.5]
		self.ydels=[1,0.5]
	def update(self,win):
		self.obj.imagex=pygame.transform.scale(self.obj.imagexOrig,(int(self.obj.width),int(self.obj.height)))		
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
		w2screen(win,"width:"+str(round(self.obj.width/v.xscale)),300,100)
		w2screen(win,"height:"+str(round(self.obj.height/v.yscale)),300,150)
		w2screen(win,"xpos:"+str(round(self.obj.position.x/v.xscale)),300,200)
		w2screen(win,"ypos:"+str(round(self.obj.position.y/v.yscale)),300,250)
		if v.TPRESSED:
			self.obj.height=self.adjustSliderValues(self.obj.height,self.hdels,False)
		elif v.BPRESSED:
			self.obj.height=self.adjustSliderValues(self.obj.height,self.hdels,True)
		else:
			self.hdels[0]=1
		if v.HPRESSED:
			self.obj.width=self.adjustSliderValues(self.obj.width,self.wdels,False)
		elif v.FPRESSED:
			self.obj.width=self.adjustSliderValues(self.obj.width,self.wdels,True)
		else:
			self.wdels[0]=1
		

		if v.IPRESSED:
			self.obj.position.y=self.adjustSliderValues(self.obj.position.y,self.ydels,False)
		elif v.MPRESSED:
			self.obj.position.y=self.adjustSliderValues(self.obj.position.y,self.ydels,True)
		else:
			self.ydels[0]=1
		if v.LPRESSED:
			self.obj.position.x=self.adjustSliderValues(self.obj.position.x,self.xdels,False)
		elif v.JPRESSED:
			self.obj.position.x=self.adjustSliderValues(self.obj.position.x,self.xdels,True)
		else:
			self.xdels[0]=1

################### Position changer ends #################################


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
			self.imagexOrig=HORIZONTAL_PIPE
		else:
			self.imagexOrig=VERTICAL_PIPE

		self.imagex=pygame.transform.scale(self.imagexOrig,(self.width,self.height))

		if hori:
			self.leftCollider= collisionBox(x-self.width*0.49,y                 ,0.02*self.width,self.height)
			self.rightCollider=collisionBox(x+self.width*0.49,y                 ,0.02*self.width,self.height)
			self.topCollider =collisionBox(x                 ,y-self.height*0.4,self.width ,0.2*self.height,'green')
			self.bottomCollider =collisionBox(x              ,y+self.height*0.4,self.width ,0.2*self.height,'green')
			self.colliders=[self.leftCollider,self.rightCollider,self.bottomCollider,self.topCollider]
		else:
			self.leftCollider= collisionBox(x-self.width*0.4,y       ,0.2*self.width,self.height)
			self.rightCollider=collisionBox(x+self.width*0.4,y       ,0.2*self.width,self.height)
			self.topCollider =collisionBox(x                 ,y-self.height*0.49,self.width ,0.02*self.height,'green')
			self.bottomCollider =collisionBox(x              ,y+self.height*0.49,self.width ,0.02*self.height,'green')
			self.colliders=[self.leftCollider,self.rightCollider,self.bottomCollider,self.topCollider]

	def checkCollisions(self,obj):
		if boxCollision(self.leftCollider,obj.boxCollider):
			obj.reelLeft()
		if boxCollision(self.rightCollider,obj.boxCollider):
			obj.reelRight()
		if boxCollision(self.bottomCollider,obj.boxCollider):
			obj.reelDown()
		if boxCollision(self.topCollider,obj.boxCollider):
			obj.reelUp()



	def display(self,win):
		
		draw_translate_rotate(self.imagex,
							  self.angle,self.position.x-self.width/2-v.camera.position.x,
							  self.position.y-self.height/2-v.camera.position.y,win)	
		# self.displayColliders(win)
	def displayColliders(self,win):
		for i,col in enumerate(self.colliders):			
			col.display(win)


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
	

			




		