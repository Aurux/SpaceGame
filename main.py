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
pygame.display.set_caption('The Psychon Assault')

clock = pygame.time.Clock()

font_size = 60
pygame.freetype.init()
font = pygame.freetype.Font("Xolonium-Bold.ttf", font_size)

# Define sprite groups
all_sprites = pygame.sprite.Group()
playerGroup = pygame.sprite.Group()
proj_list = pygame.sprite.Group()
alien_list = pygame.sprite.Group()
alien_proj_list = pygame.sprite.Group()

# Load projectile sprites.
purpleLaser = pygame.image.load("art/purple_laser.png")
redLaser = pygame.image.load("art/red_laser.png")
redLaser = pygame.transform.rotate(redLaser,180)

# Initialise player variables.
playerSprite = pygame.image.load("art/player.png")
playerSprite = pygame.transform.scale(playerSprite,(80,80))

# Funtion to render game stats
def Stats(score,wave,health,alien_health):
    font.render_to(gameDisplay, (12, 12), "Score: "+str(score), (0,0,0), None, size=30)
    font.render_to(gameDisplay, (12, 36), "Wave: "+str(wave), (0,0,0), None, size=30)
    font.render_to(gameDisplay, (45, 922), "Hull Integrity: "+str(health)+"%", (0,0,0), None, size=15)
    font.render_to(gameDisplay, (18, 90), "Psychon Strength: "+str("%.0f" % abs(alien_health))+"%", (0,0,0), None, size=15)

def ProjectileTranslate(oldPos,speed,angle):
    angle = math.degrees(angle)
    newX = oldPos[0] + (speed*math.sin(angle))
    newY = oldPos[1] + (speed*math.cos(angle))
    return newX, newY
# The player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = playerSprite
        self.image_init = playerSprite
        self.rect = self.image.get_rect()
        self.rect.bottom = resY - 20
        self.rect.centerx = resX * 0.625
        self.speed = 5
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.score = 0
        self.health = 100
        self.damage = 1
        self.angle = 0
        self.direction = pygame.math.Vector2(0,-1)
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
        mouseX, mouseY = pygame.mouse.get_pos()
        relX, relY = mouseX - self.rect.centerx, mouseY - self.rect.centery
        self.angle = -math.atan2(relY,relX)
        self.image = pygame.transform.rotate(self.image_init, int(math.degrees(self.angle)- 90))
    def fire(self):
        shot = Projectile(purpleLaser,self.rect.centerx,self.rect.top)
        proj_list.add(shot)
        all_sprites.add(shot)

player = Player()
playerGroup.add(player)
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
    def fire(self):
        shot = Projectile(redLaser,self.rect.centerx,self.rect.bottom)
        alien_proj_list.add(shot)
        all_sprites.add(shot)

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
        self.image_init = image
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.speed = 10
    def update(self):
        if self.image == purpleLaser:
            self.rect.centery -= self.speed
        if self.image == redLaser:
            self.rect.centery += self.speed / 2
        if self.rect.y > resY or self.rect.y < 0 or self.rect.x > resX or self.rect.x < play_areaX:
            self.kill()

# Setup play area.
play_areaX = resX * 0.25
playBoundX = resX - 80
playBoundY = resY - 80
alienBoundX = resX - 50

# Define static rectangles
playRect = pygame.Rect(play_areaX, 0, resX, resY)
scoreRect = pygame.Rect(10, 10, play_areaX - 20, 50)
alienHealthBarBase = pygame.Rect(10, 70, play_areaX - 20, 50)
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
pause = False
#THE GAME LOOP.
while gameRunning:
    #HANDLE EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRunning = False
        elif event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_SPACE and len(alien_list) > 0:
                player.fire()
            if event.key == pygame.K_r:
                readyFlag = True
    
    while pause == True:
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_p:
                    pause = False
                    player.health = 100
                    waveCount = 1
                    player = Player()
                    playerGroup.add(player)
                    all_sprites.add(player)

    
    # Draws play area
    gameDisplay.fill((56, 0 ,153))
    healthBarFill = pygame.Rect(10, 902, (play_areaX - 20)*((player.health)/100), resY * 0.05)

    # Draws HUD
    pygame.draw.rect(gameDisplay, (0,0,0), playRect)
    pygame.draw.rect(gameDisplay, (0,71,158), scoreRect,0,3)
    pygame.draw.rect(gameDisplay, (252,186,3), alienHealthBarBase,0,3)
    pygame.draw.rect(gameDisplay, (255,0,0), healthBarBase,0,3)
    pygame.draw.rect(gameDisplay, (0,255,0), healthBarFill,0,3)

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
    
    # Check for players hits
    hits = pygame.sprite.groupcollide(proj_list,alien_list,False,False)
    for i in hits.values():
        for alien in i:
            alien.health -= player.damage
            alien_health -= player.damage
    
    # Check for alien hits
    if pygame.sprite.spritecollide(player,alien_proj_list,True):
        player.health -= 1

    if player.health <= 0:
        for i in all_sprites:
            i.kill()
        font.render_to(gameDisplay, (resX * 0.25 + 80, resY /2), "GAME OVER", (255,255,255), None, size=80)
        pause = True
    # Monitor total health of alien wave.
    alien_health_percent = (alien_health / total_alien_health) * 100

    alienHealthBarFill = pygame.Rect(10, 70, (play_areaX - 20)*(alien_health_percent/100), 50)


    pygame.draw.rect(gameDisplay, (3,194,252), alienHealthBarFill,0,3)

    # Randomly select when enemies fire
    for alien in alien_list:
        choice = choice = random.randint(0,1000)   
        if choice > 998:
            alien.fire()
    
    # Check how many enemies are alive. Go to next wave if all dead and player is ready.
    if len(alien_list) == 0 and player.health > 0:
        for proj in alien_proj_list:
            proj.kill()
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