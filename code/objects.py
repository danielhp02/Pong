import random

class Ball():

    def __init__(self, startX, startY, pygame, surface, radius):
        self.startPos = (startX, startY) # This is where the ball will return to after a point is scored
        self.x = startX
        self.y = startY

        # These are so the bats can interact with the game without pygame being
        # imported or this class having to be in the main file.
        self.pygame = pygame
        self.surface = surface

        self.radius = radius

        # Getting a random direction for the ball to start in
        self.dx = random.randint(-1, 1) * 3
        while self.dx == 0:
            self.dx = random.randint(-1, 1) * 3
        self.dy = random.randint(-3, 3)
        while self.dy == 0:
            self.dy = random.randint(-3, 3)

        self.colour = (255, 255, 255)

        self.score = [0,0]
        self.pauseTime = 500 # The amount of time (in milliseconds) that the ball stops for after a point is won
        self.scoredTime = 0  # The time when the last point was scored; used mainly externally for pausing just the ball

        self.scored = False

        # Secret!
        self.nggyu = self.pygame.mixer.Sound("../assets/nggyu.ogg")
        self.cej = self.pygame.mixer.Sound("../assets/cej.ogg")
        self.songs = [self.nggyu, self.cej]

    def playSong(self): # A suprise for a point is scored (sometimes)
        if random.random() < 0.2:
            random.choice(self.songs).play()

    # Reset the ball after a point is scored
    def resetBall(self):
        self.scored = True
        self.scoredTime = self.pygame.time.get_ticks() # Gets the time when a point was scored

        # Reset ball position
        self.x = self.startPos[0]
        self.y = self.startPos[1]

        # Getting a new random direction for the ball to begin in
        self.dx = random.randint(-1, 1) * 3
        while self.dx == 0:
            self.dx = random.randint(-1, 1) * 3
        self.dy = random.randint(-3, 3)
        while self.dy == 0:
            self.dy = random.randint(-3, 3)

    # Check for collisions with the bats and the edges of the window
    def checkForCollisions(self, windowWidth, windowHeight, leftBat, rightBat):
        # Check For collision with top and bottom boundaries
        if self.y - self.radius < 0 or self.y + self.radius > windowHeight:
            self.dy *= -1

        # Left side - awards point to right player
        if self.x - self.radius < 0:
            self.score[1] += 1
            self.resetBall()
            self.playSong()

        # Right side - awards point to left player
        elif self.x + self.radius > windowWidth:
            self.score[0] += 1
            self.resetBall()
            self.playSong()

        # Left Bat - Note for both bats: the collisions are only with the innermost side.
        if self.x - self.radius < leftBat.x + leftBat.width and leftBat.y < self.y < leftBat.y + leftBat.height:
            self.dx *= -1
            self.speedUp()

        # Right Bat
        if self.x + self.radius > rightBat.x and rightBat.y < self.y < rightBat.y + rightBat.height:
            self.dx *= -1
            self.speedUp()

    def move(self, windowWidth, windowHeight, leftBat, rightBat):
        self.checkForCollisions(windowWidth, windowHeight, leftBat, rightBat)
        self.x += self.dx
        self.y += self.dy

    def draw(self, drawAtStartPos):
        if drawAtStartPos:
            self.pygame.draw.circle(self.surface, self.colour, (self.startPos[0], self.startPos[1]), self.radius)
        else:
            self.pygame.draw.circle(self.surface, self.colour, (int(round(self.x)), int(round(self.y))), self.radius)
            self.scored = False

    # Speeds the ball up if the bat it is colliding with is moving during the collision
    def speedUp():
        if leftBat.isMoving or rightBat.isMoving:
            self.dx *= 1.1
            self.dy *= 1.1

class Bat(object):

    def __init__(self, x, startY, pygame, surface, width, height):
        self.x = x
        self.y = startY

        # These are so the bats can interact with the game without pygame being
        # imported or this class having to be in the main file.
        self.pygame = pygame
        self.surface = surface

        self.width = width
        self.height = height

        self.speed = 2.5 # The speed the bat will do either way
        self.dy = 0 # The speed the bat is currently doing
        self.isMoving = False # For the ball to speed up when it collides with a moving bat

        self.colour = (255, 255, 255)

    def move(self, up, down, bottomLimit):
        if up and self.y > 0:
            self.dy = -self.speed
            self.isMoving = True
        elif down and self.y + self.height < bottomLimit:
            self.dy = self.speed
            self.isMoving = True
        else:
            self.dy = 0
            self.isMoving = False

        self.y += self.dy

    def draw(self):
        self.pygame.draw.rect(self.surface, self.colour, (self.x, self.y, self.width, self.height))
