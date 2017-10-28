import pygame, sys, random
from pygame.locals import *

WIDTH = 375
HEIGHT = 600
FPS = 30

PLAYERMOVESPEED = 15

pygame.init()
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption("Asteroids")

fpsClock = pygame.time.Clock()

# Load fonts
FONT16 = pygame.font.SysFont("Comic sans MS", 16)
FONT26 = pygame.font.SysFont("Comic sans MS", 26)
FONT36 = pygame.font.SysFont("Comic sans MS", 36)

# Load background sprites
backgroundObj = pygame.image.load('images/space.png') # Image credit: GameArtGuppy.com

# Load and transform player sprites
playerSprite1 = pygame.image.load('images/spaceship/spaceship_1.gif') # Image credit: simeontemplar.deviantart.com
playerSprite1 = pygame.transform.scale(playerSprite1, (75, 75))
playerSprite2 = pygame.image.load('images/spaceship/spaceship_2.gif')
playerSprite2 = pygame.transform.scale(playerSprite2, (75, 75))

# Load and transform bolt sprites
boltSprite1 = pygame.image.load('images/bolt.png')
boltSprite1 = pygame.transform.scale(boltSprite1, (50, 33))
boltSprite1 = pygame.transform.rotate(boltSprite1, 90)

# Load and transform roid sprites
roidSprite1 = pygame.image.load('images/asteroid.png')
roidSprite1 = pygame.transform.scale(roidSprite1, (25,25))

class OpeningState(object):

    def __init__(self, master):
        self.master = master
        self.active = False
        self.entering = False

    def enter(self):
        if self.entering == False:
            self.entering = pygame.time.get_ticks()
        t = float(pygame.time.get_ticks() - self.entering)
        screen.fill((0,0,0))
        gray = min(max(0,int(255*t/500)), 255)
        text_meteorstorm = FONT36.render("METEOR STORM", False,
                                         (gray,gray,gray))

        if t > 500:
            if t > 1000:
                self.active = True
                self.entering = False
            else:
                text_ms_rect = text_meteorstorm.get_rect()
                text_ms_rect.center = (187, 300)
                screen.blit(text_meteorstorm, text_ms_rect)
        else:
            # Opening Animation
            text_meteorstorm = pygame.transform.rotozoom(text_meteorstorm, 0, t/500)
            text_ms_rect = text_meteorstorm.get_rect()
            text_ms_rect.center = (187, 300)
            screen.blit(text_meteorstorm, text_ms_rect)
        

    def update(self):
        if self.active:
            self.master.goto(self.master.playingstate)
        else: # Entering isn't finished
            self.enter()

    def leave(self):
        self.active = False

class GameOverState(object):

    def __init__(self, master):
        self.master = master
        self.active = False
        self.entering = False
        self._panel = self.get_panel()
        
    def get_panel(self, btn=False):
        panel = pygame.Surface((300,200))
        panel.fill((127,127,127))
        msgSurfObj = FONT26.render("GAME OVER", False,
                                   (255,255,255))
        msgRectObj = msgSurfObj.get_rect()
        msgRectObj.center = (150, 50)
        panel.blit(msgSurfObj, msgRectObj)

        btn_restart = pygame.Surface((90, 30))
        msgSurfObj = None
        if btn:
            btn_restart.fill((0,0,0))
            pygame.draw.rect(btn_restart, (65, 65, 65), (3,3, 84, 24), 1)
            msgSurfObj = FONT16.render("RESTART", False,
                                       (255,255,255))
        else:
            btn_restart.fill((255, 255, 255))
            pygame.draw.rect(btn_restart, (190, 190, 190), (3,3, 84, 24), 1)
            msgSurfObj = FONT16.render("RESTART", False,
                                       (0,0,0))
        msgRectObj = msgSurfObj.get_rect()
        msgRectObj.center = btn_restart.get_rect().center
        btn_restart.blit(msgSurfObj, msgRectObj)

        btn_res_rect = btn_restart.get_rect()
        btn_res_rect.center = (150, 100)
        panel.blit(btn_restart, btn_res_rect)
        

        return panel.convert()

    def enter(self):
        if self.entering == False:
            self.entering = pygame.time.get_ticks()
        t = float(pygame.time.get_ticks() - self.entering)

        screen.blit(backgroundObj, (0,0))

        # Finish asteroid explosions
        for a in self.master.roids:
            if a.explode == False:
                a.explode = self.entering
            a.vely = 20
            a.draw()

        # Do animation
        if t > 500:
            panel_rect = self._panel.get_rect()
            panel_rect.center = (187, 300)
            screen.blit(self._panel, panel_rect)
            
            self.active = True
            self.entering = False
        else:
            panel = pygame.transform.rotozoom(self._panel, 0, t/500)
            panel_rect = panel.get_rect()
            panel_rect.center = (187, 100+ 200*t/500)
            screen.blit(panel, panel_rect)

    def update(self):
        if self.active:
            screen.blit(backgroundObj, (0,0))

            btn_rect = pygame.Rect((0,0),(90,30))
            btn_rect.center = (187, 300)
            btn_active = btn_rect.collidepoint(pygame.mouse.get_pos())
            panel = self.get_panel(btn=btn_active)

            panel_rect = panel.get_rect()
            panel_rect.center = (187, 300)

            screen.blit(panel, panel_rect)

            if btn_active and pygame.mouse.get_pressed()[0]:
                self.master.goto(self.master.playingstate)
        else: # Not finished entering state
            self.enter()
    def leave(self):
        self.active = False
    

class PlayingState(object):

    def __init__(self, master):
        self.master = master
        self.active = False

    def enter(self):
        self.active = True

    def update(self):
        if self.active:
            # Asteroid generation
            if self.master.newroid == 0:
                Asteroid(self.master, random.randint(0, 14)*25, random.randint(-5,5), random.randint(2,8))
                self.master.newroid = self.master.roidrate
            # Player movement
            keys = pygame.key.get_pressed()
            if keys[K_ESCAPE]:
                pygame.quit()
                sys.exit()
            if keys[K_UP]:
                self.master.roidrate /= 2
                if self.master.roidrate < 10:
                    self.master.roidrate = 10
            if keys[K_DOWN]:
                self.master.roidrate *= 2
            if  keys[K_LEFT] or keys[K_a]:
                self.master.player.move(-PLAYERMOVESPEED,0)
            if keys[K_RIGHT] or keys[K_d]:
                self.master.player.move(PLAYERMOVESPEED, 0)

            if keys[K_SPACE] or keys[K_f]:
               self.master.player.fire()

            # Draw background
            screen.blit(backgroundObj, (0,0))

            # Update and draw entities
            for b in self.master.bolts:
                b.update()
            for a in self.master.roids:
                a.update()

            # Update and draw player
            self.master.player.update()

            # Render poitns
            msgSurfObj = FONT16.render("Points: " + str(self.master.points), False, (255,255,255))
            msgRectObj = msgSurfObj.get_rect()
            msgRectObj.topleft = (3, 3)
            screen.blit(msgSurfObj, msgRectObj)

            # Decrease new asteroid timer
            self.master.newroid = max(self.master.newroid - fpsClock.get_time(), 0)

    def leave(self):
        self.master.points = 0
        self.active = False


class GameManager(object):
    OPENING = 0
    GAMEPLAY = 1
    GAMEOVER = 2
    def __init__(self):
        self.points = 0
        self.bolts = []
        self.roids = []

        self.openingstate = OpeningState(self)
        self.playingstate = PlayingState(self)
        self.gameoverstate = GameOverState(self)

        self.state = None

        self.player = Player(self)
        
        self.newroid = 0
        self.roidrate = 1000 # New asteroid every 1000 milliseconds
        
        self.goto(self.openingstate)

    def update(self):
        if self.state:
            self.state.update()
    def goto(self, state):
        if self.state:
            self.state.leave()
        self.state = state
        self.state.enter()
        

class Player(object):
    def __init__(self, gm):
        self.gm = gm
        self.rect = pygame.Rect(150,513, 75, 75)
        self.canfire = 0
        self.explode = False

    def move(self, x, y):
        self.rect = self.rect.move(x, y)
        if self.rect.centerx < 0:
            self.rect.centerx = 0
        if self.rect.centerx > WIDTH:
            self.rect.centerx = WIDTH

    def fire(self):
        if self.canfire == 0:
            Bolt(self.gm, self.rect.centerx - 18, self.rect.top - 25)
            self.canfire = 3

    def update(self):
        self.canfire = max(self.canfire-1, 0)
        self.draw()
        if self.explode:
            dt = pygame.time.get_ticks() - self.explode
            pygame.draw.circle(screen, (255,127,31), self.rect.center, dt/2)
            if dt > 100:
                self.explode = False
                self.gm.goto(self.gm.gameoverstate)

    def draw(self):
        if pygame.time.get_ticks() % 200 < 100:
            screen.blit(playerSprite1, self.rect.topleft)
        else:
            screen.blit(playerSprite2, self.rect.topleft)
        

class Bolt(object):
    def __init__(self, gm, x, y):
        self.rect = pygame.Rect(x, y, 10, 30)
        self.id = len(gm.bolts)
        self.gm = gm
        gm.bolts.append(self)
        
    def update(self):
        self.rect = self.rect.move(0,-25)
        if self.rect.bottom < 0:
            self.gm.bolts.remove(self)
        self.draw()

    def draw(self):
        screen.blit(boltSprite1, self.rect.topleft)

class Asteroid(object):
    def __init__(self, gm, x, velx=0, vely=5):
        self.gm = gm
        self.rect = pygame.Rect(x, -25, 25, 25)
        self.velx = velx
        self.vely = vely

        gm.roids.append(self)
        self.explode = False

    def update(self):
        self.rect = self.rect.move(self.velx, self.vely)
        if self.rect.left < 0:
            self.rect.left = 0
            self.velx = -self.velx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.velx = -self.velx
            
        if self.rect.top > HEIGHT:
            self.gm.roids.remove(self)

        for e in self.gm.bolts + self.gm.roids + [self.gm.player]:
            if type(e) == Bolt:
                if self.rect.colliderect(e.rect) and self.explode == False:
                    self.explode = pygame.time.get_ticks()
                    self.gm.bolts.remove(e)
                    self.gm.points += 5
            elif type(e) == Asteroid and e != self:
                if self.rect.colliderect(e.rect):
                    self.explode = pygame.time.get_ticks()
            elif type(e) == Player:
                if self.rect.colliderect(e.rect):
                    self.explode = pygame.time.get_ticks()
                    self.gm.player.explode = pygame.time.get_ticks()

        self.draw()

    def draw(self):
        screen.blit(roidSprite1, self.rect)
        if self.explode:
            t = pygame.time.get_ticks() - self.explode
            pygame.draw.circle(screen, (255,255,255), self.rect.center, t/2)
            if t > 50:
                self.explode = False
                self.gm.roids.remove(self)
        
                



manager = GameManager()


# Mainloop
while True:
    
    manager.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.flip()
    fpsClock.tick(FPS)
