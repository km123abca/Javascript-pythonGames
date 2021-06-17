import pygame
import pygame_gui	
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

pygame.init()

'''
manager = pygame_gui.UIManager((800, 600))
text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(40,75, 100, 100), manager=manager)
'''

pygame.display.set_caption('Init Setup')

# pygame.font.init()


v.LEFTPRESSED,v.RIGHTPRESSED,v.UPPRESSED,v.DOWNPRESSED=False,False,False,False
v.FRAME_RATE=30
v.BACKGROUND_COLOR=(0,0,0)
v.WIN_WIDTH,v.WIN_HEIGHT=1000,500
v.xscale=int(v.WIN_WIDTH/1000)
v.yscale=int(v.WIN_HEIGHT/500)
v.mouseAtx,v.mouseAty,v.mouseClicked=0,0,False
v.soldiersList=[]
v.pipesList=[]
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
v.pipesList.append(pipe(500*v.xscale,450*v.yscale,900*v.xscale,40*v.yscale))
v.pipesList.append(pipe(50* v.xscale,250*v.yscale,40*v.xscale,400*v.yscale,False))
def RunGame():
	v.camera.runwithmouse()
	win.fill(v.BACKGROUND_COLOR)
	for x in v.soldiersList:
		if not x.onScreen:
			continue
		x.display(win)
		x.update()
	for x in v.pipesList:
		if not x.onScreen:
			continue
		x.display(win)




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
			v.mouseClicked = True
			

		if event.type == MOUSEBUTTONUP:						
			v.mouseClicked = False
		if event.type == MOUSEMOTION:
			v.mousex, v.mousey = event.pos
	'''
		if event.type == pygame.USEREVENT:
			if event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
				if event.ui_element == text_input:
					print(text_input.text)
		manager.process_events(event)

	manager.update(1/v.FRAME_RATE)
	manager.draw_ui(win)
	'''
	RunGame()	
	pygame.display.update()