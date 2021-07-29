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

###########################Player Starts########################################
###########################Player ends#####################################

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
	pass

	

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
pygame.display.set_caption('Boss Fight1')
MOUSEX,MOUSEY=0,0
LEFTPRESSED,RIGHTPRESSED,UPPRESSED,DOWNPRESSED=False,False,False,False
IPRESSED,LPRESSED,MPRESSED,JPRESSED,ZPRESSED,CPRESSED=False,False,False,False,False,False
TPRESSED,HPRESSED,BPRESSED,FPRESSED=False,False,False,False
SPACEPRESSED,MOUSECLICKED,CTRLPRESSED=False,False,False
FRAME_RATE=30
WIN_WIDTH,WIN_HEIGHT=1400,800
xscale,yscale=int(WIN_WIDTH/1400),int(WIN_HEIGHT/800)
camera=Camera()



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
whoosh=pygame.mixer.Sound('./sounds/whoosh.wav')
parry=pygame.mixer.Sound('./sounds/parry.wav')
GetCoin=pygame.mixer.Sound('./sounds/GetCoin.wav')




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


