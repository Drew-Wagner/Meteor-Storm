import random
import sys

import pygame
from pygame.locals import *

# Define Constants
WIDTH = 375
HEIGHT = 600
FPS = 30
PLAYER_MOVE_SPEED = 15
ASTEROID_MAX_X = 5
ASTEROID_MAX_Y = 8
ASTEROID_MIN_Y = 2

# Create lists to store sprites
ASTEROID_SPRITES = []

# Initialize Pygame and fpsClock
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
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
        try:
            s = pygame.image.load('images/asteroids/asteroid' + str(i + 1) + '.png')
        except pygame.error:
            if ASTEROID_SPRITES:
                break
            else:
                raise Exception("Could not load asteroid sprites.")
        else:
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

    # noinspection PyMethodMayBeStatic
    def draw(self, dt):
        """Draws the opening animation"""
        # Begin drawing animation
        screen.fill((0, 0, 0))
        gray = min(max(0, int(255 * dt / 500)), 255)
        lbl_meteorstorm = FONT_L.render("METEOR STORM", True,
                                        (gray, gray, gray))

        # Opening fade-in animation
        if dt < 500:
            lbl_meteorstorm = pygame.transform.rotozoom(
                lbl_meteorstorm, 0, dt / 500)
            rect_meteorstorm = lbl_meteorstorm.get_rect()
            rect_meteorstorm.center = (187, 300)
            screen.blit(lbl_meteorstorm, rect_meteorstorm)
        # Fade-in complete
        else:
            rect_meteorstorm = lbl_meteorstorm.get_rect()
            rect_meteorstorm.center = (187, 300)
            screen.blit(lbl_meteorstorm, rect_meteorstorm)

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

        if dt > 1000:
            # Finished entering state
            self.active = True
            self.timer = False
        else:
            self.draw(dt)

    def update(self):
        """State update"""
        if self.active:
            self.master.goto(self.master.mainmenustate)
        else:  # State entry is not complete
            self.enter(self.prev)

    # noinspection PyProtectedMember
    def leave(self, state):
        """State exit

        Args:
            state: Next state
        """
        self.active = False
        # noinspection PyProtectedMember
        self.master._enter(state)


class MainMenuState(object):
    """Handles Main menu

    Has buttons leading to: PlayingState, LeaderBoardState,
    InstructionsState(Not yet implemented), and option to quit.
    
    Attributes:
        master: the attached GameManager instance.
        name: "MAINMENU"
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

    # noinspection PyMethodMayBeStatic
    def black(self):
        """Returns Overlay from opening scene for fade-out"""
        black = pygame.Surface((WIDTH, HEIGHT))
        black.fill((0, 0, 0))

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
        screen.blit(backgroundObj, (0, 0))

        # Draw Title
        lbl_title_line_1 = FONT_XL.render("METEOR", True,
                                          (255, 255, 255))
        rect_title_line_1 = lbl_title_line_1.get_rect()
        rect_title_line_1.center = (187, 90)
        screen.blit(lbl_title_line_1, rect_title_line_1)
        lbl_title_line_2 = FONT_XL.render("STORM", True,
                                          (255, 255, 255))
        rect_title_line_2 = lbl_title_line_2.get_rect()
        rect_title_line_2.center = (187, 150)
        screen.blit(lbl_title_line_2, rect_title_line_2)

        # Draw Play button
        btn_play = pygame.Surface((300, 50))
        if btn_p:
            btn_play.fill((0, 0, 0))
            pygame.draw.rect(btn_play, (65, 65, 65), (6, 6, 288, 38), 2)
            lbl_play = FONT_M.render("PLAY", True,
                                     (255, 255, 255))
        else:
            btn_play.fill((255, 255, 255))
            pygame.draw.rect(btn_play, (190, 190, 190), (6, 6, 288, 38), 2)
            lbl_play = FONT_M.render("PLAY", True,
                                     (0, 0, 0))
        rect_lbl_play = lbl_play.get_rect()
        rect_lbl_play.center = btn_play.get_rect().center
        btn_play.blit(lbl_play, rect_lbl_play)

        rect_play = btn_play.get_rect()
        rect_play.center = self._PLAY
        screen.blit(btn_play, rect_play)

        # Draw Instructions button
        btn_instructions = pygame.Surface((300, 50))

        if btn_ins:
            btn_instructions.fill((0, 0, 0))
            pygame.draw.rect(btn_instructions, (65, 65, 65), (6, 6, 288, 38), 2)
            lbl_instructions = FONT_M.render("INSTRUCTIONS", True,
                                             (255, 255, 255))
        else:
            btn_instructions.fill((255, 255, 255))
            pygame.draw.rect(btn_instructions, (190, 190, 190), (6, 6, 288, 38), 2)
            lbl_instructions = FONT_M.render("INSTRUCTIONS", True,
                                             (0, 0, 0))
        rect_lbl_inst = lbl_instructions.get_rect()
        rect_lbl_inst.center = btn_instructions.get_rect().center
        btn_instructions.blit(lbl_instructions, rect_lbl_inst)

        rect_instructions = btn_instructions.get_rect()
        rect_instructions.center = self._INST
        screen.blit(btn_instructions, rect_instructions)

        # Draw Leaderboard button
        btn_lead = pygame.Surface((300, 50))
        if btn_l:
            btn_lead.fill((0, 0, 0))
            pygame.draw.rect(btn_lead, (65, 65, 65), (6, 6, 288, 38), 2)
            lbl_lead = FONT_M.render("LEADER BOARD", True,
                                     (255, 255, 255))
        else:
            btn_lead.fill((255, 255, 255))
            pygame.draw.rect(btn_lead, (190, 190, 190), (6, 6, 288, 38), 2)
            lbl_lead = FONT_M.render("LEADER BOARD", True,
                                     (0, 0, 0))
        rect_lbl_lead = lbl_lead.get_rect()
        rect_lbl_lead.center = btn_lead.get_rect().center
        btn_lead.blit(lbl_lead, rect_lbl_lead)

        rect_lead = btn_lead.get_rect()
        rect_lead.center = self._LEAD
        screen.blit(btn_lead, rect_lead)

        # Draw QUIT button
        btn_quit = pygame.Surface((300, 50))
        if btn_q:
            btn_quit.fill((0, 0, 0))
            pygame.draw.rect(btn_quit, (65, 65, 65), (6, 6, 288, 38), 2)
            lbl_quit = FONT_M.render("QUIT", True,
                                     (255, 255, 255))
        else:
            btn_quit.fill((255, 255, 255))
            pygame.draw.rect(btn_quit, (190, 190, 190), (6, 6, 288, 38), 2)
            lbl_quit = FONT_M.render("QUIT", True,
                                     (0, 0, 0))
        rect_lbl_quit = lbl_quit.get_rect()
        rect_lbl_quit.center = btn_quit.get_rect().center
        btn_quit.blit(lbl_quit, rect_lbl_quit)

        rect_quit = btn_quit.get_rect()
        rect_quit.center = self._QUIT
        screen.blit(btn_quit, rect_quit)

        # Draw Signature
        lbl_sig = FONT_S.render("Created by Drew Wagner", True, (255, 255, 255))
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

        screen.blit(black, (0, 0))

        # Animation is finished
        if dt > 1000:
            self.active = True
            self.timer = False

    def update(self):
        """State update"""
        if self.active:
            # Set Rects for buttons and test for mouseover
            btn_play_rect = pygame.Rect((0, 0), (300, 50))
            btn_play_rect.center = self._PLAY
            btn_play_active = btn_play_rect.collidepoint(pygame.mouse.get_pos())

            btn_inst_rect = pygame.Rect((0, 0), (300, 50))
            btn_inst_rect.center = self._INST
            btn_inst_active = btn_inst_rect.collidepoint(pygame.mouse.get_pos())

            btn_lead_rect = pygame.Rect((0, 0), (300, 50))
            btn_lead_rect.center = self._LEAD
            btn_lead_active = btn_lead_rect.collidepoint(pygame.mouse.get_pos())

            btn_quit_rect = pygame.Rect((0, 0), (300, 50))
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
                    # TODO goto quit state once QuitState is implemented
                    pygame.quit()
                    sys.exit()

            self.draw(btn_play_active, btn_inst_active, btn_lead_active, btn_quit_active)
        else:
            self.enter(self.prev)  # State entry is not complete

    def leave(self, state):
        """Exit state

        Args:
            state: Next state.
        """
        self.active = False
        # noinspection PyProtectedMember
        self.master._enter(state)


class GameOverState(object):
    """ Handles game over

    Displays player score and high score on game over. Gives option to
    restart, or save the score.

    Attributes:
        master: the attached GameManager instance.
        name: "GAMEOVER"
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
            btn_ss: Flag for save button mouseover.
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
        panel = pygame.Surface((300, 200))
        panel.fill((127, 127, 127))
        pygame.draw.rect(panel, (65, 65, 65), panel.get_rect(), 5)

        lbl_gameover = FONT_M.render("GAME OVER", True,
                                     (255, 255, 255))
        rect_gameover = lbl_gameover.get_rect()
        rect_gameover.center = (150, _gameovery)
        panel.blit(lbl_gameover, rect_gameover)

        # Display score and/or (new) highscore
        if new_high:
            lbl_highscore = FONT_S.render("NEW HIGHSCORE: " + str(self.master.points), True,
                                          (255, 255, 255))
        else:
            lbl_highscore = FONT_S.render("HIGHSCORE: " + str(self.master.highscore), True,
                                          (255, 255, 255))
            lbl_score = FONT_S.render("SCORE: " + str(self.master.points), True,
                                      (255, 255, 255))
            rect_score = lbl_score.get_rect()
            rect_score.center = (150, 59)
            panel.blit(lbl_score, rect_score)
        rect_highscore = lbl_highscore.get_rect()
        rect_highscore.center = (150, _highscorey)
        panel.blit(lbl_highscore, rect_highscore)

        # Draw Restart button
        btn_restart = pygame.Surface((115, 30))
        if btn_res:
            btn_restart.fill((0, 0, 0))
            pygame.draw.rect(btn_restart, (65, 65, 65), (3, 3, 109, 24), 1)
            lbl_restart = FONT_S.render("RESTART", True,
                                        (255, 255, 255))
        else:
            btn_restart.fill((255, 255, 255))
            pygame.draw.rect(btn_restart, (190, 190, 190), (3, 3, 109, 24), 1)
            lbl_restart = FONT_S.render("RESTART", True,
                                        (0, 0, 0))

        rect_lbl_restart = lbl_restart.get_rect()
        rect_lbl_restart.center = btn_restart.get_rect().center
        btn_restart.blit(lbl_restart, rect_lbl_restart)

        rect_restart = btn_restart.get_rect()
        rect_restart.center = (150, 110)
        panel.blit(btn_restart, rect_restart)

        # Draw Save button
        btn_save = pygame.Surface((115, 30))
        if btn_ss:
            btn_save.fill((0, 0, 0))
            pygame.draw.rect(btn_save, (65, 65, 65), (3, 3, 109, 24), 1)
            lbl_save = FONT_S.render("SAVE SCORE", True,
                                     (255, 255, 255))
        else:
            btn_save.fill((255, 255, 255))
            pygame.draw.rect(btn_save, (190, 190, 190), (3, 3, 109, 24), 1)
            lbl_save = FONT_S.render("SAVE SCORE", True,
                                     (0, 0, 0))

        rect_lbl_save = lbl_save.get_rect()
        rect_lbl_save.center = btn_save.get_rect().center
        btn_save.blit(lbl_save, rect_lbl_save)

        rect_save = btn_save.get_rect()
        rect_save.center = (150, 145)
        panel.blit(btn_save, rect_save)

        # Convert panel to more efficient surface and return
        return panel.convert()

    def draw_entry(self, dt):
        """Draws entry animation"""
        screen.blit(backgroundObj, (0, 0))

        # Explode remaining asteroids and player
        for a in self.master.roids:
            if not a.explode:
                a.explode = self.timer
            a.vely = 20
            a.draw()
        if self.prev is not self.master.leaderboardstate:
            if not self.master.player.explode:
                self.master.player.explode = self.timer
            self.master.player.draw()

        # Do animation
        if self.master.points > self.master.highscore:
            new_high = True
        else:
            new_high = False
        panel = self.get_panel(new_high=new_high)
        if dt < 500:
            panel = pygame.transform.rotozoom(panel, 0, dt / 500)
            panel_rect = panel.get_rect()
            panel_rect.center = (187, 100 + 200 * dt / 500)
            screen.blit(panel, panel_rect)
        else:
            panel_rect = panel.get_rect()
            panel_rect.center = (187, 300)
            screen.blit(panel, panel_rect)

    def enter(self, prev):
        """Executes on entering the state

        Args:
            prev: Previous state
        """
        self.prev = prev
        if not self.timer:
            self.timer = pygame.time.get_ticks()
        dt = float(pygame.time.get_ticks() - self.timer)

        if dt > 500:
            self.master.player.explode = False
            self.active = True
            self.timer = False
        else:
            self.draw_entry(dt)

    def update(self):
        """State update"""
        if self.active:
            # Draw background
            screen.blit(backgroundObj, (0, 0))

            # Set Rects for buttons and check for mouseover
            btn_res_rect = pygame.Rect((0, 0), (115, 30))
            btn_res_rect.center = (187, 310)
            btn_res_active = btn_res_rect.collidepoint(pygame.mouse.get_pos())

            btn_mm_rect = pygame.Rect((0, 0), (115, 30))
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
            self.enter(self.prev)  # State entry not complete

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
        # noinspection PyProtectedMember
        self.master._enter(state)


class PauseState(object):
    """Handles pausing

    Attributes:
        master: the attached GameManager instance.
        name: "PAUSED"
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

    # noinspection PyMethodMayBeStatic
    def get_panel(self, btn_res=False, btn_mm=False):
        """Returns surface for pause screen panel

        Args:
            btn_res: Flag for resume button mouseover
            btn_mm: Flag for mainmenu button mouseover
        """

        # Create panel surface
        panel = pygame.Surface((300, 200))
        panel.fill((127, 127, 127))
        pygame.draw.rect(panel, (65, 65, 65), panel.get_rect(), 5)

        # Draw title
        lbl_paused = FONT_M.render("PAUSED", True,
                                   (255, 255, 255))
        rect_paused = lbl_paused.get_rect()
        rect_paused.center = (150, 50)
        panel.blit(lbl_paused, rect_paused)

        # Draw resume button
        btn_resume = pygame.Surface((115, 30))
        if btn_res:
            btn_resume.fill((0, 0, 0))
            pygame.draw.rect(btn_resume, (65, 65, 65), (3, 3, 109, 24), 1)
            lbl_resume = FONT_S.render("RESUME", True,
                                       (255, 255, 255))
        else:
            btn_resume.fill((255, 255, 255))
            pygame.draw.rect(btn_resume, (190, 190, 190), (3, 3, 109, 24), 1)
            lbl_resume = FONT_S.render("RESUME", True,
                                       (0, 0, 0))

        rect_lbl_resume = lbl_resume.get_rect()
        rect_lbl_resume.center = btn_resume.get_rect().center
        btn_resume.blit(lbl_resume, rect_lbl_resume)

        rect_resume = btn_resume.get_rect()
        rect_resume.center = (150, 110)
        panel.blit(btn_resume, rect_resume)

        # Draw mainmenu button
        btn_mainmenu = pygame.Surface((115, 30))
        if btn_mm:
            btn_mainmenu.fill((0, 0, 0))
            pygame.draw.rect(btn_mainmenu, (65, 65, 65), (3, 3, 109, 24), 1)
            lbl_mainmenu = FONT_S.render("MAIN MENU", True,
                                         (255, 255, 255))
        else:
            btn_mainmenu.fill((255, 255, 255))
            pygame.draw.rect(btn_mainmenu, (190, 190, 190), (3, 3, 109, 24), 1)
            lbl_mainmenu = FONT_S.render("MAIN MENU", True,
                                         (0, 0, 0))

        rect_lbl_mainmenu = lbl_mainmenu.get_rect()
        rect_lbl_mainmenu.center = btn_mainmenu.get_rect().center
        btn_mainmenu.blit(lbl_mainmenu, rect_lbl_mainmenu)

        rect_mainmenu = btn_mainmenu.get_rect()
        rect_mainmenu.center = (150, 145)
        panel.blit(btn_mainmenu, rect_mainmenu)

        return panel.convert()

    def draw_entry(self, dt):
        """Draws entry animation"""
        # Draw background
        screen.blit(backgroundObj, (0, 0))

        # Do animation
        panel = self.get_panel()

        if dt < 250:
            panel = pygame.transform.rotozoom(panel, 0, dt / 250)
            panel_rect = panel.get_rect()
            panel_rect.center = (187, 300)
            screen.blit(panel, panel_rect)
        else:
            panel_rect = panel.get_rect()
            panel_rect.center = (187, 300)
            screen.blit(panel, panel_rect)

    def draw_exit(self, dt):
        """Draws exit animation"""
        # Draw background
        screen.blit(backgroundObj, (0, 0))

        # Do animation
        panel = self.get_panel()
        if dt < 250:
            panel = pygame.transform.rotozoom(panel, 0, (250 - dt) / 250)
            panel_rect = panel.get_rect()
            panel_rect.center = (187, 300)
            screen.blit(panel, panel_rect)

    def enter(self, prev):
        """Handles state entry

        Args:
            prev: Previous state
        """
        self.prev = prev
        if not self.timer:
            self.timer = pygame.time.get_ticks()
        dt = float(pygame.time.get_ticks() - self.timer)

        if dt > 250:
            self.active = True
            self.timer = False
        else:
            self.draw_entry(dt)

    def update(self):
        """Handles state update"""
        if self.active and not self.leaving:
            # Draw background
            screen.blit(backgroundObj, (0, 0))

            # Set Rects for buttons and check for mouseover
            btn_res_rect = pygame.Rect((0, 0), (115, 30))
            btn_res_rect.center = (187, 310)
            btn_res_active = btn_res_rect.collidepoint(pygame.mouse.get_pos())

            btn_mm_rect = pygame.Rect((0, 0), (115, 30))
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
            keys_pressed = pygame.event.get(KEYDOWN)
            for e in keys_pressed:
                if e.key == K_ESCAPE:
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
            if not self.timer:
                self.timer = pygame.time.get_ticks()
            dt = float(pygame.time.get_ticks() - self.timer)

            if dt > 250:
                self.leaving = False
                self._nextstate = False
                self.active = False
                self.timer = False
                # noinspection PyProtectedMember
                self.master._enter(state)
            else:
                self.draw_exit(dt)


class Input(object):
    """Rudimentary text entry object for pygame

    TODO Shift, Special characters, Improve speed
    Attributes:
        maxwidth: Maximum number of characters
        font: Font used by the object
            Defaut - FONT_MONO_M
        _text: text contained by the object
    """

    def __init__(self, maxwidth=10, font=FONT_MONO_M):
        self.maxwidth = maxwidth
        self.font = font
        self._text = ""

    def get_text(self):
        """Getter for self._text"""
        return self._text

    def update(self):
        """Method for listening for key input"""
        keys_pressed = pygame.event.get(KEYDOWN)
        for e in keys_pressed:
            if len(self._text) < self.maxwidth:
                if e.key == K_a:
                    self._text += "a"
                elif e.key == K_b:
                    self._text += "b"
                elif e.key == K_c:
                    self._text += "c"
                elif e.key == K_d:
                    self._text += "d"
                elif e.key == K_e:
                    self._text += "e"
                elif e.key == K_f:
                    self._text += "f"
                elif e.key == K_g:
                    self._text += "g"
                elif e.key == K_h:
                    self._text += "h"
                elif e.key == K_i:
                    self._text += "i"
                elif e.key == K_j:
                    self._text += "j"
                elif e.key == K_k:
                    self._text += "k"
                elif e.key == K_l:
                    self._text += "l"
                elif e.key == K_m:
                    self._text += "m"
                elif e.key == K_n:
                    self._text += "n"
                elif e.key == K_o:
                    self._text += "o"
                elif e.key == K_p:
                    self._text += "p"
                elif e.key == K_q:
                    self._text += "q"
                elif e.key == K_r:
                    self._text += "r"
                elif e.key == K_s:
                    self._text += "s"
                elif e.key == K_t:
                    self._text += "t"
                elif e.key == K_u:
                    self._text += "u"
                elif e.key == K_v:
                    self._text += "v"
                elif e.key == K_w:
                    self._text += "w"
                elif e.key == K_x:
                    self._text += "x"
                elif e.key == K_y:
                    self._text += "y"
                elif e.key == K_z:
                    self._text += "z"
                elif e.key == K_SPACE:
                    self._text += " "
                elif e.key == K_0:
                    self._text += "0"
                elif e.key == K_1:
                    self._text += "1"
                elif e.key == K_2:
                    self._text += "2"
                elif e.key == K_3:
                    self._text += "3"
                elif e.key == K_4:
                    self._text += "4"
                elif e.key == K_5:
                    self._text += "5"
                elif e.key == K_6:
                    self._text += "6"
                elif e.key == K_7:
                    self._text += "7"
                elif e.key == K_8:
                    self._text += "8"
                elif e.key == K_9:
                    self._text += "9"
            if e.key == K_BACKSPACE:
                self._text = self._text[:-1]
        self._text = self._text.upper()

    def get_surface(self):
        """Returns text entry surface"""
        surf = pygame.Surface((170, self.font.get_height()))
        surf.fill((255, 255, 255))
        pygame.draw.rect(surf, (65, 65, 65), surf.get_rect(), 2)
        surf.blit(self.font.render(self.get_text(), True, (0, 0, 0)), (0, 0))
        return surf.convert()


class SaveScoreState(object):
    # noinspection PyUnresolvedReferences
    """Handles save score interface

        Attributes:
            master: the attached GameManager instance.
            name: "SAVESCORE"
            active: Flag indicating whether the state is active
            timer: Counts ticks for animations (Currently unused)
            prev: The previous state
        """

    def __init__(self, master):
        """Inits SaveScoreState"""
        self.master = master
        self.prev = None
        self.name = "SAVESCORE"
        self.points = 0
        self.active = False
        self.input = Input()

    def get_panel(self, btn_s=False):
        """Returns panel surface

        Args:
            btn_s: Flag for save button mouseover.
        """
        # Create and draw panel surface
        panel = pygame.Surface((300, 200))
        panel.fill((127, 127, 127))
        pygame.draw.rect(panel, (65, 65, 65), panel.get_rect(), 5)

        # Draw title
        lbl_save = FONT_M.render("SAVE SCORE", True,
                                 (255, 255, 255))
        rect_lbl_save = lbl_save.get_rect()
        rect_lbl_save.center = (150, 30)
        panel.blit(lbl_save, rect_lbl_save)

        # Draw save button
        btn_save = pygame.Surface((115, 30))
        if btn_s:
            btn_save.fill((0, 0, 0))
            pygame.draw.rect(btn_save, (65, 65, 65), (3, 3, 109, 24), 1)
            lbl_save = FONT_S.render("SAVE", True,
                                     (255, 255, 255))
        else:
            btn_save.fill((255, 255, 255))
            pygame.draw.rect(btn_save, (190, 190, 190), (3, 3, 109, 24), 1)
            lbl_save = FONT_S.render("SAVE", True,
                                     (0, 0, 0))

        rect_lbl_save = lbl_save.get_rect()
        rect_lbl_save.center = btn_save.get_rect().center
        btn_save.blit(lbl_save, rect_lbl_save)

        rect_save = btn_save.get_rect()
        rect_save.center = (150, 150)
        panel.blit(btn_save, rect_save)

        input_ = self.input.get_surface()
        rect_input = input_.get_rect()
        rect_input.center = (150, 100)
        panel.blit(input_, rect_input)

        return panel.convert()

    def enter(self, prev):
        """Handles state entry

        Args:
            prev: Previous state.
        """
        self.prev = prev
        self.active = True

    def update(self):
        """State update"""
        if self.active:
            # Set Rect for save button and check for mouseover
            btn_save_rect = pygame.Rect((0, 0), (115, 30))
            btn_save_rect.center = (187, 350)
            btn_save_active = btn_save_rect.collidepoint(pygame.mouse.get_pos())

            # Update text entry
            self.input.update()

            # Draw background
            screen.blit(backgroundObj, (0, 0))

            # Get and draw panel
            panel = self.get_panel(btn_save_active)
            panel_rect = panel.get_rect()
            panel_rect.center = (187, 300)
            screen.blit(panel, panel_rect)

            # Check for mouse click and go to appropriate state
            if btn_save_active and pygame.mouse.get_pressed()[0]:
                if not self.input.get_text():
                    pass  # TODO Play sound and/or animation
                else:
                    self.master.save_new_score(self.points, self.input.get_text())
                    self.master.goto(self.master.leaderboardstate)

        else:
            self.enter(self.prev)

    def leave(self, state):
        """Handles state exit
        Args:
            state: Next state.
        """
        self.active = False
        # noinspection PyProtectedMember
        self.master._enter(state)


class LeaderBoardState(object):
    """Handles the leaderboard

    Displays the top 11 scores. Back button returns to previous state.
    Attributes:
        master: the attached GameManager instance.
        name: "LEADERBOARD"
        active: Flag indicating whether the state is active
        timer: Counts ticks for animations
        prev: The previous state
    """

    def __init__(self, master):
        """Inits LeaderBoardState"""
        self.master = master
        self.name = "LEADERBOARD"
        self.active = False
        self.timer = False
        self.prev = None

    def get_panel(self, btn_b=False):
        """Returns panel surface

        Args:
            btn_b: Flag for back button mouseover.
        """
        # Create and draw panel
        panel = pygame.Surface((300, 500))
        panel.fill((127, 127, 127))
        pygame.draw.rect(panel, (65, 65, 65), panel.get_rect(), 3)

        # Draw title
        msg = FONT_L.render("LEADER BOARD", True, (255, 255, 255))
        msg_rect = msg.get_rect()
        msg_rect.center = (150, 30)
        panel.blit(msg, msg_rect)

        # Create and draw subpanel to display scores
        sub_panel = pygame.Surface((240, 385))
        r = pygame.Rect((0, 0), (240, 35))
        for i in range(11):
            if i % 2 == 0:
                sub_panel.fill((240, 240, 240), r)
            else:
                sub_panel.fill((190, 190, 190), r)
            try:
                msg = FONT_S.render(self.master.scores[i][1], True, (0, 0, 0))
                msg_rect = msg.get_rect()
                msg_rect.centerx = 60
                msg_rect.centery = r.centery
                sub_panel.blit(msg, msg_rect)

                msg = FONT_S.render(str(self.master.scores[i][0]), True, (0, 0, 0))
                msg_rect = msg.get_rect()
                msg_rect.centerx = 180
                msg_rect.centery = r.centery
                sub_panel.blit(msg, msg_rect)
            except IndexError:
                # There are less than 11 saved scores, but we continue the loop
                # and draw blank spaces
                pass
            r.top += 35
        pygame.draw.rect(sub_panel, (65, 65, 65), sub_panel.get_rect(), 2)
        sub_panel_rect = sub_panel.get_rect()
        sub_panel_rect.topleft = (30, 65)
        panel.blit(sub_panel, sub_panel_rect)

        # Draw back button
        btn_back = pygame.Surface((115, 30))
        if btn_b:
            btn_back.fill((0, 0, 0))
            pygame.draw.rect(btn_back, (65, 65, 65), (3, 3, 109, 24), 1)
            lbl_back = FONT_S.render("BACK", True,
                                     (255, 255, 255))
        else:
            btn_back.fill((255, 255, 255))
            pygame.draw.rect(btn_back, (190, 190, 190), (3, 3, 109, 24), 1)
            lbl_back = FONT_S.render("BACK", True,
                                     (0, 0, 0))

        rect_lbl_back = lbl_back.get_rect()
        rect_lbl_back.center = btn_back.get_rect().center
        btn_back.blit(lbl_back, rect_lbl_back)

        rect_back = btn_back.get_rect()
        rect_back.center = (150, 473)
        panel.blit(btn_back, rect_back)

        return panel.convert()

    def enter(self, prev):
        """Handles state entry

        Args:
            prev: Previous state
        """
        self.active = True
        self.prev = prev

    def update(self):
        """Handles state update"""
        if self.active:
            # Set Rect for back button and check for mouseover
            btn_back_rect = pygame.Rect((0, 0), (115, 30))
            btn_back_rect.center = (187, 473 + 50)
            btn_back_active = btn_back_rect.collidepoint(pygame.mouse.get_pos())

            # Draw background
            screen.blit(backgroundObj, (0, 0))

            # Get and draw panel
            panel = self.get_panel(btn_back_active)
            panel_rect = panel.get_rect()
            panel_rect.center = (187, 300)
            screen.blit(panel, panel_rect)

            # Check for mouse click and go to previous state
            if btn_back_active and pygame.mouse.get_pressed()[0]:
                if self.prev:
                    if type(self.prev) == SaveScoreState:
                        self.master.goto(self.prev.prev)
                    else:
                        self.master.goto(self.prev)

        else:
            self.enter(self.prev)  # State entry is incomplete

    def leave(self, state):
        """Handles state exit
        Args:
            state: Next state
        """
        self.active = False
        # noinspection PyProtectedMember
        self.master._enter(state)


# noinspection PyUnresolvedReferences
class PlayingState(object):
    """Handles the game logic and graphics

    Attributes:
        master: the attached GameManager instance.
        name: "PLAYING"
        active: Flag indicating whether the state is active
        prev: The previous state
    """

    def __init__(self, master):
        """Inits PlayingState"""
        self.master = master
        self.name = "PLAYING"
        self.active = False
        self.prev = None

        self._start_time = 0 # pygame time when gameplay started
        self._prev_points = 0# score in previous update

    # noinspection PyMethodMayBeStatic
    def draw_lives(self, n):
        """Draws 'live' icons in upper right corner

        Args:
            n: Number of 'lives' to draw
        """
        r = pygame.Rect((0, 0), (28, 28))
        r.right = WIDTH - 2
        r.centery = 18
        for i in range(n):
            screen.blit(heartSprite, r)
            r.left -= 28

    def get_time(self):
        """Get time since the beginning of gameplay"""
        return pygame.time.get_ticks() - self._start_time

    def enter(self, prev):
        """Handles state entry

        Args:
            prev: Previous state.
        """
        self.prev = prev
        self.master.highscore = self.master.get_highscore()

        if self.prev is self.master.mainmenustate or self.prev is self.master.gameoverstate:
            self._start_time = pygame.time.get_ticks()
        self.active = True

    def update(self):
        """Handles game execution"""
        global ASTEROID_MAX_X, ASTEROID_MIN_Y, ASTEROID_MAX_Y

        if self.active:
            if self.master.points != self._prev_points:
                self._prev_points = self.master.points

            # Asteroid generation
            if self.master.newroid == 0:
                Asteroid(
                    self.master, random.randint(0, 14) * 25,
                    random.randint(-ASTEROID_MAX_X, ASTEROID_MAX_X),
                    random.randint(ASTEROID_MIN_Y, ASTEROID_MAX_Y))
                self.master.newroid = self.master.roidrate

            # Keybindings
            keys_down = pygame.event.get(KEYDOWN)
            for e in keys_down:
                if e.key == K_ESCAPE:
                    self.master.goto(self.master.pausestate)

                # Debugging keys
                # TODO Remove these for final release
                elif e.key == K_UP:
                    self.master.roidrate /= 2
                    if self.master.roidrate < 10:
                        self.master.roidrate = 10
                elif e.key == K_DOWN:
                    self.master.roidrate *= 2
                elif e.key == K_RETURN:
                    self.master.goto(self.master.gameoverstate)

            # Player movement
            keys = pygame.key.get_pressed()
            if keys[K_LEFT] or keys[K_a]:
                self.master.player.move(-PLAYER_MOVE_SPEED, 0)
            elif keys[K_RIGHT] or keys[K_d]:
                self.master.player.move(PLAYER_MOVE_SPEED, 0)
            # Gun control
            if keys[K_SPACE] or keys[K_f]:
                self.master.player.fire()

            # Collision checks:
            for a in self.master.roids:

                # Player-Asteroid collision check
                if a.rect.bottom > self.master.player.rect.top:
                    if a.rect.colliderect(self.master.player.rect) and not a.explode:
                        self.master.player.lives -= 1
                        a.explode = pygame.time.get_ticks()
                        a.vely = 0

                # Bolt-asteroid collision check
                for b in self.master.bolts:
                    if a.rect.colliderect(b.rect):
                        self.master.points += 5
                        self.master.bolts.remove(b)
                        a.explode = pygame.time.get_ticks()

                # Asteroid-asteroid collision check
                # TODO Collision is not working properly (Asteroids double collide)
                for a2 in self.master.roids:
                    if a is not a2:
                        if a.rect.colliderect(a2.rect):
                            a.velx = -a.velx
                            a2.velx = -a2.velx

                            offset = (a.rect.centerx - a2.rect.centerx) / 2 + 1
                            a.rect.centerx += offset
                            a2.rect.centerx -= offset

            # Draw background
            screen.blit(backgroundObj, (0, 0))

            # Update and draw entities
            # Order is important for layering!
            for b in self.master.bolts:
                b.update()
            for a in self.master.roids:
                a.update()

            # Update and draw player
            self.master.player.update()

            # Render points
            lbl_score = FONT_M.render("SCORE: " + str(self.master.points), True, (255, 255, 255))
            rect_lbl_score = lbl_score.get_rect()
            rect_lbl_score.left = 3
            rect_lbl_score.top = 0
            screen.blit(lbl_score, rect_lbl_score)

            # Render lives
            lives = self.master.player.lives
            if lives > 0:
                self.draw_lives(lives)
            else:
                self.master.goto(self.master.gameoverstate)

            # Decrease new asteroid timer
            self.master.newroid = max(self.master.newroid - fpsClock.get_time(), 0)

            # Progressive difficulty
            if self.master.points < 750:
                # Minimum delay: 250 milliseconds
                self.master.roidrate = 1000 - self.master.points
            if self.master.points > 550:
                if self.master.points % 150 == 0 and self.master.points != self._prev_points:
                    ASTEROID_MAX_X += 1
                    ASTEROID_MAX_Y += 1
                if self.master.points % 300 == 0 and self.master.points != self._prev_points:
                    ASTEROID_MIN_Y += 1

    def leave(self, state):
        """Handles state exit

        Args:
            state: Next state.
        """
        self.active = False
        # noinspection PyProtectedMember
        self.master._enter(state)


class GameManager(object):
    """Coordinates the whole game

    Manages state transitions, stores game variables, and handles
    loading/saving of data.

    Attributes:
        points: Current score
        bolts: Stores Bolt instances
        roids: Stores Asteroid instances
        player: The current instance of Player
        scores: Lists all saved scores as tuple (int score, str name)
        highscore: Current highscore
        newroid: Countdown to new asteroid generation
        roidrate: Frequency of new asteroid generation
    """

    def __init__(self):
        """Inits GameManager

        Instantiates all states and player. Loads saved scores.
        """
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
        self.load_scores()
        self.highscore = self.get_highscore()
        self.newroid = 0
        self.roidrate = 1000  # New asteroid every 1000 milliseconds

        self._state = None
        self._enter(self.openingstate)

    # noinspection PyBroadException
    def load_scores(self):
        """Loads scores from /user_scores.txt"""
        self.scores = []
        with open("user_scores.txt", 'r') as f:
            lines = f.readlines()
            for L in lines:
                L = L.split(',')
                # noinspection PyPep8
                try:
                    self.scores.append((int(L[0]), L[1].strip('\n')))
                except Exception:
                    break

    def save_new_score(self, score, name):
        """Saves scores

        Called by SaveScoreState. Scores are saved in order from
        highest to lowest.

        Args:
            score: The new score to save
            name: Name of player who earned the score
        """
        self.scores.append((score, name))
        self.scores.sort(key=lambda t: t[0], reverse=True)

        with open("user_scores.txt", 'w') as f:
            for l in self.scores:
                f.write(str(l[0]) + ',' + l[1] + '\n')

    def get_highscore(self):
        """Returns current highscore"""
        if self.scores:
            return self.scores[0][0]
        else:
            return 0

    def update(self):
        """Calls the current states update function"""
        if self._state:
            self._state.update()

    def get_state(self):
        """Returns the name of the current state"""
        return self._state.name

    def goto(self, state):
        """Tells the current state to exit and go to the next state

        Args:
            state: Next state.
        """
        self._state.leave(state)

    def _enter(self, state):
        """Enters a new state without leaving the current state

        Should only be called from a states 'leave' method.

        Args:
            state: The state to go to.
        """
        prev = self._state
        self._state = state
        self._state.enter(prev)


class Player(object):
    """Handles player movement and stores player variables

    Attributes:
        master: The attached GameManager instance
        rect: Stores the player's Rect for position and collisions
        lives: Remaining lives
        can_fire: Countdown until the player can fire a bolt again
        explode: Timer for explosion animation
    """

    def __init__(self, master):
        """Inits the player"""
        self.master = master
        self.rect = pygame.Rect(0, 0, 75, 35)
        self.rect.centerx = 187
        self.rect.centery = 550
        self.lives = 3
        self.can_fire = 0
        self.explode = False

    def move(self, x, y):
        """Moves the player by specified offset

        Checks for collisions with the edge of the window.

        Args:
            x: Offset in the x direction
            y: Offset in the y direction
        """
        self.rect = self.rect.move(x, y)
        if self.rect.centerx < 0:
            self.rect.centerx = 0
        if self.rect.centerx > WIDTH:
            self.rect.centerx = WIDTH

    def fire(self):
        """Fires a new Bolt instance"""
        if self.can_fire == 0:
            Bolt(self.master, self.rect.centerx - 18, self.rect.top - 25)
            self.can_fire = 3

    def update(self):
        """Handles drawing"""
        self.can_fire = max(self.can_fire - 1, 0)
        self.draw()

    def draw(self):
        """Draws Player sprite animation"""
        if not self.explode:
            r = (self.rect.left, self.rect.top - 25)
            if pygame.time.get_ticks() % 200 < 100:
                screen.blit(playerSprite1, r)
            else:
                screen.blit(playerSprite2, r)
        else:
            dt = pygame.time.get_ticks() - self.explode
            if dt < 150:
                pygame.draw.circle(screen, (255, 127, 31), self.rect.center, dt / 2)


class Bolt(object):
    """Handles Bolt movement

    Attributes:
        master: The attached GameManager instance
        rect: Bolt Rect for position and collisions
        id: Index in master.bolts
    """

    def __init__(self, master, x, y):
        """Inits Bolt and adds reference to master.bolts"""
        self.master = master
        self.rect = pygame.Rect(x, y, 10, 30)
        self.id = len(master.bolts)
        self.master.bolts.append(self)

    def update(self):
        """Handles movement and drawing"""
        self.rect = self.rect.move(0, -25)
        if self.rect.bottom < 0:
            self.master.bolts.remove(self)
        self.draw()

    def draw(self):
        """Draws the bolt sprite"""
        screen.blit(boltSprite1, self.rect.topleft)


class Asteroid(object):
    """Handles asteroid movement and collisions

    Attributes:
        master: The attached GameManager instance
        rect: The Asteroid rect for position and collisions
        velx: Velocity in the x direction
        vely: Velocity in the  y direction
        explode: Timer for explosion animations
    """

    def __init__(self, master, x, velx=0, vely=5):
        """Inits Asteroid

        Chooses a sprite at random from ASTEROID_SPRITES.

        Args:
            x: The x coordinate
            velx: Initial velocity in the x direction
            vely: Initial velocity in the y direction (Default: 5)
        """
        self.master = master
        self.rect = pygame.Rect(x, -25, 25, 25)
        self.velx = velx
        self.vely = vely

        self._sprite = ASTEROID_SPRITES[random.randint(0, len(ASTEROID_SPRITES) - 1)]

        self.master.roids.append(self)
        self.explode = False

    def update(self):
        """Handles asteroid movement and collisions"""
        self.rect = self.rect.move(self.velx, self.vely)
        if self.rect.left < 0:
            self.rect.left = 0
            self.velx = -self.velx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.velx = -self.velx

        if self.rect.top > HEIGHT:
            self.master.roids.remove(self)
            self.master.goto(self.master.gameoverstate)

        self.draw()

    def draw(self):
        """Draws sprite and iff self.explode, draws the explosion animation

        Deletes reference from self.master.roids upon completion of explosion.
        """
        screen.blit(self._sprite, self.rect)

        if self.explode:
            dt = pygame.time.get_ticks() - self.explode
            pygame.draw.circle(screen, (255, 255, 255), self.rect.center, dt / 2)
            if dt > 50:
                self.explode = False
                self.master.roids.remove(self)


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
