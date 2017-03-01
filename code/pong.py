import pygame, sys, os
import pygame.event as GAME_EVENTS
import pygame.time as GAME_TIME

import objects # This contains the classes necessary for the game

# Window dimensions and derived values
windowWidth = 800
windowHeight = 600
centreX = windowWidth/2
centreY = windowHeight/2

# Initialize Pygame and the mixer
pygame.init()
pygame.mixer.init()

# Initialize the surface for objects to be drawn on
surface = pygame.display.set_mode((windowWidth, windowHeight))

# Get a font for the score display set up
scoreFontFile = open(os.path.abspath("../assets/pong_score.ttf"), "r")
scoreFont = pygame.font.Font(scoreFontFile, 50)

# Set the title of the window
pygame.display.set_caption("Pong")

# A dictionary with the states of all the control keys (apart from esc) to allow
# continuous movement
controlsState = {"leftUp": False, "leftDown": False, "rightUp": False, "rightDown": False}

# Initialize the game objects
ball = objects.Ball(centreX, centreY, pygame, surface, 15)
leftBat = objects.Bat(10, centreY, pygame, surface, 15, 100)
rightBat = objects.Bat(windowWidth - 25, centreY, pygame, surface, 15, 100)

# Draw the net (dotted line) down the middle of the window
def drawNet():
    numberOfLines = 20
    width = 15
    height = windowHeight / (numberOfLines*2)

    i = height/2 # i is not initialized to 0 because it is offset to make the line a bit more centred

    while i < windowHeight:
        pygame.draw.line(surface, (127,127,127), (centreX, i), (centreX, i+height), width)
        i += 2*height

# Display the score for the users to see during the game
def drawScore():
    scoreColour = (127,127,127)

    p1Score = scoreFont.render(str(ball.score[0]), 1, scoreColour)
    p2Score = scoreFont.render(str(ball.score[1]), 1, scoreColour)

    thirdOfWindow = windowWidth//3
    surface.blit(p1Score, (centreX - 100 - scoreFont.size( str(ball.score[1]) )[0] // 2, 50))
    surface.blit(p2Score, (centreX + 100, 50)) # - scoreFont.size( str(ball.score[1]) )[0] // 2

# Quit and uninitialise the game
def quitGame():
    print(ball.score)
    scoreFontFile.close()
    pygame.quit()
    sys.exit()

# The main loop
while True:

    # Cover the previous frame in order to avoid smearing and make it appear as
    # if things were moving
    surface.fill((0, 0, 0))

    # Check for system and user events and act appropriately
    for event in GAME_EVENTS.get():

        if event.type == pygame.KEYDOWN:

            # Movement for player 1 or the left bat
            if event.key == pygame.K_w:
                controlsState["leftUp"] = True
                controlsState["leftDown"] = False
            if event.key == pygame.K_s:
                controlsState["leftDown"] = True
                controlsState["leftUp"] = False

            # Movement for player 2 or the right bat
            if event.key == pygame.K_UP:
                controlsState["rightUp"] = True
                controlsState["rightDown"] = False
            if event.key == pygame.K_DOWN:
                controlsState["rightDown"] = True
                controlsState["rightUp"] = False

            # Quit if the user hits the escape key
            if event.key == pygame.K_ESCAPE:
                quitGame()

        # Stop movement when a key is no longer being held down
        if event.type == pygame.KEYUP:

            if event.key == pygame.K_w:
                controlsState["leftUp"] = False
            if event.key == pygame.K_s:
                controlsState["leftDown"] = False

            if event.key == pygame.K_UP:
                controlsState["rightUp"] = False
            if event.key == pygame.K_DOWN:
                controlsState["rightDown"] = False

        # Quit if the user clicks the close button or closes it in any other way
        if event.type == pygame.QUIT:
            quitGame()

    # Draw the current score (for both players) and the net
    drawScore()
    drawNet()

    # Check if a point has been scored in the last ball.pauseTime ms. If so, the
    # ball is drawn at the starting position, otherwise it is moved then drawn accordingly.
    if ball.scored and GAME_TIME.get_ticks() - ball.scoredTime < ball.pauseTime:
        ball.draw(True) # Draw the ball at the starting position
    else:
        ball.move(windowWidth, windowHeight, leftBat, rightBat)
        ball.draw(False) # Draw the ball wherever it may be

    # Move and draw the bats/paddles/whatever you want to call them
    leftBat.move(controlsState["leftUp"], controlsState["leftDown"], windowHeight)
    leftBat.draw()

    rightBat.move(controlsState["rightUp"], controlsState["rightDown"], windowHeight)
    rightBat.draw()

    # Lock the fps to ~60 and update the display
    GAME_TIME.Clock().tick(60)
    pygame.display.update()
