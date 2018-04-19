import pygame,sys,time
import random
from pygame.locals import *

BOARDWIDTH = 4
BOARDHEIGHT = 4
FPS = 20
TILESIZE = 150
WINDOWWIDTH = 1200
WINDOWHEIGHT = 1000
GAPSIZE = 4
XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH-1)))/2)
YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDWIDTH + (BOARDWIDTH-1)))/2)
TIMEOUT = 4

CROCODILLE = pygame.image.load('data/1.gif')
FROG = pygame.image.load('data/2.gif')
FOX = pygame.image.load('data/3.gif')
CACTUS = pygame.image.load('data/4.gif')
JARDIAN = pygame.image.load('data/5.gif')
BUTTERFLY = pygame.image.load('data/6.gif')
PIG = pygame.image.load('data/7.gif')
MONSTER = pygame.image.load('data/8.gif')
CHICKEN = pygame.image.load('data/9.gif')
DINO = pygame.image.load('data/10.gif')
HUMAN = pygame.image.load('data/11.gif')
CRAB = pygame.image.load('data/12.gif')
BEAR = pygame.image.load('data/13.gif')
DROPY = pygame.image.load('data/14.gif')
LION = pygame.image.load('data/15.gif')
GHOST = pygame.image.load('data/16.gif')
#BACKGROUND = pygame.image.load('data/tv.gif')



WHITE    = (255, 255, 255)
BLACK = (0,0,0)
MAGENTA = (255,0,255)
ORCHID = (127,0,255)
GREY = (192,192,192)
GREEN = (0,255,0)
BRIGHTYELLOW = (255, 255,0)


ALLIMAGES = (CROCODILLE,FROG,FOX,CACTUS,JARDIAN,BUTTERFLY,PIG,MONSTER,CHICKEN,DINO,HUMAN,CRAB,BEAR,DROPY,LION,GHOST)
    
def main():
    global DISPLAYSURF,FPSCLOCK,num_of_item,BEEP1,BEEP2,BEEP3,BEEP4,OVER
    pygame.init()
    num_of_item = 1
    waitforinput = False
    pattern = []
    currentStep = 0
    lastclicktime = 0
    level = 1;

    BASICFONT = pygame.font.Font('freesansbold.ttf', 20)
    BEEP1 = pygame.mixer.Sound('data/beep1.ogg')
    BEEP2 = pygame.mixer.Sound('data/beep2.ogg')
    BEEP3 = pygame.mixer.Sound('data/beep3.ogg')
    BEEP4 = pygame.mixer.Sound('data/beep4.ogg')
    BEGIN = pygame.mixer.Sound('data/begin.ogg')
    OVER = pygame.mixer.Sound('data/end.ogg')

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    pygame.display.set_caption('MemoryGame')
    pygame.display.toggle_fullscreen()
    BEGIN.play()
    while True:
        clickedBox = None
        DISPLAYSURF.fill(BRIGHTYELLOW)
        mainboard = getBoard()
        drawBoard(mainboard)
        infoSurf = BASICFONT.render('Match The Pattern',1,BLACK)
        infoRect = infoSurf.get_rect()
        infoRect.topleft = (300,830)
        scoreSurf = BASICFONT.render('Level '+ str(level),1,BLACK)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (300,850)
        DISPLAYSURF.blit(infoSurf,infoRect)
        DISPLAYSURF.blit(scoreSurf,scoreRect)
        checkForQuit()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                    #pygame.display.toggle_fullscreen()
            elif event.type == MOUSEBUTTONUP:
                mousex,mousey = event.pos
                clickedBox = getBoxAtPixel(mousex,mousey)

        if not waitforinput:
            pygame.display.update()
            pygame.time.wait(1000)
            pattern = reset()
            for box in pattern:
                flashButtonAnimation(box)
            waitforinput = True
        else:
            if clickedBox and clickedBox == pattern[currentStep]:
                flashButtonAnimation(clickedBox)
                currentStep += 1
                lastclicktime = time.time()
                if currentStep == len(pattern):
                    currentStep = 0
                    level += 1
                    waitforinput = False
            elif (clickedBox and clickedBox != pattern[currentStep]) or (currentStep!=0 and time.time() - TIMEOUT > lastclicktime):
                OVER.play()
                pygame.time.wait(2000) 
                pattern = []
                currentStep = 0
                level = 1
                waitforinput = False
                terminate() 


        pygame.display.update()
        FPSCLOCK.tick(FPS)
	
def terminate():
    pygame.quit()
    sys.exit()

def checkForQuit():
    for event in pygame.event.get(QUIT):
         terminate()

def leftTopCord(boxx,boxy):
    left = boxx*(TILESIZE+GAPSIZE) + XMARGIN
    top = boxy*(TILESIZE+GAPSIZE) + YMARGIN
    return (left,top)

def drawTile(image,x,y):
    DISPLAYSURF.blit(image,(x,y))

def reset():
    global num_of_item
    pattern = []
    num_of_item = num_of_item +1
    for i in range(num_of_item):
            x = random.choice((0,1,2,3))
            y = random.choice((0,1,2,3))
            pattern.append((x,y))
    return pattern

def getBoard():
    icon = []
    for image in ALLIMAGES:
        icon.append(image)
    board = []
    for x in range(BOARDWIDTH):
        colummn = []
        for y in range(BOARDHEIGHT):
            colummn.append(icon[0])
            del icon[0]
    	board.append(colummn)
    return board

def drawBoard(board):
	for boxx in range(BOARDWIDTH):
		for boxy in range(BOARDHEIGHT):
			left,top = leftTopCord(boxx,boxy)
			pygame.draw.rect(DISPLAYSURF,WHITE,(left,top,TILESIZE,TILESIZE))
			image = board[boxx][boxy]
			drawTile(image,left,top)

def getBoxAtPixel(x,y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left,top = leftTopCord(boxx,boxy)
            boxRect = pygame.Rect(left,top,TILESIZE,TILESIZE)
            if boxRect.collidepoint(x,y):
                 return (boxx,boxy)
    return (None,None)

def flashButtonAnimation(button,animationspeed = 20):
    flashColor = WHITE
    if button[0] == 0:
            sound = BEEP1
    elif button[0] == 1:
            sound = BEEP2
    elif button[0] == 2:
            sound = BEEP3
    elif button[0] == 3:
            sound = BEEP4
    left,top = leftTopCord(*button)
    orig = DISPLAYSURF.copy()
    flashSurf = pygame.Surface((TILESIZE,TILESIZE))
    flashSurf.convert_alpha()
    r,g,b = flashColor
    sound.play()
    for start,end,step in ((0,255,1),(255,0,-1)):
        for alpha in range(start,end,animationspeed*step):
            checkForQuit()
            DISPLAYSURF.blit(orig,(0,0))
            flashSurf.fill((r,g,b,alpha))
            DISPLAYSURF.blit(flashSurf,(left,top))
            pygame.display.update()
            FPSCLOCK.tick(animationspeed)

    DISPLAYSURF.blit(orig,(0,0))

if __name__ == '__main__':
    main()

