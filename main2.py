import pygame
import random
import time
import math
import pygame.freetype


smallAlien = pygame.transform.scale(pygame.image.load("art/smallAlien.png"),(30,30))
largeAlien = pygame.transform.scale(pygame.image.load("art/largeAlien.png"),(60,60))
bossAlien = pygame.transform.scale(pygame.image.load("art/Boss.png"),(200,200))

# The player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("art/player.png"),(80,80))
        self.image_init = self.image
        self.rect = self.image.get_rect()
        self.rect.bottom = Game.resY - 20
        self.rect.centerx = Game.resX * 0.625
        self.speed = 5
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.score = 0
        self.health = 100
        self.damage = 10
        self.angle = 0
        self.direction = pygame.math.Vector2(0,-1)
        self.firerate = 500
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
        if keys[ord(' ')] and len(Game.alien_list) > 0:
            player.fire()
        if self.rect.left <= Game.resX * 0.25:
            self.rect.left = Game.resX * 0.25
        elif self.rect.right >= Game.resX:
            self.rect.right = Game.resX
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= Game.resY:
            self.rect.bottom = Game.resY
        mouseX, mouseY = pygame.mouse.get_pos()
        relX, relY = mouseX - self.rect.centerx, mouseY - self.rect.centery
        self.angle = -math.atan2(relY,relX)
        self.image = pygame.transform.rotate(self.image_init, int(math.degrees(self.angle)- 90))
    def fire(self):
        shot = Projectile(purpleLaser,self.rect.centerx,self.rect.centery,int(math.degrees(self.angle)- 90))
        Game.proj_list.add(shot)
        Game.all_sprites.add(shot)

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
        if self.rect.left < Game.resX * 0.25 + 50 or self.rect.right > Game.resX - 50:
            self.speed[0] = -self.speed[0]
        if self.rect.top < 50 or self.rect.bottom > Game.resY * 0.70:
            self.speed[1] = -self.speed[1]
        if self.health <= 0:
            self.kill()
            if self.image == smallAlien:
                player.score += 5
            if self.image == largeAlien:
                player.score += 10
    def hit(self):
        self.kill()
    def spawn(waveCount):
        # Spawns in varying amounts of aliens and varying sizes of aliens depending on which wave you're on.
        if waveCount < 5:
            for i in range(50*waveCount):
                alienX = Game.resX * 0.625
                alienY = 100
                i = Enemy(smallAlien,alienX,alienY,10)
                Game.alien_list.add(i)
                Game.all_sprites.add(i)
        if waveCount >= 5:
            for i in range(10+waveCount):
                alienX = Game.resX * 0.625
                alienY = 100
                i = Enemy(smallAlien,alienX,alienY,10)
                Game.alien_list.add(i)
                Game.all_sprites.add(i)
            if waveCount % 5 == 0:
                for i in range(waveCount):
                    alienX = Game.resX * 0.625
                    alienY = 100
                    i = Enemy(largeAlien,alienX,alienY,30)
                    Game.alien_list.add(i)
                    Game.all_sprites.add(i)
            if waveCount % 10 == 0:
                print(waveCount)
                for i in range(int(waveCount/10)):
                    alienX = Game.resX * 0.625
                    alienY = 100
                    i = Enemy(bossAlien,alienX,alienY,100)
                    Game.alien_list.add(i)
                    Game.all_sprites.add(i) 
        return
    def fire(self):
        shot = Projectile(redLaser,self.rect.centerx,self.rect.centery,180)
        Game.alien_proj_list.add(shot)
        Game.all_sprites.add(shot)

# Projectile class
class Projectile(pygame.sprite.Sprite):
    def __init__(self,image,x,y,angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.image_init = image
        self.x = x
        self.y = y
        self.speed = 10
        self.angle = angle
        self.rect = self.image.get_rect()
        
        self.rect.center = (x,y)
    def update(self):
        if self.image == purpleLaser:
            change = ((self.rect.centerx) - int((self.speed * math.sin(math.radians(self.angle)))),(self.rect.centery) - int((self.speed * math.cos(math.radians(self.angle)))))
            self.rect.center = change
        if self.image == redLaser:
            change = ((self.rect.centerx) - int((self.speed /2 * math.sin(math.radians(self.angle)))),(self.rect.centery) - int((self.speed /2* math.cos(math.radians(self.angle)))))
            self.rect.center = change
        if self.rect.y > Game.resY or self.rect.y < 0 or self.rect.x > Game.resX or self.rect.x < Game.resX * 0.25:
            self.kill()

class Game:
    resX = 960
    resY = 960
    FPS = 60
    all_sprites = pygame.sprite.Group()
    playerGroup = pygame.sprite.Group()
    proj_list = pygame.sprite.Group()
    alien_list = pygame.sprite.Group()
    alien_proj_list = pygame.sprite.Group()

    screen = pygame.display.set_mode((resX,resY))
    pygame.display.set_caption('The Psychon Assault')
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.font_size = 60
        self.font = pygame.freetype.Font("Xolonium-Bold.ttf", self.font_size)
        
        
        self.running = True
        self.startFlag = True
        self.readyFlag = False
        self.pause = False
    def run(self):
        self.setup()
        while self.running:
            self.event_handle()
            self.game_logic()
            self.draw()
    def event_handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_r:
                    self.readyFlag = True
    
        while self.pause == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_p:
                        self.pause = False
                        waveCount = 1
                        player = Player()
                        self.playerGroup.add(player)
                        self.all_sprites.add(player)
    def setup(self):
        #Static rects
        playRect = pygame.Rect(self.resX * 0.25, 0, self.resX, self.resY)
        scoreRect = pygame.Rect(10, 10, self.resX * 0.25 - 20, 50)
        alienHealthBarBase = pygame.Rect(10, 70, self.resX * 0.25 - 20, 50)
        healthBarBase = pygame.Rect(10, 902, self.resX * 0.25 - 20, self.resY * 0.05)

        #Star generation
        starXs = []
        starYs = []
        starCount = 200
        for i in range(starCount):
            starXs.append(random.randint(self.resX * 0.25, self.resX))
            starYs.append(random.randint(0, self.resY))

        # Load Sprites
        purpleLaser = pygame.image.load("art/purple_laser_round.png")
        redLaser = pygame.transform.rotate(pygame.image.load("art/red_laser_round.png"),180)
        smallAlien = pygame.transform.scale(pygame.image.load("art/smallAlien.png"),(30,30))
        largeAlien = pygame.transform.scale(pygame.image.load("art/largeAlien.png"),(60,60))
        bossAlien = pygame.transform.scale(pygame.image.load("art/Boss.png"),(200,200))

        # Setup sprites and sprite variables
        self.player = Player()
        self.playerGroup.add(self.player)
        self.all_sprites.add(self.player)

        waveCount = 1
        waveHealth = []
        alien_health = 0
        total_alien_health = 0
        alien_wave = Enemy.spawn(waveCount)
        for alien in self.alien_list:
            total_alien_health += alien.health
        alien_health = total_alien_health
    def draw(self):
        # Draw play area
        self.screen.fill((56, 0 ,153))
        # Draw HUD
        healthBarFill = pygame.Rect(10, 902, (self.resX * 0.25 - 20)*((player.health)/100), self.resY * 0.05)

        pygame.draw.rect(self.screen, (0,0,0), playRect)
        pygame.draw.rect(self.screen, (0,71,158), scoreRect,0,3)
        pygame.draw.rect(self.screen, (252,186,3), alienHealthBarBase,0,3)
        pygame.draw.rect(self.screen, (255,0,0), healthBarBase,0,3)
        pygame.draw.rect(self.screen, (0,255,0), healthBarFill,0,3)

        # Draw Stars
        for i in range(starCount):
            pygame.draw.circle(self.screen, (255, 255, 255), (starXs[i], starYs[i]), 1, 1)
            starYs[i] += 3

        if starYs[i] > self.resY:
            starYs[i] = 10
        
        if self.startFlag: # Runs once at the start of every wave to store total wave health.
            self.startFlag = False
            total_alien_health = 0
            for alien in self.alien_list:
                total_alien_health += alien.health
            alien_health = total_alien_health

        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        Stats(player.score,waveCount,player.health,alien_health_percent)
    
    def game_logic(self):
        # Check for players hits
        hits = pygame.sprite.groupcollide(self.proj_list,self.alien_list,True,False)
        for i in hits.values():
            for alien in i:
                alien.health -= self.player.damage
                alien_health -= self.player.damage
        # Check for alien hits
        if pygame.sprite.spritecollide(self.player,self.alien_proj_list,True):
            self.player.health -= 1

        if self.player.health <= 0:
            for i in self.all_sprites:
                i.kill()
            self.font.render_to(self.screen, (self.resX * 0.25 + 80, self.resY /2), "GAME OVER", (255,255,255), None, size=80)
            self.pause = True
        # Monitor total health of alien wave.
        alien_health_percent = (alien_health / total_alien_health) * 100

        alienHealthBarFill = pygame.Rect(10, 70, (self.resX * 0.25 - 20)*(alien_health_percent/100), 50)


        pygame.draw.rect(self.screen, (3,194,252), alienHealthBarFill,0,3)

        # Randomly select when enemies fire
        for alien in self.alien_list:
            choice = choice = random.randint(0,1000)   
            if choice > 998:
                alien.fire()
        
        if len(self.alien_list) == 0 and player.health > 0:
            for proj in self.alien_proj_list:
                proj.kill()
            for proj in self.proj_list:
                proj.kill()
            self.font.render_to(self.screen, (self.resX * 0.25 + 15, self.resY /2), "Wave "+str(waveCount)+" cleared! Press R to start next wave.", (255,255,255), None, size=28)
            player.rect.centerx = self.resX * 0.625
            player.rect.bottom = self.resY - 20
            if self.readyFlag:
                waveCount += 1
                self.startFlag = True
                self.readyFlag = False
                alien_wave = spawn(waveCount)
                total_alien_health = 0
                for alien in self.alien_list:
                    total_alien_health += alien.health
                alien_health = total_alien_health
    def Stats(score,wave,health,alien_health):
        self.font.render_to(self.screen, (12, 12), "Score: "+str(score), (0,0,0), None, size=30)
        self.font.render_to(self.screen, (12, 36), "Wave: "+str(wave), (0,0,0), None, size=30)
        self.font.render_to(self.screen, (45, 922), "Hull Integrity: "+str(health)+"%", (0,0,0), None, size=15)
        self.font.render_to(self.screen, (18, 90), "Psychon Strength: "+str("%.0f" % abs(alien_health))+"%", (0,0,0), None, size=15)


pygame.init()
Game().run()
pygame.quit()
quit()