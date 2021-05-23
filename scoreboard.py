# init
import json
import tkinter
import pygame
import button
import switch
import config
import hyperlink
import text_field
import repeated_timer
import threading
from time import sleep
from tkinter import filedialog

useless = tkinter.Tk()
useless.withdraw()

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
font_96 = pygame.font.Font('assets/denhome.otf', 96)

current_ui = "menu"

color_bg = (0, 255, 255)
color_board_outline = (0, 204, 204)
color_board_bg = (0, 102, 102)
color_red = (255, 0, 0)
color_green = (44, 242, 0)
color_info_bg = (255, 140, 26)
color_info_outline = (195, 204, 217)

global_config = config.config({}, 'config_global.json') # load the config file
global_config.load('config_global.json')
global_config.get('voice', True)
global_config.get('victories', True)
global_config.get('progress', True)
global_config.get('blink_time', 10) # for each setting we need, check if it's there and if it's not, set it to default value

game_config = {}

font_score = {'-': pygame.image.load('assets/hyphen.png').convert_alpha(),
              '.': pygame.image.load('assets/dot.png').convert_alpha(),
              '0': pygame.image.load('assets/number_0.png').convert_alpha(),
              '1': pygame.image.load('assets/number_1.png').convert_alpha(),
              '2': pygame.image.load('assets/number_2.png').convert_alpha(),
              '3': pygame.image.load('assets/number_3.png').convert_alpha(),
              '4': pygame.image.load('assets/number_4.png').convert_alpha(),
              '5': pygame.image.load('assets/number_5.png').convert_alpha(),
              '6': pygame.image.load('assets/number_6.png').convert_alpha(),
              '7': pygame.image.load('assets/number_7.png').convert_alpha(),
              '8': pygame.image.load('assets/number_8.png').convert_alpha(),
              '9': pygame.image.load('assets/number_9.png').convert_alpha()}

# predefine variables to use in definitions safely
game_name = '' ## there used to be '<insert a meme here>' here  ## i have not achieved comedy
players = 2 # i can not put anything here, because in the end, it does matter and it doesn't get overwritten as soon as you start the game
scores = [0, 0]
victories = [0, 0]
goals = [2147483647, 2147483647]
names = ['Player 1', 'Player 2']
score_limit = 125
log = []
field_colors = [0, 0]

blink_time = 10
voice = True
show_victories = True
progress = True

is_game_running = False

error_messages = []

game_conf_file = ''
player_page = 0

# utility functions
def draw_rect(x1, y1, x2, y2, fill_color = (0, 204, 204), outline=3, outline_color = (0, 0, 0), surface=pygame.display.get_surface()):
    '''A utility function that draws a rectangle with just one line'''
    if x1 > x2 or y1 > y2:
        raise ValueError("first set of coordinates must represent top left corner")
    dx = x2 - x1
    dy = y2 - y1
    pygame.draw.rect(surface, fill_color, (x1, y1, dx, dy))
    pygame.draw.rect(surface, outline_color, (x1, y1, dx, dy), outline)
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
def blit(text, font, pos, center=False, color=(0, 0, 0), surface=pygame.display.get_surface()):
    '''Blits some text to a chosen surface with only one line instead of two'''
    j = font.render(text, 1, color)
    if center:
        pos = (pos[0]-j.get_width() / 2, pos[1])
    surface.blit(j, pos)

# blink control functions
def blink_half_second_multiple(player, color, count): # makes a player's field to change color for half a second
    for i in range(count):
        global field_colors
        field_colors[player] = color
        sleep(0.5)
        field_colors[player] = 0
        sleep(0.5)
# blink_thread = threading.Thread(target=blink_half_second_multiple, name='blink_thread', args=(1, 1, 10)) ## doesn't work

class menu:
    def __init__(self):
        self.surface = window

        self.btn_new_file = button.button(color_board_outline, 490, 250, 300, 75, 'New file')
        self.btn_import = button.button(color_board_outline, 490, 335, 300, 75, 'Open file')
        self.btn_settings = button.button(color_board_outline, 490, 420, 300, 75, 'Settings')

    def draw(self):
        global log
        global goals
        global names
        global scores
        global players
        global progress
        global victories
        global game_name
        global current_ui
        global score_limit
        self.surface.fill(color_bg)
        if draw_button(self.btn_import, 72, self.surface):
            filename = filedialog.askopenfilename(title='Load game', filetypes=[('Game file', '*.json'), ('All files', '*.*')])
            try:
                with open(filename, 'r', -1, 'utf-8') as file:
                    game_config = json.load(file)
            except FileNotFoundError:
                return
            try:
                game_name = game_config['game_name']
            except KeyError:
                game_name = '<error>'
            try:
                log = game_config['log']
            except KeyError:
                log = []
            try:
                goals = game_config['goals']
                names = game_config['names']
                scores = game_config['scores']
                players = game_config['players']
                progress = game_config['progress']
                victories = game_config['victories']
                score_limit = game_config['score_limit']
            except KeyError:
                print('File error: some of the critical values were not found, cannot proceed')
                return
            current_ui = 'game'
        if draw_button(self.btn_settings, 72, self.surface):
            current_ui = 'settings'
        if draw_button(self.btn_new_file, 72, self.surface):
            current_ui = 'setup'
        blit(game_version, font_28, (10, 690))


class settings:
    def __init__(self):
        self.surface = window
        # global settings
        self.voice_enabled = switch.switch(1180, 100, self.surface) ## note: a switch is 86x36 pixels
        self.show_victories = switch.switch(1180, 150, self.surface)
        self.show_goal_progress = switch.switch(1180, 200, self.surface)
        self.blink_time = text_field.text_field(1180, 250, 90, 40, blink_time, font_50, self.surface, 'int')
        # game settings
        self.game_name = text_field.text_field(1180, 100, 90, 40, game_name, font_50, game_name, self.surface)
        self.score_lim = text_field.text_field(1180, 150, 90, 40, score_limit, font_50, score_limit, self.surface, 'float')
        self.goto_player_name = button.button(color_board_outline, 10, 440, 90, 40, 'Player names')
        # player names
        self.player_names = []
        for i in range(18):
            self.player_names.append(text_field.text_field(20+415*(i%3) + 175, (i//3) * 100 + 100, 220, 50, '', font_50, self.surface))
        # utility stuff
        self.go_back = hyperlink.hyperlink((0, 0, 0), 10, 0, '< Back')

        ## note: everything in self is not the settings, but the tool used to change them
    
    def draw_global(self):
        global current_ui
        global voice
        global show_victories
        global progress
        global blink_time
        self.surface.fill(color_bg)
        if self.go_back.smart_draw(self.surface):
            current_ui = 'menu'
            global_config.save()
            if is_game_running and game_conf_file:
                with open(game_conf_file, 'w', -1, 'utf-8') as file:
                    file.write(json.dumps(game_config, indent=4, ensure_ascii=False))
        blit('Program settings', font_40, (20, 50), False, (100, 100, 100))
        blit('Use voice output', font_72, (20, 80))
        blit('Show player victory count', font_72, (20, 130))
        blit('Show goal progress', font_72, (20, 180))
        blit('Player visualization duration', font_72, (20, 230))
        if self.voice_enabled.smart_draw(global_config.get('voice')):
            voice = not voice
            global_config.set('voice', voice)
        if self.show_victories.smart_draw(global_config.get('victories')):
            show_victories = not show_victories
            global_config.set('victories', show_victories)
        if self.show_goal_progress.smart_draw(global_config.get('progress')):
            progress = not progress
            global_config.set('progress', progress)
        temp_blink_time = self.blink_time.draw()
        if not temp_blink_time is False:
            blink_time = temp_blink_time
            global_config.set('blink_time', temp_blink_time)
        if is_game_running:
            self._draw_game()

    def _draw_game(self):
        global current_ui
        global game_name
        global score_limit
        blit('Game settings', font_40, (20, 280), (100, 100, 100))
        blit('Game name', font_72, (20, 310))
        blit('Score limit', font_72, (20, 360))
        if draw_button(self.goto_player_name, 72, self.surface):
            current_ui = 'player_edit'
        temp = self.game_name.draw()
        if not temp is False:
            game_name = temp
        temp = self.score_lim.draw()
        if not temp is False:
            score_limit = temp

    def draw_player_list(self):
        global current_ui
        self.surface.fill(color_bg)
        for i in range(players):
            blit(f'Player {i+1}', font_72, (20+415*(i%3), (i//3) * 100 + 100))
            temp = self.player_names[i].draw()
            if not temp is False:
                names[i] = temp
                game_config['names'][i] = temp
        if self.go_back.smart_draw(self.surface):
            if current_ui == 'player_edit':
                current_ui = 'settings'
            else:
                current_ui = 'setup'
            if game_conf_file:
                with open(game_conf_file, 'w', -1, 'utf-8') as file:
                    file.write(json.dumps(game_config, indent=4, ensure_ascii=False))


class game:
    def __init__(self):
        self.surface = window
        self.game_name = text_field.text_field(800, 90, 460, 65, game_name, font_72, self.surface)
        self.player_count = text_field.text_field(800, 160, 460, 65, players, font_72, self.surface, 'int')
        self.score_lim = text_field.text_field(800, 230, 460, 65, score_limit, font_72, self.surface, 'float')
        self.set_player_names = button.button(color_board_outline, 20, 300, 400, 65, 'Set player names')
        self.start = button.button(color_board_outline, 950, 630, 310, 75, 'Save and start')
        self.go_menu = hyperlink.hyperlink((0, 0, 0), 10, 0, '< Main Menu')
        self.start_no_file = button.button(color_board_outline, 585, 630, 350, 75, 'Start without saving')

        self.no_file = button.button((168, 0, 0), 425, 375, 200, 60, 'Continue')
        self.try_again = button.button(color_board_outline, 655, 375, 200, 60, 'Back')

        self.color_index = [color_board_bg, color_red, color_green]

    def draw_setup(self):
        global game_name
        global players
        global score_limit
        global current_ui
        global error_messages
        global game_conf_file
        global names
        global game_config
        self.surface.fill(color_bg)
        text = font_96.render('New game', 1, (0, 0, 0))
        self.surface.blit(text, (640 - text.get_width()/2, 10)) # we can't use blit() because it can't center the text around a point
        blit('Game name', font_72, (20, 80))
        blit('Number of players', font_72, (20, 150))
        blit('Score to lose (score limit)', font_72, (20, 220))
        error_messages = []
        if players < 2:
            error_messages.append('There must be at least two players')
        if players > 18:
            error_messages.append('Currently you cannot have more than 18 players')
        if score_limit <= 0:
            error_messages.append('Score limit must be positive')
        if error_messages:
            j = 0
            for i in error_messages:
                blit(i, font_50, (20, j*50 + 370), False, (200, 0, 0))
                j += 1
        temp = self.game_name.draw()
        if not temp is False:
            game_name = temp
            game_config['name'] = temp
        temp = self.player_count.draw()
        if not temp is False:
            players = temp
            game_config['player_count'] = temp
        temp = self.score_lim.draw()
        if not temp is False:
            score_limit = temp
            game_config['score_limit'] = temp
        if self.go_menu.smart_draw(self.surface):
            current_ui = 'menu'
        if draw_button(self.set_player_names, 72, self.surface) and players <= 18:
            try:
                names[players-1]
                game_config['names'][players-1]
            except:
                names = ['player'] * players
                game_config['names'] = ['player'] * players
            current_ui = 'player_setup'
        if draw_button(self.start_no_file, 72, self.surface) and not error_messages:
            current_ui = 'game'
        if draw_button(self.start, 72, self.surface):
            if not error_messages:
                game_conf_file = filedialog.asksaveasfilename(defaultextension = '.json', filetypes = [('JSON files', '*.json'), ('All files', '*.*')], title = 'Save game data')
                try:
                    with open(game_conf_file, 'w', -1, 'utf-8') as file:
                        game_config['scores'] = scores
                        game_config['victories'] = victories
                        game_config['goals'] = goals
                        game_config['log'] = log
                        file.write(json.dumps(game_config, indent=4, ensure_ascii=False))
                except:
                    draw_rect(410, 270, 870, 450)
                    draw_rect(410, 270, 870, 300, color_bg)
                    blit('No file specified', font_28, (640, 270), True)
                    blit("You didn't choose a file, which means that", font_40, (640, 300), True)
                    blit("nothing will be saved. Continue?", font_40, (640, 330), True)
                    while True:
                        if draw_button(self.no_file, 60, self.surface, (168, 0, 0), (200, 0, 0), (128, 0, 0)):
                            break
                        if draw_button(self.try_again):
                            return
                        pygame.event.get()
                        pygame.display.update()
                        gametick.tick(max_fps)
                current_ui = 'game'

    def draw_game(self):
        # draw the stuff
        self.surface.fill(color_bg)
        pygame.draw.rect(self.surface, color_board_bg, (10, 10, 1060, 600))
        pygame.draw.rect(self.surface, self.color_index[field_colors[player_page * 3]], (10, 10, 1060, 200))
        #  TO DO: render text
        # draw the box for it (slightly bigger than the text)
        # draw the text itself (in the middle of that box)
        # draw the score
        try:
            pygame.draw.rect(self.surface, self.color_index[field_colors[player_page * 3 + 1]], (10, 210, 1060, 200))
            # repeat for other players
            pygame.draw.rect(self.surface, self.color_index[field_colors[player_page * 3 + 2]], (10, 410, 1060, 200))
        except:
            pass
        pygame.draw.rect(self.surface, color_board_outline, (10, 10, 1060, 600), 4)
        
ui_menu = menu()
ui_settings = settings()
ui_game = game()

while True:
    if pygame.event.get(pygame.QUIT):
        pygame.quit()
        exit(0)
    if current_ui == "menu":
        ui_menu.draw()
    elif current_ui == 'settings':
        ui_settings.draw_global()
    elif current_ui == 'player_edit' or current_ui == 'player_setup':
        ui_settings.draw_player_list()
    elif current_ui == 'setup':
        ui_game.draw_setup()
    elif current_ui == 'game':
        ui_game.draw_game()
    pygame.display.update()
    gametick.tick(max_fps)