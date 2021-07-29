import pygame
import neat
import time
import os
import random
import math
from pygame.locals import *

pygame.font.init()

def w2screen(txt,px,py,fsiz=50):
	STAT_FONT= pygame.font.SysFont("comicsans",fsiz)
	text=STAT_FONT.render(txt,1,(255,0,0))
	win.blit(text,(px,py))


WIN_WIDTH,WIN_HEIGHT=1000,500
LEFTPRESSED,RIGHTPRESSED,UPPRESSED,DOWNPRESSED=False,False,False,False
mouseAtx,mouseAty,mouseClicked=0,0,True

'''
BACKGROUND_IMAGE=pygame.transform.scale( pygame.image.load(
														   os.path.join("images","background.png")
														 ),
										 (WIN_WIDTH,WIN_HEIGHT)
									    )    
'''

def draw_background(win):
	win.blit(BACKGROUND_IMAGE,(0,0))


def draw_translate_rotate(img,rotangle,x,y,win):
	rotated_image = pygame.transform.rotate(img, rotangle)
	new_rect = rotated_image.get_rect(center=img.get_rect(topleft=(x,y)).center)
	win.blit(rotated_image,new_rect.topleft)
def d2r(ang):
	return ang/180*math.pi

def check_collision(obj1,obj2):
	mask1=obj1.get_mask()
	mask2=obj2.get_mask()
	offset=(round(obj2.x-obj1.x),round(obj2.y-obj1.y))
	if mask1.overlap(mask2,offset):
		return True
	return False


#MAIN PROGRAM STARTS HERE
win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
clock= pygame.time.Clock()
run=True



while run:	
	clock.tick(30)
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run=False
			pygame.quit()
			quit()

		if event.type == KEYUP:
			if event.key in (K_UP, K_w):
				UPPRESSED=False
			elif event.key in (K_DOWN, K_s):
				DOWNPRESSED = False	        
			elif event.key in (K_LEFT, K_a):
				LEFTPRESSED= False      
			elif event.key in (K_RIGHT, K_d):
				RIGHTPRESSED= False
			if event.key==K_ESCAPE:
				pygame.quit()
				sys.exit()

		elif event.type == KEYDOWN:
			if event.key in (K_UP, K_w):
				# print('up key pressed')
				UPPRESSED=True
			elif event.key in (K_DOWN, K_s):
				DOWNPRESSED = True	        
			elif event.key in (K_LEFT, K_a):
				LEFTPRESSED= True      
			elif event.key in (K_RIGHT, K_d):
				RIGHTPRESSED= True

		if event.type == MOUSEBUTTONDOWN:
			mousex, mousey = event.pos
			mouseClicked = True
			

		if event.type == MOUSEBUTTONUP:
			mousex,mousey = event.pos			
			mouseClicked = False

	#draw_background(win)
	#ALL OBJECTS WILL WORK BELOW
	
	pygame.draw.line(win, (255,0,0), (0.2*WIN_WIDTH,0.2*WIN_HEIGHT), (0.8*WIN_WIDTH,0.8*WIN_HEIGHT), 2)
	w2screen("Kitchu is here",10,10,40)


	#ALL OBJECTS WILL WORK ABOVE
	pygame.display.update()