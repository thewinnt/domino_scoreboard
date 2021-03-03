# init
import pygame
import button
import switch
import config
import hyperlink
import text_field

pygame.init()

max_fps = 30
gametick = pygame.time.Clock()

icon = pygame.image.load("assets/window.png")
pygame.display.set_icon(icon)
window = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Таблица очков для домино (v. 1.0 development version)")
game_version = "v. 1.0 (work in progress)"

font_28 = pygame.font.Font('assets/denhome.otf', 28)
font_40 = pygame.font.Font('assets/denhome.otf', 40)
font_50 = pygame.font.Font('assets/denhome.otf', 50)
font_72 = pygame.font.Font('assets/denhome.otf', 72)

current_ui = "menu"

color_bg = (0, 255, 255)
color_board_outline = (0, 204, 204)
color_board_bg = (0, 102, 102)

global_config = config.config(config.get_file('config_global.json'), 'config_global.json')
global_config.get('voice', True)
global_config.get('victories', True)
global_config.get('progress', True)
global_config.get('blink_time', 10)

# predefine variables to use in definitions safely
game_name = '<insert a meme here>' ## what's a good program without some easter eggs? :)
players = 2 # i can put anything here, because in the end, in doesn't even matter and it gets overwritten as soon as you start the game
scores = [0, 0]
victories = [0, 0]
goals = [2147483647, 2147483647]
names = ['Player 1', 'Player 2']
score_limit = 125
blink_time = 5

# utility functions grouped in a class
class util:
    def draw_button(button, font_size = 60, surface=pygame.display.get_surface(), default_color=(0, 204, 204), hover_color=(0, 255, 255), click_color=(0, 102, 102), text_color=(0, 0, 0), outline_color=(0, 0, 0)) -> bool:
        '''Draws the button and returns its click state'''
        to_return = False
        if button.isOver():
            button.color = hover_color
            if pygame.mouse.get_pressed()[0]:
                button.color = click_color
                pygame.event.clear()
                to_return = True
        if not button.isOver() and not pygame.mouse.get_pressed()[0]:
            button.color = default_color
        button.draw(surface, outline_color, text_color, font_size)
        return to_return
    def blit(text, font, pos, color=(0, 0, 0), surface=pygame.display.get_surface()):
        '''Blits some text to a chosen surface with only one line instead of two'''
        j = font.render(text, 1, color)
        surface.blit(j, pos)


class menu:
    def __init__(self, surface=pygame.display.get_surface()):
        self.surface = surface

        self.btn_new_file = button.button(color_board_outline, 490, 250, 300, 75, 'New file')
        self.btn_import = button.button(color_board_outline, 490, 335, 300, 75, 'Open file')
        self.btn_settings = button.button(color_board_outline, 490, 420, 300, 75, 'Settings')

    def draw(self):
        global current_ui
        self.surface.fill(color_bg)
        if util.draw_button(self.btn_import, 72, self.surface):
            pass # here will be the actual start, TBD
        if util.draw_button(self.btn_settings, 72, self.surface):
            current_ui = 'settings_global'
        if util.draw_button(self.btn_new_file, 72, self.surface):
            pass # new file, TBD

class settings:
    def __init__(self, surface=pygame.display.get_surface()):
        self.surface = surface

        # global settings
        self.voice_enabled = switch.switch(1180, 100, self.surface) ## note: a switch is 86x36 pixels
        self.show_victories = switch.switch(1180, 150, self.surface)
        self.show_goal_progress = switch.switch(1180, 200, self.surface)
        self.blink_time = text_field.text_field(90, 40, blink_time, font_28, self.surface, 'int')
        # game settings
        self.game_name = text_field.text_field(90, 40, game_name, font_28, self.surface)
        self.score_lim = text_field.text_field(90, 40, score_limit, font_28, self.surface, 'float')
        self.goto_player_name = button.button(color_board_outline, 10, 440, 90, 40, 'Player names')
        # player names
        self.player_names = []
        for i in range(players):
            self.player_names.append(text_field.text_field(400, 40, names[i], font_28, self.surface))
        # utility stuff
        self.go_back = hyperlink.hyperlink((0, 0, 0), 10, 0, '< Back')

        ## note: everything in self is not the settings, but the tool used to change them
    
    def draw_global(self):
        global current_ui
        self.surface.fill(color_bg)
        if self.go_back.smart_draw(self.surface):
            current_ui = 'menu'
        util.blit('Program settings', font_40, (20, 50), (100, 100, 100))
        util.blit('Use voice output', font_72, (20, 80))
        util.blit('Show player victory count', font_72, (20, 130))
        util.blit('Show goal progress', font_72, (20, 180))
        util.blit('Player visualization duration', font_72, (20, 230))
        global_config.set('voice', self.voice_enabled.smart_draw(global_config.get('voice')))
        global_config.set('victories', self.show_victories.smart_draw(global_config.get('victories')))
        global_config.set('progress', self.show_goal_progress.smart_draw(global_config.get('progress')))
        #global_config.set('blink_time', self.blink_time.draw(1180, 250))

class game:
    def __init__(self, surface):
        self.surface = surface

ui_menu = menu(window)
ui_settings = settings(window)
ui_game = game(window)

while True:
    if pygame.event.get(pygame.QUIT):
        pygame.quit()
        exit(0)
    if current_ui == "menu":
        ui_menu.draw()
    if current_ui == 'settings_global':
        ui_settings.draw_global()
    pygame.display.update()
    gametick.tick(max_fps)