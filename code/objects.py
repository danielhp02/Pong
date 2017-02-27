import random

class Ball():

    def __init__(self, startX, startY, pygame, surface, radius):
        self.startPos = (startX, startY)
        self.x = startX
        self.y = startY
        self.pygame = pygame
        self.surface = surface
        self.radius = radius

        self.dx = random.randint(-1, 1) * 3
        while self.dx == 0:
            self.dx = random.randint(-1, 1) * 3
        self.dy = random.randint(-3, 3)
        while self.dy == 0:
            self.dy = random.randint(-3, 3)

        self.colour = (255, 255, 255)

        self.score = [0,0]
        self.pauseTime = 500 # The amount of time (in milliseconds) that the ball stops for after a point is won
        self.scoredTime = 0  # The time when the last point was scored

        self.scored = False

        self.nggyu = self.pygame.mixer.Sound("../assets/nggyu.ogg")
        self.cej = self.pygame.mixer.Sound("../assets/cej.ogg")
        self.songs = [self.nggyu, self.cej]

    def playSong(self):
        if random.random() < 0.2:
            random.choice(self.songs).play()

    def resetBall(self):
        self.scored = True
        self.scoredTime = self.pygame.time.get_ticks()
        self.x = self.startPos[0]
        self.y = self.startPos[1]

        self.dx = random.randint(-1, 1) * 3
        while self.dx == 0:
            self.dx = random.randint(-1, 1) * 3
        self.dy = random.randint(-3, 3)
        while self.dy == 0:
            self.dy = random.randint(-3, 3)

    def checkForCollisions(self, windowWidth, windowHeight, leftBat, rightBat):
        # Boundaries First
        if self.y - self.radius < 0 or self.y + self.radius > windowHeight:
            self.dy *= -1

        # Left side
        if self.x - self.radius < 0:
            self.score[1] += 1
            self.resetBall()
            self.playSong()
            return "left"

        # Right side
        elif self.x + self.radius > windowWidth:
            self.score[0] += 1
            self.resetBall()
            self.playSong()
            return "right"

        # Left Bat
        if self.x - self.radius < leftBat.x + leftBat.width and leftBat.y < self.y < leftBat.y + leftBat.height:
            self.dx *= -1

        # Right Bat
        if self.x + self.radius > rightBat.x and rightBat.y < self.y < rightBat.y + rightBat.height:
            self.dx *= -1

    def move(self, windowWidth, windowHeight, leftBat, rightBat):
        if not self.scored:
            self.checkForCollisions(windowWidth, windowHeight, leftBat, rightBat)
            self.x += self.dx
            self.y += self.dy

    def draw(self, drawAtStartPos):
        if drawAtStartPos:
            self.pygame.draw.circle(self.surface, self.colour, (self.startPos[0], self.startPos[1]), self.radius)
        else:
            self.pygame.draw.circle(self.surface, self.colour, (self.x, self.y), self.radius)
            self.scored = False

class Bat(object):

    def __init__(self, x, startY, pygame, surface, width, height):
        self.x = x
        self.y = startY
        self.pygame = pygame
        self.surface = surface

        self.width = width
        self.height = height

        self.speed = 2.5
        self.dy = 0

        self.colour = (255, 255, 255)

    def move(self, up, down, bottomLimit):
        if up and self.y > 0:
            self.dy = -self.speed
        elif down and self.y + self.height < bottomLimit:
            self.dy = self.speed
        else:
            self.dy = 0

        self.y += self.dy

    def draw(self):
        self.pygame.draw.rect(self.surface, self.colour, (self.x, self.y, self.width, self.height))
