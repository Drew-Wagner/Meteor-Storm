import random
import sys

import pygame
from pygame.locals import *

# Define Constants
WIDTH = 375
HEIGHT = 600
FPS = 30
PLAYER_MOVE_SPEED = 15

# Create lists to store sprites
ASTEROID_SPRITES = [] 

# Initialize Pygame and fpsClock
pygame.init()
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption("Meteor Storm - by Drew Wagner")
fpsClock = pygame.time.Clock()

# Loads and transforms asteroid sprites
def load_asteroids(num):
    """ Loads and transforms asteroid sprites

    Loads images from /images/asteroids/

    Args:
        num: An integer indicating how many sprites to load.
    """
    for i in range(num):
        # TODO(Drew) Stop if images don't exist
        s = pygame.image.load('images/asteroids/asteroid'+str(i+1)+'.png')
        s = pygame.transform.scale(s, (25, 25))
        ASTEROID_SPRITES.append(s)

# Load fonts
FONT_S = pygame.font.SysFont("Impact", 20)
FONT_M = pygame.font.SysFont("Impact", 28)
FONT_L = pygame.font.SysFont("Impact", 46)
FONT_XL = pygame.font.SysFont("Impact", 66)
FONT_MONO_M = pygame.font.SysFont("Courier", 28)

# Load background sprite - Image credit: GameArtGuppy.com
backgroundObj = pygame.image.load('images/space.png')

# Load and transform player sprites
# Image credit: simeontemplar.deviantart.com
playerSprite1 = pygame.image.load('images/spaceship/spaceship_1.gif')
playerSprite1 = pygame.transform.scale(playerSprite1, (75, 75))
playerSprite2 = pygame.image.load('images/spaceship/spaceship_2.gif')
playerSprite2 = pygame.transform.scale(playerSprite2, (75, 75))

# Load and transform bolt sprites
boltSprite1 = pygame.image.load('images/bolt.png')
boltSprite1 = pygame.transform.scale(boltSprite1, (50, 33))
boltSprite1 = pygame.transform.rotate(boltSprite1, 90)

# Load and transform heart
heartSprite = pygame.image.load('images/heart.png')
heartSprite = pygame.transform.scale(heartSprite, (28, 28))

# Load and transform asteroid sprites
load_asteroids(4)

class OpeningState(object):
    """Handles Opening Animation

    Leads to MainMenuState

    Attributes:
        master: the attached GameManager instance.
        name: "OPENING"
        active: Flag indicating whether the state is active
        timer: Counts ticks for animations
        prev: The previous state
        
    """
    def __init__(self, master):
        """Inits OpeningState"""
        self.master = master
        self.name = "OPENING"
        self.active = False
        self.timer = False
        self.prev = None

    def enter(self, prev):
        """Executed on entering the state

        Args:
            prev: the previous state
        """

        # Reset all gameplay variables
        self.prev = prev
        self.master.points = 0
        self.master.player.lives = 3

        # If this is the first time through
        if not self.timer:
            self.timer = pygame.time.get_ticks()
        dt = float(pygame.time.get_ticks() - self.timer)

        # Begin drawing animation
        screen.fill((0,0,0))
        gray = min(max(0,int(255*dt/500)), 255)
        lbl_meteorstorm = FONT_L.render("METEOR STORM", True,
                                         (gray,gray,gray))

        if dt > 500:
            if dt > 1000:
                # Finished entering state
                self.active = True
                self.timer = False
            else:
                rect_meteorstorm = lbl_meteorstorm.get_rect()
                rect_meteorstorm.center = (187, 300)
                screen.blit(lbl_meteorstorm, rect_meteorstorm)
        else:
            # Opening Animation
            lbl_meteorstorm = pygame.transform.rotozoom(
                lbl_meteorstorm, 0, dt/500)
            rect_meteorstorm = lbl_meteorstorm.get_rect()
            rect_meteorstorm.center = (187, 300)
            screen.blit(lbl_meteorstorm, rect_meteorstorm)

    def update(self):
        """State update"""
        if self.active:
            self.master.goto(self.master.mainmenustate)
        else: # State entry is not complete
            self.enter(self.prev)

    def leave(self, state):
        """State exit

        Args:
            state: Next state
        """
        self.active = False
        self.master._enter(state)

class MainMenuState(object):
    """Handles Main menu

    Has buttons leading to: PlayingState, LeaderBoardState,
    InstructionsState(Not yet implemented), and option to quit.
    
    Attributes:
        master: the attached GameManager instance.
        name: "MainMenu"
        active: Flag indicating whether the state is active
        timer: Counts ticks for animations
        prev: The previous state
    """
    _PLAY = (187, 250)
    _INST = (187, 310)
    _LEAD = (187, 370)
    _QUIT = (187, 430)
    def __init__(self, master):
        """Inits MainMenuState"""
        self.master = master
        self.name = "MAINMENU"
        self.active = False
        self.timer = False
        self.prev = None

    # TODO(Drew) Implement full overlay
    def black(self):
        """Returns Overlay from opening scene for fade-out"""
        black = pygame.Surface((WIDTH,HEIGHT))
        black.fill((0,0,0))

        return black.convert()

    def draw(self, btn_p=False, btn_ins=False, btn_l=False, btn_q=False):
        """Draws the menu

        Args:
            btn_p: Flag for play button mouseover
            btn_ins: Flag for instructions button mouseover
            btn_l: Flag for leader board button mouseover
            btn_q: Flag for quit button mouseover
        """
        # Draw background
        screen.blit(backgroundObj, (0,0))

        # Draw Title
        lbl_title_line_1 = FONT_XL.render("METEOR", True,
                                      (255,255,255))
        rect_title_line_1 = lbl_title_line_1.get_rect()
        rect_title_line_1.center = (187, 90)
        screen.blit(lbl_title_line_1, rect_title_line_1)
        lbl_title_line_2 = FONT_XL.render("STORM", True,
                                      (255,255,255))
        rect_title_line_2 = lbl_title_line_2.get_rect()
        rect_title_line_2.center = (187, 150)
        screen.blit(lbl_title_line_2, rect_title_line_2)

        # Draw Play button
        btn_play = pygame.Surface((300, 50))
        if btn_p:
            btn_play.fill((0,0,0))
            pygame.draw.rect(btn_play, (65, 65, 65), (6,6, 288, 38), 2)
            lbl_play = FONT_M.render("PLAY", True,
                                       (255,255,255))
        else:
            btn_play.fill((255, 255, 255))
            pygame.draw.rect(btn_play, (190, 190, 190), (6,6, 288, 38), 2)
            lbl_play = FONT_M.render("PLAY", True,
                                       (0,0,0))
        rect_lbl_play = lbl_play.get_rect()
        rect_lbl_play.center = btn_play.get_rect().center
        btn_play.blit(lbl_play, rect_lbl_play)

        rect_play = btn_play.get_rect()
        rect_play.center = self._PLAY
        screen.blit(btn_play, rect_play)

        # Draw Instructions button
        btn_instructions = pygame.Surface((300, 50))

        if btn_ins:
            btn_instructions.fill((0,0,0))
            pygame.draw.rect(btn_instructions, (65, 65, 65), (6,6, 288, 38), 2)
            lbl_instructions = FONT_M.render("INSTRUCTIONS", True,
                                       (255,255,255))
        else:
            btn_instructions.fill((255, 255, 255))
            pygame.draw.rect(btn_instructions, (190, 190, 190), (6,6, 288, 38), 2)
            lbl_instructions = FONT_M.render("INSTRUCTIONS", True,
                                       (0,0,0))
        rect_lbl_inst = lbl_instructions.get_rect()
        rect_lbl_inst.center = btn_instructions.get_rect().center
        btn_instructions.blit(lbl_instructions, rect_lbl_inst)

        rect_instructions = btn_instructions.get_rect()
        rect_instructions.center = self._INST
        screen.blit(btn_instructions, rect_instructions)

        # Draw Leaderboard button
        btn_lead = pygame.Surface((300, 50))
        msgSurfObj = None
        if btn_l:
            btn_lead.fill((0,0,0))
            pygame.draw.rect(btn_lead, (65, 65, 65), (6,6, 288, 38), 2)
            lbl_lead = FONT_M.render("LEADER BOARD", True,
                                       (255,255,255))
        else:
            btn_lead.fill((255, 255, 255))
            pygame.draw.rect(btn_lead, (190, 190, 190), (6,6, 288, 38), 2)
            lbl_lead = FONT_M.render("LEADER BOARD", True,
                                       (0,0,0))
        rect_lbl_lead = lbl_lead.get_rect()
        rect_lbl_lead.center = btn_lead.get_rect().center
        btn_lead.blit(lbl_lead, rect_lbl_lead)

        rect_lead = btn_lead.get_rect()
        rect_lead.center = self._LEAD
        screen.blit(btn_lead, rect_lead)

        # Draw QUIT button
        btn_quit = pygame.Surface((300, 50))
        if btn_q:
            btn_quit.fill((0,0,0))
            pygame.draw.rect(btn_quit, (65, 65, 65), (6,6, 288, 38), 2)
            lbl_quit = FONT_M.render("QUIT", True,
                                       (255,255,255))
        else:
            btn_quit.fill((255, 255, 255))
            pygame.draw.rect(btn_quit, (190, 190, 190), (6,6, 288, 38), 2)
            lbl_quit = FONT_M.render("QUIT", True,
                                       (0,0,0))
        rect_lbl_quit = lbl_quit.get_rect()
        rect_lbl_quit.center = btn_quit.get_rect().center
        btn_quit.blit(lbl_quit, rect_lbl_quit)

        rect_quit = btn_quit.get_rect()
        rect_quit.center = self._QUIT
        screen.blit(btn_quit, rect_quit)

        # Draw Signature
        lbl_sig = FONT_S.render("Created by Drew Wagner", True, (255,255,255))
        rect_sig = lbl_sig.get_rect()
        rect_sig.bottom = 600
        rect_sig.centerx = 187
        screen.blit(lbl_sig, rect_sig)

    def enter(self, prev):
        """Executed on entering state

        Args:
            prev: Previous state
        """
        self.prev = prev
        if not self.timer:
            self.timer = pygame.time.get_ticks()
        dt = float(pygame.time.get_ticks() - self.timer)

        # Begin drawing fade-in animation
        self.draw()
        black = self.black()
        black.set_alpha(int(max(255 - dt, 0)))

        screen.blit(black, (0,0))

        # Animation is finished
        if dt > 1000:
            self.active = True
            self.timer = False

    def update(self):
        """State update"""
        if self.active:
            # Set Rects for buttons and test for mouseover
            btn_play_rect = pygame.Rect((0,0),(300,50))
            btn_play_rect.center = self._PLAY
            btn_play_active = btn_play_rect.collidepoint(pygame.mouse.get_pos())

            btn_inst_rect = pygame.Rect((0,0),(300,50))
            btn_inst_rect.center = self._INST
            btn_inst_active = btn_inst_rect.collidepoint(pygame.mouse.get_pos())

            btn_lead_rect = pygame.Rect((0,0),(300,50))
            btn_lead_rect.center = self._LEAD
            btn_lead_active = btn_lead_rect.collidepoint(pygame.mouse.get_pos())
            
            btn_quit_rect = pygame.Rect((0,0),(300,50))
            btn_quit_rect.center = self._QUIT
            btn_quit_active = btn_quit_rect.collidepoint(pygame.mouse.get_pos())

            # Check for mouse click and go to appropriate states
            flag = pygame.mouse.get_pressed()[0]
            if flag:
                if btn_play_active:
                    self.master.goto(self.master.playingstate)
                elif btn_inst_active:
                    pass
                elif btn_lead_active:
                    self.master.goto(self.master.leaderboardstate)
                elif btn_quit_active:
                    # TODO goto exit state
                    pygame.quit()
                    sys.exit()
            
            self.draw(btn_play_active, btn_inst_active, btn_lead_active, btn_quit_active)
        else:
            self.enter(self.prev) # State entry is not complete

    def leave(self, state):
        """Exit state

        Args:
            state: Next state.
        """
        self.active = False
        self.master._enter(state)

class GameOverState(object):
    """ Handles game over

    Displays player score and high score on game over. Gives option to
    restart, or save the score.

    Attributes:
        master: the attached GameManager instance.
        name: "MainMenu"
        active: Flag indicating whether the state is active
        timer: Counts ticks for animations
        prev: The previous state
    """

    def __init__(self, master):
        """Inits GameOverState"""
        self.master = master
        self.name = "GAMEOVER"
        self.active = False
        self.timer = False
        self.prev = None

    def get_panel(self, btn_res=False, btn_ss=False, new_high=False):
        """Returns the surface for the gameover panel.

        Args:
            btn_res: Flag for resume button mouseover.
            btn_mm: Flag for save button mouseover.
            new_high: Flag for if score is a new highscore.
        """
        # Set the y coordinates for the title and highscore labels
        if new_high:
            _gameovery = 50
            _highscorey = 75
        else:
            _gameovery = 30
            _highscorey = 79

        # Create panel surface
        panel = pygame.Surface((300,200))
        panel.fill((127,127,127))
        pygame.draw.rect(panel, (65,65,65), panel.get_rect(), 5)
        
        lbl_gameover = FONT_M.render("GAME OVER", True,
                                   (255,255,255))
        rect_gameover = lbl_gameover.get_rect()
        rect_gameover.center = (150, _gameovery)
        panel.blit(lbl_gameover, rect_gameover)

        # Display score and/or (new) highscore
        if new_high:
            lbl_highscore = FONT_S.render("NEW HIGHSCORE: " + str(self.master.points), True,
                                       (255,255,255))
        else:
            lbl_highscore = FONT_S.render("HIGHSCORE: " + str(self.master.highscore), True,
                                       (255,255,255))
            lbl_score = FONT_S.render("SCORE: " + str(self.master.points), True,
                                       (255,255,255))
            rect_score = lbl_score.get_rect()
            rect_score.center = (150, 59)
            panel.blit(lbl_score, rect_score)
        rect_highscore = lbl_highscore.get_rect()
        rect_highscore.center = (150, _highscorey)
        panel.blit(lbl_highscore, rect_highscore)

        # Draw Restart button
        btn_restart = pygame.Surface((115, 30))
        if btn_res:
            btn_restart.fill((0,0,0))
            pygame.draw.rect(btn_restart, (65, 65, 65), (3,3, 109, 24), 1)
            lbl_restart = FONT_S.render("RESTART", True,
                                       (255,255,255))
        else:
            btn_restart.fill((255, 255, 255))
            pygame.draw.rect(btn_restart, (190, 190, 190), (3,3, 109, 24), 1)
            lbl_restart = FONT_S.render("RESTART", True,
                                       (0,0,0))

        rect_lbl_restart = lbl_restart.get_rect()
        rect_lbl_restart.center = btn_restart.get_rect().center
        btn_restart.blit(lbl_restart, rect_lbl_restart)

        rect_restart = btn_restart.get_rect()
        rect_restart.center = (150, 110)
        panel.blit(btn_restart, rect_restart)

        # Draw Save button
        btn_save = pygame.Surface((115, 30))
        if btn_ss:
            btn_save.fill((0,0,0))
            pygame.draw.rect(btn_save, (65, 65, 65), (3,3, 109, 24), 1)
            lbl_save = FONT_S.render("SAVE SCORE", True,
                                       (255,255,255))
        else:
            btn_save.fill((255, 255, 255))
            pygame.draw.rect(btn_save, (190, 190, 190), (3,3, 109, 24), 1)
            lbl_save = FONT_S.render("SAVE SCORE", True,
                                       (0,0,0))

        rect_lbl_save = lbl_save.get_rect()
        rect_lbl_save.center = btn_save.get_rect().center
        btn_save.blit(lbl_save, rect_lbl_save)

        rect_save = btn_save.get_rect()
        rect_save.center = (150, 145)
        panel.blit(btn_save, rect_save)

        # Convert panel to more efficient surface and return
        return panel.convert()

    def enter(self, prev):
        """Executes on entering the state

        Args:
            prev: Previous state
        """
        self.prev = prev
        if self.timer == False:
            self.timer = pygame.time.get_ticks()
        dt = float(pygame.time.get_ticks() - self.timer)

        screen.blit(backgroundObj, (0,0))

        # Explode remaining asteroids and player
        # TODO Explode player
        for a in self.master.roids:
            if a.explode == False:
                a.explode = self.timer
            a.vely = 20
            a.draw()

        # Do animation
        if self.master.points > self.master.highscore:
            new_high = True
        else:
            new_high = False
        panel = self.get_panel(new_high=new_high)

        if dt < 500:
            panel = pygame.transform.rotozoom(panel, 0, dt/500)
            panel_rect = panel.get_rect()
            panel_rect.center = (187, 100+ 200*dt/500)
            screen.blit(panel, panel_rect)
        # Finished entering
        else:
            panel_rect = panel.get_rect()
            panel_rect.center = (187, 300)
            screen.blit(panel, panel_rect)
            
            self.active = True
            self.timer = False 

    def update(self):
        """State update"""
        if self.active:
            # Draw background
            screen.blit(backgroundObj, (0,0))

            # Set Rects for buttons and check for mouseover
            btn_res_rect = pygame.Rect((0,0),(115,30))
            btn_res_rect.center = (187, 310)
            btn_res_active = btn_res_rect.collidepoint(pygame.mouse.get_pos())

            btn_mm_rect = pygame.Rect((0,0),(115,30))
            btn_mm_rect.center = (187, 345)
            btn_mm_active = btn_mm_rect.collidepoint(pygame.mouse.get_pos())

            # Test for new highscore
            if self.master.points > self.master.highscore:
                new_high = True
            else:
                new_high = False

            # Get and draw the panel
            panel = self.get_panel(btn_res_active, btn_mm_active, new_high)
            panel_rect = panel.get_rect()
            panel_rect.center = (187, 300)
            screen.blit(panel, panel_rect)

            # Check for mouse clicks and goto appropriate state
            flag = pygame.mouse.get_pressed()[0]
            if flag:
                if btn_res_active:
                    self.master.goto(self.master.playingstate)

                elif btn_mm_active:
                    self.master.goto(self.master.savescorestate)
                
        else:
            self.enter(self.prev) # State entry not complete
            
    def leave(self, state):
        """Handles state exit.

        Args:
            state: Next state.
        """
        # Pass score along to SaveScoreState
        if type(state) == SaveScoreState:
            state.points = self.master.points

        # Reset gameplay variables and goto next state
        self.master.points = 0
        self.master.player.lives = 3
        self.active = False
        self.master._enter(state)

class PauseState(object):
    """Handles pausing

    Attributes:
        master: the attached GameManager instance.
        name: "MainMenu"
        active: Flag indicating whether the state is active
        timer: Counts ticks for animations
        prev: The previous state
        leaving: Flag indicating whether the state is stopping
    """
    def __init__(self, master):
        """Inits PauseState"""
        self.master = master
        self.name = "PAUSED"
        self.active = False
        self.timer = False
        self.prev = None
        self.leaving = False
        self._nextstate = None

    def get_panel(self, btn_res=False, btn_mm=False):
        """Returns surface for pause screen panel

        Args:
            btn_res: Flag for resume button mouseover
            btn_mm: Flag for mainmenu button mouseover
        """

        # Create panel surface
        panel = pygame.Surface((300,200))
        panel.fill((127,127,127))
        pygame.draw.rect(panel, (65,65,65), panel.get_rect(), 5)

        # Draw title
        lbl_paused = FONT_M.render("PAUSED", True,
                                   (255,255,255))
        rect_paused = lbl_paused.get_rect()
        rect_paused.center = (150, 50)
        panel.blit(lbl_paused, rect_paused)

        # Draw resume button
        btn_resume = pygame.Surface((115, 30))
        if btn_res:
            btn_resume.fill((0,0,0))
            pygame.draw.rect(btn_resume, (65, 65, 65), (3,3, 109, 24), 1)
            lbl_resume = FONT_S.render("RESUME", True,
                                       (255,255,255))
        else:
            btn_resume.fill((255, 255, 255))
            pygame.draw.rect(btn_resume, (190, 190, 190), (3,3, 109, 24), 1)
            lbl_resume = FONT_S.render("RESUME", True,
                                       (0,0,0))

        rect_lbl_resume = lbl_resume.get_rect()
        rect_lbl_resume.center = lbl_resume.get_rect().center
        btn_resume.blit(lbl_resume, rect_lbl_resume)

        rect_resume = btn_resume.get_rect()
        rect_resume.center = (150, 110)
        panel.blit(btn_resume, rect_resume)

        # Draw mainmenu button
        btn_mainmenu = pygame.Surface((115, 30))
        if btn_mm:
            btn_mainmenu.fill((0,0,0))
            pygame.draw.rect(btn_mainmenu, (65, 65, 65), (3,3, 109, 24), 1)
            lbl_mainmenu = FONT_S.render("MAIN MENU", True,
                                       (255,255,255))
        else:
            btn_mainmenu.fill((255, 255, 255))
            pygame.draw.rect(btn_mainmenu, (190, 190, 190), (3,3, 109, 24), 1)
            lbl_mainmenu = FONT_S.render("MAIN MENU", True,
                                       (0,0,0))

        rect_lbl_mainmenu = lbl_mainmenu.get_rect()
        rect_lbl_mainmenu.center = btn_mainmenu.get_rect().center
        btn_mainmenu.blit(lbl_mainmenu, rect_label_mainmenu)

        rect_mainmenu = btn_mainmenu.get_rect()
        rect_mainmenu.center = (150, 145)
        panel.blit(btn_mainmenu, rect_mainmenu)

        return panel.convert()    

    def enter(self, prev):
        """Handles state entry

        Args:
            prev: Previous state
        """
        self.prev = prev
        if self.timer == False:
            self.timer = pygame.time.get_ticks()
        dt = float(pygame.time.get_ticks() - self.timer)

        # Draw background
        screen.blit(backgroundObj, (0,0))

        # Do animation
        panel = self.get_panel()
        if dt < 250:
            panel = pygame.transform.rotozoom(panel, 0, dt/250)
            panel_rect = panel.get_rect()
            panel_rect.center = (187, 300)
            screen.blit(panel, panel_rect)
        # State entry complete
        else:
            panel_rect = panel.get_rect()
            panel_rect.center = (187, 300)
            screen.blit(panel, panel_rect)
            
            self.active = True
            self.timer = False

    def update(self):
        """Handles state update"""
        if self.active and not self.leaving:
            # Draw background
            screen.blit(backgroundObj, (0,0))

            # Set Rects for buttons and check for mouseover
            btn_res_rect = pygame.Rect((0,0),(115,30))
            btn_res_rect.center = (187, 310)
            btn_res_active = btn_res_rect.collidepoint(pygame.mouse.get_pos())

            btn_mm_rect = pygame.Rect((0,0),(115,30))
            btn_mm_rect.center = (187, 345)
            btn_mm_active = btn_mm_rect.collidepoint(pygame.mouse.get_pos())

            # Get panel and draw
            panel = self.get_panel(btn_res_active, btn_mm_active)
            panel_rect = panel.get_rect()
            panel_rect.center = (187, 300)
            screen.blit(panel, panel_rect)

            # Check for mouseclicks and go to appropriate state
            flag = pygame.mouse.get_pressed()[0]
            if flag:
                if btn_res_active:
                    self.master.goto(self.master.playingstate)

                elif btn_mm_active:
                    self.master.goto(self.master.mainmenustate)

            # Resume on 'Escape' key press
            # TODO Convert to KEYDOWN event
            keys = pygame.key.get_pressed()
            if keys[K_ESCAPE]:
                self.master.goto(self.master.playingstate)
        elif self.leaving:
            self.leave(self._nextstate)
        else:
            self.enter(self.prev)

    def leave(self, state):
        """Handles state exit

        Args:
            state: Next state.
        """
        # Set timer for animation
        if not self.leaving:
            self.leaving = True
            self._nextstate = state
        else:
            if self.timer == False:
                self.timer = pygame.time.get_ticks()
            dt = float(pygame.time.get_ticks() - self.timer)

            # Draw background
            screen.blit(backgroundObj, (0,0))

            # Do animation
            panel = self.get_panel()
            if dt < 250:
                panel = pygame.transform.rotozoom(panel, 0, (250-dt)/250)
                panel_rect = panel.get_rect()
                panel_rect.center = (187, 300)
                screen.blit(panel, panel_rect)
            # State exit complete, go to next state
            else:
                self.leaving = False
                self._nextstate = False
                self.active = False
                self.timer = False
                self.master._enter(state)

class Input(object):
    """Rudimentary text entry object for pygame

    TODO Shift, Special Characters
    Attributes:
        maxwidth: Maximum number of characters
        font: Font used by the object
            Defaut - FONT_MONO_M
        text: text contained by the object
    """
    def __init__(self, maxwidth=10, font=FONT_MONO_M):
        self.maxwidth = maxwidth
        self.font = font
        self.text = ""

    # TODO Make text private and add getter
    def update(self):
        """Method for listening for key input"""
        keys_pressed = pygame.event.get(KEYDOWN)
        for event in keys_pressed:
            if len(self.text) < self.maxwidth:
                if event.key == K_a:
                    self.text += "a"
                elif event.key == K_b:
                    self.text += "b"
                elif event.key == K_c:
                    self.text += "c"
                elif event.key == K_d:
                    self.text += "d"
                elif event.key == K_e:
                    self.text += "e"
                elif event.key == K_f:
                    self.text += "f"
                elif event.key == K_g:
                    self.text += "g"
                elif event.key == K_h:
                    self.text += "h"
                elif event.key == K_i:
                    self.text += "i"
                elif event.key == K_j:
                    self.text += "j"
                elif event.key == K_k:
                    self.text += "k"
                elif event.key == K_l:
                    self.text += "l"
                elif event.key == K_m:
                    self.text += "m"
                elif event.key == K_n:
                    self.text += "n"
                elif event.key == K_o:
                    self.text += "o"
                elif event.key == K_p:
                    self.text += "p"
                elif event.key == K_q:
                    self.text += "q"
                elif event.key == K_r:
                    self.text += "r"
                elif event.key == K_s:
                    self.text += "s"
                elif event.key == K_t:
                    self.text += "t"
                elif event.key == K_u:
                    self.text += "u"
                elif event.key == K_v:
                    self.text += "v"
                elif event.key == K_w:
                    self.text += "w"
                elif event.key == K_x:
                    self.text += "x"
                elif event.key == K_y:
                    self.text += "y"
                elif event.key == K_z:
                    self.text += "z"
                elif event.key == K_SPACE:
                    self.text += " "
                elif event.key == K_0:
                    self.text += "0"
                elif event.key == K_1:
                    self.text += "1"
                elif event.key == K_2:
                    self.text += "2"
                elif event.key == K_3:
                    self.text += "3"
                elif event.key == K_4:
                    self.text += "4"
                elif event.key == K_5:
                    self.text += "5"
                elif event.key == K_6:
                    self.text += "6"
                elif event.key == K_7:
                    self.text += "7"
                elif event.key == K_8:
                    self.text += "8"
                elif event.key == K_9:
                    self.text += "9"
            if event.key == K_BACKSPACE:
                self.text = self.text[:-1]
        self.text = self.text.upper()

    # TODO Make this return a Surface for better flexibility
    def draw(self):
        """Draws the text entry box to the screen"""
        surf = pygame.Surface((170,self.font.get_height()))
        surf.fill((255,255,255))
        surf.blit(self.font.render(self.text, True, (0,0,0)), (0,0))
        surf_rect = surf.get_rect()
        surf_rect.center = (187, 300)
        pygame.draw.rect(surf, (65,65,65), surf_rect, 2)
        screen.blit(surf, surf_rect)

class SaveScoreState(object):
    def __init__(self, master):
        self.master = master
        self.prev = None
        self.name = "SAVESCORE"
        self.points = 0
        self.active = False
        self.input = Input()

    def get_panel(self, btn_s = False):
        panel = pygame.Surface((300, 200))
        panel.fill((127,127,127))
        pygame.draw.rect(panel, (65,65,65), panel.get_rect(), 5)

        msgSurfObj = FONT_M.render("SAVE SCORE", True,
                                   (255,255,255))
        msgRectObj = msgSurfObj.get_rect()
        msgRectObj.center = (150, 30)
        panel.blit(msgSurfObj, msgRectObj)

        btn_save = pygame.Surface((115, 30))
        msgSurfObj = None
        if btn_s:
            btn_save.fill((0,0,0))
            pygame.draw.rect(btn_save, (65, 65, 65), (3,3, 109, 24), 1)
            msgSurfObj = FONT_S.render("SAVE", True,
                                       (255,255,255))
        else:
            btn_save.fill((255, 255, 255))
            pygame.draw.rect(btn_save, (190, 190, 190), (3,3, 109, 24), 1)
            msgSurfObj = FONT_S.render("SAVE", True,
                                       (0,0,0))

        msgRectObj = msgSurfObj.get_rect()
        msgRectObj.center = btn_save.get_rect().center
        btn_save.blit(msgSurfObj, msgRectObj)

        btn_save_rect = btn_save.get_rect()
        btn_save_rect.center = (150, 150)
        panel.blit(btn_save, btn_save_rect)

        return panel.convert()
        
    def enter(self, prev):
        self.prev = prev
        self.active = True

    def update(self):
        if self.active:
            btn_save_rect = pygame.Rect((0,0),(115,30))
            btn_save_rect.center = (187, 350)
            btn_save_active = btn_save_rect.collidepoint(pygame.mouse.get_pos())
            
            panel = self.get_panel(btn_save_active)
            
            panel_rect = panel.get_rect()
            panel_rect.center = (187, 300)
            screen.blit(backgroundObj, (0,0))
            screen.blit(panel, panel_rect)

            self.input.update()
            self.input.draw()

            if btn_save_active and pygame.mouse.get_pressed()[0]:
                if self.input.text == "":
                    pass #Play sound
                else:
                    self.master.savenewscore(self.points, self.input.text)
                    self.master.goto(self.master.leaderboardstate)
            
        else:
            self.enter(self.prev)

    def leave(self, state):
        self.active = False
        self.master._enter(state)
        
class LeaderBoardState(object):
    def __init__(self, master):
        self.master = master
        self.prev = None
        self.name = "LEADERBOARD"
        self.active = False

    def get_panel(self, btn_b=False):
        panel = pygame.Surface((300, 500))
        panel.fill((127,127,127))
        pygame.draw.rect(panel, (65,65,65), panel.get_rect(), 3)

        msg = FONT_L.render("LEADER BOARD", True, (255,255,255))
        msg_rect = msg.get_rect()
        msg_rect.center = (150, 30)
        panel.blit(msg, msg_rect)

        sub_panel = pygame.Surface((240, 385))
        r = pygame.Rect((0, 0), (240, 35))
        for i in range(11):
            if i % 2 == 0:
                sub_panel.fill((240,240,240), r)
            else:
                sub_panel.fill((190,190,190), r)
            try:
                msg = FONT_S.render(self.master.scores[i][1], True, (0,0,0))
                msg_rect = msg.get_rect()
                msg_rect.centerx = 60
                msg_rect.centery = r.centery
                sub_panel.blit(msg, msg_rect)

                msg = FONT_S.render(str(self.master.scores[i][0]), True, (0,0,0))
                msg_rect = msg.get_rect()
                msg_rect.centerx = 180
                msg_rect.centery = r.centery
                sub_panel.blit(msg, msg_rect)
            except IndexError:
                pass
            r.top += 35
        pygame.draw.rect(sub_panel, (65, 65, 65), sub_panel.get_rect(), 2)
        sub_panel_rect = sub_panel.get_rect()
        sub_panel_rect.topleft = (30, 65)
        panel.blit(sub_panel, sub_panel_rect)

        btn_back = pygame.Surface((115, 30))
        msgSurfObj = None
        if btn_b:
            btn_back.fill((0,0,0))
            pygame.draw.rect(btn_back, (65, 65, 65), (3,3, 109, 24), 1)
            msgSurfObj = FONT_S.render("BACK", True,
                                       (255,255,255))
        else:
            btn_back.fill((255, 255, 255))
            pygame.draw.rect(btn_back, (190, 190, 190), (3,3, 109, 24), 1)
            msgSurfObj = FONT_S.render("BACK", True,
                                       (0,0,0))

        msgRectObj = msgSurfObj.get_rect()
        msgRectObj.center = btn_back.get_rect().center
        btn_back.blit(msgSurfObj, msgRectObj)

        btn_back_rect = btn_back.get_rect()
        btn_back_rect.center = (150, 473)
        panel.blit(btn_back, btn_back_rect)

        return panel.convert()
        
    def enter(self, prev):
        self.active = True
        self.prev = prev

    def update(self):
        if self.active:
            btn_back_rect = pygame.Rect((0,0), (115, 30))
            btn_back_rect.center = (187, 473+50)
            btn_back_active = btn_back_rect.collidepoint(pygame.mouse.get_pos())
            
            panel = self.get_panel(btn_back_active)
            
            panel_rect = panel.get_rect()
            panel_rect.center = (187, 300)

            screen.blit(backgroundObj, (0,0))
            screen.blit(panel, panel_rect)

            if btn_back_active and pygame.mouse.get_pressed()[0]:
                if self.prev:
                    if type(self.prev) == SaveScoreState:
                        self.master.goto(self.prev.prev)
                    else:
                        self.master.goto(self.prev)

        else:
            self.enter(self.prev)

    def leave(self, state):
        self.active = False
        self.master._enter(state)
            

class PlayingState(object):

    def __init__(self, master):
        self.master = master
        self.prev = None
        self.name = "PLAYING"
        self.active = False

    def drawlives(self, n):
        r = pygame.Rect((0, 0), (28, 28))
        r.right = WIDTH-2
        r.centery = 18
        for i in range(n):
            screen.blit(heartSprite, r)
            r.left -= 28

    def enter(self, prev):
        self.prev = prev
        pygame.time.wait(250)
        self.master.highscore = self.master.getHighScore()
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
                self.master.player.move(-PLAYER_MOVE_SPEED,0)
            if keys[K_RIGHT] or keys[K_d]:
                self.master.player.move(PLAYER_MOVE_SPEED, 0)

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

            # Render points
            msgSurfObj = FONT_M.render("SCORE: " + str(self.master.points), True, (255,255,255))
            msgRectObj = msgSurfObj.get_rect()
            msgRectObj.left = 3
            msgRectObj.top = 0
            screen.blit(msgSurfObj, msgRectObj)

            # Render lives
            lives = self.master.player.lives
            if lives > 0:
                self.drawlives(lives)
            else:
                self.master.goto(self.master.gameoverstate)

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
        self.savescorestate = SaveScoreState(self)
        self.leaderboardstate = LeaderBoardState(self)
        self.gameoverstate = GameOverState(self)

        self.player = Player(self)
        self.scores = []
        self.loadscores()
        self.highscore = self.getHighScore()
        self.newroid = 0
        self.roidrate = 1000 # New asteroid every 1000 milliseconds

        self._state = None
        self._enter(self.openingstate)

    def loadscores(self):
        self.scores = []
        with open("user_scores.txt", 'r') as f:
            lines = f.readlines()
            for l in lines:
                    l = l.split(',')
                    try:
                        self.scores.append((int(l[0]), l[1].strip('\n')))
                    except:
                        break

    def savenewscore(self, score, name):
        self.scores.append((score, name))
        self.scores.sort(key=lambda t: t[0], reverse=True)

        with open("user_scores.txt", 'w') as f:
            for l in self.scores:
                f.write(str(l[0])+','+l[1]+'\n')

    def getHighScore(self):
        if self.scores:
            return self.scores[0][0]
        else:
            return 0

    def update(self):
        if self._state:
            self._state.update()

    def get_state(self):
        return self._state.name
    
    def goto(self, state):
        self._state.leave(state)
        
    def _enter(self, state):
        prev = self._state
        self._state = state
        self._state.enter(prev)
        

class Player(object):
    def __init__(self, gm):
        self.gm = gm
        self.rect = pygame.Rect(150,513, 75, 75)
        self.lives = 3
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
        
        self._sprite = ASTEROID_SPRITES[random.randint(0, len(ASTEROID_SPRITES)-1)]

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
            self.gm.goto(self.gm.gameoverstate)

        for e in self.gm.bolts + self.gm.roids + [self.gm.player]:
            if type(e) == Bolt:
                if self.rect.colliderect(e.rect) and not self.explode:
                    self.explode = pygame.time.get_ticks()
                    self.gm.bolts.remove(e)
                    self.gm.points += 5
            elif type(e) == Asteroid and e != self and not self.explode:
                if self.rect.colliderect(e.rect):
                    # TODO Fix Choppiness
                    self.velx = -self.velx
                    e.velx = -e.velx
                    overlap = (self.rect.centerx-e.rect.centerx)/2
                    e.rect.centerx -= overlap
                    self.rect.centerx += overlap
            elif type(e) == Player:
                if self.rect.colliderect(e.rect) and not self.explode:
                    self.explode = pygame.time.get_ticks()
                    self.vely = -self.vely
                    self.gm.player.lives -= 1

        self.draw()

    def draw(self):
        screen.blit(self._sprite, self.rect)
            
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
