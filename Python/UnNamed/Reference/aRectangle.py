
import pygame, sys
from pygame.locals import *

def main():
    pygame.init()
    mousex,mousey=0,0
    DISPLAY=pygame.display.set_mode((400,400),0,32)     

    while True:
        DISPLAY.fill((0,0,0))

        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEMOTION:
                mousex,mousey=event.pos
        pygame.draw.rect(DISPLAY,(255,0,0),(200,200,100,50))
        w2screen(DISPLAY,str(round(mousex))+','+str(round(mousey)))
        pygame.display.update()

def w2screen(win,txt):
    pyfont=pygame.font.SysFont("comicsans",24)
    text=pyfont.render(txt,1,(255,255,255))
    win.blit(text,(20,20))

main()