global FRAME_RATE

global BACKGROUND_COLOR
global WIN_WIDTH,WIN_HEIGHT
global LEFTPRESSED,RIGHTPRESSED,UPPRESSED,DOWNPRESSED,SPACEPRESSED
global TPRESSED,HPRESSED,BPRESSED,FPRESSED
global IPRESSED,LPRESSED,MPRESSED,JPRESSED
global mouseAtx,mouseAty,mouseClicked,mousex,mousey
global soldiersList,pipesList,roadBlocks,cloudsList,hazesList,doorTriggersList,gatesList,beetlesList,enemiesList
global xscale,yscale
global startScreenDisplayed
global musicStarted
global shootingSound,fogGateSound
global pChanger
global camera
global gameManager

try: 
	mousex==0
except:
	mousex,mousey=0,0
	TPRESSED,HPRESSED,BPRESSED,FPRESSED=False,False,False,False
	IPRESSED,LPRESSED,MPRESSED,JPRESSED=False,False,False,False
	SPACEPRESSED=False
	cloudsList,hazesList,doorTriggersList,gatesList,beetlesList,enemiesList=[],[],[],[],[],[]
	startScreenDisplayed=False
	musicStarted=False
	gameManager=None


