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
FIREBALLIMAGE=pygame.image.load('./sprites/fireball.png')
HORIZONTAL_PIPE=pygame.image.load('./sprites/Pipes/pipeHori.png')
VERTICAL_PIPE=pygame.image.load('./sprites/Pipes/pipe.png')
HAZE=pygame.image.load('./sprites/haze.png')
GATE=pygame.image.load('./sprites/gate.png')
global BULLETIMAGE,BULLETSIZEFAC
BULLETIMAGE=REDCUBEIMAGE
BULLETSIZEFAC=0.05
#############################################
def changeBullet(gun):	
	global BULLETIMAGE,BULLETSIZEFAC
	if gun=='handgun':					
		BULLETSIZEFAC=0.05
		BULLETIMAGE=REDCUBEIMAGE
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
	def __init__(self,x,y,width,height):
		self.position=CreateVector(x,y)
		self.width=width
		self.height=height
		self.imagexOrig=GATE
		self.imagex=pygame.transform.scale(self.imagexOrig,(self.width,self.height))
		self.onScreen=True
		self.active=False
		self.leftCollider=collisionBox(self.position.x-0.36*self.width,self.position.y,0.2*self.width,self.height)
		self.rightCollider=collisionBox(self.position.x+0.36*self.width,self.position.y,0.2*self.width,self.height)
		self.topCollider=collisionBox(self.position.x,self.position.y-0.45*self.height,self.width,0.1*self.height)
		self.bottomCollider=collisionBox(self.position.x,self.position.y+0.45*self.height,self.width,0.1*self.height)
		self.colliders=[self.leftCollider,self.rightCollider,self.topCollider,self.bottomCollider]
	def display(self,win):
		myrect=self.imagex.get_rect()
		myrect.centerx=self.position.x-v.camera.position.x
		myrect.centery=self.position.y-v.camera.position.y
		win.blit(self.imagex,myrect)
		self.displayAndUpdateColliders(win)

	def displayAndUpdateColliders(self,win):
		if not self.active:
			return
		for x in self.colliders:
			x.display(win)


	def update(self):
		pass

		
class GameManager:
	def __init__(self):
		self.scenesLoaded=[False,False,False,False,False,False,False,False]
		self.scenesReady=[True,False,False,False,False,False,False,False]
		self.loadingObjects=False
		self.loadingType=None
		
	def checkScenes(self):
		#if self.sceneLoadingInProgress:
			#self.loadScene(i)
		for i,scene in enumerate(self.scenesLoaded):
			if self.scenesReady[i] and not scene:
				self.loadScene(i)

				
	def loadScene(self,i):
		filex=open('./SceneData.txt','r')
		for line in filex.readlines():
			if line[0]=='#':
				continue

			if 'scene'+str(i) in line:
				self.loadingObjects=True
			elif self.loadingObjects and 'sceneend' in line:
				self.scenesLoaded[i]=True				
				return
			elif self.loadingObjects:
				self.LoadObjects(line)

	def LoadObjects(self,line):
		if not re.search(r'[0-9]',line):
			self.loadingType=re.findall(r'[a-z]+',line)[0]
			# print("loading Type:"+self.loadingType)
		else:
			nums=re.findall(r'[0-9\-]+',line)
			# print("values:"+str(nums))
			# return
			if self.loadingType=='pipe':
				v.pipesList.append(pipe(int(nums[0])*v.xscale,
					                    int(nums[1])*v.yscale,
					                    int(nums[2])*v.xscale,
					                    int(nums[3])*v.yscale,
					                    int(nums[4])==1 if True else False,
					                    int(nums[5])==1 if True else False
					               ))
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
											 int(nums[3])*v.yscale
											 ))
			elif self.loadingType=='player':
				v.soldiersList.append(soldier(int(nums[0])*v.xscale,
											  int(nums[1])*v.yscale))
				v.camera.target=v.soldiersList[0]

	def update(self):
		self.checkScenes()



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
	def __init__(self,x,y,angle,parent):
		self.onScreen=True
		self.parent=parent
		self.position=CreateVector(x,y)
		self.width=int(self.parent.width*BULLETSIZEFAC)
		self.height=int(self.parent.width*BULLETSIZEFAC)
		self.image=pygame.transform.scale(BULLETIMAGE,(self.width,self.height))
		self.angle=angle
		self.speed=20*v.xscale
		self.velocity=CreateVector(self.speed * math.cos(d2r(self.angle)),self.speed * math.sin(d2r(self.angle)))



	def display(self,win):
		draw_translate_rotate(self.image,
							  360-self.angle,self.position.x-self.width/2-v.camera.position.x,
							  self.position.y-self.height/2-v.camera.position.y,win)

	def update(self):
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

	def OutOfBoundsCheck(self):
		if self.position.x - v.camera.position.x > v.WIN_WIDTH or self.position.x - v.camera.position.x < 0:
			self.onScreen=False
		if self.position.y - v.camera.position.y > v.WIN_HEIGHT or self.position.y - v.camera.position.y < 0:
			self.onScreen = False 


class soldier:
	def __init__(self,x,y):
		self.onScreen=True
		self.width=200
		self.height=200
		self.position=CreateVector(x,y)
		self.boxCollider=collisionBox(x,y,self.width*0.5,self.height*0.5)
		self.shootPosition=positionBlock(x,y,91*v.xscale,49*v.yscale,0,self.width*0.05,self.height*0.05)
		self.idle_images,self.move_images,self.shoot_images,self.reload_images,self.melee_images=[],[],[],[],[]		
		self.images=[]	
		self.angle=0
		self.animInQueue=None
		self.weaponIndex=0
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
		self.rotationSpeed=2
		self.vmax=10
		self.velMin=1
		self.velocity=CreateVector(self.velMin,0)	
		self.vel=self.velMin
		self.bullets=[]
		self.lastShootTime=0
		self.shootGap=2
		self.us=userSlider()
		self.weaponChangeAuthorized=True
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
				self.bullets.append(bullet(self.shootPosition.position.x,self.shootPosition.position.y,360-self.angle,self))
				self.ChangeAnimation("shoot")
				v.shootingSound.play()
			else:
				self.ChangeAnimation("melee")
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
		print("here here")
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

	def update(self,win):
		self.updateRunBullets(win)
		self.updateAndDrawShootPos(win)
		self.changeWeapons()
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
			if self.runningAnimation()=="idle":
				self.ChangeAnimation("move")		
			self.ApplyVelocity()
		else:
			if self.runningAnimation()=="move":
				self.ChangeAnimation("idle")
			self.DeApplyVelocity()

		self.boxCollider.updateP(self.position)
		
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
		
		for col in self.colliders:
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
	

			




		