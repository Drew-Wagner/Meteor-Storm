import pygame, sys, random

from pygame.locals import *

WIDTH = 375
HEIGHT = 600
FPS = 30

PLAYERMOVESPEED = 15

class GameManager(object):
    def __init__(self):
        self.points = 0
        self.bolts = []
        self.roids = []

        self.player = Player(self)
        
        self.newroid = 0
        
    def update(self):
        # Asteroid generation
        if self.newroid == 0:
            Asteroid(self, random.randint(0, 14)*25, random.randint(-5,5), random.randint(2,8))
            self.newroid = 1000 # New asteroid every 1000 milliseconds
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            pygame.quit()
            sys.exit()
        if  keys[K_LEFT] or keys[K_a]:
            self.player.move(-PLAYERMOVESPEED,0)
        if keys[K_RIGHT] or keys[K_d]:
            self.player.move(PLAYERMOVESPEED, 0)

        if keys[K_SPACE] or keys[K_f]:
           self.player.fire()

       # Update entities
        for b in self.bolts:
            b.update()
        for a in self.roids:
            a.update()
        self.player.update()

        # Render poitns
        msgSurfObj = fontObj.render("Points: " + str(self.points), False, (255,255,255))
        msgRectObj = msgSurfObj.get_rect()
        msgRectObj.topleft = (3, 3)
        screen.blit(msgSurfObj, msgRectObj)

        # Decrease new asteroid timer
        self.newroid = max(self.newroid - fpsClock.get_time(), 0)

class Player(object):
    def __init__(self, gm):
        self.gm = gm
        self.rect = pygame.Rect(150,513, 75, 75)
        self.canfire = 0

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
            self.gm.points -= 50 # Take away points for missing asteroid
            self.gm.roids.remove(self)

        for b in self.gm.bolts:
            if self.rect.colliderect(b.rect) and self.explode == False:
                self.explode = pygame.time.get_ticks()
                self.gm.bolts.remove(b)
                self.gm.points += 5

        self.draw()

    def draw(self):
        screen.blit(roidSprite1, self.rect)
        if self.explode:
            t = pygame.time.get_ticks() - self.explode
            pygame.draw.circle(screen, (255,255,255), self.rect.center, t/2)
            if t > 50:
                self.explode = False
                self.gm.roids.remove(self)
        
                

pygame.init()
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption("Asteroids")

fpsClock = pygame.time.Clock()

# Load fonts
fontObj = pygame.font.SysFont("Comic sans MS", 16)

# Load background sprites
backgroundObj = pygame.image.load('space.png') # Image credit: GameArtGuppy.com

# Load and transform player sprites
playerSprite1 = pygame.image.load('spaceship.gif') # Image credit: simeontemplar.deviantart.com
playerSprite1 = pygame.transform.scale(playerSprite1, (75, 75))
playerSprite2 = pygame.image.load('spaceship2.gif')
playerSprite2 = pygame.transform.scale(playerSprite2, (75, 75))

# Load and transform bolt sprites
boltSprite1 = pygame.image.load('bolt1.png')
boltSprite1 = pygame.transform.scale(boltSprite1, (50, 33))
boltSprite1 = pygame.transform.rotate(boltSprite1, 90)

# Load and transform roid sprites
roidSprite1 = pygame.image.load('asteroid.png')
roidSprite1 = pygame.transform.scale(roidSprite1, (25,25))

manager = GameManager()


while True:
    screen.blit(backgroundObj, (0,0))

    manager.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    

    pygame.display.flip()
    fpsClock.tick(FPS)
