import pygame, sys, os
import pygame.event as GAME_EVENTS
import pygame.time as GAME_TIME

import objects

windowWidth = 800
windowHeight = 600

pygame.init()
surface = pygame.display.set_mode((windowWidth, windowHeight))
scoreFontFile = open(os.path.abspath("../assets/pong_score.ttf"), "r")
scoreFont = pygame.font.Font(scoreFontFile, 50)

pygame.display.set_caption("Pong")

controlsState = {"leftUp": False, "leftDown": False, "rightUp": False, "rightDown": False}

ball = objects.Ball(windowWidth/2, windowHeight/2, pygame, surface, 15)
leftBat = objects.Bat(10, windowHeight/2, pygame, surface, 15, 100)
rightBat = objects.Bat(windowWidth - 25, windowHeight/2, pygame, surface, 15, 100)

def drawScore():
    scoreColour = (127,127,127)
    
    p1Score = scoreFont.render(str(ball.score[0]), 1, scoreColour)
    p2Score = scoreFont.render(str(ball.score[1]), 1, scoreColour)

    thirdOfWindow = windowWidth/3
    surface.blit(p1Score, (300 - scoreFont.size(str(ball.score[0]))[0]/2, 50)) # If uncentred try this after thirdOfWindow, without "": ""
    surface.blit(p2Score, (500 - scoreFont.size(str(ball.score[1]))[0]/2, 50)) # ""
    
def quitGame():
    print(ball.score)
    scoreFontFile.close()
    pygame.quit()
    sys.exit()

while True:

    surface.fill((0, 0, 0))

    for event in GAME_EVENTS.get():

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_w:
                controlsState["leftUp"] = True
                controlsState["leftDown"] = False
            if event.key == pygame.K_s:
                controlsState["leftDown"] = True
                controlsState["leftUp"] = False

            if event.key == pygame.K_UP:
                controlsState["rightUp"] = True
                controlsState["rightDown"] = False
            if event.key == pygame.K_DOWN:
                controlsState["rightDown"] = True
                controlsState["rightUp"] = False

            if event.key == pygame.K_ESCAPE:
                quitGame()

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_w:
                controlsState["leftUp"] = False
            if event.key == pygame.K_s:
                controlsState["leftDown"] = False
                
            if event.key == pygame.K_UP:
                controlsState["rightUp"] = False
            if event.key == pygame.K_DOWN:
                controlsState["rightDown"] = False

        if event.type == pygame.QUIT:
            quitGame()

    drawScore()

    ball.move(windowWidth, windowHeight, leftBat, rightBat)
    if ball.scored and GAME_TIME.get_ticks() - ball.scoredTime < ball.pauseTime:
        ball.draw(True)
    else:
        ball.draw(False)

    leftBat.move(controlsState["leftUp"], controlsState["leftDown"], windowHeight)
    leftBat.draw()

    rightBat.move(controlsState["rightUp"], controlsState["rightDown"], windowHeight)
    rightBat.draw()

    GAME_TIME.Clock().tick(60)
    pygame.display.update()