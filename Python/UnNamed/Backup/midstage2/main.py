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
# pygame.mixer.music.load('./music/majula.mp3')
pygame.mixer.music.load('./music/majula.mp3')
pygame.mixer.music.set_volume(0.2)
v.shootingSound=pygame.mixer.Sound('./music/shoot.wav')
v.fogGateSound=pygame.mixer.Sound('./music/fogGate.wav')
v.fogGateSound.set_volume(0.2)
# pygame.font.init()


v.LEFTPRESSED,v.RIGHTPRESSED,v.UPPRESSED,v.DOWNPRESSED=False,False,False,False
v.FRAME_RATE=30
v.BACKGROUND_COLOR=(0,0,0)
v.WIN_WIDTH,v.WIN_HEIGHT=1400,800
v.xscale=int(v.WIN_WIDTH/1000)
v.yscale=int(v.WIN_HEIGHT/500)
v.mouseAtx,v.mouseAty,v.mouseClicked=0,0,False
v.soldiersList=[]
v.pipesList=[]
v.startScreenDisplayed=False
v.camera=Camera()

##################Global Images ###########################################
SOLDIER_IMAGE=pygame.image.load('./sprites/soldier/idle/survivor-idle_handgun_0.png')

###########################################################################

'''
BACKGROUND_IMAGE=pygame.transform.scale( pygame.image.load(
														   os.path.join("images","background.png")
														 ),
										 (WIN_WIDTH,WIN_HEIGHT)
									    )    
'''

def draw_background(win):
	win.blit(BACKGROUND_IMAGE,(0,0))


def startMusic():
	if not v.musicStarted:
		pygame.mixer.music.play(-1,0.0)
		v.musicStarted=True

def unloadStuff():
	# pygame.mixer.music.unload()
	print("unloaded to do here")
def startScreen():
	if v.startScreenDisplayed:
		return
	BASICFONT = pygame.font.Font('freesansbold.ttf', 32)
	imagex=pygame.transform.scale(SOLDIER_IMAGE,(400,400))
	startImageRect=imagex.get_rect()
	startImageRect.top=int(50*v.yscale)
	startImageRect.centerx=int(v.WIN_WIDTH/2)
	win.fill((  183,204,223))
	win.blit(imagex,startImageRect)
	instructions=['Press Left and Right Arrows to Turn','Up arrow to move','space to shoot']
	displayTop=startImageRect.top
	displayTop+=startImageRect.height
	for i in range(len(instructions)):
		instSurf=BASICFONT.render(instructions[i].upper(),1,(0,0,0))
		instRect=instSurf.get_rect()
		displayTop+=int(10*v.yscale)
		instRect.top=displayTop
		instRect.centerx=int(v.WIN_WIDTH/2)
		displayTop+=instRect.height
		win.blit(instSurf,instRect)
	while True:
		for event in pygame.event.get():
			if event.type==QUIT:
				unloadStuff()
				terminate()
			elif event.type == KEYDOWN:
				if event.key ==K_ESCAPE:
					unloadStuff()
					terminate()
				v.startScreenDisplayed=True
				return
		pygame.display.update()
		clock.tick(v.FRAME_RATE)








v.roadBlocks=[]
v.doorTriggersList=[]

'''
v.soldiersList.append(soldier(v.WIN_WIDTH/2,v.WIN_HEIGHT/2))
v.camera.target=v.soldiersList[0]
v.pipesList.append(pipe(661*v.xscale,769*v.yscale,1262*v.xscale,40*v.yscale,True,False))
v.pipesList.append(pipe(21* v.xscale,390*v.yscale,40*v.xscale,800*v.yscale,False,False))
v.pipesList.append(pipe(661*v.xscale,44*v.yscale,1262*v.xscale,40*v.yscale,True,False))
v.pipesList.append(pipe(1278* v.xscale,489*v.yscale,40*v.xscale,524*v.yscale,False,False))
v.pipesList.append(pipe(1922*v.xscale,769*v.yscale,1262*v.xscale,40*v.yscale,True,False))
v.pipesList.append(pipe(1783*v.xscale,40*v.yscale,987*v.xscale,40*v.yscale,True,False))
v.pipesList.append(pipe(2564* v.xscale,390*v.yscale,40*v.xscale,800*v.yscale,False,False))
v.pipesList.append(pipe(3207*v.xscale,769*v.yscale,1262*v.xscale,40*v.yscale,True,False))
v.pipesList.append(pipe(3852* v.xscale,270*v.yscale,40*v.xscale,536*v.yscale,False,False))
v.pipesList.append(pipe(3330*v.xscale,50*v.yscale,1006*v.xscale,40*v.yscale,True,False))
v.pipesList.append(pipe(21* v.xscale,-369*v.yscale,40*v.xscale,800*v.yscale,False,False))
v.pipesList.append(pipe(21* v.xscale,-1128*v.yscale,40*v.xscale,800*v.yscale,False,False))
v.pipesList.append(pipe(661*v.xscale,-1476*v.yscale,1262*v.xscale,40*v.yscale,True,False))
v.pipesList.append(pipe(661*v.xscale,-1476*v.yscale,1262*v.xscale,40*v.yscale,True,False))
v.pipesList.append(pipe(1923*v.xscale,-1476*v.yscale,1262*v.xscale,40*v.yscale,True,False))
v.pipesList.append(pipe(3185*v.xscale,-1476*v.yscale,1262*v.xscale,40*v.yscale,True,False))
v.pipesList.append(pipe(502*v.xscale,-712*v.yscale,928*v.xscale,40*v.yscale,True,False))
v.pipesList.append(pipe(1923*v.xscale,-712*v.yscale,1262*v.xscale,40*v.yscale,True,False))
v.pipesList.append(pipe(1277* v.xscale,-1004*v.yscale,40*v.xscale,568*v.yscale,False,False))
v.pipesList.append(pipe(2542* v.xscale,-1004*v.yscale,40*v.xscale,568*v.yscale,False,False))
v.pipesList.append(pipe(3850* v.xscale,-1131*v.yscale,40*v.xscale,800*v.yscale,False,False))
v.pipesList.append(pipe(3853* v.xscale,-371*v.yscale,40*v.xscale,800*v.yscale,False,False))
v.pipesList.append(pipe(2560* v.xscale,-371*v.yscale,40*v.xscale,800*v.yscale,False,False))
v.pipesList.append(pipe(3064*v.xscale,-711*v.yscale,986*v.xscale,40*v.yscale,True,False))
v.pipesList.append(pipe(1282* v.xscale,-462*v.yscale,40*v.xscale,560*v.yscale,False,False))
v.pipesList.append(pipe(4606*v.xscale,772*v.yscale,1488*v.xscale,40*v.yscale,True,False))
v.pipesList.append(pipe(4606*v.xscale,-37*v.yscale,1488*v.xscale,40*v.yscale,True,False))
v.pipesList.append(pipe(5333* v.xscale,348*v.yscale,40*v.xscale,812*v.yscale,False,False))
v.hazesList.append(haze(1922*v.xscale,406*v.yscale,1264*v.xscale,696*v.yscale,'door2'))
v.hazesList.append(haze(3208*v.xscale,406*v.yscale,1264*v.xscale,696*v.yscale,'door3'))
v.hazesList.append(haze(650*v.xscale,-330*v.yscale,1224*v.xscale,696*v.yscale,'door4'))
v.hazesList.append(haze(1934*v.xscale,-334*v.yscale,1264*v.xscale,705*v.yscale,'door5'))
v.hazesList.append(haze(3208*v.xscale,-334*v.yscale,1250*v.xscale,705*v.yscale,'door6'))
v.hazesList.append(haze(648*v.xscale,-1092*v.yscale,1264*v.xscale,730*v.yscale,'door7'))
v.hazesList.append(haze(1910*v.xscale,-1092*v.yscale,1220*v.xscale,730*v.yscale,'door8'))
v.hazesList.append(haze(3203*v.xscale,-1092*v.yscale,1264*v.xscale,730*v.yscale,'door9'))
v.doorTriggersList.append(doorTrigger(1274*v.xscale,159*v.yscale,36*v.xscale,184*v.yscale,'door12'))
v.doorTriggersList.append(doorTrigger(2410*v.xscale,36*v.yscale,261*v.xscale,34*v.yscale,'door25'))
v.doorTriggersList.append(doorTrigger(1281*v.xscale,-78*v.yscale,27*v.xscale,196*v.yscale,'door54'))
v.doorTriggersList.append(doorTrigger(1113*v.xscale,-705*v.yscale,289*v.xscale,38*v.yscale,'door47'))
v.doorTriggersList.append(doorTrigger(1284*v.xscale,-1358*v.yscale,26*v.xscale,194*v.yscale,'door87'))
v.doorTriggersList.append(doorTrigger(2540*v.xscale,-1358*v.yscale,26*v.xscale,194*v.yscale,'door89'))
v.doorTriggersList.append(doorTrigger(3694*v.xscale,-712*v.yscale,267*v.xscale,26*v.yscale,'door69'))
v.doorTriggersList.append(doorTrigger(2703*v.xscale,48*v.yscale,252*v.xscale,26*v.yscale,'door63'))
v.gatesList.append(gratedGate(3852*v.xscale,643*v.yscale,30*v.xscale,216*v.yscale))
'''


# v.pChanger=posChanger(v.gatesList[0])
for p in v.pipesList:
	v.roadBlocks.append(p)

v.gameManager=GameManager()
def RunGame():
	v.gameManager.update()
	# v.camera.runwithmouse()
	startScreen()
	startMusic()
	v.camera.followTarget()
	win.fill(v.BACKGROUND_COLOR)
	for x in v.soldiersList:
		if not x.onScreen:
			continue
		x.display(win)
		x.update(win)

	for x in v.pipesList:
		if not x.onScreen:
			continue
		x.display(win)		
		# x.update(win)

	for x in v.cloudsList:
		if not x.onScreen:
			continue
		x.display(win)
		x.update()
	flushList(v.cloudsList)

	for x in v.hazesList:
		# continue
		if not x.onScreen:
			continue
		x.display(win)

	flushList(v.hazesList)

	for x in v.doorTriggersList:
		if not x.onScreen:
			continue
		x.display(win)
		x.update()
	flushList(v.doorTriggersList)

	for x in v.gatesList:
		if not x.onScreen:
			continue
		x.display(win)
		x.update()
	flushList(v.gatesList)

	# v.pChanger.update(win)

	# w2screen(win,f'{v.camera.position.x+v.mousex},{v.camera.position.y+v.mousey}',50,100)



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

			if event.key ==K_SPACE:
				v.SPACEPRESSED=False

			elif event.key == K_t:
				v.TPRESSED= False
			elif event.key == K_h:
				v.HPRESSED= False
			elif event.key == K_b:
				v.BPRESSED= False
			elif event.key == K_f:
				v.FPRESSED= False
			elif event.key == K_i:
				v.IPRESSED= False
			elif event.key == K_l:
				v.LPRESSED= False
			elif event.key == K_m:
				v.MPRESSED= False
			elif event.key == K_j:
				v.JPRESSED= False

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

			if event.key ==K_SPACE:
				v.SPACEPRESSED=True

			elif event.key == K_t:
				v.TPRESSED= True
			elif event.key == K_h:
				v.HPRESSED= True
			elif event.key == K_b:
				v.BPRESSED= True
			elif event.key == K_f:
				v.FPRESSED= True
			elif event.key == K_i:
				v.IPRESSED= True
			elif event.key == K_l:
				v.LPRESSED= True
			elif event.key == K_m:
				v.MPRESSED= True
			elif event.key == K_j:
				v.JPRESSED= True

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