import pygame
# import neat
import time
import os
import random
import math
from pygame.locals import *
from helpers import *
from soldier import *
from Camera import *
import variableStore as v

pygame.font.init()


v.LEFTPRESSED,v.RIGHTPRESSED,v.UPPRESSED,v.DOWNPRESSED=False,False,False,False
v.FRAME_RATE=30
v.BACKGROUND_COLOR=(0,0,0)
v.WIN_WIDTH,v.WIN_HEIGHT=1000,500
v.mouseAtx,v.mouseAty,v.mouseClicked=0,0,True
v.soldiersList=[]
v.camera=Camera()
'''
BACKGROUND_IMAGE=pygame.transform.scale( pygame.image.load(
														   os.path.join("images","background.png")
														 ),
										 (WIN_WIDTH,WIN_HEIGHT)
									    )    
'''

def draw_background(win):
	win.blit(BACKGROUND_IMAGE,(0,0))









v.soldiersList.append(soldier(v.WIN_WIDTH/2,v.WIN_HEIGHT/2))
def RunGame():
	win.fill(v.BACKGROUND_COLOR)
	for x in v.soldiersList:
		x.display(win)
		x.update()




#MAIN PROGRAM STARTS HERE
win = pygame.display.set_mode((v.WIN_WIDTH,v.WIN_HEIGHT))
clock= pygame.time.Clock()
run=True



while run:	
	clock.tick(v.FRAME_RATE)
	
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run=False
			pygame.quit()
			quit()

		if event.type == KEYUP:
			if event.key in (K_UP, K_w):
				v.UPPRESSED=False
			elif event.key in (K_DOWN, K_s):
				v.DOWNPRESSED = False	        
			elif event.key in (K_LEFT, K_a):
				v.LEFTPRESSED= False      
			elif event.key in (K_RIGHT, K_d):
				v.RIGHTPRESSED= False
			if event.key==K_ESCAPE:
				pygame.quit()
				sys.exit()

		elif event.type == KEYDOWN:
			if event.key in (K_UP, K_w):
				# print('up key pressed')
				v.UPPRESSED=True
			elif event.key in (K_DOWN, K_s):
				v.DOWNPRESSED = True	        
			elif event.key in (K_LEFT, K_a):
				v.LEFTPRESSED= True      
			elif event.key in (K_RIGHT, K_d):
				v.RIGHTPRESSED= True

		if event.type == MOUSEBUTTONDOWN:
			v.mousex, v.mousey = event.pos
			v.mouseClicked = True
			

		if event.type == MOUSEBUTTONUP:
			v.mousex,v.mousey = event.pos			
			v.mouseClicked = False

	#draw_background(win)
	#ALL OBJECTS WILL WORK BELOW
	RunGame()
	#ALL OBJECTS WILL WORK ABOVE
	pygame.display.update()