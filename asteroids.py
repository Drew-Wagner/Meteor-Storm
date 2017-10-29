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
FONT_S = pygame.font.SysFont("Impact", 18)
FONT_M = pygame.font.SysFont("Impact", 28)
FONT_L = pygame.font.SysFont("Impact", 46)
FONT_XL = pygame.font.SysFont("Impact", 66)

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
        self.name = "OPENING"
        self.active = False
        self.timer = False

    def enter(self):
        self.master.points = 0
        if self.timer == False:
            self.timer = pygame.time.get_ticks()
        t = float(pygame.time.get_ticks() - self.timer)
        screen.fill((0,0,0))
        gray = min(max(0,int(255*t/500)), 255)
        text_meteorstorm = FONT_L.render("METEOR STORM", False,
                                         (gray,gray,gray))

        if t > 500:
            if t > 1000:
                self.active = True
                self.timer = False
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
            self.master.goto(self.master.mainmenustate)
        else: # timer isn't finished
            self.enter()

    def leave(self, state):
        self.active = False
        self.master._enter(state)

class MainMenuState(object):

    def __init__(self, master):
        self.master = master
        self.name = "MAINMENU"
        self.active = False
        self.timer = False

    def black(self): # Overlay from opening scene for fade-out
        black = pygame.Surface((WIDTH,HEIGHT))
        black.fill((0,0,0))

        return black.convert()

    def draw(self, btn_p=False, btn_ins=False, btn_q=False):
        # Draw background
        screen.blit(backgroundObj, (0,0))

        # Draw Title
        title = FONT_XL.render("METEOR", False,
                                      (255,255,255))
        title_rect = title.get_rect()
        title_rect.center = (187, 90)
        screen.blit(title, title_rect)
        title = FONT_XL.render("STORM", False,
                                      (255,255,255))
        title_rect = title.get_rect()
        title_rect.center = (187, 150)
        screen.blit(title, title_rect)

        # Draw Play button
        btn_play = pygame.Surface((300, 50))
        msgSurfObj = None
        if btn_p:
            btn_play.fill((0,0,0))
            pygame.draw.rect(btn_play, (65, 65, 65), (6,6, 288, 38), 2)
            msgSurfObj = FONT_M.render("PLAY", False,
                                       (255,255,255))
        else:
            btn_play.fill((255, 255, 255))
            pygame.draw.rect(btn_play, (190, 190, 190), (6,6, 288, 38), 2)
            msgSurfObj = FONT_M.render("PLAY", False,
                                       (0,0,0))
        msg_rect = msgSurfObj.get_rect()
        msg_rect.center = btn_play.get_rect().center
        btn_play.blit(msgSurfObj, msg_rect)

        btn_play_rect = btn_play.get_rect()
        btn_play_rect.center = (187, 250)
        screen.blit(btn_play, btn_play_rect)

        # Draw Instructions button
        btn_instructions = pygame.Surface((300, 50))
        msgSurfObj = None
        if btn_ins:
            btn_instructions.fill((0,0,0))
            pygame.draw.rect(btn_instructions, (65, 65, 65), (6,6, 288, 38), 2)
            msgSurfObj = FONT_M.render("INSTRUCTIONS", False,
                                       (255,255,255))
        else:
            btn_instructions.fill((255, 255, 255))
            pygame.draw.rect(btn_instructions, (190, 190, 190), (6,6, 288, 38), 2)
            msgSurfObj = FONT_M.render("INSTRUCTIONS", False,
                                       (0,0,0))
        msg_rect = msgSurfObj.get_rect()
        msg_rect.center = btn_instructions.get_rect().center
        btn_instructions.blit(msgSurfObj, msg_rect)

        btn_ins_rect = btn_instructions.get_rect()
        btn_ins_rect.center = (187, 350)
        screen.blit(btn_instructions, btn_ins_rect)

        # Draw QUIT button
        btn_quit = pygame.Surface((300, 50))
        msgSurfObj = None
        if btn_q:
            btn_quit.fill((0,0,0))
            pygame.draw.rect(btn_quit, (65, 65, 65), (6,6, 288, 38), 2)
            msgSurfObj = FONT_M.render("QUIT", False,
                                       (255,255,255))
        else:
            btn_quit.fill((255, 255, 255))
            pygame.draw.rect(btn_quit, (190, 190, 190), (6,6, 288, 38), 2)
            msgSurfObj = FONT_M.render("QUIT", False,
                                       (0,0,0))
        msg_rect = msgSurfObj.get_rect()
        msg_rect.center = btn_quit.get_rect().center
        btn_quit.blit(msgSurfObj, msg_rect)

        btn_quit_rect = btn_quit.get_rect()
        btn_quit_rect.center = (187, 450)
        screen.blit(btn_quit, btn_quit_rect)

    def enter(self):
        if not self.timer:
            self.timer = pygame.time.get_ticks()
        else:
            t = float(pygame.time.get_ticks() - self.timer)

            self.draw()
            black = self.black()
            black.set_alpha(int(max(255 - t, 0)))

            screen.blit(black, (0,0))

            if t > 1000:
                self.active = True
                self.timer = False

    def update(self):
        if self.active:
            btn_play_rect = pygame.Rect((0,0),(300,50))
            btn_play_rect.center = (187, 250)
            btn_play_active = btn_play_rect.collidepoint(pygame.mouse.get_pos())

            btn_inst_rect = pygame.Rect((0,0),(300,50))
            btn_inst_rect.center = (187, 350)
            btn_inst_active = btn_inst_rect.collidepoint(pygame.mouse.get_pos())
            
            btn_quit_rect = pygame.Rect((0,0),(300,50))
            btn_quit_rect.center = (187, 450)
            btn_quit_active = btn_quit_rect.collidepoint(pygame.mouse.get_pos())

            flag = pygame.mouse.get_pressed()[0]
            if flag:
                if btn_play_active:
                    self.master.goto(self.master.playingstate)
                elif btn_inst_active:
                    pass
                elif btn_quit_active:
                    # TODO goto exit state
                    pygame.quit()
                    sys.exit()
            
            self.draw(btn_play_active, btn_inst_active, btn_quit_active)
        else:
            self.enter()

    def leave(self, state):
        self.active = False
        self.master._enter(state)

class GameOverState(object):

    def __init__(self, master):
        self.master = master
        self.name = "GAMEOVER"
        self.active = False
        self.timer = False
        
    def get_panel(self, btn_res=False, btn_mm=False):
        panel = pygame.Surface((300,200))
        panel.fill((127,127,127))
        pygame.draw.rect(panel, (65,65,65), panel.get_rect(), 5)
        
        msgSurfObj = FONT_M.render("GAME OVER", False,
                                   (255,255,255))
        msgRectObj = msgSurfObj.get_rect()
        msgRectObj.center = (150, 50)
        panel.blit(msgSurfObj, msgRectObj)

        msgSurfObj = FONT_S.render("SCORE: " + str(self.master.points), False,
                                   (255,255,255))
        msgRectObj = msgSurfObj.get_rect()
        msgRectObj.center = (150, 75)
        panel.blit(msgSurfObj, msgRectObj)

        btn_restart = pygame.Surface((115, 30))
        msgSurfObj = None
        if btn_res:
            btn_restart.fill((0,0,0))
            pygame.draw.rect(btn_restart, (65, 65, 65), (3,3, 109, 24), 1)
            msgSurfObj = FONT_S.render("RESTART", False,
                                       (255,255,255))
        else:
            btn_restart.fill((255, 255, 255))
            pygame.draw.rect(btn_restart, (190, 190, 190), (3,3, 109, 24), 1)
            msgSurfObj = FONT_S.render("RESTART", False,
                                       (0,0,0))

        msgRectObj = msgSurfObj.get_rect()
        msgRectObj.center = btn_restart.get_rect().center
        btn_restart.blit(msgSurfObj, msgRectObj)

        btn_mainmenu = pygame.Surface((115, 30))
        msgSurfObj = None
        if btn_mm:
            btn_mainmenu.fill((0,0,0))
            pygame.draw.rect(btn_mainmenu, (65, 65, 65), (3,3, 109, 24), 1)
            msgSurfObj = FONT_S.render("MAIN MENU", False,
                                       (255,255,255))
        else:
            btn_mainmenu.fill((255, 255, 255))
            pygame.draw.rect(btn_mainmenu, (190, 190, 190), (3,3, 109, 24), 1)
            msgSurfObj = FONT_S.render("MAIN MENU", False,
                                       (0,0,0))

        msgRectObj = msgSurfObj.get_rect()
        msgRectObj.center = btn_mainmenu.get_rect().center
        btn_mainmenu.blit(msgSurfObj, msgRectObj)

        btn_res_rect = btn_restart.get_rect()
        btn_res_rect.center = (150, 110)
        panel.blit(btn_restart, btn_res_rect)

        btn_mm_rect = btn_mainmenu.get_rect()
        btn_mm_rect.center = (150, 145)
        panel.blit(btn_mainmenu, btn_mm_rect)

        return panel.convert()

    def enter(self):
        if self.timer == False:
            self.timer = pygame.time.get_ticks()
        t = float(pygame.time.get_ticks() - self.timer)

        screen.blit(backgroundObj, (0,0))

        # Finish asteroid explosions
        for a in self.master.roids:
            if a.explode == False:
                a.explode = self.timer
            a.vely = 20
            a.draw()

        # Do animation
        panel = self.get_panel()
        if t > 500:
            panel_rect = panel.get_rect()
            panel_rect.center = (187, 300)
            screen.blit(panel, panel_rect)
            
            self.active = True
            self.timer = False
        else:
            panel = pygame.transform.rotozoom(panel, 0, t/500)
            panel_rect = panel.get_rect()
            panel_rect.center = (187, 100+ 200*t/500)
            screen.blit(panel, panel_rect)

    def update(self):
        if self.active:
            screen.blit(backgroundObj, (0,0))

            btn_res_rect = pygame.Rect((0,0),(115,30))
            btn_res_rect.center = (187, 310)
            btn_res_active = btn_res_rect.collidepoint(pygame.mouse.get_pos())

            btn_mm_rect = pygame.Rect((0,0),(115,30))
            btn_mm_rect.center = (187, 345)
            btn_mm_active = btn_mm_rect.collidepoint(pygame.mouse.get_pos())
            
            panel = self.get_panel(btn_res_active, btn_mm_active)

            panel_rect = panel.get_rect()
            panel_rect.center = (187, 300)

            screen.blit(panel, panel_rect)

            flag = pygame.mouse.get_pressed()[0]
            if flag:
                if btn_res_active:
                    self.master.goto(self.master.playingstate)

                elif btn_mm_active:
                    self.master.goto(self.master.mainmenustate)
                
        else: # Not finished timer state
            self.enter()
    def leave(self, state):
        self.master.points = 0
        self.active = False
        self.master._enter(state)

class PauseState(object):

    def __init__(self, master):
        self.master = master
        self.name = "PAUSED"
        self.active = False
        self.timer = False
        self.leaving = False
        self._nextstate = None

    def get_panel(self, btn_res=False, btn_mm=False):
        panel = pygame.Surface((300,200))
        panel.fill((127,127,127))
        pygame.draw.rect(panel, (65,65,65), panel.get_rect(), 5)
        
        msgSurfObj = FONT_M.render("PAUSED", False,
                                   (255,255,255))
        msgRectObj = msgSurfObj.get_rect()
        msgRectObj.center = (150, 50)
        panel.blit(msgSurfObj, msgRectObj)

        btn_resume = pygame.Surface((115, 30))
        msgSurfObj = None
        if btn_res:
            btn_resume.fill((0,0,0))
            pygame.draw.rect(btn_resume, (65, 65, 65), (3,3, 109, 24), 1)
            msgSurfObj = FONT_S.render("RESUME", False,
                                       (255,255,255))
        else:
            btn_resume.fill((255, 255, 255))
            pygame.draw.rect(btn_resume, (190, 190, 190), (3,3, 109, 24), 1)
            msgSurfObj = FONT_S.render("RESUME", False,
                                       (0,0,0))

        msgRectObj = msgSurfObj.get_rect()
        msgRectObj.center = btn_resume.get_rect().center
        btn_resume.blit(msgSurfObj, msgRectObj)

        btn_mainmenu = pygame.Surface((115, 30))
        msgSurfObj = None
        if btn_mm:
            btn_mainmenu.fill((0,0,0))
            pygame.draw.rect(btn_mainmenu, (65, 65, 65), (3,3, 109, 24), 1)
            msgSurfObj = FONT_S.render("MAIN MENU", False,
                                       (255,255,255))
        else:
            btn_mainmenu.fill((255, 255, 255))
            pygame.draw.rect(btn_mainmenu, (190, 190, 190), (3,3, 109, 24), 1)
            msgSurfObj = FONT_S.render("MAIN MENU", False,
                                       (0,0,0))

        msgRectObj = msgSurfObj.get_rect()
        msgRectObj.center = btn_mainmenu.get_rect().center
        btn_mainmenu.blit(msgSurfObj, msgRectObj)

        btn_resume_rect = btn_resume.get_rect()
        btn_resume_rect.center = (150, 110)
        panel.blit(btn_resume, btn_resume_rect)

        btn_mm_rect = btn_mainmenu.get_rect()
        btn_mm_rect.center = (150, 145)
        panel.blit(btn_mainmenu, btn_mm_rect)

        return panel.convert()    

    def enter(self):
        if self.timer == False:
            self.timer = pygame.time.get_ticks()
        t = float(pygame.time.get_ticks() - self.timer)

        screen.blit(backgroundObj, (0,0))

        # Do animation
        panel = self.get_panel()
        if t > 250:
            panel_rect = panel.get_rect()
            panel_rect.center = (187, 300)
            screen.blit(panel, panel_rect)
            
            self.active = True
            self.timer = False
        else:
            panel = pygame.transform.rotozoom(panel, 0, t/250)
            panel_rect = panel.get_rect()
            panel_rect.center = (187, 300)
            screen.blit(panel, panel_rect)

    def update(self):
        if self.active and not self.leaving:
            screen.blit(backgroundObj, (0,0))

            btn_res_rect = pygame.Rect((0,0),(115,30))
            btn_res_rect.center = (187, 310)
            btn_res_active = btn_res_rect.collidepoint(pygame.mouse.get_pos())

            btn_mm_rect = pygame.Rect((0,0),(115,30))
            btn_mm_rect.center = (187, 345)
            btn_mm_active = btn_mm_rect.collidepoint(pygame.mouse.get_pos())
            
            panel = self.get_panel(btn_res_active, btn_mm_active)

            panel_rect = panel.get_rect()
            panel_rect.center = (187, 300)

            screen.blit(panel, panel_rect)

            flag = pygame.mouse.get_pressed()[0]
            if flag:
                if btn_res_active:
                    self.master.goto(self.master.playingstate)

                elif btn_mm_active:
                    self.master.goto(self.master.mainmenustate)

            keys = pygame.key.get_pressed()
            if keys[K_ESCAPE]:
                self.master.goto(self.master.playingstate)
        elif self.leaving:
            self.leave(self._nextstate)
        else:
            self.enter()

    def leave(self, state):
        if not self.leaving:
            self.leaving = True
            self._nextstate = state
            self.timer = pygame.time.get_ticks()
        else:
            if self.timer == False:
                self.timer = pygame.time.get_ticks()
            t = float(pygame.time.get_ticks() - self.timer)

            screen.blit(backgroundObj, (0,0))

            # Do animation
            panel = self.get_panel()
            if t > 250:
                self.leaving = False
                self._nextstate = False
                self.active = False
                self.timer = False
                self.master._enter(state)
            else:
                panel = pygame.transform.rotozoom(panel, 0, (250-t)/250)
                panel_rect = panel.get_rect()
                panel_rect.center = (187, 300)
                screen.blit(panel, panel_rect)
            

class PlayingState(object):

    def __init__(self, master):
        self.master = master
        self.name = "PLAYING"
        self.active = False

    def enter(self):
        pygame.time.wait(250)
        self.active = True

    def update(self):
        if self.active:
            # Asteroid generation
            if self.master.newroid == 0:
                Asteroid(self.master, random.randint(0, 14)*25, random.randint(-5,5), random.randint(2,8))
                self.master.newroid = self.master.roidrate

            keys = pygame.key.get_pressed()
            # Keybindings
            if keys[K_ESCAPE]:
                self.master.goto(self.master.pausestate)
            if keys[K_UP]:
                self.master.roidrate /= 2
                if self.master.roidrate < 10:
                    self.master.roidrate = 10
            if keys[K_DOWN]:
                self.master.roidrate *= 2
            if keys[K_RETURN]:
                self.master.goto(self.master.gameoverstate)

            # Player movement
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
            msgSurfObj = FONT_S.render("SCORE: " + str(self.master.points), False, (255,255,255))
            msgRectObj = msgSurfObj.get_rect()
            msgRectObj.topleft = (3, 3)
            screen.blit(msgSurfObj, msgRectObj)

            # Decrease new asteroid timer
            self.master.newroid = max(self.master.newroid - fpsClock.get_time(), 0)

    def leave(self, state):
        self.active = False
        self.master._enter(state)


class GameManager(object):
    OPENING = 0
    GAMEPLAY = 1
    GAMEOVER = 2
    def __init__(self):
        self.points = 0
        self.bolts = []
        self.roids = []

        self.openingstate = OpeningState(self)
        self.mainmenustate = MainMenuState(self)
        self.playingstate = PlayingState(self)
        self.pausestate = PauseState(self)
        self.gameoverstate = GameOverState(self)

        self.player = Player(self)
        
        self.newroid = 0
        self.roidrate = 1000 # New asteroid every 1000 milliseconds

        self._state = self.openingstate
        self._state.enter()

    def update(self):
        if self._state:
            self._state.update()

    def get_state(self):
        return self._state.name
    
    def goto(self, state):
        self._state.leave(state)
        
    def _enter(self, state):
        self._state = state
        self._state.enter()
        

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
