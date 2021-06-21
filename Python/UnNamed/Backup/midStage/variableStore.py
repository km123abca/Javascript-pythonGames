global FRAME_RATE

global BACKGROUND_COLOR
global WIN_WIDTH,WIN_HEIGHT
global LEFTPRESSED,RIGHTPRESSED,UPPRESSED,DOWNPRESSED,SPACEPRESSED
global TPRESSED,HPRESSED,BPRESSED,FPRESSED
global IPRESSED,LPRESSED,MPRESSED,JPRESSED
global mouseAtx,mouseAty,mouseClicked,mousex,mousey
global soldiersList,pipesList,roadBlocks
global xscale,yscale

global camera


try: 
	mousex==0
except:
	mousex,mousey=0,0
	TPRESSED,HPRESSED,BPRESSED,FPRESSED=False,False,False,False
	IPRESSED,LPRESSED,MPRESSED,JPRESSED=False,False,False,False
	SPACEPRESSED=False


