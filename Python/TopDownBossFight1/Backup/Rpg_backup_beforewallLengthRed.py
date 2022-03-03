import pygame
from pygame.locals import *
import time
import os,sys
import random
import math,re



################## Helper functions start #################
def terminate():
    pygame.quit()
    sys.exit()
def Lerp(startValue,endValue,lerpFac):
	return startValue+(endValue-startValue)/lerpFac

def AngleLerp(startValue,endValue,lerpFac):
	if abs(endValue - startValue) < SepFrom360(startValue) + SepFrom360(endValue):
		return startValue+(endValue-startValue)/lerpFac
	return CloseAngleDistance360(startValue,(SepFrom360(startValue)+SepFrom360(endValue))/lerpFac )


def SepFrom360(angle):
	if angle < 180:
		return angle
	return 360 - angle

def CloseAngleDistance360(startAngle,delta):
	if startAngle < 180:
		if startAngle > delta:
			return startAngle - delta
		return 360 - (delta - startAngle)
	else:
		if 360 - startAngle > delta:
			return startAngle + delta
		return delta - (360 - startAngle)


def w2screen(win,txt,px,py,fsiz=50):	
	STAT_FONT= pygame.font.SysFont("comicsans",fsiz)
	text=STAT_FONT.render(txt,1,(255,0,0))
	win.blit(text,(px,py))

def vectorInRotAx(a,angle):
	t=d2r(angle)
	xval= a.x * math.cos(t)+a.y*math.sin(t)
	yval=-a.x * math.sin(t)+a.y*math.cos(t)
	return CreateVector(xval,yval)

def vectorInrRotAx(a,angle):
	t=d2r(angle)
	xval= a.x * math.cos(t)-a.y*math.sin(t)
	yval= a.x * math.sin(t)+a.y*math.cos(t)
	return CreateVector(xval,yval) 

def d2r(ang):
	return ang/180*math.pi
def r2d(ang):
	return ang/math.pi*180

def getUnitVector(angle):
	return CreateVector(math.cos(d2r(angle)),math.sin(d2r(angle)))


def draw_translate_rotate(img,rotangle,x,y,win):
	rotated_image = pygame.transform.rotate(img, rotangle)
	new_rect = rotated_image.get_rect(center=img.get_rect(topleft=(x,y)).center)
	win.blit(rotated_image,new_rect.topleft)

def boxCollision(obj1,obj2):
	rect1=pygame.Rect(obj1.position.x-obj1.width/2-gameManager.camera.position.x,
					  obj1.position.y-obj1.height/2-gameManager.camera.position.y,
					  obj1.width,obj1.height)
	rect2=pygame.Rect(obj2.position.x-obj2.width/2-gameManager.camera.position.x,
					  obj2.position.y-obj2.height/2-gameManager.camera.position.y,
					  obj2.width,obj2.height)
	return rect1.colliderect(rect2)

def check_collision(obj1,obj2):
	mask1=obj1.get_mask()
	mask2=obj2.get_mask()
	offset=(round(obj2.position.x-obj1.position.x),round(obj2.position.y-obj1.position.y))
	if mask1.overlap(mask2,offset):
		return True
	return False

def flushList(lis):
	for elem in lis[:]:
		if not elem.onScreen:
			lis.remove(elem)


class CreateVector:
	def __init__(self,x,y):
		self.x=x
		self.y=y

	def set(self,x,y):
		self.x=x
		self.y=y
	def setVec(self,vec):
		self.x=vec.x
		self.y=vec.y
	def mag(self):
		return math.sqrt(self.x**2+self.y**2)	
	def add(self,vec):
		self.x+=vec.x
		self.y+=vec.y
		return self
	def sub(self,vec):
		self.x-=vec.x
		self.y-=vec.y
		return self
	def mult(self,num):
		self.x*=num
		self.y*=num
		return self
	def div(self,num):
		self.x/=num
		self.y/=num
		return self
	def normalize(self):
		magnitude=self.mag()
		self.x/=magnitude
		self.y/=magnitude
		return self
	def normalized(self):
		copyVec=self.copy()
		return copyVec.normalize()
	def copy(self):
		copyVec=CreateVector(self.x,self.y)
		return copyVec

	def equals(self,vec):
		return self.x==vec.x and self.y==vec.y
	def desc(self):
		return (f'Vector with values x:{self.x} and y:{self.y}' )
	def heading(self):
		angx=r2d(math.atan2(self.y,self.x))
		if angx < 0:
			angx+=360
		return angx
	def pointToAngle(self,angle):
		mag=self.mag()
		self.x=mag*math.cos(d2r(angle))
		self.y=mag*math.sin(d2r(angle))
		return self
	def rotateByAngle(self,delta):
		ang=self.heading()
		return self.pointToAngle(delta+ang)

	def dot(self,vec):
		return self.x*vec.x+self.y*vec.y

def Raycast(originx,direction,lenx,objToCheck):
	origin=originx.copy()
	destin=originx.copy().add(direction.copy().mult(lenx))
	# pygame.draw.line(win,(255,0,0),(origin.x-gameManager.camera.position.x,origin.y-gameManager.camera.position.y),(destin.x-gameManager.camera.position.x,destin.y-gameManager.camera.position.y))
	deltaz=2*xscale
	startLen=0
	while startLen < lenx:		
		if PointInsideObject(objToCheck,origin.add(direction.copy().mult(deltaz))):
			return True
		startLen+=deltaz
	return False

def PointInsideObject(objToCheck,pt):
	if pt.x > objToCheck.position.x-objToCheck.width/2 and pt.x < objToCheck.position.x+objToCheck.width/2:
		if pt.y > objToCheck.position.y-objToCheck.height/2 and pt.y < objToCheck.position.y+objToCheck.height/2:
			return True
	return False

def FarOut(obj):
	camSepx=obj.position.x-gameManager.camera.position.x
	camSepy=obj.position.y-gameManager.camera.position.y
	return (((camSepx > 0 and camSepx-obj.width/2 > WIN_WIDTH) or (camSepx < 0 and abs(camSepx) > obj.width/2)) or ((camSepy > 0 and camSepy-obj.height/2 > WIN_HEIGHT) or (camSepy < 0 and abs(camSepy) > obj.height/2)))

################## Helper functions end   #################

################### Camera starts #############################################
class Camera:
	def __init__(self):
		self.position=CreateVector(0,0)
		self.target=None
		self.mouseLockX=0
		self.mouseLockY=0
		self.temp=0
		self.maxAllowedXRoaming=WIN_WIDTH*0.3
		self.maxAllowedYRoaming=WIN_HEIGHT*0.3
		self.onTemporaryFix=False
		self.tgtPosition=None
		self.camSpeed=100*xscale
		self.lerpFactor=8
	def runwithmouse(self):
		if MOUSECLICKED:			
			if self.mouseLockX==0:
				self.mouseLockX=MOUSEX
			if self.mouseLockY==0:
				self.mouseLockY=MOUSEY 
			self.position.x-=(MOUSEX-self.mouseLockX)/10
			self.position.y-=(MOUSEY-self.mouseLockY)/10			
		else:
			if self.mouseLockX!=0:
				self.mouseLockX=0
			if self.mouseLockY!=0:
				self.mouseLockY=0
	def TemporarilySkipToPoint(self,tgtPosition):
		self.onTemporaryFix=True
		self.tgtPosition=tgtPosition.sub(CreateVector(-300*xscale,-300*yscale))
		print(f'{self.tgtPosition.x},{self.tgtPosition.y}')
	def FixToTempPoint():
		if math.abs(self.tgtPosition.x-self.position.x) <= self.camSpeed:
			if math.abs(self.tgtPosition.y-self.position.y) <=self.camSpeed:
				self.onTemporaryFix=False
				return
		if self.tgtPosition.x > self.position.x:
			self.position.x+=self.camSpeed
		else:
			self.position.x-=self.camSpeed

		if self.tgtPosition.y > self.position.y:
			self.position.y+=self.camSpeed
		else:
			self.position.y-=self.camSpeed

	def SmoothFocus(self,horiFollow,vertFollow):		
		if not self.target:
			return
		if horiFollow:
			self.position.x=Lerp(self.position.x,self.target.position.x- WIN_WIDTH/2,self.lerpFactor)
		if vertFollow:
			self.position.y=Lerp(self.position.y,self.target.position.y- WIN_HEIGHT/2,self.lerpFactor)


	def followTarget(self,horiFollow=True,vertFollow=True):
		if not self.target:
			return
		self.SmoothFocus(horiFollow,vertFollow)
		return
		if horiFollow:
			roamingDistX=self.target.position.x-(WIN_WIDTH/2+self.position.x)
			if abs(roamingDistX) > self.maxAllowedXRoaming:			
				if roamingDistX > 0:
					self.position.x+=roamingDistX-self.maxAllowedXRoaming
				else:
					self.position.x+=roamingDistX+self.maxAllowedXRoaming
		if vertFollow:
			roamingDistY=self.target.position.y-(WIN_HEIGHT/2+self.position.y)
			if abs(roamingDistY) > self.maxAllowedYRoaming:
				if roamingDistY > 0:
					self.position.y+=roamingDistY-self.maxAllowedYRoaming
				else:
					self.position.y+=roamingDistY+self.maxAllowedYRoaming
################### Camera ends   #############################################

###################Dummy Focus Point starts ##############################
class DummyFocus:
	def __init__(self,x,y):
		self.onScreen=True
		self.position=CreateVector(x,y)
###################Dummy Focus Point ends ################################

################### Position changer starts #################################
class posChanger:
	def __init__(self,obj,scaleImage=True):
		self.onScreen=True
		self.obj=obj
		self.hdels=[1,0.5]
		self.wdels=[1,0.5]
		self.xdels=[1,0.5]
		self.ydels=[1,0.5]
		self.scaleImage=scaleImage
	def assignObject(self,obj):
		self.obj=obj
	def update(self,win):
		if self.scaleImage:
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
		w2screen(win,"width:"+str(round(self.obj.width/xscale)),300,100)
		w2screen(win,"height:"+str(round(self.obj.height/yscale)),300,150)
		w2screen(win,"xpos:"+str(round(self.obj.position.x/xscale)),300,200)
		w2screen(win,"ypos:"+str(round(self.obj.position.y/yscale)),300,250)
		if TPRESSED:
			self.obj.height=self.adjustSliderValues(self.obj.height,self.hdels,False)
		elif BPRESSED:
			self.obj.height=self.adjustSliderValues(self.obj.height,self.hdels,True)
		else:
			self.hdels[0]=1
		if HPRESSED:
			self.obj.width=self.adjustSliderValues(self.obj.width,self.wdels,False)
		elif FPRESSED:
			self.obj.width=self.adjustSliderValues(self.obj.width,self.wdels,True)
		else:
			self.wdels[0]=1
		

		if IPRESSED:
			self.obj.position.y=self.adjustSliderValues(self.obj.position.y,self.ydels,False)
		elif MPRESSED:
			self.obj.position.y=self.adjustSliderValues(self.obj.position.y,self.ydels,True)
		else:
			self.ydels[0]=1
		if LPRESSED:
			self.obj.position.x=self.adjustSliderValues(self.obj.position.x,self.xdels,False)
		elif JPRESSED:
			self.obj.position.x=self.adjustSliderValues(self.obj.position.x,self.xdels,True)
		else:
			self.xdels[0]=1

################### Position changer ends #################################

#ActiveGameObject starts
class ActiveGameObject:
	def __init__(self):
		self.obj=None
	def update(self):
		if not self.obj:
			return
#ActiveGameObject ends
################## Position Block Starts ###################################
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
			
	def display(self):
		if self.centered:
			pygame.draw.rect(win,self.col,
									(self.position.x-self.width/2-gameManager.camera.position.x,
									 self.position.y-self.height/2-gameManager.camera.position.y,self.width,self.height))
		else:
			pygame.draw.rect(win,self.col,
									(self.position.x-gameManager.camera.position.x,
									 self.position.y-self.height/2-gameManager.camera.position.y,self.width,self.height))
################## Position Block Ends   ###################################

##Gate Starts ##
class Gate:
	def __init__(self,x,y,width,height,hori=True):
		self.onScreen=True
		self.position=CreateVector(x,y)
		self.width=int(width*xscale)
		self.height=int(height*yscale)
		self.hori=hori
		self.imagexOrig=LADDER
		self.imagex=pygame.transform.scale(self.imagexOrig,(self.width,self.height))
		self.slideVelocity=CreateVector(5*xscale,0) if hori else CreateVector(0,5*yscale)
		self.slideStartTime=0
		self.maxSlideTime=1.5
		self.slidingDone=False
		self.sliding=False
		if hori:
			self.leftCollider=positionBlock(x,y,-0.495*width,0,0,0.01*width,0.8*height,(0,0,255))
			self.rightCollider=positionBlock(x,y,0.495*width,0,0,0.01*width,0.8*height,(0,0,255))
			self.topCollider=positionBlock(x,y,0,-0.45*height,0,width,0.1*height)
			self.bottomCollider=positionBlock(x,y,0,0.45*height,0,width,0.1*height)
		else:
			self.leftCollider=positionBlock(x,y,-0.48*width,0,0,0.04*width,height,(0,0,255))
			self.rightCollider=positionBlock(x,y,0.48*width,0,0,0.04*width,height,(0,0,255))
			self.topCollider=positionBlock(x,y,0,-0.495*height,0,0.99*width,0.01*height)
			self.bottomCollider=positionBlock(x,y,0,0.495*height,0,0.99*width,0.01*height)
		self.colliders=[self.leftCollider,self.rightCollider,self.topCollider,self.bottomCollider]
	def display(self):
		myrect=self.imagex.get_rect()
		myrect.centerx,myrect.centery=self.position.x-gameManager.camera.position.x,self.position.y-gameManager.camera.position.y
		win.blit(self.imagex,myrect)
		# for x in self.colliders:
		# 	x.display()

	def updateColliderPositions(self):		
		self.leftCollider.update(0,self.position)
		self.rightCollider.update(0,self.position)
		self.topCollider.update(0,self.position)
		self.bottomCollider.update(0,self.position)
		

	def update(self):
		# if SPACEPRESSED:
		# 	self.CloseGate()
		self.Slide()

	def CloseGate(self):
		if not self.sliding and not self.slidingDone:
			self.sliding=True
			self.slideStartTime=time.time()
	def Slide(self):
		if self.slidingDone or not self.sliding:
			return
		self.position.add(self.slideVelocity)
		self.updateColliderPositions()
		if time.time()- self.slideStartTime > self.maxSlideTime:
			self.slidingDone=True
			self.sliding= False

##Gate Ends ##

################## BrickWall Starts ######################################
class BrickWall:
	def __init__(self,x,y,width,height,hori=True):
		self.onScreen=True
		self.position=CreateVector(x,y)
		self.hori=hori
		self.width=int(width*xscale)
		self.height=int(height*yscale)
		self.imagexOrig=BRICKWALL
		self.imagex=pygame.transform.scale(self.imagexOrig,(self.width,self.height))
		if hori:
			self.leftCollider=positionBlock(x,y,-0.495*width,0,0,0.01*width,0.8*height,(0,0,255))
			self.rightCollider=positionBlock(x,y,0.495*width,0,0,0.01*width,0.8*height,(0,0,255))
			self.topCollider=positionBlock(x,y,0,-0.45*height,0,width,0.1*height)
			self.bottomCollider=positionBlock(x,y,0,0.45*height,0,width,0.1*height)
		else:
			self.leftCollider=positionBlock(x,y,-0.48*width,0,0,0.04*width,height,(0,0,255))
			self.rightCollider=positionBlock(x,y,0.48*width,0,0,0.04*width,height,(0,0,255))
			self.topCollider=positionBlock(x,y,0,-0.495*height,0,0.99*width,0.01*height)
			self.bottomCollider=positionBlock(x,y,0,0.495*height,0,0.99*width,0.01*height)
		self.colliders=[self.leftCollider,self.rightCollider,self.topCollider,self.bottomCollider]
	def display(self):
		myrect=self.imagex.get_rect()
		myrect.centerx,myrect.centery=self.position.x-gameManager.camera.position.x,self.position.y-gameManager.camera.position.y
		win.blit(self.imagex,myrect)
		# for x in self.colliders:
		# 	x.display()
	def update(self):
		pass
################## BrickWall Ends ########################################
################### Collision Box Starts #################################
class collisionBox:
	def __init__(self,x,y,width,height,col='red'):
		self.width=width
		self.height=height
		self.position=CreateVector(x,y)
		self.col=(255,0,0) if col=='red' else (0,0,255)
	def display(self):
		pygame.draw.rect(win,self.col,
									(self.position.x-self.width/2-gameManager.camera.position.x,
									 self.position.y-self.height/2-gameManager.camera.position.y,self.width,self.height))
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
################## Collision Box Ends ######################################
#####################HealthBar with Position Block starts #####################
class positionBlockStatic:
	def __init__(self,x,y,rx,ry,angle,width,height,col=(255,0,0),centered=True,screenBar=True):
		self.width=width
		self.height=height
		self.angle=angle
		self.aposition=CreateVector(x,y)
		self.relPosition=CreateVector(rx,ry)		
		self.position=self.aposition.copy().add(vectorInrRotAx(self.relPosition,self.angle))
		self.col=col
		self.centered=centered
		self.screenBar=screenBar #screenBar=True implies that the position of the healthBar is static

		
	def update(self,angle,position):
		if self.angle!=angle or not self.position.equals(position):
			self.aposition.setVec(position)
			self.angle=angle			
			self.position=self.aposition.copy().add(vectorInrRotAx(self.relPosition,self.angle))
	def display(self):
		camerax=gameManager.camera.position.x
		cameray=gameManager.camera.position.y		
		if self.screenBar:			
			camerax,cameray=0,0
		if self.centered:
			pygame.draw.rect(win,self.col,
									(self.position.x-self.width/2-camerax,
									 self.position.y-self.height/2-cameray,self.width,self.height))
		else:
			pygame.draw.rect(win,self.col,
									(self.position.x-camerax,
									 self.position.y-self.height/2-cameray,self.width,self.height))

class HealthBar:
	def __init__(self,x,y,rx,ry,angle,width,height,maxHealth,screenBar=True):		
		self.greenBar=positionBlockStatic(x,y,rx,ry,angle,width,height,(26,255,209),False,screenBar)
		self.redBar=positionBlockStatic(x,y,rx,ry,angle,width,height,(163,163,194),False,screenBar)
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
	def display(self):		
		self.redBar.display()
		self.greenBar.display()
#####################HealthBar with Position Block ends #######################

##################Cloud Burst ##################################################
class cloudBurst:
	def __init__(self,x,y):
		self.onScreen=True
		self.position=CreateVector(x,y)
		self.width=int(30*xscale)
		self.height=int(30*yscale)
		self.origWidth=self.width
		self.image=pygame.transform.scale(CLOUDIMAGE,(self.width,self.height))
		self.startTime=time.time()
		self.age=0.2
		self.velocity=CreateVector(random.randint(-4,4),random.randint(-4,4))
	def display(self):
		myrect=self.image.get_rect()
		myrect.centerx,myrect.centery=self.position.x-gameManager.camera.position.x,self.position.y-gameManager.camera.position.y
		win.blit(self.image,myrect)
	def update(self):
		self.position.add(self.velocity)	
		self.width=int(self.width*0.95)
		self.height=int(self.height*0.95)
		self.image=pygame.transform.scale(CLOUDIMAGE,(self.width,self.height))
		if self.width/self.origWidth < 0.05:
			self.onScreen=False
###################Cloud Burst Ends##################################################
def SpawnCloudGroup(pos):
	for i in range(30):
		gameManager.cloudsList.append(cloudBurst(pos.x,pos.y))
		gameManager.volatiles.append(gameManager.cloudsList[-1])

##Zombie starts###
class Zombie:
	def __init__(self,x,y,width,height):
		self.onScreen=True
		self.position=CreateVector(x,y)	
		self.focusPoint=DummyFocus(x,y)
		self.width=int(width*xscale)
		self.height=int(height*yscale)
		self.boxCollider=collisionBox(x,y,self.width*0.5,self.height*0.5)
		self.angle=0
		self.idle_images,self.attack_images,self.move_images=[],[],[]
		self.imageLoaders=[['idle','skeleton-idle_',17,self.idle_images],
						   ['move','skeleton-move_',13,self.move_images],
						   ['attack','skeleton-attack_',13,self.attack_images]
						  ]
		for x in self.imageLoaders:
			for i in range(x[2]):
				imagex=pygame.transform.scale(pygame.image.load(f'./sprites/Zombie/{x[0]}/{x[1]+str(i)}.png'),(self.width,self.height))
				x[3].append(imagex)
		self.images=[self.idle_images,self.move_images,self.attack_images]
		self.animTimers=[0,0,0]
		self.animTimersMax=[1,1,2]
		self.anim=0
		self.frame=0
		self.animInQueue=None
		self.velocityMax=10*xscale
		self.enemy=gameManager.player
		self.enemyProxim=200*xscale
		self.hitBoxSpawn=positionBlock(self.position.x,self.position.y,40*xscale,10*yscale,0,0.3*self.width,0.3*self.width)
		self.state="idle"
		self.maxAttackGap=2.5
		self.attackGap=self.maxAttackGap-random.random()
		self.attacks=[]
		self.lastAttackTime=0
		self.maxHealth=100
		self.health=self.maxHealth
		self.healthBar=HealthBar(self.position.x,self.position.y,0,-80*yscale,-40*xscale,200*xscale,10*yscale,self.health,False)
		self.healthBarHidden=False
		self.healthBarClock=0
		self.healthBarMaxTime=2
		self.enemyDirection=CreateVector(0,0)
		self.minEnemyDetectDistance=200*xscale
		self.enemyLocked=False
		self.target=gameManager.player


	def ShowHealthBar(self):
		self.healthBarHidden=False
		self.healthBarClock=time.time()

	def HideHealthBar(self):
		if not self.healthBarHidden:			
			if time.time()-self.healthBarClock > self.healthBarMaxTime:
				self.healthBarHidden=True
	def updateAndDrawHealthBar(self):
		self.HideHealthBar()
		self.healthBar.update(-self.angle,self.position)
		if not self.healthBarHidden:
			self.healthBar.display()

	def update(self):		
		self.updateAndDrawHealthBar()
		self.boxCollider.updateP(self.position)
		self.RunStateMachine()
		self.hitBoxSpawn.update(self.angle,self.position)

	def display(self):		
		rotated_image=pygame.transform.rotate(self.images[self.anim][self.frame],-self.angle)
		myrect=rotated_image.get_rect()		
		# print(f'{self.position.x-gameManager.camera.position.x},{self.position.y-gameManager.camera.position.y}')
		# print(f'{self.position.x},{self.position.y}')
		# return
		myrect.centerx=self.position.x-gameManager.camera.position.x
		myrect.centery=self.position.y-gameManager.camera.position.y
		win.blit(rotated_image,myrect)
		self.updateAnimation()
		# self.hitBoxSpawn.display()
		# self.boxCollider.display()
		

	def RunStateMachine(self):
		if self.state=="idle":
			self.DoIdleStuff()

	def DoIdleStuff(self):		
		if self.enemyLocked:
			self.PursueTarget()
		else:
			self.AttemptEnemyLock()

	def AttemptEnemyLock(self):
		enemyDirection=self.enemy.position.copy().sub(self.position)
		if enemyDirection.mag() < self.minEnemyDetectDistance:
			self.enemyLocked=True
			gameManager.camera.target = self.focusPoint
			for gt in gameManager.gatesList:
				gt.CloseGate()

	def PursueTarget(self):
		enemyDirection=self.enemy.position.copy().sub(self.position)
		enemyAngle=enemyDirection.heading()
		if 360+enemyAngle - self.angle < abs(enemyAngle-self.angle):
			self.angle=Lerp(self.angle,360+enemyAngle,8)
		elif 360+self.angle - enemyAngle < abs(enemyAngle-self.angle):
			self.angle+=360
			self.angle=Lerp(self.angle,enemyAngle,8)
		else:
			self.angle=Lerp(self.angle,enemyAngle,8)
		if self.angle > 360:
			self.angle-=360


		if enemyDirection.mag() > self.enemyProxim:	
			self.AnimMove()
			self.position.add(enemyDirection.normalized().mult(self.velocityMax))
		else:
			self.AnimStop()		


	def updateAnimation(self):
		if not self.clearToAnim():
			return
		self.frame+=1
		if self.frame >= len(self.images[self.anim]):
			if not self.animInQueue:
				self.frame=0
			else:
				self.changeAnimation(self.animInQueue)
				self.animInQueue=None

	def clearToAnim(self):
		self.animTimers[self.anim]+=1
		if self.animTimers[self.anim] >= self.animTimersMax[self.anim]:
			self.animTimers[self.anim]=0
			return True
		return False

	def getRunningAnimation(self):
		if self.anim==0:
			return "idle"
		if self.anim==1:
			return "move"
		if self.anim==2:
			return "attack"
		return "unknown"
	def AnimMove(self):
		if self.getRunningAnimation()=="idle":
			self.changeAnimation("move")

	def changeAnimation(self,anim):
		if anim=="idle" and self.anim!=0:
			self.anim=0
			self.frame=0
		elif anim=="move" and self.anim!=1:
			self.anim=1
			self.frame=0
		elif anim=="attack" and self.anim!=2:
			self.anim=2
			self.frame=0

	def AnimStop(self):
		if self.getRunningAnimation()=="move":
			self.changeAnimation("idle")

	def TakeDamage(self,dmg):
		self.health-=dmg
		self.healthBar.reduceHealth(dmg)
		self.ShowHealthBar()
		if self.health < 0:
			'''
			camera.target=player			
			pygame.mixer.music.load('./sounds/majula.mp3')
			pygame.mixer.music.play(-1,0.0)
			gameManager.SetText("Zombie is dead please stay for next boss")
			player.onScreen=False
			gameManager.LoadNextLevel()
			'''
			gameManager.camera.target=gameManager.player
			self.health=0
			SpawnCloudGroup(self.position)
			self.onScreen=False

##Zombie ends###


###########################Player Starts########################################
class Player:
	def __init__(self,x,y,wid,hei):
		self.onScreen=True
		
		self.width=int(wid*xscale)
		self.height=int(hei*yscale)
		self.position=CreateVector(x*xscale,y*yscale)
		self.boxCollider=collisionBox(x*xscale,y*yscale,self.width*0.5,self.height*0.5)
		self.shootPosition=positionBlock(x*xscale,y*yscale,45*xscale,25*yscale,0,self.width*0.05,self.height*0.05) #45 25
		# self.width=wid
		# self.height=hei
		# self.position=CreateVector(x,y)
		# self.boxCollider=collisionBox(x,y,self.width*0.5,self.height*0.5)
		# self.shootPosition=positionBlock(x,y,45*xscale,25*yscale,0,self.width*0.05,self.height*0.05)

		self.idle_images,self.move_images,self.shoot_images,self.reload_images,self.melee_images=[],[],[],[],[]		
		self.images=[]	
		self.angle=0
		self.animInQueue=None
		self.weaponIndex=0
		self.health=100
		self.maxHealth=100
		self.meleeRegistered=False
		self.healthBar=HealthBar(x,y,0,-80*yscale,-40*xscale,200*xscale,10*yscale,self.maxHealth,False)
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
		self.rotationSpeedAcc=0.25
		self.rotationSpeedMax=20
		self.rotationSpeed=self.rotationSpeedMax

		self.vmax=10*xscale
		self.vmaxOrig=10*xscale
		self.velMin=1
		self.velocity=CreateVector(self.velMin,0)	
		self.vel=self.velMin
		self.bullets=[]
		self.lastShootTime=0
		self.shootGap=0.8	
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
		self.reloadCommandGiven=False
		self.dashOn=False
		self.dashStartTime=0
		self.maxDashTime=1
		self.dashVelocity=20*xscale
		self.dashTriggerOn=True
		self.maxDashGap=0.5
		self.dashTime=0.3

		self.lastRifleShot=0
		self.rifleShotGap=0.25
		self.shootCount=0
		self.maxShootCount=3
		self.autoShootOn=False
		self.rifleShots=2
		self.shotGunShots=3

		self.lastBlockTime=0
		self.minGapBetweenBlocks=0

		self.gunStartTime=0
		self.gunMaxTime=4

		self.lockedOnToTarget=False
		self.player_s_target=None
		self.OTRIGGER=False
		self.enemyDir_player=CreateVector(0,0)
		self.runningInDir="towards"
		self.action_required="stop" #variable used in lockedmovement to decide whether to move or stop

	def WaitForReloadTime(self):
		if time.time()-self.gunStartTime > self.gunMaxTime:
			self.rifleShots=5
			self.shotGunShots=5

	def MindDash(self):
		if not self.dashOn:
			return
		if time.time()-self.dashStartTime > self.dashTime:
			self.dashOn=False
			self.dashStartTime=time.time()


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
		if self.InvincibleMode:
			return False	
		self.health-=dmg
		lossBuzz.play()
		self.healthBar.reduceHealth(dmg)
		self.ShowHealthBar()
		if enemyVel:
			self.startStagger(enemyVel)
		self.InvincibleMode=True
		self.invincibleStartTime=time.time()
		if self.health < 0:
			self.health=0
			self.onScreen=False			
			gameManager.SetText("You Died .....")
			SpawnCloudGroup(self.position)
			gameManager.reloadLevel()
			glassBreak.play()
	def changeWeapon(self):
		self.weaponIndex+=1
		if self.weaponIndex >= len(self.weaponAnims):
			self.weaponIndex=0
		self.images=self.weaponAnims[self.weaponIndex]
	def changeWeapons(self):
		if TPRESSED:
			if self.weaponChangeAuthorized:
				self.weaponChangeAuthorized=False
				self.changeWeapon()
				changeBullet(self.presentWeapon())
		elif not self.weaponChangeAuthorized:
			self.weaponChangeAuthorized=True

	def CheckPostPassed(self):
		if self.presentWeapon()=="rifle" and self.rifleShots<=0:
			self.WaitForReloadTime()
			return False
		if self.presentWeapon()=="shotgun" and self.shotGunShots<=0:
			self.WaitForReloadTime()
			return False
		return True

	def shoot(self):
		if self.runningAnimation() in ["shoot","reload","melee"]:
			return False
		if not self.CheckPostPassed():
			#play a sound here
			return
		if time.time()-self.lastShootTime > self.shootGap:
			self.animInQueue=self.runningAnimation()
			if self.presentWeapon() not in ['flashlight','knife','rifle','shotgun']:
				self.bullets.append(bullet(self.shootPosition.position.x,self.shootPosition.position.y,self.angle,self,'player'))
				# print("changed animation to shoot")
				self.ChangeAnimation("shoot")				
				shootingSound.play()
			elif self.presentWeapon()=='shotgun':
				self.shotGunShots-=1
				if self.shotGunShots <= 0:
					self.gunStartTime=time.time()
					# gameManager.PlayerRequest('shotgun')
				self.bullets.append(bullet(self.shootPosition.position.x,self.shootPosition.position.y,self.angle,self,'player'))
				self.ChangeAnimation("shoot")
				parry.play()
			elif self.presentWeapon()=='rifle':
				self.rifleShots-=1
				if self.rifleShots <= 0:
					self.gunStartTime=time.time()
					# gameManager.PlayerRequest("rifle")
				self.autoShootOn=True				
				self.ChangeAnimation("shoot")
			else:				
				self.ChangeAnimation("melee")
			self.lastShootTime=time.time()



	def autoShoot(self):
		if not self.autoShootOn:
			return
		if time.time()-self.lastRifleShot > self.rifleShotGap:
			self.lastRifleShot=time.time()
			self.bullets.append(bullet(self.shootPosition.position.x,self.shootPosition.position.y,self.angle,self,'player'))
			self.shootCount+=1
			shootingSound.play()
			if self.shootCount > self.maxShootCount:
				self.shootCount=0
				self.autoShootOn=False 

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
			for elem in gameManager.roadBlocksList:
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

	def HitOnMelee(self):
		if self.presentWeapon()!="knife" and not self.meleeRegistered:
			return
		if self.presentWeapon()=="knife" and self.runningAnimation()=="melee" and self.frame==9 and not self.meleeRegistered:
			# SpawnCloudGroup(self.shootPosition.position)
			for x in gameManager.rocks:
				if not x.onScreen:
					continue
				if boxCollision(self.shootPosition,x):
					SpawnCloudGroup(self.shootPosition.position)
					rockSmash.play()
					x.onScreen=False
			self.meleeRegistered=True
		elif self.runningAnimation()!="melee" and self.meleeRegistered:
			self.meleeRegistered=False

	def BlockWithGun(self):
		if self.InvincibleMode:
			return False
		if time.time()-self.lastBlockTime < self.minGapBetweenBlocks:
			return False
		if self.presentWeapon() in ['knife','flashlight'] or self.runningAnimation() in ['shoot','reload','melee']:
			return False
		self.animInQueue=self.runningAnimation()
		self.ChangeAnimation("melee")
		self.lastBlockTime=time.time()

	def IsBlocking(self):
		if self.runningAnimation()=='melee' and self.frame >3 and self.frame < 13:
			return True
		return False 

	def adjustToDestinationAngle(self,ang):	
		if self.angle==ang:
			self.ApplyVelocity()
			return
		if self.vel > self.velMin:
			self.vel=self.velMin
		if abs(self.angle - ang) < self.rotationSpeed:
			self.angle=ang
		else:
			if(360+ang-self.angle < abs(ang-self.angle)):
				self.angle+=self.rotationSpeed 
			elif(360+self.angle-ang < abs(ang-self.angle)):
				self.angle-=self.rotationSpeed
			elif ang > self.angle:
				self.angle+=self.rotationSpeed
			elif ang < self.angle:
				self.angle-=self.rotationSpeed
			if self.angle >= 360:
				self.angle-=360
			elif self.angle < 0:
				self.angle+=360	
		self.updateVelocity()

	def displayPositionDetails(self):
		w2screen(win,"xpos:"+str(round(self.position.x/xscale)),300,200)
		w2screen(win,"ypos:"+str(round(self.position.y/yscale)),300,250)
		

	def update(self):
		# self.displayPositionDetails()
		self.HitOnMelee()
		self.MindDash()
		self.autoShoot()
		self.HideHealthBar()
		self.ManageInvincibility()
		self.updateRunBullets(win)
		self.updateAndDrawShootPos(win)
		self.updateAndDrawHealthBar(win)
		self.changeWeapons()

		if self.staggering:
			self.staggerBack()
		else:
			if SPACEPRESSED:
				self.shoot()
			if BPRESSED:
				self.BlockWithGun()
		if self.lockedOnToTarget:
			self.LockedMovement()
		else:
			self.UnlockedMovement()

		self.boxCollider.updateP(self.position)

	def LockedMovement(self):
		if OPRESSED and not self.OTRIGGER:
			self.OTRIGGER=True
			self.lockedOnToTarget=False
			self.player_s_target=gameManager.zombiesList[0]
		elif not OPRESSED:
			if self.OTRIGGER:
				self.OTRIGGER=False

		self.angle= AngleLerp(self.angle,self.enemyDir_player.heading(),5)

		if CPRESSED:
			if self.dashTriggerOn:
				self.dashTriggerOn=False
				if not self.dashOn and time.time()-self.dashStartTime > self.maxDashGap:
					SpawnCloudGroup(self.position)
					whoosh.play()
					self.dashOn=True
					self.dashStartTime=time.time()
		elif not self.dashTriggerOn:
			self.dashTriggerOn=True
		
		self.FixVelocityOnLock()	
		if self.dashOn:
			self.action_required = "move"
			self.runningInDir="right"	
		if UPPRESSED:			
			if self.runningInDir!="towards":
				self.runningInDir="towards"	
			self.action_required = "move"
		elif DOWNPRESSED:
			if self.runningInDir != "away":
				self.runningInDir = "away"
				self.action_required = "move"
		elif RIGHTPRESSED:
			if self.runningInDir != "right":
				self.runningInDir = "right"
				self.action_required = "move"
		elif LEFTPRESSED:
			if self.runningInDir != "left":
				self.runningInDir = "left"
				self.action_required = "move"	
		elif not self.dashOn:
			self.action_required="stop"

		if self.action_required == "move":			
			if self.runningAnimation()=="idle":
				self.ChangeAnimation("move")		
			self.ApplyVelocity()
		elif self.action_required == "stop":
			if self.runningAnimation()=="move":
				self.ChangeAnimation("idle")			
			self.DeApplyVelocity()

	def UnlockedMovement(self):
		if OPRESSED and not self.OTRIGGER:
			self.OTRIGGER=True
			self.lockedOnToTarget=True
			self.player_s_target=gameManager.zombiesList[0]
		elif not OPRESSED:
			if self.OTRIGGER:
				self.OTRIGGER=False
		if CPRESSED:
			if self.dashTriggerOn:
				self.dashTriggerOn=False
				if not self.dashOn and time.time()-self.dashStartTime > self.maxDashGap:
					SpawnCloudGroup(self.position)
					whoosh.play()
					self.dashOn=True
					self.dashStartTime=time.time()
		elif not self.dashTriggerOn:
			self.dashTriggerOn=True
		if self.dashOn:
			self.ApplyVelocity()
			return	
		if LEFTPRESSED:
			self.angle-=self.rotationSpeed
			self.IncreaseRotationSpeed()
			if self.angle < 360:
				self.angle+=360
			self.updateVelocity()

		elif RIGHTPRESSED:
			self.angle+=self.rotationSpeed
			self.IncreaseRotationSpeed()
			if self.angle > 360:
				self.angle-=360
			self.updateVelocity()
		else:
			self.rotationSpeed=self.rotationSpeedMin

		if UPPRESSED:	
			if self.runningAnimation()=="idle":
				self.ChangeAnimation("move")		
			self.ApplyVelocity()
		else:
			if self.runningAnimation()=="move":
				self.ChangeAnimation("idle")
			self.DeApplyVelocity()

	def updateAndDrawHealthBar(self,win):
		self.healthBar.update(-self.angle,self.position)
		if not self.healthBarHidden:
			self.healthBar.display()
		
	def updateAndDrawShootPos(self,win):
		self.shootPosition.update(self.angle,self.position)
		# self.shootPosition.display()	

	def FixVelocityOnLock(self):
		if self.runningInDir == "towards":			
			enemyDirection=self.player_s_target.position.copy().sub(self.position)
		elif self.runningInDir == "away":			
			enemyDirection=self.position.copy().sub(self.player_s_target.position)
		elif self.runningInDir == "right":			
			enemyDirection = self.player_s_target.position.copy().sub(self.position).rotateByAngle(90)
		elif self.runningInDir == "left":			
			enemyDirection = self.position.copy().sub(self.player_s_target.position).rotateByAngle(90)
		if enemyDirection.equals(self.enemyDir_player):
			return
		self.enemyDir_player.setVec(enemyDirection)
		
	
		
	def updateVelocity(self):
		# rangle=360-self.angle
		self.velocity.x=self.vel * math.cos(d2r(self.angle))
		self.velocity.y=self.vel * math.sin(d2r(self.angle))	


	def ApplyVelocity(self):		
		if self.dashOn:
			self.vel=self.vmax=self.dashVelocity
		elif self.vmax!=self.vmaxOrig:
			self.vmax=self.vmaxOrig
			self.vel=0
		if self.vel <= self.vmax:
			self.vel+=1
			if not self.lockedOnToTarget:
				self.updateVelocity()
			else:				
				self.velocity.setVec(self.enemyDir_player.normalized().copy().mult(self.vel))
		self.position.add(self.velocity)		
		self.checkCollisionWithRoadBlocks()
		

	def DeApplyVelocity(self):
		if self.vmax != self.vmaxOrig:
			self.vmax = self.vmaxOrig
			self.vel = self.vmaxOrig
		if self.vel <=self.velMin:
			# self.velocity.set(0,0)
			if self.runningInDir != "towards":
				self.runningInDir = "towards"
			return True
		self.vel-=1
		if not self.lockedOnToTarget:
			self.updateVelocity()
		else:			
			self.velocity.setVec(self.enemyDir_player.normalized().copy().mult(self.vel))
		self.position.add(self.velocity)
		self.checkCollisionWithRoadBlocks()

	def checkCollisionWithRoadBlocks(self):
		for x in gameManager.roadBlocksList:
			if not x.onScreen:
				continue
			if boxCollision(self.boxCollider,x.topCollider):
				self.position.y-=abs(self.velocity.y)
			if boxCollision(self.boxCollider,x.bottomCollider):
				self.position.y+=abs(self.velocity.y)
			if boxCollision(self.boxCollider,x.leftCollider):
				self.position.x-=abs(self.velocity.x)
			if boxCollision(self.boxCollider,x.rightCollider):
				self.position.x+=abs(self.velocity.x)

	def display2(self):
		if not self.FlickerManagerCleared():
			return
		draw_translate_rotate(self.images[self.anim][self.frame],
							  self.angle,self.position.x-self.width/2-gameManager.camera.position.x,
							  self.position.y-self.height/2-gameManager.camera.position.y,win)
		self.updateAnimation()
		#self.boxCollider.display(win)
	def display(self):
		self.rotatedImage=pygame.transform.rotate(self.images[self.anim][self.frame],-self.angle)
		myrect=self.rotatedImage.get_rect()
		myrect.centerx,myrect.centery=self.position.x-gameManager.camera.position.x,self.position.y-gameManager.camera.position.y		
		win.blit(self.rotatedImage,myrect)
		self.updateAnimation()		
		# self.updateAndDrawShootPos(win)
###########################Player ends#####################################

###########################bullet starts #########################################
class bullet:
	def __init__(self,x,y,angle,parent,bulletType,lifeTime=0):
		self.onScreen=True
		self.bulletType=bulletType
		self.parent=parent
		self.position=CreateVector(x,y)
		# self.width=int(self.parent.width*BULLETSIZEFAC)
		# self.height=int(self.parent.width*BULLETSIZEFAC)
		self.width=int(30*xscale)
		self.height=int(30*xscale)
		if bulletType=="player":
			self.image=pygame.transform.scale(BULLETIMAGE_PLAYER,(self.width,self.height))
		else:
			self.image=pygame.transform.scale(BULLETIMAGE,(self.width,self.height))
		self.angle=angle
		self.speed=20*xscale
		self.velocity=CreateVector(self.speed * math.cos(d2r(self.angle)),self.speed * math.sin(d2r(self.angle)))

		self.lifeTime=lifeTime
		self.timeOfBirth=time.time()


	def checkLife(self):
		if self.lifeTime!=0:
			if time.time()-self.timeOfBirth > self.lifeTime:
				self.onScreen=False
	def display(self,win):
		draw_translate_rotate(self.image,
							  360-self.angle,self.position.x-self.width/2-gameManager.camera.position.x,
							  self.position.y-self.height/2-gameManager.camera.position.y,win)

	def update(self):
		self.checkLife()
		self.position.add(self.velocity)
		self.checkCollisions()
		self.OutOfBoundsCheck()

	def checkCollisions(self):
		for x in gameManager.roadBlocksList:
			if not x.onScreen:
				continue
			if boxCollision(self,x):
				self.onScreen=False
				SpawnCloudGroup(self.position)
				shootingSound.play()
		if self.bulletType=="player":
			for x in gameManager.enemiesList:
				if not x.onScreen:
					continue
				if boxCollision(self,x.boxCollider):
					self.onScreen=False
					SpawnCloudGroup(self.position)
					shootingSound.play()
					if gameManager.player.presentWeapon()=="shotgun":						
						x.TakeDamage(20)
					else:
						x.TakeDamage(5)
		elif self.bulletType=="enemy":			
			if not gameManager.player.onScreen or gameManager.player.InvincibleMode:
				return
			if boxCollision(self,player.boxCollider):
				if not player.IsBlocking():
					self.onScreen=False
					SpawnCloudGroup(self.position)
					shootingSound.play()
					player.TakeDamage(5)
				else:
					self.velocity.rotateByAngle(45)


	def OutOfBoundsCheck(self):
		if self.position.x - gameManager.camera.position.x > WIN_WIDTH or self.position.x - gameManager.camera.position.x < 0:
			self.onScreen=False
		if self.position.y - gameManager.camera.position.y > WIN_HEIGHT or self.position.y - gameManager.camera.position.y < 0:
			self.onScreen = False 
###########################bullet ends############################################

##dummy object starts##  
#type0=> right
#type1=> left
#type2=> top
#type3=> bottom
class DummyObject:
	def __init__(self,x,y,wid,hei,typex):
		self.onScreen=True
		self.position=CreateVector(x,y)
		self.width=int(wid*xscale)
		self.height=int(hei*yscale)
		self.type=typex
		self.imagexOrig=SHRUB
		self.imagex=pygame.transform.scale(self.imagexOrig,(self.width,self.height))

	def update(self):
		pass
	def CheckFollow(self,position):
		if self.type==0 and position.x > self.position.x:
			return (False,True)
		elif self.type==1 and position.x < self.position.x:
			return (False,True) 
		elif self.type==2 and position.y < self.position.y:
			return (True,False) 
		elif self.type==3 and position.y > self.position.y:
			return (True,False) 
		return (True,True) 
	def display(self):
		myrect=self.imagex.get_rect()
		myrect.centerx,myrect.centery=self.position.x-gameManager.camera.position.x,self.position.y-gameManager.camera.position.y
		win.blit(self.imagex,myrect)
##dummy object ends##

##NextSceneObject object starts##  

class NextSceneObject:
	def __init__(self,x,y,wid,hei,typex):
		self.onScreen=True
		self.position=CreateVector(x,y)
		self.width=int(wid*xscale)
		self.height=int(hei*yscale)
		self.type="next" if typex==0 else "previous"
		self.imagexOrig=SHRUB
		self.imagex=pygame.transform.scale(self.imagexOrig,(self.width,self.height))

	def update(self):
		if boxCollision(self,gameManager.player):			
			if self.type=="next":
				gameManager.LoadNextLevel()
			elif self.type=="previous":
				gameManager.LoadPreviousLevel()

	def display(self):		
		myrect=self.imagex.get_rect()
		myrect.centerx,myrect.centery=self.position.x-gameManager.camera.position.x,self.position.y-gameManager.camera.position.y
		win.blit(self.imagex,myrect)
##NextSceneObject object ends##

## staticdot starts ##
class StaticDot:
	def __init__(self,x,y,wid,hei):
		self.onScreen=False
		self.position=CreateVector(x,y)
		self.width=int(wid*xscale)
		self.height=int(hei*yscale)
		self.imagexOrig=REDSPHEREIMAGE
		self.imagex=pygame.transform.scale(self.imagexOrig,(self.width,self.height))
	def shift(self,obj):
		self.position.x=obj.position.x
		self.position.y=obj.position.y
	def update(self):
		pass
	def display(self):
		myrect=self.imagex.get_rect()
		myrect.centerx,myrect.centery=self.position.x-gameManager.camera.position.x,self.position.y-gameManager.camera.position.y
		win.blit(self.imagex,myrect)
## staticdot ends ##

######################## Grabable items###########################################
class Grabable:
	def __init__(self,x,y,wid,hei,item):
		self.onScreen=True
		self.position=CreateVector(x,y)
		self.width=int(wid*xscale)
		self.height=int(hei*yscale)
		self.item=item
		if self.item=="rifle":
			self.imagexOrig=COIN
		elif self.item=="shotgun":
			self.imagexOrig=PRIZEBLOCK
		self.imagex=pygame.transform.scale(self.imagexOrig,(self.width,self.height))

	def display(self):
		myrect=self.imagex.get_rect()
		myrect.centerx,myrect.centery=self.position.x-gameManager.camera.position.x,self.position.y-gameManager.camera.position.y
		win.blit(self.imagex,myrect)

	def update(self):
		self.GetGrabbed()

	def GetGrabbed(self):
		if not player.onScreen:
			return
		if boxCollision(player.boxCollider,self):
			self.onScreen=False
			if self.item=="rifle":
				player.rifleShots+=5
			elif self.item=="shotgun":
				player.shotGunShots+=5

######################## Grabable ends############################################

####### DisplayInformationScreen starts ##############################
def DisplayInformationScreen(instructions):
	BASICFONT = pygame.font.Font('freesansbold.ttf', 32)
	imagex=pygame.transform.scale(SOLDIER_IMAGE,(400,400))
	startImageRect=imagex.get_rect()
	startImageRect.top=int(50*yscale)
	startImageRect.centerx=int(WIN_WIDTH/2)
	win.fill((183,204,223))
	win.blit(imagex,startImageRect)
	displayTop=startImageRect.top
	displayTop+=startImageRect.height
	for i in range(len(instructions)):
		instSurf=BASICFONT.render(instructions[i].upper(),1,(0,0,0))
		instRect=instSurf.get_rect()
		displayTop+=int(10*yscale)
		instRect.top=displayTop
		instRect.centerx=int(WIN_WIDTH/2)
		displayTop+=instRect.height
		win.blit(instSurf,instRect)

####### DisplayInformationScreen ends ################################ 




################## Game Manager starts ###################################
class GameManager:
	def __init__(self):
		self.scenesLoaded=[True,False,False,False,False,False,False,False,False]
		self.scenesReady=[True,True,False,False,False,False,False,False,False]
		self.loadingObjects=False
		self.loadingType=None
		self.currentScene=-1
		self.reloading=False
		self.gameStopTime=0
		self.maxReloadGap=3
		self.readyForNextLevel=False
		self.readyForPrevLevel=False		
		self.basicFont=pygame.font.Font('freesansbold.ttf',32)
		self.textToBeDisplayed=''
		self.roadBlocksList,self.cloudsList,self.wallsList,self.enemiesList,self.grabables,self.rocks,self.camStoppers,self.nsobjs,self.gatesList=[],[],[],[],[],[],[],[],[]
		self.volatiles,self.nonvolatiles=[],[]
		self.zombiesList=[]
		self.allGameObjects=[]
		self.player=None
		self.pChanger=None
		self.camera=Camera()

		self.placementMode=True
		self.objOnFocus=-1
		self.gTrigger=False
		self.indicatorDot=StaticDot(1,1,50,50)

		self.infoScreenLive=False
		self.startGameInstructions=['Press Left and Right Arrows to Turn','Up arrow to move','space to shoot']

	def SetText(self,tex):
		self.textToBeDisplayed=tex 
	def ClearText(self):
		self.textToBeDisplayed=''

	def HandleInfoScreen(self,instructions):
		DisplayInformationScreen(instructions)
		if ANYKEYPRESSED:			
			self.infoScreenLive=False

	def WithInAllStoppers(self):
		for elem in self.camStoppers:
			c1,c2=elem.CheckFollow(self.camera.target.position)
			if not(c1 and c2):
				return (c1,c2)
		return (True,True)

	def HandlePlacement(self):
		if not self.placementMode:
			return
		if self.indicatorDot.onScreen:			
			self.indicatorDot.display()
		if GPRESSED and not self.gTrigger:
			if not self.indicatorDot.onScreen:
				self.indicatorDot.onScreen=True
			self.gTrigger=True
			self.objOnFocus+=1
			self.objOnFocus=self.objOnFocus if self.objOnFocus < len(self.allGameObjects) else 0

			self.indicatorDot.shift(self.allGameObjects[self.objOnFocus])
			if not self.pChanger:
				self.pChanger=posChanger(self.allGameObjects[self.objOnFocus])
			else:
				self.pChanger.assignObject(self.allGameObjects[self.objOnFocus])
		elif not GPRESSED and self.gTrigger:
			self.gTrigger=False
			
		

	def PlayerRequest(self,weapon):		
		self.grabables.append(Grabable(self.player.position.x+(240*random.random()-120)*xscale,self.player.position.y+(240*random.random()-120)*yscale,100,100,weapon))	

	def DisplayStuffOnScreen(self):
		if self.textToBeDisplayed=="":
			return
		fontSurface=self.basicFont.render(self.textToBeDisplayed,1,(255,255,255))
		fontRect=fontSurface.get_rect()
		fontRect.centerx,fontRect.centery=WIN_WIDTH/2,WIN_HEIGHT/2
		win.blit(fontSurface,fontRect)

	def checkScenes(self):
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
			self.unloadComponents()
			# self.ClearText()
	def LoadPreviousLevel(self):
		if not self.readyForPrevLevel:
			self.readyForPrevLevel=True
			self.gameStopTime=time.time()
			self.unloadComponents()

	def loadScene(self,i):
		print('loading scene:'+str(i))
		#DisplayInformationScreen(['LOADING.......']) #This wont work why?
		filex=open('./SceneData3.txt','r')
		for line in filex.readlines():			
			if line[0]=='#':
				continue
			if 'scene'+str(i) in line:
				self.loadingObjects=True
			elif self.loadingObjects and 'sceneend' in line:
				self.scenesLoaded[i]=True
				self.loadingObjects=False
				self.currentScene=i		
				print('loading complete')		
				return
			elif self.loadingObjects:
				self.LoadObjects(line)
		filex.close()

	def LoadObjects(self,line):
		# global pChanger,player
		if not re.search(r'[0-9]',line):
			self.loadingType=re.findall(r'[a-z]+',line)[0]			
		else:
			nums=re.findall(r'[0-9\-]+',line)
			if self.loadingType=='wall':
				self.wallsList.append(BrickWall(int(nums[0])*xscale,
					                            int(nums[1])*yscale,
							                    int(nums[2]),
							                    int(nums[3]),
							                    True if int(nums[4])==1 else False					                    
					                ))
				self.allGameObjects.append(self.wallsList[-1])
				self.roadBlocksList.append(self.wallsList[-1])	
				self.nonvolatiles.append(self.wallsList[-1])	
			elif self.loadingType=='gate':
				self.gatesList.append(Gate(int(nums[0])*xscale,
					                            int(nums[1])*yscale,
							                    int(nums[2]),
							                    int(nums[3]),
							                    True if int(nums[4])==1 else False					                    
					                ))
				self.allGameObjects.append(self.gatesList[-1])
				self.roadBlocksList.append(self.gatesList[-1])	
				self.nonvolatiles.append(self.gatesList[-1])		

			elif self.loadingType=='player':
				self.player=Player(int(nums[0]),int(nums[1]),int(nums[2]),int(nums[3]))
				self.camera.target=self.player
				# pChanger=posChanger(player,False)
			elif self.loadingType=='zombie':
				self.zombiesList.append(Zombie(int(nums[0])*xscale,int(nums[1])*yscale,int(nums[2]),int(nums[3])))
				self.volatiles.append(self.zombiesList[-1])
				self.enemiesList.append(self.zombiesList[-1])
			elif self.loadingType=='dummyobject':				
				self.camStoppers.append(DummyObject(int(nums[0])*xscale,
												int(nums[1])*yscale,
												int(nums[2]),
												int(nums[3]),
												int(nums[4])
												)
									)
				self.allGameObjects.append(self.camStoppers[-1])
				self.nonvolatiles.append(self.camStoppers[-1])

			elif self.loadingType=='nextsceneobject':				
				self.nsobjs.append(NextSceneObject(int(nums[0])*xscale,
												int(nums[1])*yscale,
												int(nums[2]),
												int(nums[3]),
												int(nums[4])
												)
									)
				self.allGameObjects.append(self.nsobjs[-1])
				self.nonvolatiles.append(self.nsobjs[-1])

	def update(self):
		self.DisplayStuffOnScreen()
		if self.infoScreenLive:
			self.HandleInfoScreen(self.startGameInstructions)
			return
		self.checkScenes()
		self.runGame()		
		self.HandlePlacement()

		followParam1,followParam2=self.WithInAllStoppers()
		self.camera.followTarget(followParam1,followParam2)
		# self.camera.runwithmouse()
		if self.reloading:
			if time.time()-self.gameStopTime > self.maxReloadGap:
				self.reloading=False
				self.ClearText()
				self.unloadComponents()
				self.scenesLoaded[self.currentScene]=False
		elif self.readyForNextLevel:
			if time.time()-self.gameStopTime > self.maxReloadGap:
				self.readyForNextLevel=False
				# self.unloadComponents()
				self.scenesReady[self.currentScene+1]=True
				self.ClearText()
		elif self.readyForPrevLevel:
			if time.time()-self.gameStopTime > self.maxReloadGap:
				self.readyForPrevLevel=False
				# self.unloadComponents()
				self.scenesReady[self.currentScene]=False
				self.scenesLoaded[self.currentScene]=False
				self.scenesLoaded[self.currentScene-1]=False
				self.ClearText()


	def unloadComponents(self):	
		self.player=None	
		self.roadBlocksList,self.cloudsList,self.wallsList,self.enemiesList,self.grabables,self.rocks,self.camStoppers,self.nsobjs=[],[],[],[],[],[],[],[]
		self.allGameObjects,self.volatiles,self.nonvolatiles=[],[],[]

	def runGame(self):	
		# w2screen(win,f'{int(MOUSEX+gameManager.camera.position.x)},{int(MOUSEY+gameManager.camera.position.y)}',500*xscale,300*yscale)	
		if self.pChanger:		
			self.pChanger.update(win)
		if self.player and self.player.onScreen:		
			self.player.update()
			self.player.display()

		for x in self.volatiles:
			if x.onScreen:
				x.update()
				x.display()			
		flushList(self.volatiles)
		for x in self.nonvolatiles:
			if x.onScreen:
				x.update()
				x.display()			

		#Deletable
		# for x in self.cloudsList:
		# 	if x.onScreen:
		# 		x.update()
		# 		x.display()			
		# flushList(self.cloudsList)
		# for x in self.wallsList:
		# 	if x.onScreen:
		# 		x.display()
		# for x in self.camStoppers:
		# 	if x.onScreen:
		# 		x.display()
		# for x in self.nsobjs:
		# 	if x.onScreen:
		# 		x.update()
		# 		x.display()
		# for x in self.gatesList:
		# 	if x.onScreen:
		# 		x.update()
		# 		x.display()
		# for x in self.zombiesList:
		# 	if x.onScreen:
		# 		x.update()
		# 		x.display()
		# flushList(self.zombiesList)
		




################## Game Manager ends ###################################

##########Initialization of pygame starts
pygame.init()
##########Initialization of pygame ends


######### Global Variables ##################
CLOUDIMAGE=pygame.image.load('./sprites/cloud-1.png')
REDCUBEIMAGE =pygame.image.load('./sprites/redcube.png')
REDSPHEREIMAGE=pygame.image.load('./sprites/redSphere.png')
FIREBALLIMAGE=pygame.image.load('./sprites/fireball.png')
HORIZONTAL_PIPE=pygame.image.load('./sprites/Pipes/pipeHori.png')
VERTICAL_PIPE=pygame.image.load('./sprites/Pipes/pipe.png')
SOLDIER_IMAGE=pygame.image.load('./sprites/soldier/idle/survivor-idle_handgun_0.png')
HAZE=pygame.image.load('./sprites/haze.png')
GATE=pygame.image.load('./sprites/gate.png')
SHRUB=pygame.image.load('./sprites/TreeShrub.png')
LADDER=pygame.image.load('./sprites/gate.png')
global BULLETIMAGE,BULLETSIZEFAC
BULLETIMAGE=REDSPHEREIMAGE
BULLETIMAGE_PLAYER=BULLETIMAGE
BULLETSIZEFAC=0.05
BEETLE_IDLE=pygame.image.load('./sprites/beetles/idle1.png')
BEETLE_MOVE1=pygame.image.load('./sprites/beetles/move1.png')
BEETLE_MOVE2=pygame.image.load('./sprites/beetles/move2.png')
CAVEENTRANCEIMAGE=pygame.image.load('./sprites/caveEntrance.png')
CIRCLEIMAGE=pygame.image.load('./sprites/circle.png')
BRICKWALL=pygame.image.load('./sprites/Wall.png')
RIFLE=pygame.image.load('./sprites/rifle.png')
SHOTGUN=pygame.image.load('./sprites/shotgun.png')
COIN=pygame.image.load('./sprites/Coin.png')
PRIZEBLOCK=pygame.image.load('./sprites/PrizeBlock.png')
fogGateSound=pygame.mixer.Sound('./sounds/fogGate.wav')
rockSmash=pygame.mixer.Sound('./sounds/RockSmash.wav')
goalBloop=pygame.mixer.Sound('./sounds/GoalBloop.wav')
lossBuzz=pygame.mixer.Sound('./sounds/LossBuzz.wav')
whoosh=pygame.mixer.Sound('./sounds/whoosh.wav')
parry=pygame.mixer.Sound('./sounds/parry.wav')
GetCoin=pygame.mixer.Sound('./sounds/GetCoin.wav')
shootingSound=pygame.mixer.Sound('./sounds/shoot.wav')
glassBreak=pygame.mixer.Sound('./sounds/glassBreak.wav')
fogGateSound.set_volume(0.2)
#############################################

#################Change Bullet function starts ########################
def changeBullet(gun):	
	global BULLETIMAGE_PLAYER,BULLETSIZEFAC
	if gun=='handgun':					
		BULLETSIZEFAC=0.05
		BULLETIMAGE_PLAYER=REDSPHEREIMAGE
	elif gun=='rifle':						
		BULLETSIZEFAC=0.2
		BULLETIMAGE_PLAYER=FIREBALLIMAGE
	elif gun=='shotgun':					
		BULLETSIZEFAC=0.3
		BULLETIMAGE_PLAYER=FIREBALLIMAGE

#################Change Bullet function ends ##########################



############# Main Section Starts ##########################

pygame.display.set_caption('Boss Fight1')
MOUSEX,MOUSEY=0,0
ANYKEYPRESSED=False
LEFTPRESSED,RIGHTPRESSED,UPPRESSED,DOWNPRESSED=False,False,False,False
IPRESSED,LPRESSED,MPRESSED,JPRESSED,ZPRESSED,CPRESSED,OPRESSED=False,False,False,False,False,False,False
GPRESSED,KPRESSED,YPRESSED,UPPRESSED,EPRESSED,RPRESSED=False,False,False,False,False,False
TPRESSED,HPRESSED,BPRESSED,FPRESSED=False,False,False,False
SPACEPRESSED,MOUSECLICKED,CTRLPRESSED=False,False,False
FRAME_RATE=30
WIN_WIDTH,WIN_HEIGHT=1200,700
# WIN_WIDTH,WIN_HEIGHT=1400,900
xscale,yscale=WIN_WIDTH/1200,WIN_HEIGHT/700

gameManager=GameManager()
# global player,pChanger
# pChanger,player=None,None
roadBlocksList,wallsList=[],[]

win=pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
clock=pygame.time.Clock()
run=True
while run:
	clock.tick(FRAME_RATE)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run=False
			pygame.quit()
			quit()
		if event.type == KEYUP:
			ANYKEYPRESSED=False
			if event.key in (K_UP,K_w):
				UPPRESSED=False
			elif event.key in (K_DOWN,K_s):
				DOWNPRESSED=False
			elif event.key in (K_LEFT,K_a):
				LEFTPRESSED=False
			elif event.key in (K_RIGHT,K_d):
				RIGHTPRESSED=False
			if event.key == K_SPACE:
				SPACEPRESSED=False	
			if event.key == K_RCTRL:
				CTRLPRESSED=False

			if event.key == K_i:
				IPRESSED=False
			if event.key == K_l:
				LPRESSED=False
			if event.key == K_m:
				MPRESSED=False
			if event.key == K_o:
				OPRESSED=False
			if event.key == K_j:
				JPRESSED=False
			if event.key == K_t:
				TPRESSED=False
			if event.key == K_h:
				HPRESSED=False
			if event.key == K_b:
				BPRESSED=False
			if event.key == K_f:
				FPRESSED=False
			if event.key == K_z:
				ZPRESSED =False
			if event.key == K_c:
				CPRESSED =False

			if event.key == K_g:
				GPRESSED= False
			if event.key == K_k:
				KPRESSED= False
			if event.key == K_y:
				YPRESSED= False
			if event.key == K_u:
				UPRESSED= False
			if event.key == K_e:
				EPRESSED= False
			if event.key == K_r:
				RPRESSED= False

			if event.key == K_ESCAPE:
				run=False
				pygame.quit()
				sys.exit()

		if event.type == KEYDOWN:
			ANYKEYPRESSED=True
			if event.key in (K_UP,K_w):
				UPPRESSED=True
			elif event.key in (K_DOWN,K_s):
				DOWNPRESSED=True
			elif event.key in (K_LEFT,K_a):
				LEFTPRESSED=True
			elif event.key in (K_RIGHT,K_d):
				RIGHTPRESSED=True
			if event.key == K_SPACE:
				SPACEPRESSED=True
			if event.key == K_RCTRL:
				CTRLPRESSED=True

			if event.key == K_i:
				IPRESSED=True
			if event.key == K_l:
				LPRESSED=True
			if event.key == K_m:
				MPRESSED=True
			if event.key == K_o:
				OPRESSED=True
			if event.key == K_j:
				JPRESSED=True
			if event.key == K_t:
				TPRESSED=True
			if event.key == K_h:
				HPRESSED=True
			if event.key == K_b:
				BPRESSED=True
			if event.key == K_f:
				FPRESSED=True
			if event.key== K_z:
				ZPRESSED=True
			if event.key == K_c:
				CPRESSED=True

			if event.key == K_g:
				GPRESSED= True
			if event.key == K_k:
				KPRESSED= True
			if event.key == K_y:
				YPRESSED= True
			if event.key == K_u:
				UPRESSED= True
			if event.key == K_e:
				EPRESSED= True
			if event.key == K_r:
				RPRESSED= True

			if event.key == K_ESCAPE:
				pygame.quit()
				sys.exit()

		if event.type == MOUSEBUTTONDOWN:
			MOUSECLICKED=True
		elif event.type == MOUSEBUTTONUP:
			MOUSECLICKED=False

		if event.type == MOUSEMOTION:
			MOUSEX,MOUSEY=event.pos
	if not gameManager.infoScreenLive:
		win.fill((42,19,5))
	gameManager.update()
	# w2screen(win,f'{int(MOUSEX+gameManager.camera.position.x)},{int(MOUSEY+gameManager.camera.position.y)}',500*xscale,300*yscale)
	pygame.display.update()
	
############# Main Section Ends ##########################