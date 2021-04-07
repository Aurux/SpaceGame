#SETUP
import pygame
import random
import time
import math
import pygame.freetype


pygame.init()
resY = 960
resX = 960
FPS = 60
gameDisplay = pygame.display.set_mode((resX,resY))
clock = pygame.time.Clock()
pygame.display.set_caption('Space Game')
all_sprites = pygame.sprite.Group()
proj_list = pygame.sprite.Group()
# Load projectile sprites.
purpleLaser = pygame.image.load("art/purple_laser.png")
xPos = resX * 0.45
yPos = resY * 0.70
# Initialise player variables.
playerSprite = pygame.image.load("art/player.png")
playerSprite = pygame.transform.scale(playerSprite,(80,80))
playerScore = 0
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = playerSprite
        self.rect = self.image.get_rect()
        self.rect.bottom = resY - 20
        self.rect.left = resX * 0.45
        self.speed = 5
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
    def update(self):
        # Takes key input to move player around with bounding condtions to keep player within play area.
        keys = pygame.key.get_pressed()
        if keys[ord('a')]:
            self.rect.x -= self.speed
        if keys[ord('d')]:
            self.rect.x += self.speed
        if keys[ord('w')]:
            self.rect.y -= self.speed
        if keys[ord('s')]:
            self.rect.y += self.speed
        if self.rect.left <= play_areaX:
            self.rect.left = play_areaX
        elif self.rect.right >= resX:
            self.rect.right = resX
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= resY:
            self.rect.bottom = resY
    def fire(self):
        shot = Projectile(purpleLaser,self.rect.centerx,self.rect.top)
        print("FIRE")
        proj_list.add(shot)
        all_sprites.add(shot)

player = Player()
all_sprites.add(player)

# Initialise aliens
smallAlien = pygame.image.load("art/smallAlien.png")
smallAlien = pygame.transform.scale(smallAlien,(60,60))
largeAlien = pygame.image.load("art/largeAlien.png")
bossAlien = pygame.image.load("art/Boss.png")


class Enemy(pygame.sprite.Sprite):
    def __init__(self,image,x,y,health):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = health
        self.speed = [random.randint(-5,5),random.randint(-5,5)]
    def update(self):
        self.rect = self.rect.move(self.speed)
        if self.rect.left < play_areaX or self.rect.right > resX:
            self.speed[0] = -self.speed[0]
        if self.rect.top < 0 or self.rect.bottom > resY * 0.70:
            self.speed[1] = -self.speed[1]
        #if pygame.sprite.spritecollide(self,alien_list,False):
        #    self.speed[0] = -self.speed[0]
        #    self.speed[1] = -self.speed[1]

    def keepApart(self, otherEntity):
        if self.rect.colliderect(otherEntity):
            self.rect.x -= 10

alien_list = pygame.sprite.Group()
def spawn_alien_wave(waveCount):
    # Spawns in varying amounts of enemies and varying sizes of enemies depending on which wave you're on.
    
    if waveCount < 5:
        for i in range(50+waveCount):
            alienX = resX * 0.67
            alienY = 70
            i = Enemy(smallAlien,alienX,alienY,1)
            alien_list.add(i)
            all_sprites.add(i)
    if waveCount % 5 == 0:
        for i in range(10+waveCount):
            alienX = random.randint(play_areaX, resX)
            alienY = random.randint(0, resY * 0.4)
            i = Enemy(smallAlien,alienX,alienY,1)
            alien_list.add(i)
            all_sprites.add(i)
        for i in range(waveCount):
            alienX = random.randint(play_areaX, resX)
            alienY = random.randint(0, resY * 0.4)
            i = Enemy(largeAlien,alienX,alienY,5)
            alien_list.add(i)
            all_sprites.add(i)
    
    return alien_list

class Projectile(pygame.sprite.Sprite):
    def __init__(self,image,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = 5
    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()



def DetectCollision(targetX, targetY, projectileX, projectileY):
    distance = math.sqrt(math.pow((targetX - projectileX),2) + math.pow((targetY - projectileY),2))
    print(distance)
    if distance < 300:
        return True
    return False
# Setup play area.
play_areaX = resX * 0.25
playBoundX = resX - 80
playBoundY = resY - 80
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
alien_wave = spawn_alien_wave(waveCount)

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
            if event.key == pygame.K_SPACE:
                player.fire()

    
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

    # Spawns in player and enemies
    '''
    for alien in alien_list:
        alien.draw(gameDisplay)
        alien.y += random.randint(-5,5)
        alien.x += random.randint(-5,5)
        if alien.x <= play_areaX:
            alien.x = play_areaX
        elif alien.x >= alienBoundX:
            alien.x = alienBoundX
        if alien.y <= 0:
            alien.y = 0
        elif alien.y >= resY / 2:
            alien.y = resY / 2
    '''
    
    
    all_sprites.update()
    
    # Check for collisions
    hits = pygame.sprite.groupcollide(proj_list,alien_list,True,True)
    if hits:
        playerScore += 1

    # Check how many enemies are alive. Go to next wave if all dead.
    if len(alien_list) == 0:
        waveCount += 1
        alien_wave = spawn_alien_wave(waveCount)
    
    all_sprites.draw(gameDisplay)
    print(playerScore)
    pygame.display.update()
    clock.tick(FPS)

#CLEAN UP WHEN FINISHED.
pygame.quit()
quit()