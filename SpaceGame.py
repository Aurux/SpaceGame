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
pygame.display.set_caption('Space Game')

clock = pygame.time.Clock()

font_size = 60
pygame.freetype.init()
font = pygame.freetype.Font("Xolonium-Bold.ttf", font_size)

# Define sprite groups
all_sprites = pygame.sprite.Group()
proj_list = pygame.sprite.Group()
alien_list = pygame.sprite.Group()

# Load projectile sprites.
purpleLaser = pygame.image.load("art/purple_laser.png")

# Initialise player variables.
playerSprite = pygame.image.load("art/player.png")
playerSprite = pygame.transform.scale(playerSprite,(80,80))

# Funtion to render game stats
def Stats(score,wave,health,alien_health):
    font.render_to(gameDisplay, (12, 12), "Score: "+str(score), (0,0,0), None, size=30)
    font.render_to(gameDisplay, (12, 36), "Wave: "+str(wave), (0,0,0), None, size=30)
    font.render_to(gameDisplay, (45, 922), "Hull Integrity: "+str(health)+"%", (0,0,0), None, size=15)
    font.render_to(gameDisplay, (20, 880), "Psychon Strength: "+str("%.0f" % abs(alien_health))+"%", (0,0,0), None, size=15)

# The player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = playerSprite
        self.rect = self.image.get_rect()
        self.rect.bottom = resY - 20
        self.rect.centerx = resX * 0.625
        self.speed = 5
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.score = 0
        self.health = 100
        self.damage = 1
        
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
        proj_list.add(shot)
        all_sprites.add(shot)

player = Player()
all_sprites.add(player)

# Initialise aliens
smallAlien = pygame.image.load("art/smallAlien.png")
smallAlien = pygame.transform.scale(smallAlien,(40,40))
largeAlien = pygame.image.load("art/largeAlien.png")
lergeAlien = pygame.transform.scale(largeAlien,(80,40))
bossAlien = pygame.image.load("art/Boss.png")

# Enemy class for any NPCs
class Enemy(pygame.sprite.Sprite):
    def __init__(self,image,x,y,health):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        self.health = health
        self.speed = [random.randint(-5,5),random.randint(-5,5)]
    def update(self):
        self.rect = self.rect.move(self.speed)
        if self.rect.left < play_areaX + 50 or self.rect.right > resX - 50:
            self.speed[0] = -self.speed[0]
        if self.rect.top < 50 or self.rect.bottom > resY * 0.70:
            self.speed[1] = -self.speed[1]
        #if pygame.sprite.spritecollide(self,alien_list,False):
        #    self.speed[0] = -self.speed[0]
        #    self.speed[1] = -self.speed[1]
        if self.health <= 0:
            self.kill()
            if self.image == smallAlien:
                player.score += 5
            if self.image == largeAlien:
                player.score += 10
    def hit(self):
        self.kill()

def spawn_alien_wave(waveCount):
    # Spawns in varying amounts of aliens and varying sizes of aliens depending on which wave you're on.
    if waveCount < 5:
        for i in range(50+waveCount):
            alienX = resX * 0.625
            alienY = 70
            i = Enemy(smallAlien,alienX,alienY,10)
            alien_list.add(i)
            all_sprites.add(i)
    if waveCount % 5 == 0:
        for i in range(10+waveCount):
            alienX = random.randint(play_areaX+50, resX-50)
            alienY = random.randint(50, resY * 0.4)
            i = Enemy(smallAlien,alienX,alienY,10)
            alien_list.add(i)
            all_sprites.add(i)
        for i in range(waveCount):
            alienX = random.randint(play_areaX, resX)
            alienY = random.randint(0, resY * 0.4)
            i = Enemy(largeAlien,alienX,alienY,30)
            alien_list.add(i)
            all_sprites.add(i)
    
    return alien_list

# Projectile class
class Projectile(pygame.sprite.Sprite):
    def __init__(self,image,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = 10
    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

# Setup play area.
play_areaX = resX * 0.25
playBoundX = resX - 80
playBoundY = resY - 80
alienBoundX = resX - 50

# Define static rectangles
playRect = pygame.Rect(play_areaX, 0, resX, resY)
scoreRect = pygame.Rect(10, 10, play_areaX - 20, 50)
healthBarBase = pygame.Rect(10, 902, play_areaX - 20, resY * 0.05)

# Generate star coordinates
starXs = []
starYs = []
starCount = 200
for i in range(starCount):
    starXs.append(random.randint(play_areaX, resX))
    starYs.append(random.randint(0, resY))


waveCount = 1
waveHealth = []
alien_health = 0
total_alien_health = 0
alien_wave = spawn_alien_wave(waveCount)

#THE USER DOES SOMETHING TO START THE GAME.
gameRunning = True
startFlag = True
readyFlag = False
#THE GAME LOOP.
while gameRunning:
    #HANDLE EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRunning = False
        elif event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_SPACE:
                player.fire()
            if event.key == pygame.K_r:
                readyFlag = True

    
    # Draws play area
    gameDisplay.fill((56, 0 ,153))
    healthBarFill = pygame.Rect(10, 902, (play_areaX - 20)*((player.health)/100), resY * 0.05)

    # Draws HUD
    pygame.draw.rect(gameDisplay, (0,0,0), playRect)
    pygame.draw.rect(gameDisplay, (0,71,158), scoreRect)
    pygame.draw.rect(gameDisplay, (255,0,0), healthBarBase)
    pygame.draw.rect(gameDisplay, (0,255,0), healthBarFill)

    # Draws stars
    for i in range(starCount):
        pygame.draw.circle(gameDisplay, (255, 255, 255), (starXs[i], starYs[i]), 1, 1)
        starYs[i] += 3

        if starYs[i] > resY:
            starYs[i] = 10

    if startFlag: # Runs once at the start of every wave to store total wave health.
        startFlag = False
        total_alien_health = 0
        for alien in alien_list:
            total_alien_health += alien.health
        alien_health = total_alien_health

    all_sprites.update()
    
    # Check for collisions
    hits = pygame.sprite.groupcollide(proj_list,alien_list,False,False)
    for i in hits.values():
        for alien in i:
            print("HIT HIT HIT")
            alien.health -= player.damage
            alien_health -= player.damage
    
    # Monitor total health of alien wave.
    alien_health_percent = (alien_health / total_alien_health) * 100
        
    
    
    # Check how many enemies are alive. Go to next wave if all dead and player is ready.
    if len(alien_list) == 0:
        font.render_to(gameDisplay, (resX * 0.25 + 15, resY /2), "Wave "+str(waveCount)+" cleared! Press R to start next wave.", (255,255,255), None, size=28)
        player.rect.centerx = resX * 0.625
        player.rect.bottom = resY - 20
        if readyFlag:
            waveCount += 1
            startFlag = True
            readyFlag = False
            alien_wave = spawn_alien_wave(waveCount)
    
    all_sprites.draw(gameDisplay)
    
    Stats(player.score,waveCount,player.health,alien_health_percent)

    pygame.display.update()
    clock.tick(FPS)

#CLEAN UP WHEN FINISHED.
pygame.quit()
quit()