import math
import pygame
from pygame.locals import *
import variableStore as v
import sys
FRAME_RATE=30
deltaTime=1000/FRAME_RATE

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
	rect1=pygame.Rect(obj1.position.x-obj1.width/2-v.camera.position.x,
					  obj1.position.y-obj1.height/2-v.camera.position.y,
					  obj1.width,obj1.height)
	rect2=pygame.Rect(obj2.position.x-obj2.width/2-v.camera.position.x,
					  obj2.position.y-obj2.height/2-v.camera.position.y,
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





