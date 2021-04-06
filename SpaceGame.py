#SETUP
import pygame
import random
import time
import pygame.freetype


pygame.init()
resY = 960
resX = 960
gameDisplay = pygame.display.set_mode((resX,resY))
clock = pygame.time.Clock()
pygame.display.set_caption('Space Game')

# Load projectile sprites.
purpleLaser = pygame.image.load("art/purple_laser.png")

# Initialise player variables.
player = pygame.image.load("art/player.png")
player = pygame.transform.rotozoom(player, 90, 0.4)
xPos = resX * 0.45
yPos = resY * 0.70
playerSpeed = 5
playerScore = 0
def Player():
    gameDisplay.blit(player, (xPos, yPos))

# Initialise aliens
smallAlien = pygame.image.load("art/smallAlien.png")
largeAlien = pygame.image.load("art/largeAlien.png")
bossAlien = pygame.image.load("art/Boss.png")


class Enemy(pygame.sprite.Sprite):
    def __init__(self,image,x,y,health):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.x = x
        self.y = y
        self.health = health
        self.rect = self.image.get_rect()
    def draw(self, gameDisplay):
        gameDisplay.blit(self.image, (self.x,self.y))

def spawn_alien_wave(waveCount):
    # Spawns in varying amounts of enemies and varying sizes of enemies depending on which wave you're on.
    alien_list = []
    if waveCount < 5:
        for i in range(10+waveCount):
            alienX = random.randint(play_areaX, resX)
            alienY = random.randint(0, resY * 0.4)
            i = Enemy(smallAlien,alienX,alienY,1)
            alien_list.append(i)
    if waveCount % 5 == 0:
        for i in range(10+waveCount):
            alienX = random.randint(play_areaX, resX)
            alienY = random.randint(0, resY * 0.4)
            i = Enemy(smallAlien,alienX,alienY,1)
            alien_list.append(i)
        for i in range(waveCount):
            alienX = random.randint(play_areaX, resX)
            alienY = random.randint(0, resY * 0.4)
            i = Enemy(largeAlien,alienX,alienY,5)
            alien_list.append(i)
    
    return alien_list

class Projectile(pygame.sprite.Sprite):
    def __init__(self,image,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
    def draw(self, gameDisplay):
        gameDisplay.blit(self.image, (self.x,self.y))

player_proj_list = []
def PlayerShoot():
    if len(player_proj_list) < 25:
        shot = Projectile(purpleLaser,xPos,yPos)
        player_proj_list.append(shot)
    return player_proj_list


# Setup play area.
play_areaX = resX * 0.25
playBoundX = resX - (player.get_width())
playBoundY = resY - (player.get_height())
alienBoundX = resX - 50

playRect = pygame.Rect(play_areaX, 0, resX, resY)
scoreRect = pygame.Rect(10, 10, play_areaX - 20, resY * 0.2)
healthBar = pygame.Rect(10, 902, play_areaX - 20, resY * 0.05)

starXs = []
starYs = []
starCount = 200
for i in range(starCount):
    starXs.append(random.randint(play_areaX, resX))
    starYs.append(random.randint(0, resY))


waveCount = 1
waveList = spawn_alien_wave(waveCount)

#THE USER DOES SOMETHING TO START THE GAME.
gameRunning = True
frameNum = 0

#THE GAME LOOP.
while gameRunning:
    #HANDLE EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRunning = False
        elif event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_q:
                gameRunning = False
    # Check for key presses.
    keys = pygame.key.get_pressed()
    if keys[ord('a')]:
        xPos -= playerSpeed
    if keys[ord('d')]:
        xPos += playerSpeed
    if keys[ord('w')]:
        yPos -= playerSpeed
    if keys[ord('s')]:
        yPos += playerSpeed
    if keys[ord(' ')]:
        PlayerShoot()
    
    # Draws play area
    gameDisplay.fill((56, 0 ,153))

    pygame.draw.rect(gameDisplay, (0,0,0), playRect)
    pygame.draw.rect(gameDisplay, (0,71,158), scoreRect)
    pygame.draw.rect(gameDisplay, (255,0,0), healthBar)

    for i in range(starCount):
        pygame.draw.circle(gameDisplay, (255, 255, 255), (starXs[i], starYs[i]), 1, 1)
        starYs[i] += 3

        if starYs[i] > resY:
            starYs[i] = 10

    
    # Creates bounds for player to move within.
    if xPos <= play_areaX:
        xPos = play_areaX
    elif xPos >= playBoundX:
        xPos = playBoundX
    if yPos <= 0:
        yPos = 0
    elif yPos >= playBoundY:
        yPos = playBoundY
    
    # Spawns in player and enemies
    Player()

    for alien in waveList:
        alien.draw(gameDisplay)
        alien.y += 0.5
        alien.x += random.randint(-5,5)
        if alien.x <= play_areaX:
            alien.x = play_areaX
        elif alien.x >= alienBoundX:
            alien.x = alienBoundX

    for projectile in player_proj_list:
        projectile.draw(gameDisplay)
        projectile.y -= 5
        if projectile.y < -5:
            player_proj_list.remove(projectile)
    
    
    pygame.display.update()
    clock.tick(60)

#CLEAN UP WHEN FINISHED.
pygame.quit()
quit()