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
	return startValue+(endValue-startValue)/lerpFac;

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
	rect1=pygame.Rect(obj1.position.x-obj1.width/2-camera.position.x,
					  obj1.position.y-obj1.height/2-camera.position.y,
					  obj1.width,obj1.height)
	rect2=pygame.Rect(obj2.position.x-obj2.width/2-camera.position.x,
					  obj2.position.y-obj2.height/2-camera.position.y,
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
	def dot(self,vec):
		return self.x*vec.x+self.y*vec.y

def Raycast(originx,direction,lenx,objToCheck):
	origin=originx.copy()
	destin=originx.copy().add(direction.copy().mult(lenx))
	# pygame.draw.line(win,(255,0,0),(origin.x-camera.position.x,origin.y-camera.position.y),(destin.x-camera.position.x,destin.y-camera.position.y))
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

################## Helper functions end   #################

####IMAGES STARTS #########################################
HORIZONTALPIPE=pygame.image.load('./sprites/Pipes/pipeHori.png')
VERTICALPIPE=pygame.image.load('./sprites/Pipes/pipe.png')
VENGEFUL_SPIRIT=pygame.image.load('./sprites/misc/Vengeful_Spirit.png')
GATE_IMAGE=pygame.image.load('./sprites/misc/gate.png')
SPHERE_IMAGE=pygame.image.load('./sprites/misc/sphere.png')
TREE_IMAGE=pygame.image.load('./sprites/misc/Tree.png')
CLOUDIMAGE=pygame.image.load('./sprites/misc/cloud.png')
DOT=pygame.image.load('./sprites/misc/RedDot.png')

####IMAGES ENDS ###########################################

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

	def SmoothFocus(self):
		#todo  camera first smoothly sails over to target and then does the following
		if not self.target:
			return
		camera.position.x=Lerp(camera.position.x,self.target.position.x-600*xscale,self.lerpFactor)
		camera.position.y=Lerp(camera.position.y,self.target.position.y-550*yscale,self.lerpFactor)


	def followTarget(self):
		'''
		if not self.target or self.onTemporaryFix:
			return
		if self.onTemporaryFix:
			self.FixToTempPoint()
			return
		'''
		if not self.target:
			return
		self.SmoothFocus()
		return
		roamingDistX=self.target.position.x-(WIN_WIDTH/2+self.position.x)
		if abs(roamingDistX) > self.maxAllowedXRoaming:			
			if roamingDistX > 0:
				self.position.x+=roamingDistX-self.maxAllowedXRoaming
			else:
				self.position.x+=roamingDistX+self.maxAllowedXRoaming

		roamingDistY=self.target.position.y-(WIN_HEIGHT/2+self.position.y)
		if abs(roamingDistY) > self.maxAllowedYRoaming:
			if roamingDistY > 0:
				self.position.y+=roamingDistY-self.maxAllowedYRoaming
			else:
				self.position.y+=roamingDistY+self.maxAllowedYRoaming
################### Camera ends   #############################################

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
		camerax=camera.position.x
		cameray=camera.position.y		
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
		self.width=30*xscale
		self.height=30*yscale
		self.origWidth=self.width
		self.image=pygame.transform.scale(CLOUDIMAGE,(self.width,self.height))
		self.startTime=time.time()
		self.age=0.2
		self.velocity=CreateVector(random.randint(0,4),random.randint(0,4))
	def display(self):
		myrect=self.image.get_rect()
		myrect.centerx,myrect.centery=self.position.x-camera.position.x,self.position.y-camera.position.y
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
		cloudsList.append(cloudBurst(pos.x,pos.y))

################## Platform starts ########################################
class Platform:
	def __init__(self,x,y,wid,hei,hori):
		self.position=CreateVector(x,y)
		self.onScreen=True
		self.isHorizontal=hori
		if self.isHorizontal:

			self.imagexOrig=HORIZONTALPIPE
		else:
			self.imageOrig=VERTICALPIPE
		self.width,self.height=wid*xscale,hei*yscale
		self.imagex=pygame.transform.scale(self.imagexOrig,(int(self.width),int(self.height)))

		self.leftCollider=positionBlock(x,y,-0.48*wid,0,0,0.04*wid,0.8*hei,(0,0,255))
		self.rightCollider=positionBlock(x,y,0.48*wid,0,0,0.04*wid,0.8*hei,(0,0,255))
		self.topCollider=positionBlock(x,y,0,-0.45*hei,0,0.99*wid,0.1*hei)
		self.bottomCollider=positionBlock(x,y,0,0.45*hei,0,0.99*wid,0.1*hei)
		self.colliders=[self.leftCollider,self.rightCollider,self.topCollider,self.bottomCollider]

	def display(self):
		myrect=self.imagex.get_rect()
		myrect.centerx,myrect.centery=self.position.x-camera.position.x,self.position.y-camera.position.y
		win.blit(self.imagex,myrect)
		for col in self.colliders:
			col.display()
################## Platform ends ########################################


################## Bullet starts ########################################
class Bullet:
	def __init__(self,x,y,dir,parent):
		self.parent=parent
		self.position=CreateVector(x,y)
		self.velocity=CreateVector(dir * 20,0)
		self.onScreen=True
		self.imagexOrig=VENGEFUL_SPIRIT
		self.maxWidth=80
		self.width=self.maxWidth*xscale
		self.height=self.maxWidth*yscale
		self.imagex=pygame.transform.scale(pygame.transform.flip(self.imagexOrig,True,False),(self.width,self.height))
		self.dir=dir
		self.birthTime=time.time()
	def display(self):		
		myrect=self.imagex.get_rect()
		myrect.centerx,myrect.centery=self.position.x-camera.position.x,self.position.y-camera.position.y
		win.blit(self.imagex,myrect)
	def update(self):
		self.CheckCollisions()
		self.position.add(self.velocity)
		self.width*=0.97
		self.height*=0.97
		self.imagex=pygame.transform.scale(pygame.transform.flip(self.imagexOrig,True if self.dir==-1 else False,False),(int(self.width),int(self.height)))
		if self.width < self.maxWidth/10:
			self.onScreen=False

	def CheckCollisions(self):
		if self.parent!=player:
			if boxCollision(self,player.boxCollider):
				player.TakeDamage(10)
				self.onScreen=False
				rockSmash.play()
				SpawnCloudGroup(self.position)
		else:
			for x in enemiesList[:]:
				if not x.onScreen:
					enemiesList.remove(x)
					continue
				if boxCollision(self,x):
					x.TakeDamage(10)
					self.onScreen=False
					rockSmash.play()
					SpawnCloudGroup(self.position)


################## Bullet ends   ########################################


#######################Battle Trigger starts ############################
class BattleTrigger:
	def __init__(self,x,y,wid,hei,bossID):
		self.bossID=bossID
		self.position=CreateVector(x,y)
		self.onScreen=True
		self.imagexOrig=TREE_IMAGE
		self.width=int(wid*xscale)
		self.height=int(hei*yscale)
		self.imagex=pygame.transform.scale(self.imagexOrig,(self.width,self.height))
		self.jobDone=False
		self.visible=True
	def display(self):	
		if not self.visible:
			return	
		self.imagex=pygame.transform.scale(self.imagexOrig,(int(self.width),int(self.height)))
		myrect=self.imagex.get_rect()
		myrect.centerx,myrect.centery=self.position.x-camera.position.x,self.position.y-camera.position.y
		win.blit(self.imagex,myrect)
	def update(self):
		if player and not self.jobDone:
			if boxCollision(player,self):
				gameManager.InformAboutGate(self.bossID,self)
				self.jobDone=True
				self.visible=False				
				camera.target=self
				camera.lerpFactor=16
				# camera.TemporarilySkipToPoint(self.position)
#######################Battle Trigger ends ############################

##########################FightGate starts ############################
class FightGate:
	def __init__(self,x,y,wid,hei):
		self.position=CreateVector(x,y)
		self.width=int(wid * xscale)
		self.height= int(hei * yscale)
		self.onScreen=True
		self.imagexOrig=GATE_IMAGE
		self.imagex=pygame.transform.scale(self.imagexOrig,(self.width,self.height))
		self.onScreen=True

		self.leftCollider=positionBlock(x,y,-0.45*wid,0,0,0.1*wid,0.8*hei,(0,0,255))
		self.rightCollider=positionBlock(x,y,0.45*wid,0,0,0.1*wid,0.8*hei,(0,0,255))
		self.topCollider=positionBlock(x,y,0,-0.45*hei,0,0.29*wid,0.1*hei)
		self.bottomCollider=positionBlock(x,y,0,0.45*hei,0,0.29*wid,0.1*hei)
		self.colliders=[self.leftCollider,self.rightCollider,self.topCollider,self.bottomCollider]
	def display(self):
		myrect=self.imagex.get_rect()
		myrect.centerx,myrect.centery=self.position.x-camera.position.x,self.position.y-camera.position.y
		win.blit(self.imagex,myrect)
		for col in self.colliders:
			col.display()
##########################FightGate ends ############################

##########################Sphere starts #############################
class Sphere:
	def __init__(self,x,y,gate1,gate2,itemToDestroy):
		self.position=CreateVector(x,y)
		self.width=int(100*xscale)
		self.height=int(100*yscale)
		self.onScreen=True
		self.imagexOrig=SPHERE_IMAGE
		self.imagex=pygame.transform.scale(self.imagexOrig,(self.width,self.height))
		self.bossGates=[gate1,gate2]
		self.state="idle"
		self.dir=1
		self.maxHealth=100
		self.health=self.maxHealth
		self.bullets=[]
		self.bombs=[]
		self.lastShotTime=0
		self.shootGap=2
		self.shootTimer=0
		self.maxShootSpan=2
		self.lastAttackTime=0 
		self.maxAttackGap=1
		self.attackStates=["ShootAttack","PlungeAttack","ShootAttack","PlungeAttack","RiseAndDropBombs"]
		self.plungeVelocity=CreateVector(20*xscale,0)
		self.plungeTimer=0
		self.plungeTimerRev=0
		self.hitTargetWhilePlunging=False
		self.itemToDestroy=itemToDestroy
		# self.plungeVelocitySet=False
		SpawnCloudGroup(self.position)
		self.birthTime=time.time()
		self.warmUpTime=1
		self.activated=False
		self.plungeSoundPlayed=False

		self.risingSubState="rising"
		self.riseVelocity=CreateVector(0,-10*yscale)
		self.cruiseVelocity=CreateVector(10*xscale,0)
		self.riseTimer=0
		self.cruiseTimer=0
		self.maxCruiseTime=2
		self.maxRiseTime=1.5
		self.lastBombDropTime=0
		self.maxBombGap=1
		self.maxBombGapVar=0
		self.healthBar=HealthBar(self.position.x,self.position.y,0,-50*yscale,0,100*xscale,20*yscale,self.maxHealth,False)

	def TakeDamage(self,dmg):
		self.health-=dmg
		self.healthBar.reduceHealth(dmg)		
		if self.health <= 0:
			self.onScreen=False
			self.bossGates[0].onScreen=False
			self.bossGates[1].onScreen=False
			self.itemToDestroy=False
			camera.target=player
			camera.lerpFactor=8
	def Shoot(self):
		if time.time()-self.lastShotTime > self.shootGap:
			self.lastShotTime=time.time()
			self.bullets.append(Bullet(self.position.x,self.position.y,self.dir,self))
	def updateAndRunBullets(self):
		for x in self.bullets:
			if not x.onScreen:
				continue
			x.update()
			x.display()
		flushList(self.bullets)
		for x in self.bombs:
			if not x.onScreen:
				continue
			x.update()
			x.display()
		flushList(self.bombs)
	def display(self):
		self.healthBar.display()
		myrect=self.imagex.get_rect()
		myrect.centerx,myrect.centery=self.position.x-camera.position.x,self.position.y-camera.position.y
		win.blit(self.imagex,myrect)
		self.updateAndRunBullets()

	def checkActivation(self):
		if time.time()-self.birthTime > self.warmUpTime:
			self.activated=True

	def update(self):
		self.healthBar.update(0,self.position)
		if not self.activated:
			self.checkActivation()
			return
		self.CauseDamageToPlayerOnTouch()
		if self.state=="idle":
			self.DoIdleStuff()
		elif self.state=="attack":
			self.Attack()
		elif self.state=="ShootAttack":
			self.ShootAttack()
		elif self.state=="PlungeAttack":
			self.PlungeAttack()
		elif self.state=="RiseAndDropBombs":
			self.RiseAndDropBombs()
	def DoIdleStuff(self):
		if self.enemyBehind():
			self.imagex=pygame.transform.flip(self.imagex,True,False)
			self.dir*=-1
			self.state="attack"
			fogGateSound.play()
		elif self.enemyInFront():
			self.state="attack"
	def enemyBehind(self):
		return Raycast(self.position,VECTORRIGHT.copy().mult(self.dir*-1),700*xscale,player)
	def enemyInFront(self):
		return Raycast(self.position,VECTORRIGHT.copy().mult(self.dir),400*xscale,player)

	def Attack(self):
		if self.enemyBehind():
			self.imagex=pygame.transform.flip(self.imagex,True,False)
			self.dir*=-1
		self.AttackRandomly()
	def AttackRandomly(self):
		if  time.time() -self.lastAttackTime > self.maxAttackGap:
			self.lastAttackTime=time.time()
			randomAttack=self.attackStates[random.randint(0,len(self.attackStates)-1)]
			if randomAttack=="ShootAttack":
				self.state="ShootAttack"				
			elif randomAttack=="PlungeAttack":
				self.state="PlungeAttack"
			elif randomAttack=="RiseAndDropBombs":
				self.state="RiseAndDropBombs"

	def ShootAttack(self):
		self.shootTimer+=1/FRAME_RATE
		if self.shootTimer > self.maxShootSpan:
			self.shootTimer=0
			self.lastAttackTime=time.time()
			self.state="attack"
		else:
			self.Shoot()


	def PlungeAttack(self):	
		if not self.plungeSoundPlayed:
			lossBuzz.play()
			self.plungeSoundPlayed=True	
		if self.hitTargetWhilePlunging:
			self.position.add(self.plungeVelocity.copy().mult(-self.dir))
			self.plungeTimerRev+=1/FRAME_RATE
			if self.plungeTimerRev >= self.plungeTimer:
				self.ComeOutOfPlunge()
		else:
			self.plungeTimer+=1/FRAME_RATE
			self.position.add(self.plungeVelocity.copy().mult(self.dir))
			for x in roadBlocksList:
				if x.onScreen:
					if boxCollision(self,x.leftCollider) or boxCollision(self,x.rightCollider):
						self.hitTargetWhilePlunging=True
	def ComeOutOfPlunge(self):
		self.hitTargetWhilePlunging=False
		self.state="attack"
		self.plungeTimer=0
		self.plungeTimerRev=0
		self.plungeSoundPlayed=False


	def CauseDamageToPlayerOnTouch(self):
		if not player.onScreen:
			return
		if boxCollision(self,player.boxCollider):
			player.TakeDamage(20)
			self.activated=False
			self.birthTime=time.time()
			self.warmUpTime=1
			if self.state=="PlungeAttack":
				self.hitTargetWhilePlunging=True


	#sphere rises up for a fixed time moves forward, moves forward and lowers  , dropping bombs at regular intervals the entire time
	def RiseAndDropBombs(self):
		if time.time()-self.lastBombDropTime > self.maxBombGap+self.maxBombGapVar:
			self.lastBombDropTime=time.time()
			self.maxBombGapVar=random.randrange(-2,2)/10
			self.bombs.append(Bomb(self.position.x,self.position.y,int(self.width*0.5),int(self.width*0.5)))
		if self.risingSubState=="rising":
			self.position.add(self.riseVelocity)
			self.riseTimer+=1/FRAME_RATE
			if self.riseTimer > self.maxRiseTime:
				self.risingSubState="cruising"
		elif self.risingSubState=="cruising":
			self.position.add(self.cruiseVelocity.copy().mult(self.dir))
			self.cruiseTimer+=1/FRAME_RATE
			if self.cruiseTimer > self.maxCruiseTime:
				self.risingSubState="revcruising"
		elif self.risingSubState=="revcruising":
			self.position.add(self.cruiseVelocity.copy().mult(self.dir*-1))
			self.cruiseTimer-=1/FRAME_RATE
			if self.cruiseTimer <=0:
				self.risingSubState="falling"
		else:
			self.position.add(self.riseVelocity.copy().mult(-1))
			self.riseTimer-=1/FRAME_RATE
			if self.riseTimer <= 0:
				self.risingSubState="rising"				
				self.state="attack"
				# self.comeOutOfRise()

	def comeOutOfRise(self):
		self.riseTimer=0
		self.cruiseTimer=0
		self.risingSubState="rising"
		self.state="attack"

		
##########################Sphere ends #############################

#################### Bomb starts #########################################
class Bomb:
	def __init__(self,x,y,wid,hei):
		self.onScreen=True
		self.position=CreateVector(x,y)
		self.imagexOrig=DOT
		self.width=wid
		self.height=hei
		self.imagex=pygame.transform.scale(self.imagexOrig,(self.width,self.width))
		self.acceleration=CreateVector(0,1*yscale)
		self.maxVelocity=20*yscale
		self.velocity=CreateVector(0,5*yscale)
		self.birthDay=time.time()
		self.lifeTime=4

	def display(self):
		myrect=self.imagex.get_rect()
		myrect.centerx,myrect.centery=self.position.x-camera.position.x,self.position.y-camera.position.y
		win.blit(self.imagex,myrect)

	def updateVelocity(self):
		if self.velocity.y < self.maxVelocity:
			self.velocity.add(self.acceleration)

	def update(self):
		self.updateVelocity()
		self.position.add(self.velocity)
		self.CheckCollisions()
		self.CheckAge()

	def CheckCollisions(self):
		for x in roadBlocksList:
			if boxCollision(self,x):
				self.onScreen=False
				rockSmash.play()
				SpawnCloudGroup(self.position)
				
		if boxCollision(self,player):
			x.onScreen=False
			self.onScreen=False
			rockSmash.play()
			player.TakeDamage(10)
			SpawnCloudGroup(self.position)
	def CheckAge(self):
		if time.time()-self.birthDay > self.lifeTime:
			self.onScreen=False


#################### Bomb ends   #########################################



################## Player starts #########################################
class Player:
	def __init__(self,x,y,wid,hei):
		self.onScreen=True
		self.position=CreateVector(x,y)
		self.idle_images,self.run_images,self.slash_images=[],[],[]
		self.width,self.height=wid*xscale,hei*yscale
		for i in range(10):
			idim=pygame.image.load(f'./sprites/protagonist/Idle/E_E_Sword__Idle_00{i}.png')
			runim=pygame.image.load(f'./sprites/protagonist/Run/E_E_Sword__Run_00{i}.png')
			attkim=pygame.image.load(f'./sprites/protagonist/Slash/E_E_Sword__Attack_00{i}.png')
			self.idle_images.append(idim)
			self.run_images.append(runim)
			self.slash_images.append(attkim)
		self.animations=[self.idle_images,self.run_images,self.slash_images]
		self.animFrame=0
		self.frame=0
		self.animInQueue=None
		self.velocity=CreateVector(0,0)
		self.acceleration=CreateVector(0,0)
		self.maxVelocityMag=20*yscale
		self.maxHorizontalvelocity=10*xscale
		self.dir=1
		self.jumping=False
		self.readyForSpaceBar=True
		self.jumpStartTime=0
		self.gravityScale=2
		self.jumpForce=8
		self.maxJumpTime=0.15
		self.lastShotTime=0
		self.shootGap=1
		self.bullets=[]
		self.maxHealth=100
		self.health=self.maxHealth
		self.invincible=False
		self.invincibleStartTime=0
		self.maxInvincibilityGap=3
		self.maxImmovableGap=0.5
		self.invincibilityCounter=0
		self.healthBar=HealthBar(1150*xscale,60*yscale,0,0,0,200*xscale,30*yscale,self.maxHealth)
		self.boxCollider=collisionBox(self.position.x,self.position.y,self.width*0.55,self.height*0.55)
		self.isDashing=False
		self.dashTime=0
		self.maxDashTime=0.25
		self.dashVelocity=CreateVector(30*xscale,0)
		self.allowedToDash=True
		self.immovable=False


		self.animTimers=[0,0,0]
		self.animTimersMax=[1,1,3]

	def TakeDamage(self,dmg):
		if not self.invincible:
			if self.RunningAnimation()=="run":
				self.changeAnimation("idle")
			stopRunningSound()
			self.health-=dmg
			self.healthBar.reduceHealth(dmg)
			self.immovable=True
			self.invincible=True
			self.invincibleStartTime=time.time()
			self.velocity.set(0,0)
			

	def CanDisplay(self):
		if not self.invincible:
			return True
		self.invincibilityCounter+=1
		if self.invincibilityCounter%2==0:
			return True
		return False
	def ManageInvincibility(self):
		if not self.invincible:
			return
		if time.time()-self.invincibleStartTime > self.maxInvincibilityGap:
			self.invincible=False 
		elif time.time()-self.invincibleStartTime > self.maxImmovableGap:
			self.immovable=False


	def RunBullets(self):
		for x in self.bullets:
			if not x.onScreen:
				continue
			x.update()
			x.display()
		flushList(self.bullets)

	def FollowInput(self):
		if self.RunningAnimation()=="slash":
			if self.velocity.x !=0:
				self.acceleration.x+=-self.velocity.x/abs(self.velocity.x)*1			
			return

		if RIGHTPRESSED:
			self.dir=1
			self.acceleration.x+=0.5			
			playRunningSound()
			self.changeAnimation("run")
		elif LEFTPRESSED:
			self.dir=-1
			self.acceleration.x-=0.5
			playRunningSound()
			self.changeAnimation("run")
		else:
			stopRunningSound()
			if self.velocity.x !=0:
				self.acceleration.x+=-self.velocity.x/abs(self.velocity.x)*1
			if self.RunningAnimation()=="run":
				self.changeAnimation("idle") 

		if SPACEPRESSED:
			if self.readyForSpaceBar and not self.jumping and self.CheckIfOnFloor():				
				self.readyForSpaceBar=False
				self.jumping=True
				goalBloop.play()
				self.jumpStartTime=time.time()
			elif self.jumping:
				if time.time()-self.jumpStartTime > self.maxJumpTime:
					self.jumping=False					
				self.ApplyJumpForce()
		else:
			self.readyForSpaceBar=True

		if ZPRESSED:
			self.shoot()

		if CPRESSED and self.allowedToDash and not self.isDashing:			
			self.allowedToDash=False
			self.StartDashing()
		elif not CPRESSED and not self.allowedToDash:
			self.allowedToDash=True

		if not self.CheckIfOnFloor():
			if self.RunningAnimation()=="run":
				self.changeAnimation("idle")
			stopRunningSound()


	def shoot(self):
		if time.time()-self.lastShotTime > self.shootGap:
			self.animInQueue="idle"
			self.changeAnimation("slash")
			self.lastShotTime=time.time()
			# self.bullets.append(Bullet(self.position.x,self.position.y,self.dir,self))
		
	def CheckIfOnFloor(self):
		for elem in collidableObjects:		
			if Raycast(self.position,VECTORDOWN,60*yscale,elem):
				# w2screen(win,"In Touch with Ground",600,100)
				return True
		return False


	def ClearToRunAnim(self):
		self.animTimers[self.animFrame]+=1
		if self.animTimers[self.animFrame] >= self.animTimersMax[self.animFrame]:
			self.animTimers[self.animFrame]=0
			return True
		return False

	def changeAnimation(self,anim):
		if anim=="idle" and self.animFrame!=0:
			self.animFrame=0
			self.frame=0
		elif anim=="run" and self.animFrame!=1:
			self.animFrame=1
			self.frame=0
		elif anim=="slash" and self.animFrame!=2:
			self.animFrame=2
			self.frame=0

	def RunningAnimation(self):
		if self.animFrame==0:
			return "idle"
		elif self.animFrame==1:
			return "run"
		elif self.animFrame==2:
			return "slash"
		return "unknown"

	def updateAnimations(self):
		if self.ClearToRunAnim():
			self.frame+=1
			if self.frame==4 and self.RunningAnimation()=="slash":
				self.bullets.append(Bullet(self.position.x,self.position.y,self.dir,self))
			if self.frame >= len(self.animations[self.animFrame]):
				if not self.animInQueue:
					self.frame=0					
				else:
					self.changeAnimation(self.animInQueue)
					self.animInQueue=None

	def display(self):
		self.ManageInvincibility()		
		img=pygame.transform.scale(self.animations[self.animFrame][self.frame],(int(self.width),int(self.height)))
		if self.dir==-1:
			img=pygame.transform.flip(img,True,False)
		myrect=img.get_rect()
		myrect.centerx,myrect.centery=self.position.x-camera.position.x,self.position.y-camera.position.y
		if self.CanDisplay():
			win.blit(img,myrect)
		self.updateAnimations()
		self.CheckIfOnFloor()
		self.RunBullets()
		self.healthBar.display()
		self.boxCollider.display()

	def ApplyGravity(self):
		self.acceleration.y+=self.gravityScale*yscale
	def ApplyJumpForce(self):
		self.acceleration.y-=self.jumpForce*yscale


	def Dash(self):
		self.dashTime+=1/FRAME_RATE
		if self.dashTime > self.maxDashTime or self.invincible:
			self.RecoverFromDash()
		self.position.add(self.dashVelocity.copy().mult(self.dir))

	def StartDashing(self):
		self.isDashing=True
		self.jumping=False
		self.velocity.set(0,0)
		SpawnCloudGroup(self.position)

	def RecoverFromDash(self):
		self.dashTime=0
		self.isDashing=False

	def update(self):
		self.checkCollisionWithRoadBlocks()
		# self.boxCollider.updateP(self.position)
		self.boxCollider.update(self.position.x-10*xscale,self.position.y+10*yscale,self.width*0.55,self.height*0.55)		
		if self.isDashing:
			self.Dash()
			return
		if not self.immovable:
			self.FollowInput()
		self.ApplyGravity()		
		self.velocity.add(self.acceleration)
		self.RestrictVerticalVelocity()
		self.RestrictHorizontalVelocity()
		self.position.add(self.velocity)
		self.acceleration.set(0,0)

	def RestrictHorizontalVelocity(self):
		if abs(self.velocity.x) > self.maxHorizontalvelocity:
			self.velocity.x=self.velocity.x/abs(self.velocity.x) * self.maxHorizontalvelocity
	def RestrictVerticalVelocity(self):
		if self.velocity.y > self.maxVelocityMag:
			self.velocity.y=self.maxVelocityMag*self.velocity.y/abs(self.velocity.y)

	def checkCollisionWithRoadBlocks(self):
		for elem in roadBlocksList:
			if not elem.onScreen:
				continue
			if boxCollision(self,elem.topCollider):
				self.position.y-=abs(self.velocity.y)
				self.velocity.y/=2
			if boxCollision(self,elem.bottomCollider):
				self.position.y+=abs(self.velocity.y)
			if boxCollision(self,elem.rightCollider):
				if self.isDashing:
					self.position.x+=abs(self.dashVelocity.x)
					self.RecoverFromDash()
				else:
					self.position.x+=abs(self.velocity.x)
			if boxCollision(self,elem.leftCollider):
				if self.isDashing:
					self.position.x-=abs(self.dashVelocity.x)
					self.RecoverFromDash()
				else:
					self.position.x-=abs(self.velocity.x)




################## Player ends   #########################################

################## Game Manager starts ###################################
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

	def InformAboutGate(self,bossID,btrigger):
		if bossID==0 and self.currentScene==0:
			print("sphere boss fight will be initiated")
			fightGatesList.append(FightGate(1468,392,40,300))
			roadBlocksList.append(fightGatesList[-1])
			fightGatesList.append(FightGate(2610,392,40,300))
			roadBlocksList.append(fightGatesList[-1])
			spheresList.append(Sphere(2200*xscale,480*yscale,fightGatesList[-2],fightGatesList[-1],btrigger))
			enemiesList.append(spheresList[-1])



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
				print('loading complete')		
				return
			elif self.loadingObjects:
				self.LoadObjects(line)
		filex.close()

	def LoadObjects(self,line):
		global pChanger,player
		if not re.search(r'[0-9]',line):
			self.loadingType=re.findall(r'[a-z]+',line)[0]			
		else:
			nums=re.findall(r'[0-9\-]+',line)
			if self.loadingType=='platform':
				platformList.append(Platform(int(nums[0])*xscale,
					                    int(nums[1])*yscale,
					                    int(nums[2])*xscale,
					                    int(nums[3])*yscale,
					                    True if int(nums[4])==1 else False					                    
					               ))
				collidableObjects.append(platformList[-1])
				roadBlocksList.append(platformList[-1])
				# pChanger=posChanger(platformList[-1])	
			if self.loadingType=='player':
				player=Player(int(nums[0])*xscale,int(nums[1])*yscale,int(nums[2]),int(nums[3]))
				camera.target=player
				# pChanger=posChanger(player,False)
			if self.loadingType=='trigger':
				triggersList.append(BattleTrigger(
					                    int(nums[0])*xscale,
					                    int(nums[1])*yscale,
					                    int(nums[2])*xscale,
					                    int(nums[3])*yscale,
					                    int(nums[4])					                   
												  )
								   )	
				# pChanger=posChanger(triggersList[-1])		

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
		platformList=[]


################## Game Manager ends ###################################

################### Collision Box Starts #################################
class collisionBox:
	def __init__(self,x,y,width,height,col='red'):
		self.width=width
		self.height=height
		self.position=CreateVector(x,y)
		self.col=(255,0,0) if col=='red' else (0,0,255)
	def display(self):
		pygame.draw.rect(win,self.col,
									(self.position.x-self.width/2-camera.position.x,
									 self.position.y-self.height/2-camera.position.y,self.width,self.height))
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
									(self.position.x-self.width/2-camera.position.x,
									 self.position.y-self.height/2-camera.position.y,self.width,self.height))
		else:
			pygame.draw.rect(win,self.col,
									(self.position.x-camera.position.x,
									 self.position.y-self.height/2-camera.position.y,self.width,self.height))
################## Position Block Ends   ###################################


VECTORRIGHT=CreateVector(1,0)
VECTORLEFT =CreateVector(-1,0)
VECTORDOWN =CreateVector(0,1)
VECTORUP   =CreateVector(0,-1)
def RunGame():
	gameManager.update()
	camera.followTarget()
	for x in platformList:
		x.display()
	for x in triggersList:
		if x.onScreen:
			x.display()			
			x.update()
	flushList(triggersList)
	for x in spheresList:
		if x.onScreen:
			x.display()
			x.update()
	flushList(spheresList)
	for x in fightGatesList:
		if x.onScreen:
			x.display()
	flushList(fightGatesList)
	if player:
		player.update()
		player.display()
	for x in cloudsList:
		if x.onScreen:
			x.update()
			x.display()
	flushList(cloudsList)

	if pChanger:		
		pChanger.update(win)

	

########################## sound functions starts ##################################
def playRunningSound():
	global lastTimeRunningSoundWP,runningTimeDuration
	if time.time()-lastTimeRunningSoundWP > runningTimeDuration:
		lastTimeRunningSoundWP=time.time()
		runningSound.play()
def stopRunningSound():
	global lastTimeRunningSoundWP
	runningSound.stop()
	lastTimeRunningSoundWP=time.time()-100
########################## sound functions ends   ##################################

######################### Main Region Starts #################################
pygame.init()
pygame.display.set_caption('Ladder Boy')
MOUSEX,MOUSEY=0,0
LEFTPRESSED,RIGHTPRESSED,UPPRESSED,DOWNPRESSED=False,False,False,False
IPRESSED,LPRESSED,MPRESSED,JPRESSED,ZPRESSED,CPRESSED=False,False,False,False,False,False
TPRESSED,HPRESSED,BPRESSED,FPRESSED=False,False,False,False
SPACEPRESSED,MOUSECLICKED,CTRLPRESSED=False,False,False
FRAME_RATE=30
WIN_WIDTH,WIN_HEIGHT=1400,800
xscale,yscale=int(WIN_WIDTH/1400),int(WIN_HEIGHT/800)
camera=Camera()
gameManager=GameManager()
platformList,roadBlocksList=[],[]
collidableObjects=[]
triggersList,spheresList,fightGatesList,enemiesList,cloudsList=[],[],[],[],[]


######################## Stuff that handles running sounds ##################
runningSound=pygame.mixer.Sound('./sounds/runningsound.wav')
global lastTimeRunningSoundWP,runningTimeDuration
lastTimeRunningSoundWP=0
runningTimeDuration=4
######################## Stuff that handles running sounds ends##############
fogGateSound=pygame.mixer.Sound('./sounds/fogGate.wav')
rockSmash=pygame.mixer.Sound('./sounds/RockSmash.wav')
goalBloop=pygame.mixer.Sound('./sounds/GoalBloop.wav')
lossBuzz=pygame.mixer.Sound('./sounds/LossBuzz.wav')


global pChanger,player
pChanger,player=None,None


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

			if event.key == K_ESCAPE:
				run=False
				pygame.quit()
				sys.exit()

		if event.type == KEYDOWN:
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

			if event.key == K_ESCAPE:
				pygame.quit()
				sys.exit()

		if event.type == MOUSEBUTTONDOWN:
			MOUSECLICKED=True
		elif event.type == MOUSEBUTTONUP:
			MOUSECLICKED=False

		if event.type == MOUSEMOTION:
			MOUSEX,MOUSEY=event.pos
	win.fill((0,0,0))
	RunGame()
	pygame.display.update()
######################### Main Region Ends #################################


