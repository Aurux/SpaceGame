import pygame
import random
import math
import pygame.freetype
import sys
import os


gamePath = os.path.dirname(__file__)
artPath = os.path.join(gamePath,"art")
soundPath = os.path.join(gamePath,"sounds")
pygame.init()
pygame.freetype.init()

# Global sprites
smallAlien = pygame.transform.scale(pygame.image.load(os.path.join(artPath,"smallAlien.png")),(30,30))
largeAlien = pygame.transform.scale(pygame.image.load(os.path.join(artPath,"largeAlien.png")),(60,60))
bossAlien = pygame.transform.scale(pygame.image.load(os.path.join(artPath,"Boss.png")),(200,200))
purpleLaser = pygame.image.load(os.path.join(artPath,"purple_laser_round.png"))
redLaser = pygame.transform.rotate(pygame.image.load(os.path.join(artPath,"red_laser_round.png")),180)
titleText = pygame.image.load(os.path.join(artPath,"title.png"))

pygame.display.set_icon(pygame.transform.scale(pygame.image.load(os.path.join(artPath,"player.png")),(32,32)))
# Sound effects/Music

enemyLaser = pygame.mixer.Sound(os.path.join(soundPath,"enemy_lazer.wav"))
playerLaser = pygame.mixer.Sound(os.path.join(soundPath,"lazer.wav"))
damageThud = pygame.mixer.Sound(os.path.join(soundPath,"thud.wav"))
pause = pygame.mixer.Sound(os.path.join(soundPath,"pause.wav"))
play = pygame.mixer.Sound(os.path.join(soundPath,"play.wav"))
mouseOver = pygame.mixer.Sound(os.path.join(soundPath,"mouse_over_click.wav"))



# The player class
class Player(pygame.sprite.Sprite):
    score = 0
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(artPath,"player.png")),(80,80))
        self.image_init = self.image
        self.rect = self.image.get_rect()
        self.rect.bottom = Game.resY - 20
        self.rect.centerx = Game.resX * 0.625
        self.speed = 5
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.previous_time = pygame.time.get_ticks()
        self.health = 100
        self.damage = 10
        self.angle = 0
        self.firerate = 300
        self.mask = pygame.mask.from_surface(self.image)
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
        if pygame.mouse.get_pressed()[0] or keys[ord(' ')] and len(Game.alien_list) > 0:
            current_time = pygame.time.get_ticks()
            if current_time - self.previous_time > self.firerate:
                self.previous_time = current_time
                self.fire()
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
        playerLaser.set_volume(0.5*volumePercent)
        playerLaser.play(0)
        shot = Projectile(purpleLaser,self.rect.centerx,self.rect.centery,int(math.degrees(self.angle)- 90))
        Game.proj_list.add(shot)
        Game.all_sprites.add(shot)

# Enemy class for any NPCs
class Enemy(pygame.sprite.Sprite):
    def __init__(self,image,x,y,health):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.image_init = self.image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        self.health = health
        self.speed = [random.randint(-5,5),random.randint(-5,5)]
        self.mask = pygame.mask.from_surface(self.image)
    def update(self):
        self.rect = self.rect.move(self.speed)
        if self.rect.left < Game.resX * 0.25 + 50 or self.rect.right > Game.resX - 50:
            self.speed[0] = -self.speed[0]
        if self.rect.top < 50 or self.rect.bottom > Game.resY * 0.70:
            self.speed[1] = -self.speed[1]
        if self.health <= 0:
            self.kill()
            if self.image == smallAlien:
                Player.score += 10
            if self.image == largeAlien:
                Player.score += 25
            if self.image == bossAlien:
                Player.score += 100
    def hit(self):
        self.kill()
    def spawn(waveCount):
        # Spawns in varying amounts of aliens and varying sizes of aliens depending on which wave you're on.
        
        for i in range(15*waveCount):
            alienX = Game.resX * 0.625
            alienY = 100
            i = Enemy(smallAlien,alienX,alienY,10)
            Game.alien_list.add(i)
            Game.all_sprites.add(i)
        if waveCount >= 5:
            for i in range(waveCount-4):
                alienX = Game.resX * 0.625
                alienY = 100
                i = Enemy(largeAlien,alienX,alienY,30)
                Game.alien_list.add(i)
                Game.all_sprites.add(i)
            if waveCount % 10 == 0:
                for i in range(int(waveCount/10)):
                    alienX = Game.resX * 0.625
                    alienY = 100
                    i = Enemy(bossAlien,alienX,alienY,1000)
                    Game.alien_list.add(i)
                    Game.all_sprites.add(i) 
        return
    def fire(self,targetX,targetY):
        relX, relY = targetX - self.rect.centerx, targetY - self.rect.centery
        self.angle = -math.atan2(relY,relX)
        self.image = pygame.transform.rotate(self.image_init, int(math.degrees(self.angle)+ 90))
        enemyLaser.set_volume(0.3*volumePercent)
        enemyLaser.play(0)
        shot = Projectile(redLaser,self.rect.centerx,self.rect.centery,int(math.degrees(self.angle)- 90))
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
        self.enemyspeed = 7
        self.angle = angle
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.mask = pygame.mask.from_surface(self.image)
    def update(self):
        if self.image == purpleLaser:
            change = ((self.rect.centerx) - int((self.speed * math.sin(math.radians(self.angle)))),(self.rect.centery) - int((self.speed * math.cos(math.radians(self.angle)))))
            self.rect.center = change
        if self.image == redLaser:
            change = ((self.rect.centerx) - int((self.enemyspeed * math.sin(math.radians(self.angle)))),(self.rect.centery) - int((self.enemyspeed* math.cos(math.radians(self.angle)))))
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
    font_size = 60
    font = pygame.freetype.Font(os.path.join(gamePath,"Xolonium-Bold.ttf"), font_size)
    screen = pygame.display.set_mode((resX,resY))
    pygame.display.set_caption('The Psychon Assault')
    inputName = ""
    baseColour = (128,128,128)
    activeColour = (255,255,255)
    inputColour = baseColour
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.startFlag = True
        self.readyFlag = False
        self.pause = False
        self.inputState = False
    def run(self,running):
        self.setup()
        self.running = running
        while self.running:
            self.event_handle()
            self.draw()
            self.game_logic()
            pygame.display.update()
            self.clock.tick_busy_loop(self.FPS)
            if self.running is False:
                pygame.quit()
                sys.exit()
        
        
    def event_handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEMOTION:
                # Change button colours on mouse over.
                for button in self.buttonArray:
                    if button[0].collidepoint(event.pos):
                        button[1] = (153, 105 ,0)
                        #mouseOver.play(0)
                    else:
                        button[1] = (224,153,0)
                for button in self.gameOverButtonArray:
                    if button[0].collidepoint(event.pos):
                        button[1] = (153, 105 ,0)
                        #mouseOver.play(0)
                    else:
                        button[1] = (224,153,0)
            if event.type == pygame.MOUSEBUTTONUP:
                if self.inputBox.collidepoint(event.pos):
                    self.inputState = not self.inputState
                    self.inputColour = self.activeColour
                else:
                    self.inputState = False
                    self.inputColour = self.baseColour
                if self.restartBox.collidepoint(event.pos):
                    Game().HighScoreWrite(self.player.score,self.inputName)
                    self.running = False
                    self.player.score = 0
                    for sprite in self.all_sprites:
                        sprite.kill()
                    Game().run(True)
                if self.exitBox.collidepoint(event.pos):
                    Game().HighScoreWrite(self.player.score,self.inputName)
                    self.running = False
                    self.player.score = 0
                    for sprite in self.all_sprites:
                        sprite.kill()

                    self.pause = not self.pause
                    self.running = not self.running
                    Menu().run()
                if self.resumeBox.collidepoint(event.pos):
                    self.pause = False
                    play.play()
            if event.type == pygame.KEYDOWN: 
                if self.inputState:
                    if event.key == pygame.K_RETURN:
                        self.inputState = False
                        self.inputColour = self.baseColour
                    elif event.key == pygame.K_BACKSPACE:
                        self.inputName = self.inputName[:-1]
                    else:
                        if len(self.inputName) == 10:
                            pass
                        else:
                            self.inputName += event.unicode
                if event.key == pygame.K_r:
                    self.readyFlag = True
                if event.key == pygame.K_ESCAPE:
                    self.pause = not self.pause
                    pause.set_volume(volumePercent)
                    pause.play(0)
                    while self.pause:
                        for rect, colour in self.buttonArray:
                            pygame.draw.rect(self.screen, colour, rect,0, 10)
                        self.font.render_to(self.screen, (self.resX * 0.25 + 170, self.resY /2 - 50), "PAUSED", (255,255,255), None, size=80)
                        self.font.render_to(self.screen,(self.restartBox.x + 40,self.restartBox.y + 20),"Restart",None,size=30)
                        self.font.render_to(self.screen,(self.exitBox.x + 65,self.exitBox.y + 20),"Exit",None,size=30)
                        self.font.render_to(self.screen,(self.resumeBox.x + 40,self.resumeBox.y + 20),"Resume",None,size=30)
                        self.event_handle()
                        pygame.display.update()
                        self.clock.tick_busy_loop(self.FPS)
                    play.set_volume(volumePercent)
                    play.play()
    def setup(self):
        #Static rects
        self.playRect = pygame.Rect(self.resX * 0.25, 0, self.resX, self.resY)
        self.scoreRect = pygame.Rect(10, 10, self.resX * 0.25 - 20, 50)
        self.alienHealthBarBase = pygame.Rect(10, 70, self.resX * 0.25 - 20, 50)
        self.healthBarBase = pygame.Rect(10, 902, self.resX * 0.25 - 20, self.resY * 0.05)
        self.inputBox = pygame.Rect(self.resX * 0.25 + 160, (self.resY /2), 395, 60)
        self.restartBox = pygame.Rect(self.resX * 0.25 + 160, (self.resY /2 + 70), 195, 60)
        self.exitBox = pygame.Rect(self.resX * 0.25 + 360, (self.resY /2 + 70), 195, 60)
        self.resumeBox = pygame.Rect(self.resX * 0.25 + 257.5, (self.resY /2 + 140), 195, 60)

        self.buttonArray = [
            [self.restartBox, (224,153,0)],
            [self.exitBox, (224,153,0)],
            [self.resumeBox, (224,153,0)]
        ]

        self.gameOverButtonArray = [
            [self.restartBox, (224,153,0)],
            [self.exitBox, (224,153,0)]
        ]
        #Star generation
        self.starXs = []
        self.starYs = []
        self.starCount = 200
        for i in range(self.starCount):
            self.starXs.append(random.randint(self.resX * 0.25, self.resX))
            self.starYs.append(random.randint(0, self.resY))


        # Setup sprites and sprite variables
        self.player = Player()
        self.playerGroup.add(self.player)
        self.all_sprites.add(self.player)
        Player.score = 0
        self.waveCount = 1
        waveHealth = []
        self.alien_health = 0
        self.total_alien_health = 0
        alien_wave = Enemy.spawn(self.waveCount)
        for alien in self.alien_list:
            self.total_alien_health += alien.health
        self.alien_health = self.total_alien_health        
    def draw(self):
        # Draw play area
        self.screen.fill((56, 0 ,153))
        # Draw HUD
        healthBarFill = pygame.Rect(10, 902, (self.resX * 0.25 - 20)*((self.player.health)/100), self.resY * 0.05)

        pygame.draw.rect(self.screen, (0,0,0), self.playRect)
        pygame.draw.rect(self.screen, (0,71,158), self.scoreRect,0,3)
        pygame.draw.rect(self.screen, (252,186,3), self.alienHealthBarBase,0,3)
        pygame.draw.rect(self.screen, (255,0,0), self.healthBarBase,0,3)
        pygame.draw.rect(self.screen, (0,255,0), healthBarFill,0,3)
        # Draw Stars
        for i in range(self.starCount):
            pygame.draw.circle(self.screen, (255, 255, 255), (self.starXs[i], self.starYs[i]), 1, 1)
            self.starYs[i] += 3

            if self.starYs[i] > self.resY:
                self.starYs[i] = 10

        # Runs once at the start of every wave to store total wave health.
        if self.startFlag: 
            self.startFlag = False
            self.total_alien_health = 0
            for alien in self.alien_list:
                self.total_alien_health += alien.health
            self.alien_health = self.total_alien_health

        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        
    
    def game_logic(self):
        # Check for players hits
        hits = pygame.sprite.groupcollide(self.proj_list,self.alien_list,True,False, pygame.sprite.collide_mask)
        for i in hits.values():
            for alien in i:
                alien.health -= self.player.damage
                self.alien_health -= self.player.damage
        if self.alien_health < 0:
            self.alien_health = 0

        # Check for alien hits
        if pygame.sprite.spritecollide(self.player,self.alien_proj_list,True, pygame.sprite.collide_mask):
            self.player.health -= self.waveCount / 2
            damageThud.set_volume(0.8*volumePercent)
            damageThud.play(0)

        # Check if player has died.
        if self.player.health <= 0:
            for i in self.all_sprites:
                i.kill()
            newHS = False
            highScore, hsName = Game().HighScoreRead("scores.txt")
            if int(self.player.score) > int(highScore):
                newHS = True

            self.font.render_to(self.screen, (self.resX * 0.25 + 80, self.resY /2 - 200), "GAME OVER", (255,255,255), None, size=80)
            self.font.render_to(self.screen, (self.resX * 0.25 + 250, (self.resY /2) -130), "Score: "+str(self.player.score), (255,255,255), None, size=40)
            if newHS:
                self.font.render_to(self.screen, (self.resX * 0.25 + 205, (self.resY /2) -80), "HIGH SCORE!", (255,215,0), None, size=40)
                self.font.render_to(self.screen, (self.resX * 0.25 + 160, (self.resY /2) -40), "Please enter name", (255,255,255), None, size=40)
                pygame.draw.rect(self.screen, self.inputColour,self.inputBox,0,10)
                text_surface = self.font.render(self.inputName,True,(0,0,0))
                self.font.render_to(self.screen,(self.inputBox.x + 10,self.inputBox.y + 20),self.inputName,None,size=30)
            for rect, colour in self.gameOverButtonArray:
                pygame.draw.rect(self.screen, colour, rect,0, 10)
            self.font.render_to(self.screen,(self.restartBox.x + 40,self.restartBox.y + 20),"Restart",None,size=30)
            self.font.render_to(self.screen,(self.exitBox.x + 65,self.exitBox.y + 20),"Exit",None,size=30)

        # Check for collisions / ramming
        collisions = pygame.sprite.groupcollide(self.playerGroup, self.alien_list,False,False, pygame.sprite.collide_mask)
        for i in collisions.values():
            for obj in i:
                obj.health -= 0.5
        # Monitor total health of alien wave.
        alien_health_percent = (self.alien_health / self.total_alien_health)
        alienHealthBarFill = pygame.Rect(10, 70, (self.resX * 0.25 - 20)*(alien_health_percent), 50)
        pygame.draw.rect(self.screen, (3,194,252), alienHealthBarFill,0,3)
        Game().Stats(self.player.score,self.waveCount,self.player.health,alien_health_percent*100)

        # Randomly select when enemies fire
        for alien in self.alien_list:
            choice = choice = random.randint(0,1000)   
            if choice > 998:
                alien.fire(self.player.rect.centerx,self.player.rect.centery)
        
        # Check if the wave has ended.
        if len(self.alien_list) == 0 and self.player.health > 0:
            for proj in self.alien_proj_list:
                proj.kill()
            for proj in self.proj_list:
                proj.kill()
            self.font.render_to(self.screen, (self.resX * 0.25 + 15, self.resY /2), "Wave "+str(self.waveCount)+" cleared! Press R to start next wave.", (255,255,255), None, size=28)
            self.player.rect.centerx = self.resX * 0.625
            self.player.rect.bottom = self.resY - 20
            if self.readyFlag:
                Player.score += 1000
                self.waveCount += 1
                self.startFlag = True
                self.readyFlag = False
                alien_wave = Enemy.spawn(self.waveCount)
                self.total_alien_health = 0
                for alien in self.alien_list:
                    self.total_alien_health += alien.health
                self.alien_health = self.total_alien_health
    def Stats(self,score,wave,health,alien_health):
        Game.font.render_to(self.screen, (12, 12), "Score: "+str(score), (0,0,0), None, size=30)
        self.font.render_to(self.screen, (12, 36), "Wave: "+str(wave), (0,0,0), None, size=30)
        self.font.render_to(self.screen, (45, 922), "Hull Integrity: "+str(health)+"%", (0,0,0), None, size=15)
        self.font.render_to(self.screen, (18, 90), "Psychon Strength: "+str("%.0f" % alien_health)+"%", (0,0,0), None, size=15)
    def HighScoreWrite(self,score,name):
        score_file = open("scores.txt","a")
        score_file.write(str(score)+","+name+"\n")
        score_file.close()
        return
    def HighScoreRead(self,file):
        with open(file) as scores: 
                lines = scores.read().splitlines()
                maxScore = 0
                hsName = ""
                for line in lines:
                    score = int(line.split(",")[0].strip())
                    name = line.split(",")[1].strip()
                    if score > maxScore:
                        maxScore = score
                        hsName = name
                if maxScore == 0:
                    maxScore = 0
        return maxScore, hsName
    def Quit(self):
        self.running = False
        pygame.display.quit()
        pygame.quit()

global volumeLevel
volumeLevel = 10
global volumePercent        
volumePercent = volumeLevel / 10

class Menu:
    resX = 960
    resY = 960
    FPS = 60
    font_size = 60
    font = pygame.freetype.Font(os.path.join(gamePath,"Xolonium-Bold.ttf"), font_size)
    screen = Game.screen
    #pygame.display.set_mode((resX,resY))
    pygame.display.set_caption('The Psychon Assault')
    clock = pygame.time.Clock()
    hovered = False
    optionState = False
    
    def run(self):
        self.setup()
        self.running = True
        while self.running:
            self.event_handle()
            self.draw()
            pygame.display.update()
            self.clock.tick_busy_loop(self.FPS)
    def event_handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                # Change button colours on mouse over.
                for button in self.buttonArray:
                    if button[0].collidepoint(event.pos):
                        button[1] = (153, 105 ,0)
                        #mouseOver.play(0)
                    else:
                        button[1] = (224,153,0)
                for button in self.optionButtonArray:
                    if button[0].collidepoint(event.pos):
                        button[1] = (153, 105 ,0)
                        #mouseOver.play(0)
                    else:
                        button[1] = (224,153,0)
                            
                    
            elif event.type == pygame.MOUSEBUTTONUP:
                # Decide which button was clicked.
                mousePos = event.pos
                if self.optionState is False:
                    if self.playRect.collidepoint(mousePos):
                        self.running = False
                        #pygame.mixer.music.stop()
                        Game().run(True)
                    if self.quitRect.collidepoint(mousePos):
                        self.running = False
                        pygame.quit
                    if self.resetRect.collidepoint(mousePos):
                        open('scores.txt', 'w').close()
                        self.highScore, self.hsName = Game().HighScoreRead("scores.txt")
                    if self.optRect.collidepoint(mousePos):
                        self.optionState = not self.optionState
                if self.optionState:
                    global volumeLevel
                    if self.backRect.collidepoint(mousePos):
                        self.optionState = not self.optionState
                    if self.volUpRect.collidepoint(mousePos):
                        volumeLevel += 1
                    if self.volDownRect.collidepoint(mousePos):
                        volumeLevel -= 1
                    if volumeLevel > 10:
                        volumeLevel = 10
                    elif volumeLevel < 0:
                        volumeLevel = 0
                    global volumePercent
                    volumePercent = volumeLevel / 10

    def setup(self):
        #Star generation
        self.starXs = []
        self.starYs = []
        self.starCount = 200
        for i in range(self.starCount):
            self.starXs.append(random.randint(0, self.resX))
            self.starYs.append(random.randint(0, self.resY))
        
        # Setup menu rects
        self.bgRect = pygame.Rect(160,380,640,400)
        self.playRect = pygame.Rect(210,431,220,98)
        self.optRect = pygame.Rect(210,531,220,98)
        self.quitRect = pygame.Rect(210,631,220,98)

        self.hsRect = pygame.Rect(530,431,220,98)
        self.nameRect = pygame.Rect(530,531,220,98)
        self.resetRect = pygame.Rect(530,631,220,98)

        self.backRect = pygame.Rect(370,631,220,98)
        self.volDownRect = pygame.Rect(230,460,30,30)
        self.volUpRect = pygame.Rect(305,460,30,30)

        self.optionButtonArray = [
            [self.backRect, (224,153,0)],
            [self.volUpRect, (224,153,0)],
            [self.volDownRect, (224,153,0)]
        ]

        self.buttonArray = [
            [self.playRect, (224,153,0)],
            [self.optRect, (224,153,0)],
            [self.quitRect, (224,153,0)],
            [self.resetRect, (224,153,0)],
        ]

        # Get highscore data from file.
        self.highScore, self.hsName = Game().HighScoreRead("scores.txt")

        # Play game music
        pygame.mixer.music.load(os.path.join(soundPath,"menu.wav"))
        pygame.mixer.music.play(-1)
    def draw(self):
        pygame.mixer.music.set_volume(volumePercent)
        mouseOver.set_volume(0.2*volumePercent)
        self.screen.fill((0, 0 ,0))
        # Draw Stars
        for i in range(self.starCount):
            pygame.draw.circle(self.screen, (255, 255, 255), (self.starXs[i], self.starYs[i]), 1, 1)
            self.starYs[i] += 3

            if self.starYs[i] > self.resY:
                self.starYs[i] = 10
        
        # Draw Title
        pygame.Surface.blit(self.screen,titleText,(8,80))

        pygame.draw.rect(self.screen, (56, 0 ,153), self.bgRect,0,100)
        if self.optionState:
            for rect, colour in self.optionButtonArray:
                pygame.draw.rect(self.screen, colour, rect,0, 10)
            self.font.render_to(self.screen, (415, 665), "Back", (0,0,0), None, size=50)
            self.font.render_to(self.screen, (240, 440), "Volume", (255,255,255), None, size=20)
            self.font.render_to(self.screen, (270, 470), str(volumeLevel), (255,255,255), None, size=20)
            self.font.render_to(self.screen, (315, 470), "+", (0,0,0), None, size=20)
            self.font.render_to(self.screen, (241, 475), "-", (0,0,0), None, size=20)
        else:
            # Draw rects
            
            pygame.draw.rect(self.screen, (224,153,0), self.hsRect,0,10)
            pygame.draw.rect(self.screen, (224,153,0), self.nameRect,0,10)

            for rect, colour in self.buttonArray:
                pygame.draw.rect(self.screen, colour, rect,0, 10)

            # Draw Text
            self.font.render_to(self.screen, (265, 465), "Play", (0,0,0), None, size=50)
            self.font.render_to(self.screen, (215, 565), "Options", (0,0,0), None, size=50)
            self.font.render_to(self.screen, (265, 665), "Quit", (0,0,0), None, size=50)
            self.font.render_to(self.screen, (540, 670), "Reset HS", (0,0,0), None, size=40)
            self.font.render_to(self.screen, (380, 760), "By Benjamin Wilson", (255,255,255), None, size=20)
            self.font.render_to(self.screen, (585, 435), "High Score", (0,0,0), None, size=20)
            scoreImage, scoreRect = self.font.render(str(self.highScore),(0,0,0),size=40)
            pygame.Surface.blit(self.screen,scoreImage,(640 - scoreRect[2] / 2,480 -scoreRect[3] /2))
            self.font.render_to(self.screen, (600, 535), "Held by", (0,0,0), None, size=20)
            #self.font.render_to(self.screen, (540, 580), self.hsName, (0,0,0), None, size=25)
            nameImage, nameRect = self.font.render(str(self.hsName),(0,0,0),size=25)
            pygame.Surface.blit(self.screen,nameImage,(640 - nameRect[2] / 2,578 - nameRect[3] /2))



Menu().run()
pygame.quit()
quit()