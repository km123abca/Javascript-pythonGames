import pygame
import neat
import time
import os
import random
import math
from pygame.locals import *

pygame.font.init()

def w2screen(txt,px,py,fsiz=50,rgb=(255,0,0)):
	STAT_FONT= pygame.font.SysFont("comicsans",fsiz)
	text=STAT_FONT.render(txt,1,rgb)
	win.blit(text,(px-fsiz/2,py-fsiz/2))


WIN_WIDTH,WIN_HEIGHT=1000,500
LEFTPRESSED,RIGHTPRESSED,UPPRESSED,DOWNPRESSED=False,False,False,False
mouseAtx,mouseAty,mouseClicked=0,0,True

BACKGROUND_IMAGE=pygame.transform.scale( pygame.image.load(
														   os.path.join("images","background.png")
														 ),
										 (WIN_WIDTH,WIN_HEIGHT)
									    ) 

NUM_HORI_CELLS,NUM_VERT_CELLS,CELL_SIZE,LINE_WIDTH=5,5,50,2
START_POINT=(0.2*WIN_WIDTH,0.2*WIN_HEIGHT)
time_var=0
boolean_array=[]
num_to_look_for=1
gameOver=False

def checkgame():
	global str2,gameOver
	flag=True
	for row in boolean_array:
		for elem in row:
			if not elem:
				flag=False
				break
	if flag:
		gameOver=True
		str2="GameOver, You took"+str(int(time_var))+" seconds"
	else:
		str2="Next to find:"+str(num_to_look_for)

def identify_click_point(pt):
	global num_to_look_for
	for i in range(NUM_VERT_CELLS):
		for j in range(NUM_HORI_CELLS):
			if(clicked_here(i,j,pt)):
				if nums_to_fill[i][j]==num_to_look_for:
					boolean_array[i][j]=True
					num_to_look_for+=1
				return (i,j)
	return (-1,-1)

def clicked_here(i,j,pt):
	left_wall=j*(CELL_SIZE+LINE_WIDTH)+START_POINT[0]
	right_wall=(j+1)*(CELL_SIZE+LINE_WIDTH)+START_POINT[0]
	top_wall=i*(CELL_SIZE+LINE_WIDTH)+START_POINT[1]
	bottom_wall=(i+1)*(CELL_SIZE+LINE_WIDTH)+START_POINT[1]
	if pt[0]>left_wall and pt[0]<right_wall and pt[1]>top_wall and pt[1]<bottom_wall:
		return True
	return False


def spread_list_across_grid(lis,start_point):
	for i,row in enumerate(lis):
		for j,col in enumerate(row):
			if boolean_array[i][j]:
				w2screen(str(lis[i][j]),j*(CELL_SIZE+LINE_WIDTH)+start_point[0]+CELL_SIZE/2,
					     i*(CELL_SIZE+LINE_WIDTH)+start_point[1]+CELL_SIZE/2,30,(0,255,0))
			else:							
				w2screen(str(lis[i][j]),j*(CELL_SIZE+LINE_WIDTH)+start_point[0]+CELL_SIZE/2,
					     i*(CELL_SIZE+LINE_WIDTH)+start_point[1]+CELL_SIZE/2,30)


def draw_grid(start_point):
	st_x,st_y=start_point[0],start_point[1]
	grid_ht=NUM_VERT_CELLS*(CELL_SIZE+LINE_WIDTH)+LINE_WIDTH
	grid_wd=NUM_HORI_CELLS*(CELL_SIZE+LINE_WIDTH)+LINE_WIDTH
	for i in range(NUM_HORI_CELLS+1):				
		pygame.draw.line(win, (255,0,0), (st_x,st_y), (st_x,st_y+grid_ht), LINE_WIDTH)
		st_x=st_x+(LINE_WIDTH+CELL_SIZE)
	st_x=start_point[0]
	for i in range(NUM_VERT_CELLS+1):				
		pygame.draw.line(win, (255,0,0), (st_x,st_y), (st_x+grid_wd,st_y), LINE_WIDTH)
		st_y=st_y+(LINE_WIDTH+CELL_SIZE)



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

def print2d(lis):
	for l_lis in lis:
		for elem in l_lis:
			print(elem,end=" ")
		print("\n")



#MAIN PROGRAM STARTS HERE
win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
clock= pygame.time.Clock()
run=True

#Infromation strings
str1=''
str2=''


nums_to_fill=[]
dummy_list=[]
for i in range(NUM_HORI_CELLS*NUM_VERT_CELLS):
	dummy_list.append(i+1)

for i in range(NUM_VERT_CELLS):
	x=[]
	y=[]
	for j in range(NUM_HORI_CELLS):
		selected_index=random.randint(0,len(dummy_list)-1)
		x.append(dummy_list[selected_index])
		y.append(False)
		dummy_list.pop(selected_index)
	nums_to_fill.append(x)
	boolean_array.append(y)


while run:	
	clock.tick(2)
	
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
			# str1='mouse pressed on:'+str(mousex)+','+str(mousey)
			ij=identify_click_point(event.pos)
			str1='mouse pressed on:'+str(ij[0])+','+str(ij[1])

		if event.type == MOUSEBUTTONUP:
			mousex,mousey = event.pos			
			mouseClicked = False

	draw_background(win)
	#ALL OBJECTS WILL WORK BELOW
	
	# pygame.draw.line(win, (255,0,0), (0.2*WIN_WIDTH,0.2*WIN_HEIGHT), (0.8*WIN_WIDTH,0.8*WIN_HEIGHT), 2)
	draw_grid(START_POINT)
	spread_list_across_grid(nums_to_fill,START_POINT)
	checkgame()

	w2screen(str1,30,30,40)
	w2screen(str2,WIN_WIDTH/2,60,40)

	if not gameOver:
		time_var+=0.5
	w2screen(str(int(time_var)),WIN_WIDTH/2,20,40,(255,0,255))


	#ALL OBJECTS WILL WORK ABOVE
	pygame.display.update()