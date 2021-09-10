import pygame
import sys
import time
from copy import copy, deepcopy
pygame.init()

#screen settings
title = "Game Of Life by Daaninator"
(width, height) = (1920, 1020)
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption(title)
programIcon = pygame.image.load('planet-earth.png')
pygame.display.set_icon(programIcon)
rulesBool = False

#time/fps settings
prev_time = time.time()
target_fps = 20
fps = target_fps

#image
pauseImg = pygame.image.load("pause.png")
countLife = 0

#font
fpsFontSize = 60
PauseFontSize = 200
smallFontSize = 20
rulesFontSize = 40
font = pygame.font.Font(None, fpsFontSize)
pauseFont = pygame.font.Font(None, PauseFontSize)
smallfont = pygame.font.SysFont(None, smallFontSize)
rulesFont = pygame.font.SysFont(None, rulesFontSize)
#colors
color_dark = (100, 100, 100)
color_light = (170, 170, 170)
color_white = (220, 230, 240)
color_black = (0, 0, 0)
color_text = (200, 210, 220)

#pause button
mouse = (500, 500)
pauseWidth = 200
pauseHeight = 80

#game Loop
gameLoopStop = False

#reset grid
def resetGrid():
    blockArray = [[False] * (width // blockSize + extraBlocks)]
    for i in range(height // blockSize + extraBlocks):
        blockArray.append([False] * (width // blockSize + extraBlocks))
    return blockArray

#block settings
blockSize = 20
extraBlocks = 32
blockArray = resetGrid()

#draws grid
def drawGrid():
    count = 0
    for y in range(len(blockArray)):
        for x in range(len(blockArray[0])):
            #print(f"{x} and {y}")
            rect = pygame.Rect((x - extraBlocks/2)*blockSize, (y - extraBlocks/2)*blockSize, blockSize, blockSize)
            if blockArray[y][x]:
                pygame.draw.rect(screen, color_white, rect, 0)
                count += 1
            else:
                pygame.draw.rect(screen, (20,20,20), rect, 1)
    return count

#will (un)check block
def gridClickCheck(down):
    for y in range(len(blockArray)):
        for x in range(len(blockArray[0])):
            if ((x - extraBlocks/2)*blockSize <= mouse[0] < (x - extraBlocks/2)*blockSize + blockSize and (y - extraBlocks/2)*blockSize <= mouse[1] < (y - extraBlocks/2)*blockSize + blockSize):
                if down:
                    blockArray[y][x] = True
                else:
                    blockArray[y][x] = False
#checks rules of new life
def newLifeCheck(blockArray):
    blockArrayCopy = deepcopy(blockArray)
    for y in range(1, len(blockArray)-1):
        for x in range(1, len(blockArray[0])-1):
            count = 0
            if blockArray[y-1][x-1]:
                count += 1
            if blockArray[y-1][x]:
                count += 1
            if blockArray[y-1][x+1]:
                count += 1
            if blockArray[y][x-1]:
                count += 1
            if blockArray[y][x+1]:
                count += 1
            if blockArray[y+1][x]:
                count += 1
            if blockArray[y+1][x+1]:
                count += 1
            if blockArray[y+1][x-1]:
                count += 1

            #rules
            if (count < 2 and blockArray[y][x]):
                blockArrayCopy[y][x] = False
            elif (count>3 and blockArray[y][x]):
                blockArrayCopy[y][x] = False
            elif (count == 3 and not blockArray[y][x]):
                blockArrayCopy[y][x] = True
    return blockArrayCopy

while True:
    if (pygame.mouse.get_pos() != None):
        mouse = pygame.mouse.get_pos()

    pygame.display.update()
    #handles the events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                gameLoopStop = not gameLoopStop
            if event.key == pygame.K_r:
                rulesBool = not rulesBool
        # checks if a mouse is clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            # if the mouse is clicked on the button than the game pauses
            if width / 2 - pauseWidth/2 <= mouse[0] <= width / 2 + pauseWidth/2 and height - pauseHeight <= mouse[1] <= height:
                gameLoopStop = not gameLoopStop

            if (event.button == 4):
                target_fps = min(100, target_fps + 2)
            if (event.button == 5):
                target_fps = max(2, target_fps - 2)
        #quits game when pressed on quit
        if event.type == pygame.QUIT:
            sys.exit()
        #resizes window
        if event.type == pygame.VIDEORESIZE:
            # There's some code to add back window content here.
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            (width, height) = (screen.get_width(), screen.get_height())

    #if you click on a block it will turn the oposite color. right click will delete, left click will add, middle click will reset
    if pygame.mouse.get_pressed()[0]:
        gridClickCheck(True)
    elif pygame.mouse.get_pressed()[2]:
        gridClickCheck(False)
    elif pygame.mouse.get_pressed()[1]:
        blockArray = resetGrid()

    #screen background color
    screen.fill((0,0,0))
    #draws grid
    countLife = drawGrid()
    #pauze button
    pygame.draw.rect(screen, color_text, [width / 2 - pauseWidth/2, height - pauseHeight, pauseWidth, pauseHeight])
    screen.blit(pauseImg, (width / 2 - 32, height - pauseHeight/2 - 32))

    #help text right bottom
    text = smallfont.render("wheel to change speed", True, color_text)
    screen.blit(text, (10, height - smallFontSize))
    text = smallfont.render("middle click to reset", True, color_text)
    screen.blit(text, (10, height - smallFontSize * 2))
    text = smallfont.render("space to pause", True, color_text)
    screen.blit(text, (10, height - smallFontSize * 3))
    text = smallfont.render("left click to create", True, color_text)
    screen.blit(text, (10, height - smallFontSize * 4))
    text = smallfont.render("right click to delete", True, color_text)
    screen.blit(text, (10, height - smallFontSize * 5))
    text = smallfont.render("R for rules", True, color_text)
    screen.blit(text, (10, height - smallFontSize * 6))

    #wills how rules if pressed on r
    if rulesBool:
        text = rulesFont.render("Game of life rules:", True, color_white)
        screen.blit(text, (width / 2 - text.get_width() / 2, height/2-height/5))
        text = rulesFont.render("1. Any live cell with two or three live neighbours survives.", True, color_white)
        screen.blit(text, (width / 2 - text.get_width() / 2, height/2-height/6 + text.get_height()))
        text = rulesFont.render("2. Any dead cell with three live neighbours becomes a live cell.", True, color_white)
        screen.blit(text, (width / 2 - text.get_width() / 2, height/2-height/6 + text.get_height()*2))
        text = rulesFont.render("4. All other live cells die in the next generation.", True, color_white)
        screen.blit(text, (width / 2 - text.get_width() / 2, height/2-height/6 + text.get_height()*3))

    #game is on pause
    if gameLoopStop:
        text = pauseFont.render("PAUSED", True, color_text)
        screen.blit(text, (width/2 - text.get_width()/2, 10))
        text = smallfont.render("LIFE COUNT: " + str(countLife), True, color_text)
        screen.blit(text, (width / 2 - text.get_width() / 2, 135))
        pygame.display.update()
        continue

    #checks for rules of game of life
    blockArray = newLifeCheck(blockArray)

    #text
    text = font.render("SPEED: " + str(fps), True, color_text)
    screen.blit(text, (width/2-text.get_width()/2, 10))
    text = smallfont.render("LIFE COUNT: " + str(countLife), True, color_text)
    screen.blit(text, (width / 2 - text.get_width() / 2, 55))

    #updates display
    pygame.display.update()

    #Timing code at the END!
    curr_time = time.time()#so now we have time after processing
    diff = curr_time - prev_time#frame took this much time to process and render
    delay = max(1.0/target_fps - diff, 0)#if we finished early, wait the remaining time to desired fps, else wait 0 ms!
    time.sleep(delay)
    fps = round(1.0/(delay + diff))#fps is based on total time ("processing" diff time + "wasted" delay time)
    prev_time = curr_time