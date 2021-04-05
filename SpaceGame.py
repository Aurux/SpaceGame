#SETUP
import pygame
import random
import time

pygame.init()
resY = 960
resX = 960
gameDisplay = pygame.display.set_mode((resX,resY))
clock = pygame.time.Clock()
pygame.display.set_caption('Space Game')

player = pygame.image.load("player.png")
player = pygame.transform.rotozoom(player, 90, 0.4)
xPos = resX * 0.45
yPos = resY * 0.70
playerSpeed = 5



play_areaX = resX * 0.25
playBoundX = resX - (player.get_width())
playBoundY = resY - (player.get_height())

playRect = pygame.Rect(play_areaX, 0, resX, resY)
scoreRect = pygame.Rect(10, 10, play_areaX - 20, resY * 0.2)

starXs = []
starYs = []
starCount = 200
for i in range(starCount):
    starXs.append(random.randint(play_areaX, resX))
    starYs.append(random.randint(0, resY))


waveCount = 1
    

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
        pass

    gameDisplay.fill((56, 0 ,153))

    pygame.draw.rect(gameDisplay, (0,0,0), playRect)
    pygame.draw.rect(gameDisplay, (0,71,158), scoreRect)

    for i in range(starCount):
        pygame.draw.circle(gameDisplay, (255, 255, 255), (starXs[i], starYs[i]), 1, 1)
        starYs[i] += 3

        if starYs[i] > resY:
            starYs[i] = 10

    gameDisplay.blit(player, (xPos, yPos))

    # Creates bounds for player to move within.
    if xPos <= play_areaX:
        xPos = play_areaX
    elif xPos >= playBoundX:
        xPos = playBoundX
    if yPos <= 0:
        yPos = 0
    elif yPos >= playBoundY:
        yPos = playBoundY
    
        
    pygame.display.update()
    clock.tick(144)

#CLEAN UP WHEN FINISHED.
pygame.quit()
quit()