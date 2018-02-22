# coding: utf-8
import random, time, pygame, sys
from pygame.locals import *

# 屏幕宽度640*480, 每个格长宽为20, 横向10格, 纵向20格
FPS = 25
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
BOXSIZE = 20
BOARDWIDTH = 10
BOARDHEIGHT = 20


# 游戏空间在屏幕中间靠下的位置
XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BOXSIZE) / 2)
TOPMARGIN = WINDOWHEIGHT - (BOARDHEIGHT * BOXSIZE) - 5  # 注意, topmargin高于boardheight

# 游戏中需要用的颜色设置
WHITE = (255, 255, 255)
GRAY = (185, 185, 185)
BLACK = (0,0,0)
RED = (155, 0, 0)
LIGHTRED = (175, 20, 20)
GREEN = (0, 155, 0)
LIGHTGREEN = (20, 175, 20)
BLUE = (0, 0, 155)
LIGHTBLUE = (20, 20, 175)
YELLOW = (155, 155, 0)
LIGHTYELLOW = (175, 175, 20)

BORDERCOLOR = BLUE
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY
COLORS = (BLUE, GREEN, RED, YELLOW)
LIGHTCOLORS = (LIGHTBLUE, LIGHTGREEN, LIGHTRED, LIGHTYELLOW)
assert len(COLORS) == len(LIGHTCOLORS)


BLANK = '.'  # board中的空白元素

TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5

S_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '..oo.',
                     '.oo..',
                     '.....'],
                    ['.....',
                     '..o..',
                     '..oo.',
                     '...o.',
                     '.....']]

Z_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.oo..',
                     '..oo.',
                     '.....'],
                    ['.....',
                     '..o..',
                     '.oo..',
                     '.o...',
                     '.....']]

I_SHAPE_TEMPLATE = [['..o..',
                     '..o..',
                     '..o..',
                     '..o..',
                     '.....'],
                    ['.....',
                     '.....',
                     'oooo.',
                     '.....',
                     '.....']]

O_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.oo..',
                     '.oo..',
                     '.....']]

J_SHAPE_TEMPLATE = [['.....',
                     '.o...',
                     '.ooo.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..oo.',
                     '..o..',
                     '..o..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.ooo.',
                     '...o.',
                     '.....'],
                    ['.....',
                     '..o..',
                     '..o..',
                     '.oo..',
                     '.....']]

L_SHAPE_TEMPLATE = [['.....',
                     '...o.',
                     '.ooo.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..o..',
                     '..o..',
                     '..oo.',
                     '.....'],
                    ['.....',
                     '.....',
                     '.ooo.',
                     '.o...',
                     '.....'],
                    ['.....',
                     '.oo..',
                     '..o..',
                     '..o..',
                     '.....']]

T_SHAPE_TEMPLATE = [['.....',
                     '..o..',
                     '.ooo.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..o..',
                     '..oo.',
                     '..o..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.ooo.',
                     '..o..',
                     '.....'],
                    ['.....',
                     '..o..',
                     '.oo..',
                     '..o..',
                     '.....']]

SHAPES = {'S': S_SHAPE_TEMPLATE,
          'Z': Z_SHAPE_TEMPLATE,
          'J': J_SHAPE_TEMPLATE,
          'L': L_SHAPE_TEMPLATE,
          'I': I_SHAPE_TEMPLATE,
          'O': O_SHAPE_TEMPLATE,
          'T': T_SHAPE_TEMPLATE}


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()

    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    # 游戏中用到的字体
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
    pygame.display.set_caption('Tetromino')


    while True:
        runGame()

def runGame():

    board = getBlankBoard()

    # board[3][3] = 1 # 测试drawboard


    # 测试getNewPiece

    piece = getNewPiece()
    piece['x'] = 3
    piece['y'] = 3


    while True:
        checkForQuit()


        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(board)
        drawPiece(piece)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)

def terminate():
    pygame.quit()
    sys.exit()

def getBlankBoard():
    board = []
    for i in range(BOARDWIDTH):
        board.append([BLANK] * BOARDHEIGHT)
    return board

def convertToPixelCoords(boxx, boxy):
    return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))

def drawBox(boxx, boxy,color, pixelx=None, pixely=None):
    # draw a single box at xy coordiates on the board. Or if pixelxy are
    # specified, draw to the pixel coordinates( used for the next piece)
    if color == BLANK:
        return
    if pixelx == None and pixely == None:
        pixelx, pixely = convertToPixelCoords(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, COLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 1, \
                                                  BOXSIZE - 1))
    pygame.draw.rect(DISPLAYSURF, LIGHTCOLORS[color],(pixelx + 1, pixely + 1, BOXSIZE - 4, \
                                                  BOXSIZE - 4))

def drawBoard(board):
    # draw the border around the board
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN - 3, TOPMARGIN - 7, \
                     (BOARDWIDTH * BOXSIZE) + 8, (BOARDHEIGHT * BOXSIZE) + 8), 5)

    pygame.draw.rect(DISPLAYSURF, BGCOLOR, (XMARGIN, TOPMARGIN, BOXSIZE * BOARDWIDTH, \
                                            BOXSIZE * BOARDHEIGHT))
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            drawBox(x, y, board[x][y])

def getNewPiece():
    shape = random.choice(list(SHAPES.keys()))
    newPiece = {'shape': shape,
                'rotation': random.randint(0, len(SHAPES[shape]) - 1),
                'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
                'y': -2,
                'color': random.randint(0, len(COLORS) -1)}
    return newPiece

def drawPiece(piece, pixelx=None, pixely=None):
    shapeToDraw = SHAPES[piece['shape']][piece['rotation']]

    if pixelx == None and pixely == None:
        pixelx, pixely = convertToPixelCoords(piece['x'], piece['y'])

    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if shapeToDraw[y][x] != BLANK:
                drawBox(None, None, piece['color'], pixelx + (x * BOXSIZE), \
                        pixely + (y * BOXSIZE))



if __name__ == '__main__':
    main()
