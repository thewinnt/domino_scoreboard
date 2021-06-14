# init
import json
import tkinter
import pygame
import button
import switch
import config
import hyperlink
import text_field
import fancy_blit
import event_handler
from tkinter import filedialog

useless = tkinter.Tk()
useless.withdraw()

pygame.init()

gametick = pygame.time.Clock()
game_events = event_handler.EventHandler()

icon = pygame.image.load("assets/window.png")
pygame.display.set_icon(icon)
window = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Dominoes scoreboard (v. 1.0 pre-release 2)")
game_version = "v. 1.0-pre2"

font_28 = pygame.font.Font('assets/denhome.otf', 28)
font_40 = pygame.font.Font('assets/denhome.otf', 40)
font_50 = pygame.font.Font('assets/denhome.otf', 50)
font_60 = pygame.font.Font('assets/denhome.otf', 60)
font_72 = pygame.font.Font('assets/denhome.otf', 72)
font_96 = pygame.font.Font('assets/denhome.otf', 96)
font_cmd = pygame.font.Font('assets/dhbold.ttf', 48)
font_info = pygame.font.Font('assets/arial.ttf', 32)
font_log = pygame.font.Font('assets/arialb.ttf', 20)
font_data = pygame.font.Font('assets/arial.ttf', 28)
font_msg = pygame.font.Font('assets/dhbold.ttf', 40)

current_ui = "menu"

color_bg = (0, 255, 255)
color_board_outline = (0, 204, 204)
color_board_bg = (0, 102, 102)
color_red = (255, 0, 0)
color_green = (44, 242, 0)
color_info_bg = (255, 140, 26)
color_info_outline = (195, 204, 217)
color_log_index = (87, 94, 117)
color_log_background = (252, 102, 44)
color_log_outline = (223, 91, 38)
color_log_fill = (229, 240, 255)

global_config = config.config({}, 'config_global.json') # load the config file
global_config.load('config_global.json')
global_config.get('voice', True)
global_config.get('victories', True)
global_config.get('progress', True)
global_config.get('blink_time', 5) # for each setting we need, check if it's there and if it's not, set it to default value
global_config.get('max_fps', 60)

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
font_offsets = {'-': 7,
                '.': -55,
                '0': 72,
                '1': 78,
                '2': 71,
                '3': 77,
                '4': 74,
                '5': 79,
                '6': 71,
                '7': 71,
                '8': 76,
                '9': 75}
font_player_number = {'-': pygame.transform.rotozoom(font_score['-'], 0, 0.5),
                      '.': pygame.transform.rotozoom(font_score['.'], 0, 0.5),
                      '0': pygame.transform.rotozoom(font_score['0'], 0, 0.5),
                      '1': pygame.transform.rotozoom(font_score['1'], 0, 0.5),
                      '2': pygame.transform.rotozoom(font_score['2'], 0, 0.5),
                      '3': pygame.transform.rotozoom(font_score['3'], 0, 0.5),
                      '4': pygame.transform.rotozoom(font_score['4'], 0, 0.5),
                      '5': pygame.transform.rotozoom(font_score['5'], 0, 0.5),
                      '6': pygame.transform.rotozoom(font_score['6'], 0, 0.5),
                      '7': pygame.transform.rotozoom(font_score['7'], 0, 0.5),
                      '8': pygame.transform.rotozoom(font_score['8'], 0, 0.5),
                      '9': pygame.transform.rotozoom(font_score['9'], 0, 0.5)}

# predefine variables to use in definitions safely
def predefine_variables():
    global game_name
    global players
    global max_page
    global scores
    global visible_scores
    global victories
    global goals
    global names
    global score_limit
    global log
    global field_colors
    global blink_time
    global voice
    global show_victories
    global show_progress
    global inverted_victory_mode
    global max_fps
    global is_game_running
    global error_messages
    global game_conf_file
    global player_page
    global command
    global log_cursor
    global was_pressed
    global is_updating
    global message
    global command_help
    game_name = '' ## there used to be '<insert a meme here>' here  ## i have not achieved comedy
    players = 2 # i can not put anything here, because in the end, it does matter and it doesn't get overwritten as soon as you start the game
    max_page = 0
    scores = [0, 0]
    visible_scores = [0, 0]
    victories = [0, 0]
    goals = ['2147483647', '2147483647']
    names = ['Player', 'Player']
    score_limit = 125
    log = []
    field_colors = [0, 0]

    blink_time = global_config.get('blink_time')
    voice = global_config.get('voice')
    show_victories = global_config.get('victories')
    show_progress = global_config.get('progress')
    inverted_victory_mode = False # if true, the player with the highest score wins

    max_fps = global_config.get('max_fps')

    is_game_running = False

    error_messages = []

    game_conf_file = ''
    player_page = 0

    command = ''
    log_cursor = 0

    was_pressed = False
    is_updating = False

    message = 'Enter the command here:'

    try:
        with open('assets/command_help.txt', 'r') as help_file:
            command_help = help_file.read()
    except:
        command_help = 'Help file missing'
        print('File error: missing file - assets/command_help.txt; help command will not work')

predefine_variables()

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
def draw_text_box(text, font, pos, surface, min_width=100, centered=True, box_color=color_info_bg, box_outline_color=color_info_outline, text_color=(255, 255, 255)):
    text = str(text) # this function draws a text box that looks like a Scratch variable (no input available)
    rendered_text = font.render(text, 1, text_color, box_color)
    text_area= font.size(text)
    box_width = max(min_width - 10, text_area[0]) + 14
    pygame.draw.rect(surface, box_color, (pos[0], pos[1], box_width, 50), 0, 8)
    pygame.draw.rect(surface, box_outline_color, (pos[0], pos[1], box_width, 50), 3, 8)
    if centered:
        surface.blit(rendered_text, (pos[0] + box_width / 2 - text_area[0] / 2, pos[1] + 25 - text_area[1] / 2))
    else:
        surface.blit(rendered_text, (pos[0] + 10, pos[1] + 25 - text_area[1] / 2))

# blink control functions
#def blink_half_second_multiple(player, color, count): # makes a player's field to change color for half a second
#    for i in range(count):
#        global field_colors
#        field_colors[player] = color
#        sleep(0.5)
#        field_colors[player] = 0
#        sleep(0.5)    ## will be replaced

class menu:
    def __init__(self):
        self.surface = window

        self.btn_new_file = button.button(color_board_outline, 490, 250, 300, 75, 'New file')
        self.btn_import = button.button(color_board_outline, 490, 335, 300, 75, 'Open file')
        self.btn_settings = button.button(color_board_outline, 490, 420, 300, 75, 'Settings')

        self.btn_continue = button.button(color_board_outline, 490, 195, 300, 75, 'Continue')

    def draw(self):
        global log
        global goals
        global names
        global scores
        global players
        global max_page
        global victories
        global game_name
        global current_ui
        global log_cursor
        global score_limit
        global field_colors
        global show_progress
        global show_victories
        global game_conf_file
        global visible_scores
        global is_game_running
        global inverted_victory_mode
        self.surface.fill(color_bg)
        if is_game_running:
            self.btn_new_file.y = 280
            self.btn_import.y = 365
            self.btn_settings.y = 450
            if draw_button(self.btn_continue, 72, self.surface):
                current_ui = 'game'
        else:
            self.btn_new_file.y = 250
            self.btn_import.y = 335
            self.btn_settings.y = 420
        if draw_button(self.btn_import, 72, self.surface):
            game_conf_file = filedialog.askopenfilename(title='Load game', filetypes=[('Game file', '*.json'), ('All files', '*.*')])
            try:
                with open(game_conf_file, 'r', -1, 'utf-8') as file:
                    game_config = json.load(file)
            except FileNotFoundError:
                return
            try:
                game_name = game_config['game_name']
            except KeyError:
                game_name = '<error>'
            try:
                log = game_config['log']
                log_cursor = max(0, len(log) - 10)
            except KeyError:
                log = []
            try:
                goals = game_config['goals']
                names = game_config['names']
                scores = game_config['scores']
                players = game_config['players']
                victories = game_config['victories']
                score_limit = game_config['score_limit']
                inverted_victory_mode = game_config['limit_mode']
            except KeyError:
                print('File error: some of the critical values were not found, cannot proceed')
                return
            if players % 3:
                max_page = players // 3
            else:
                max_page = players // 3 - 1
            field_colors = [0] * players
            visible_scores = scores.copy()
            is_game_running = True
            current_ui = 'game'
        if draw_button(self.btn_settings, 72, self.surface):
            ui_settings.blink_time.text = str(blink_time)
            ui_settings.game_name.text = game_name
            ui_settings.score_lim.text = str(score_limit)
            current_ui = 'settings'
        if draw_button(self.btn_new_file, 72, self.surface):
            predefine_variables() # we don't want to reload the previous game
            current_ui = 'setup'
        blit(game_version, font_40, (10, 680))


class settings:
    def __init__(self):
        self.surface = window
        # global settings
        self.voice_enabled = switch.switch(1180, 100, self.surface) ## note: a switch is 86x36 pixels
        self.show_victories = switch.switch(1180, 150, self.surface)
        self.show_goal_progress = switch.switch(1180, 200, self.surface)
        self.blink_time = text_field.text_field(1070, 250, 200, 45, blink_time, font_50, self.surface, 'int')
        # game settings
        self.game_name = text_field.text_field(1070, 350, 200, 45, game_name, font_50, self.surface)
        self.score_lim = text_field.text_field(1070, 400, 200, 45, score_limit, font_50, self.surface, 'int')
        self.score_mode = switch.switch(1180, 450, self.surface)
        self.filename = button.button(color_board_outline, 1180, 500, 90, 40, 'Change')
        self.goto_player_name = button.button(color_board_outline, 10, 550, 220, 65, 'Player names')
        self.go_menu = button.button(color_board_outline, 10, 625, 220, 65, 'Main Menu')
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
        global show_progress
        global blink_time
        self.surface.fill(color_bg)
        if self.go_back.smart_draw(self.surface):
            if current_ui == 'settings':
                current_ui = 'menu'
            else:
                current_ui = 'game'
            global_config.save()
            if is_game_running and game_conf_file:
                game_config['log'] = log
                game_config['goals'] = goals
                game_config['names'] = names
                game_config['scores'] = scores
                game_config['players'] = players
                game_config['victories'] = victories
                game_config['game_name'] = game_name
                game_config['score_limit'] = score_limit
                game_config['limit_mode'] = inverted_victory_mode
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
            show_progress = not show_progress
            global_config.set('progress', show_progress)
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
        global game_conf_file
        global inverted_victory_mode
        global is_game_running
        blit('Game settings', font_40, (20, 290), False, (100, 100, 100))
        blit('Game name', font_72, (20, 320))
        blit('Score limit', font_72, (20, 370))
        blit('Victory for the player with highest score', font_72, (20, 420))
        blit('Save file', font_72, (20, 480))
        blit('(game will be saved)', font_40, (240, 640), False, (85, 85, 85))
        filename = font_50.render(game_conf_file, 4, (0, 0, 0))
        self.surface.blit(filename, (1170 - filename.get_width(), 485))
        if draw_button(self.goto_player_name, 72, self.surface):
            for i in range(players):
                self.player_names[i].text = names[i]
            if current_ui == 'pause':
                current_ui = 'player_edit'
        if draw_button(self.go_menu, 72):
            if game_conf_file:
                game_config['log'] = log
                game_config['goals'] = goals
                game_config['names'] = names
                game_config['scores'] = scores
                game_config['players'] = players
                game_config['victories'] = victories
                game_config['game_name'] = game_name
                game_config['score_limit'] = score_limit
                game_config['limit_mode'] = inverted_victory_mode
                with open(game_conf_file, 'w') as config_file:
                    config_file.write(json.dumps(game_config, indent=4, ensure_ascii=True))
            current_ui = 'menu'
        temp = self.game_name.draw()
        if not temp is False:
            game_name = temp
        temp = self.score_lim.draw()
        if not temp is False:
            score_limit = temp
        if self.score_mode.smart_draw(inverted_victory_mode):
            inverted_victory_mode = not inverted_victory_mode
        if draw_button(self.filename):
            temp = filedialog.asksaveasfilename(defaultextension = '.json', filetypes = [('JSON files', '*.json'), ('All files', '*.*')], title = 'Save game data')
            if temp != '':
                game_conf_file = temp

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
                current_ui = 'pause'
            else:
                current_ui = 'setup'
            if game_conf_file:
                with open(game_conf_file, 'w', -1) as file:
                    file.write(json.dumps(game_config, indent=4, ensure_ascii=True))


class game:
    def __init__(self):
        self.surface = window
        self.game_name = text_field.text_field(800, 90, 460, 65, game_name, font_72, self.surface)
        self.player_count = text_field.text_field(800, 160, 460, 65, players, font_72, self.surface, 'int')
        self.score_lim = text_field.text_field(800, 230, 460, 65, score_limit, font_72, self.surface, 'int')
        self.set_player_names = button.button(color_board_outline, 20, 300, 400, 65, 'Set player names')
        self.start = button.button(color_board_outline, 950, 630, 310, 75, 'Save and start')
        self.go_menu = hyperlink.hyperlink((0, 0, 0), 10, 0, '< Main Menu')
        self.start_no_file = button.button(color_board_outline, 585, 630, 350, 75, 'Start without saving')

        self.no_file = button.button((168, 0, 0), 425, 375, 200, 60, 'Continue')
        self.try_again = button.button(color_board_outline, 655, 375, 200, 60, 'Back')

        self.color_index = [color_board_bg, color_red, color_green]

        self.command_line = text_field.text_field(10, 660, 950, 50, command, font_cmd, self.surface)
        self.cmd_desc = {'score': '§fscore <add|remove|set|limit> §b...',
                         'double': '§fdouble §b<0|6> §6<player: int>',
                         'rename': '§frename §b<player: int|game> §6<name: str>',
                         'menu': '§fmenu §c[no_save]',
                         'file': '§ffile <set|reload|save> §b...',
                         'log': '§flog <add|remove> ...',
                         'goal': '§fgoal §b<player: int> §f<fixed|relative> ...',
                         'victory': '§fvictory §b<player: int> §6<value: int>',
                         'help': '§fhelp'} # the descriptions of the commands

        self.set_desc = {'add': '§fscore add §b<player: int|all> §6<amount: int>',
                         'remove': '§fscore remove §b<player: int|all> §6<amount: int>',
                         'set': '§fscore set §b<player: int> §6<amount: int>',
                         'add all': '§fscore add §ball §6<amount: int> §a[<amount: int> for each player in order]',
                         'remove all': '§fscore remove §ball §6<amount: int> §a[<amount: int> for each player in order]',
                         'limit': '§fscore limit <set|mode>'} # descriptions of the set subcommands

        self.file_desc = {'set': '§ffile set §b[path: str]',
                          'reload': '§ffile §breload',
                          'save': '§ffile §bsave'}

    def draw_setup(self):
        global game_name
        global players
        global score_limit
        global current_ui
        global error_messages
        global game_conf_file
        global names
        global goals
        global scores
        global victories
        global field_colors
        global game_config
        global max_page
        global log_cursor
        global is_game_running
        self.surface.fill(color_bg)
        blit('New game', font_96, (640, 10), True)
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
        temp = self.game_name.draw(fancy_format=False)
        if not temp is False:
            game_name = temp
            game_config['game_name'] = temp
        temp = self.player_count.draw()
        if not temp is False:
            players = temp
            if players % 3:
                max_page = players // 3
            else:
                max_page = players // 3 - 1
            game_config['players'] = temp
            try:
                names[players-1]
                game_config['names'][players-1]
            except:
                names = ['Player'] * players
                game_config['names'] = ['player'] * players
        temp = self.score_lim.draw()
        if not temp is False:
            score_limit = temp
            game_config['score_limit'] = temp
        if self.go_menu.smart_draw(self.surface):
            current_ui = 'menu'
        if draw_button(self.set_player_names, 72, self.surface) and players <= 18:
            for i in range(players):
                ui_settings.player_names[i].text = names[i]
            try:
                names[players-1]
                game_config['names'][players-1]
            except:
                names = ['player'] * players
                game_config['names'] = ['player'] * players
            current_ui = 'player_setup'
        if draw_button(self.start_no_file, 72, self.surface) and not error_messages:
            field_colors = [0] * players
            scores = [0] * players
            visible_scores = [0] * players
            goals = ['0'] * players
            victories = [0] * players
            game_config['log'] = log
            game_config['goals'] = goals
            game_config['names'] = names
            game_config['scores'] = scores
            game_config['players'] = players
            game_config['victories'] = victories
            game_config['game_name'] = game_name
            game_config['score_limit'] = score_limit
            game_config['limit_mode'] = inverted_victory_mode
            is_game_running = True
            current_ui = 'game'
        if draw_button(self.start, 72, self.surface):
            if not error_messages:
                game_conf_file = filedialog.asksaveasfilename(defaultextension = '.json', filetypes = [('JSON files', '*.json'), ('All files', '*.*')], title = 'Save game data')
                try:
                    with open(game_conf_file, 'w') as file:
                        game_config['log'] = log
                        game_config['goals'] = goals
                        game_config['names'] = names
                        game_config['scores'] = scores
                        game_config['players'] = players
                        game_config['victories'] = victories
                        game_config['game_name'] = game_name
                        game_config['score_limit'] = score_limit
                        game_config['limit_mode'] = inverted_victory_mode
                        file.write(json.dumps(game_config, indent=4, ensure_ascii=True))
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
                field_colors = [0] * players
                scores = [0] * players
                visible_scores = [0] * players
                goals = ['0'] * players
                victories = [0] * players
                is_game_running = True
                current_ui = 'game'

    def draw_game(self):
        global player_page
        global log_cursor
        global was_pressed
        global current_ui
        global visible_scores
        global is_updating
        if not pygame.key.get_pressed()[pygame.K_LEFT] and not pygame.key.get_pressed()[pygame.K_RIGHT]:
            was_pressed = False
        # draw the stuff
        self.surface.fill(color_bg)
        first = player_page * 3
        second = player_page * 3 + 1
        third = player_page * 3 + 2
        score_first = str(int(visible_scores[first]))
        try:
            score_second = str(int(visible_scores[second]))
            score_third = str(int(visible_scores[third])) # these are the player scores as text
        except:
            pass
        if show_progress:
            if goals[first] != '0':
                goal_first = str(eval(goals[first]) - victories[first]) + ' left (' + str(round(victories[first] / eval(goals[first]) * 100, 1)) + '%)'
            else:
                goal_first = '0'
            try:
                if goals[second] != '0':
                    goal_second = str(eval(goals[second]) - victories[second]) + ' left (' + str(round(victories[second] / eval(goals[second]) * 100, 1)) + '%)'
                else:
                    goal_second = '0'
                if goals[third] != '0':
                    goal_third = str(eval(goals[third]) - victories[third]) + ' left (' + str(round(victories[third] / eval(goals[third]) * 100, 1)) + '%)'
                else:
                    goal_third = '0'
            except:
                pass
        else:
            if goals[first] != '0':
                goal_first = str(eval(goals[first]) - victories[first]) + ' left'
            else:
                goal_first = '0'
            try:
                if goals[second] != '0':
                    goal_second = str(eval(goals[second]) - victories[second]) + ' left'
                else:
                    goal_second = '0'
                if goals[third] != '0':
                    goal_third = str(eval(goals[third]) - victories[third]) + ' left'
                else:
                    goal_third = '0'
            except:
                pass
        pygame.draw.rect(self.surface, color_board_bg, (10, 10, 1060, 645))
        pygame.draw.rect(self.surface, self.color_index[field_colors[first]], (10, 10, 1060, 200))
        # draw the text
        draw_text_box(names[first], font_info, (120, 31), self.surface)
        if show_victories:
            draw_text_box(victories[first], font_info, (120, 85), self.surface)
        if goals[first] != '0':
            draw_text_box(goal_first, font_info, (120, 139), self.surface)
        # draw the score
        for i in range(len(score_first)):
            j = i + 1
            self.surface.blit(font_score[score_first[-j]], (1050 - 92 * j, 110 - font_offsets[score_first[-j]]))
        try:
            pygame.draw.rect(self.surface, self.color_index[field_colors[second]], (10, 210, 1060, 200))
            draw_text_box(names[second], font_info, (120, 231), self.surface)
            if show_victories:
                draw_text_box(victories[second], font_info, (120, 285), self.surface)
            if goals[second] != '0':
                draw_text_box(goal_second, font_info, (120, 339), self.surface)
            # draw the score
            for i in range(len(score_second)):
                j = i + 1
                self.surface.blit(font_score[score_second[-j]], (1050 - 92 * j, 310 - font_offsets[score_second[-j]]))
            pygame.draw.rect(self.surface, self.color_index[field_colors[third]], (10, 410, 1060, 200))
            draw_text_box(names[third], font_info, (120, 431), self.surface)
            if show_victories:
                draw_text_box(victories[third], font_info, (120, 485), self.surface)
            if goals[third] != '0':
                draw_text_box(goal_third, font_info, (120, 539), self.surface)
            # draw the score
            for i in range(len(score_third)):
                j = i + 1
                self.surface.blit(font_score[score_third[-j]], (1050 - 92 * j, 510 - font_offsets[score_third[-j]]))
        except:
            pass
        
        if player_page < 3:
            self.surface.blit(font_player_number[str(first + 1)], (45, 80 - font_offsets[str(first + 1)] // 2))
            if players > player_page * 3 + 1:
                self.surface.blit(font_player_number[str(second + 1)], (45, 280 - font_offsets[str(second + 1)] // 2))
            if players > player_page * 3 + 2:
                self.surface.blit(font_player_number[str(third + 1)], (45, 480 - font_offsets[str(third + 1)] // 2))
        else:
            self.surface.blit(font_player_number['1'], (20, 80 - font_offsets['1'] // 2))
            self.surface.blit(font_player_number[str(first + 1)[1]], (65, 80 - font_offsets[str(first + 1)[1]] // 2))
            if players > player_page * 3 + 1:
                self.surface.blit(font_player_number['1'], (20, 280 - font_offsets['1'] // 2))
                self.surface.blit(font_player_number[str(second + 1)[1]], (65, 280 - font_offsets[str(second + 1)[1]] // 2))
            if players > player_page * 3 + 2:
                self.surface.blit(font_player_number['1'], (20, 480 - font_offsets['1'] // 2))
                self.surface.blit(font_player_number[str(third + 1)[1]], (65, 480 - font_offsets[str(third + 1)[1]] // 2))
        pygame.draw.rect(self.surface, color_board_outline, (10, 10, 1060, 645), 4)

        draw_text_box(str(score_limit), font_info, (1175, 610), self.surface)
        draw_text_box(game_name, font_info, (970, 660), self.surface)
        blit('Score limit:', font_40, (1077, 618))
        blit('Game name:', font_40, (970, 622), False, (255, 255, 255))

        # draw the log
        # draw the outline
        pygame.draw.rect(self.surface, color_log_fill, (1073, 10, 205, 600), 0, 8)
        pygame.draw.rect(self.surface, (255, 255, 255), (1073, 10, 205, 40), 0, 8, 8, 8, 0, 0)
        pygame.draw.rect(self.surface, (255, 255, 255), (1073, 570, 205, 40), 0, 8, 0, 0, 8, 8)
        pygame.draw.rect(self.surface, color_info_outline, (1073, 10, 205, 600), 3, 8)
        # draw the info
        blit('Game log', font_log, (1175, 20), True, color_log_index)
        blit(f'Entries: {len(log)}', font_log, (1175, 577), True, color_log_index)
        # draw the entries
        for i in range(min(len(log) - log_cursor, 10)):
            blit(str(i + 1 + log_cursor), font_log, (1079, 65 + 50*i), False, color_log_index)
            pygame.draw.rect(self.surface, color_log_background, (1095 + 10*(len(str(i + 1 + log_cursor)) - 1), 55 + 50*i, 177 - 10*(len(str(i + 1 + log_cursor)) - 1), 45), 0, 8)
            pygame.draw.rect(self.surface, color_log_outline, (1095 + 10*(len(str(i + 1 + log_cursor)) - 1), 55 + 50*i, 177 - 10*(len(str(i + 1 + log_cursor)) - 1), 45), 3, 8)
            blit(log[i + log_cursor], font_data, (1100 + 10*(len(str(i + 1 + log_cursor)) - 1), 60 + 50*i), False, (255, 255, 255))
        
        if log:
            if pygame.key.get_pressed()[pygame.K_DOWN]:
                log_cursor += 1
                if log_cursor >= len(log):
                    log_cursor = len(log) - 1
            if pygame.key.get_pressed()[pygame.K_UP]:
                log_cursor -= 1
                if log_cursor < 0:
                    log_cursor = 0
        if pygame.key.get_pressed()[pygame.K_LEFT] and not was_pressed:
            player_page -= 1
            if player_page < 0:
                player_page = max_page
            was_pressed = True
        if pygame.key.get_pressed()[pygame.K_RIGHT] and not was_pressed:
            player_page += 1
            if player_page > max_page:
                player_page = 0
            was_pressed = True
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            ui_settings.blink_time.text = str(blink_time)
            ui_settings.game_name.text = game_name
            ui_settings.score_lim.text = str(score_limit)
            is_updating = False
            current_ui = 'pause'

    def process_commands(self):
        # gather input
        global command
        global is_updating # we're not gonna use the text_field's draw() method because we want to see the user typing
        global message # the message above the command prompt
        global scores
        global victories
        global names
        global score_limit
        global game_name
        global log
        global game_config
        global inverted_victory_mode
        global current_ui
        global is_game_running
        global game_conf_file
        global players
        global goals
        global field_colors
        global max_page
        global log_cursor
        process = False
        valid = True
        if not command:
            message = '§fEnter the command here:'
        if pygame.event.get(pygame.MOUSEBUTTONDOWN):
            if is_updating:
                is_updating = False
            elif self.command_line._is_over():
                pygame.event.get()
                is_updating = not is_updating
        pygame.draw.rect(self.surface, (240, 240, 240), (10, 660, 950, 50))
        if is_updating:
            command = self.command_line._update()
            if command and command[-1] == '§':
                command = command[:-1] # invalid character check
                self.command_line.text = self.command_line.text[:-1]
            if self.command_line.enter:
                process = True
        else:
            fancy_blit.fancy_blit(message, font_msg, (15, 615), self.surface, background_color=color_board_bg)
            fancy_blit.fancy_blit(command, font_cmd, (15, 660), self.surface)
            pygame.draw.rect(self.surface, (0, 0, 0), (10, 660, 950, 50), int(is_updating) * 2 + 2) # i don't want to set the outline width separately
            return

        args = command.split(' ')
        visible = args.copy()

        # colors
        if not args[0] in ['score', 'double', 'rename', 'menu', 'file', 'log', 'goal', 'victory', 'help']: # check if the command exists
            message = "§fscore|double|rename|menu|file|log|goal|victory|help ..."
            visible[0] = '§4' + visible[0]
            valid = False
        else:
            message = self.cmd_desc[args[0]]
        
        if len(args) > 1: # second argument (word)
            if args[0] == 'score':
                if not args[1] in ['add', 'remove', 'set', 'limit']:
                    visible[1] = '§4' + visible[1]
                    valid = False
                else:
                    message = self.set_desc[args[1]]
            elif args[0] == 'double': # full command
                if args[1] != '0' and args[1] != '6':
                    visible[1] = '§4' + visible[1]
                    valid = False
                else:
                    visible[1] = '§3' + visible[1]
                    try:
                        int(args[2]) # checks the length of it too
                    except:
                        if len(args) > 2:
                            visible[2] = '§4' + visible[2]
                        valid = False
                    else:
                        if 0 < int(args[2]) <= players:
                            visible[2] = '§6' + visible[2] + '§7'
                        else:
                            visible[2] = '§4' + visible[2]
                            valid = False
            elif args[0] == 'rename': # full command
                try:
                    int(args[1])
                except:
                    success = False
                else:
                    success = 0 < int(args[1]) <= players
                if success or args[1] == 'game':
                    visible[1] = '§3' + visible[1]
                    if len(args) > 2:
                        visible[2] = '§6' + visible[2]
                else:
                    visible[1] = '§4' + visible[1]
                    valid = False
            elif args[0] == 'menu': # full command
                visible[1] = '§c' + visible[1]
            elif args[0] == 'file': # full command
                if args[1] in ['set', 'reload', 'save']:
                    message = self.file_desc[args[1]]
                    if args[1] in ['reload', 'save']:
                        visible[1] = '§3' + visible[1] + '§7'
                    else:
                        visible[1] = '§0' + visible[1]
                        if len(args) > 2:
                            visible[2] = '§3' + visible[2]
                else:
                    visible[1] = '§4' + visible[1]
                    valid = False
            elif args[0] == 'help': # full command
                visible[1] = '§7' + visible[1] # this argument is ignored
            elif args[0] == 'log': # full command
                if args[1] == 'add':
                    message = '§flog add §b<entry: str>'
                    visible[1] += '§3'
                elif args[1] == 'remove':
                    message = '§flog add §b<from: int> §6[to: int]'
                    if len(args) > 2:
                        try:
                            int(args[2])
                        except:
                            success = False
                        else:
                            success = True
                        if success:
                            visible[2] = '§3' + visible[2]
                            if len(args) > 3:
                                try:
                                    int(args[3])
                                except:
                                    success = False
                                else:
                                    success = True
                                if success:
                                    visible[3] = '§6' + visible[3] + '§7'
                                else:
                                    visible[3] = '§4' + visible[3]
                                    valid = False
                        else:
                            visible[2] = '§4' + visible[2]
                            valid = False
                else:
                    visible[1] = '§4' + visible[1]
                    valid = False
            elif args[0] == 'goal': # full command
                try:
                    int(args[1])
                except:
                    success = False
                else:
                    success = 0 < int(args[1]) <= players
                if success:
                    visible[1] = '§3' + visible[1] + '§0'
                    if len(args) > 2:
                        if args[2] == 'fixed':
                            message = '§fgoal §b<player: int> §ffixed §6<value: int>'
                            if len(args) > 3:
                                try:
                                    int(args[3])
                                except:
                                    success = False
                                else:
                                    success = True
                                if success:
                                    visible[3] = '§6' + visible[3] + '§7'
                                else:
                                    visible[3] = '§4' + visible[3]
                                    valid = False
                        elif args[2] == 'relative':
                            message = '§fgoal §b<player: int> §frelative §6<player: int|most|least> §a<operation: +|-|/|*> §d<value: float>'
                            if len(args) > 3:
                                try:
                                    int(args[3])
                                except:
                                    success = False
                                else:
                                    success = 0 < int(args[3]) <= players
                                if success or args[3] in ['most', 'least']:
                                    visible[3] = '§6' + visible[3]
                                    if len(args) > 4:
                                        if args[4] in ['+', '-', '*', '/']:
                                            visible[4] = '§a' + visible[4]
                                            if len(args) > 5:
                                                try:
                                                    float(args[5])
                                                except:
                                                    success = False
                                                else:
                                                    success = True
                                                if success:
                                                    visible[5] = '§d' + visible[5] + '§7'
                                                else:
                                                    visible[5] = '§4' + visible[5]
                                                    valid = False
                                        else:
                                            visible[4] = '§4' + visible[4]
                                            valid = False
                                else:
                                    visible[3] = '§4' + visible[3]
                                    valid = False
                        else:
                            visible[2] = '§4' + visible[2]
                            valid = False
                else:
                    visible[1] = '§4' + visible[1]
                    valid = False
            elif args[0] == 'victory':
                try:
                    int(args[1])
                except:
                    success = False
                else:
                    success = 0 < int(args[1]) <= players
                if success:
                    visible[1] = '§3' + visible[1]
                    if len(args) > 2:
                        try:
                            int(args[2])
                        except:
                            success = False
                        else:
                            success = True
                        if success:
                            visible[2] = '§6' + visible[2] + '§7'
                        else:
                            visible[2] = '§4' + visible[2]
                            valid = False
                else:
                    visible[1] = '§4' + visible[1]
                    valid = False

        if len(args) > 2: # third argument, basically only the score command
            if args[0] == 'score':
                if args[1] == 'add' or args[1] == 'remove':
                    try:
                        int(args[2])
                    except:
                        success = False
                    else:
                        success = 0 < int(args[2]) <= players
                    if success or args[2] == 'all':
                        if args[2] == 'all':
                            message = self.set_desc[f'{args[1]} all']
                        else:
                            message = self.set_desc[args[1]]
                        visible[2] = '§3' + visible[2]
                        if len(args) == 4 or len(args) == 3 + players:
                            for i in range(len(args) - 3):
                                try: # i know it's a bit messy, but no one's gonna read this part anyway =)
                                    int(args[i + 3])
                                except:
                                    success = False
                                else:
                                    success = True
                                if success:
                                    if not i:
                                        visible[i+3] = '§6' + visible[i+3]
                                    else:
                                        visible[i+3] = '§a' + visible[i+3] + '§7'
                                else:
                                    visible[i+3] = '§4' + visible[i+3]
                                    valid = False
                        else:
                            if len(args) > 3:
                                visible[3] = '§4' + visible[3]
                                valid = False
                    else:
                        visible[2] = '§4' + visible[2]
                        valid = False
                elif args[1] == 'set':
                    try:
                        int(args[2])
                    except:
                        success = False
                    else:
                        success = 0 < int(args[2]) <= players
                    if success:
                        visible[2] = '§3' + visible[2]
                        if len(args) > 3:
                            try:
                                int(args[3])
                            except:
                                success = False
                            else:
                                success = True
                            if success:
                                visible[3] = '§6' + visible[3] + '§7'
                            else:
                                visible[3] = '§4' + visible[3]
                                valid = False
                    else:
                        visible[2] = '§4' + visible[2]
                        valid = False
                elif args[1] == 'limit':
                    if args[2] == 'set':
                        message = '§fscore limit set §b<value: int>'
                        if len(args) > 3:
                            try:
                                int(args[3])
                            except:
                                success = False
                            else:
                                success = True
                            if success:
                                visible[3] = '§3' + visible[3] + '§7'
                            else:
                                visible[3] = '§4' + visible[3]
                                valid = False
                    elif args[2] == 'mode':
                        message = '§fscore limit mode §b<least|most>'
                        if len(args) > 3:
                            if args[3] == 'least' or args[3] == 'most':
                                visible[3] = '§3' + visible[3] + '§7'
                            else:
                                visible[3] = '§4' + visible[3]
                                valid = False
                    else:
                        visible[2] = '§4' + visible[2]
                        valid = False

        # draw the text
        show = ''
        for i in visible:
            show = show + i + ' '
        fancy_blit.fancy_blit(message, font_msg, (15, 615), self.surface, background_color=color_board_bg)
        fancy_blit.fancy_blit(show, font_cmd, (15, 660), self.surface)
        pygame.draw.rect(self.surface, (0, 0, 0), (10, 660, 950, 50), int(is_updating) * 2 + 2) # i don't want to set the outline width separately

        # process
        if process and valid:
            ##print(f'[DEBUG] got command: {args}')
            # score command
            if args[0] == 'score': ## SCORE COMMAND
                if len(args) > 3: # there are always at least 4 arguments in a score command
                    if args[1] == 'add': ## ADD ARGUMENT
                        if args[2] == 'all':
                            try:
                                args[4]
                            except:
                                for i in range(players):
                                    scores[i] += int(args[3])
                                    game_events.add_event(True, 'increase_player', max_fps, i, int(args[3]) / max_fps)
                                    log.append(f'P{i+1}+{int(args[3])}')
                                    log_cursor = max(0, len(log) - 10)
                            else:
                                for i in range(players):
                                    scores[i] += int(args[i + 3])
                                    game_events.add_event(True, 'increase_player', max_fps, i, int(args[i + 3]) / max_fps)
                                    log.append(f'P{i+1}+{int(args[i+3])}')
                                    log_cursor = max(0, len(log) - 10)
                            game_events.add_event(False, 'score_change', max_fps)
                        else:
                            scores[int(args[2]) - 1] += int(args[3])
                            game_events.add_event(True, 'increase_player', max_fps, int(args[2]) - 1, int(args[3]) / max_fps)
                            game_events.add_event(False, 'score_change', max_fps)
                            log.append(f'P{int(args[2])}+{int(args[3])}')
                            log_cursor = max(0, len(log) - 10)
                    elif args[1] == 'remove': ## REMOVE ARGUMENT
                        if args[2] == 'all':
                            try:
                                args[4]
                            except:
                                for i in range(players):
                                    scores[i] -= int(args[3])
                                    game_events.add_event(True, 'increase_player', max_fps, i, -int(args[3]) / max_fps)
                                    log.append(f'P{i+1}-{int(args[3])}')
                                    log_cursor = max(0, len(log) - 10)
                            else:
                                for i in range(players):
                                    scores[i] -= int(args[i + 3])
                                    game_events.add_event(True, 'increase_player', max_fps, i, -int(args[i + 3]) / max_fps)
                                    log.append(f'P{i+1}-{int(args[i+3])}')
                                    log_cursor = max(0, len(log) - 10)
                            game_events.add_event(False, 'score_change', max_fps)
                        else:
                            scores[int(args[2]) - 1] -= int(args[3])
                            game_events.add_event(True, 'increase_player', max_fps, int(args[2]) - 1, -int(args[3]) / max_fps)
                            game_events.add_event(False, 'score_change', max_fps)
                            log.append(f'P{int(args[2])}-{int(args[3])}')
                            log_cursor = max(0, len(log) - 10)
                    elif args[1] == 'set': ## SET ARGUMENT
                        scores[int(args[2]) - 1] = int(args[3]) # won't be smooth
                        game_events.add_event(False, 'score_change', max_fps)
                        log.append(f'P{int(args[2])}={int(args[3])}')
                        log_cursor = max(0, len(log) - 10)
                    elif args[1] == 'limit': ## LIMIT ARGUMENT
                        if args[2] == 'set':
                            score_limit = int(args[3])
                            log.append(f'SL={int(args[3])}')
                            log_cursor = max(0, len(log) - 10)
                        elif args[2] == 'mode':
                            if args[3] == 'least':
                                inverted_victory_mode = False
                                log.append('LM=LEAST')
                                log_cursor = max(0, len(log) - 10)
                            else:
                                inverted_victory_mode = True
                                log.append('LM=MOST')
                                log_cursor = max(0, len(log) - 10)
                else:
                    print(f'Incomplete command: {command}')
            elif args[0] == 'double': ## DOUBLE COMMAND
                if len(args) > 2:
                    if args[1] == '0':
                        log.append(f'{int(args[2])}E0')
                        log_cursor = max(0, len(log) - 10)
                        victories[int(args[2]) - 1] += 1
                        game_events.add_event(True, 'blink', max_fps*blink_time - max_fps//2, int(args[2]) - 1, 2)
                    elif args[1] == '6':
                        log.append(f'{int(args[2])}E6')
                        log_cursor = max(0, len(log) - 10)
                        for i in range(players):
                            if i != int(args[2]) - 1:
                                scores[i] += 50
                                game_events.add_event(True, 'increase_player', max_fps, i, 50 / max_fps)
                                game_events.add_event(True, 'blink', max_fps*blink_time - max_fps//2, i, 1)
                        game_events.add_event(False, 'score_change', max_fps)
                else:
                    print(f'Incomplete command: {command}')
            elif args[0] == 'rename':
                try:
                    if args[1] == 'game':
                        game_name = command[12:]
                        log.append(f'GN={args[2]}')
                        log_cursor = max(0, len(log) - 10)
                    else:
                        if players < 10:
                            names[int(args[1]) - 1] = command[9:]
                            log.append(f'P{int(args[1])}N={command[9:]}')
                            log_cursor = max(0, len(log) - 10)
                        else:
                            names[int(args[1]) - 1] = command[10:]
                            log.append(f'P{int(args[1])}N={command[10:]}')
                            log_cursor = max(0, len(log) - 10)
                except:
                    print(f'Incomplete command: {command}')
            elif args[0] == 'menu':
                if game_conf_file and len(command) < 6: # if there's a save file and no_save wasn't specified:
                    game_config['log'] = log
                    game_config['goals'] = goals
                    game_config['names'] = names
                    game_config['scores'] = scores
                    game_config['players'] = players
                    game_config['victories'] = victories
                    game_config['game_name'] = game_name
                    game_config['score_limit'] = score_limit
                    game_config['limit_mode'] = inverted_victory_mode
                    with open(game_conf_file, 'w') as config_file:
                        config_file.write(json.dumps(game_config, indent=4, ensure_ascii=True))
                current_ui = 'menu'
            elif args[0] == 'file':
                if len(args) > 1:
                    if args[1] == 'set':
                        if len(args) > 2:
                            game_conf_file = command[9:]
                        else:
                            temp = filedialog.asksaveasfilename(defaultextension = '.json', filetypes = [('JSON files', '*.json'), ('All files', '*.*')], title = 'Save game data')
                            if temp:
                                game_conf_file = temp
                    if args[1] == 'save':
                        game_config['log'] = log
                        game_config['goals'] = goals
                        game_config['names'] = names
                        game_config['scores'] = scores
                        game_config['players'] = players
                        game_config['victories'] = victories
                        game_config['game_name'] = game_name
                        game_config['score_limit'] = score_limit
                        game_config['limit_mode'] = inverted_victory_mode
                        with open(game_conf_file, 'w') as config_file:
                            config_file.write(json.dumps(game_config, indent=4, ensure_ascii=True))
                    if args[1] == 'reload':
                        try:
                            with open(game_conf_file, 'r', -1, 'utf-8') as file:
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
                            victories = game_config['victories']
                            score_limit = game_config['score_limit']
                            inverted_victory_mode = game_config['limit_mode']
                        except KeyError:
                            print('File error: some of the critical values were not found, cannot proceed')
                            return
                        if players % 3:
                            max_page = players // 3
                        else:
                            max_page = players // 3 - 1
                        field_colors = [0] * players
            elif args[0] == 'help':
                print(command_help)
            elif args[0] == 'log':
                if len(args) > 2:
                    if args[1] == 'add':
                        log.append(command[8:])
                        log_cursor = max(0, len(log) - 10)
                    elif args[1] == 'remove':
                        if len(args) > 3:
                            del log[int(args[2]) - 1:int(args[3])]
                        else:
                            del log[int(args[2]) - 1]
                else:
                    print(f'Incomplete command: {command}')
            elif args[0] == 'goal':
                if len(args) > 3:
                    if args[2] == 'fixed':
                        goals[int(args[1]) - 1] = args[3]
                    elif args[2] == 'relative':
                        if len(args) > 3:
                            if args[3] == 'most':
                                goals[int(args[1]) - 1] = 'max(victories)'
                            elif args[3] == 'least':
                                goals[int(args[1]) - 1] = 'min(victories)'
                            else:
                                goals[int(args[1]) - 1] = f'victories[{int(args[3]) - 1}]'
                        if len(args) > 5:
                            goals[int(args[1]) - 1] = 'int(' + goals[int(args[1]) - 1] + args[4] + args[5] + ')'
                else:
                    print(f'Incomplete command: {command}')
            elif args[0] == 'victory':
                if len(args) > 2:
                    victories[int(args[1]) - 1] = int(args[2])
                else:
                    print(f'Incomplete command: {command}')
            command = ''
            self.command_line.text = ''
            is_updating = False
            return
        
ui_menu = menu()
ui_settings = settings()
ui_game = game()

while True:
    if pygame.event.get(pygame.QUIT):
        if is_game_running and game_conf_file:
            game_config['log'] = log
            game_config['goals'] = goals
            game_config['names'] = names
            game_config['scores'] = scores
            game_config['players'] = players
            game_config['victories'] = victories
            game_config['game_name'] = game_name
            game_config['score_limit'] = score_limit
            game_config['limit_mode'] = inverted_victory_mode
            with open(game_conf_file, 'w') as config_file:
                config_file.write(json.dumps(game_config, indent=4, ensure_ascii=True))
        pygame.quit()
        exit(0)
    changing_score = False
    for i in game_events.tick():
        if i['name'] == 'increase_player': # arg1 is the player, arg2 is the score
            visible_scores[i['arg1']] += i['arg2']
            changing_score = True
        if i['name'] == 'blink': # arg1 is the player, arg2 is the color
            if not i['time_left'] % max_fps:
                field_colors[i['arg1']] = 0
            elif i['time_left'] % max_fps == max_fps // 2:
                field_colors[i['arg1']] = i['arg2']
        if i['name'] == 'score_change':
            if max(scores) >= score_limit:
                if inverted_victory_mode:
                    j = max(scores)
                else:
                    j = min(scores)
                winners = []
                for k in range(players):
                    if scores[k] == j:
                        winners.append(k)
                        game_events.add_event(True, 'blink', max_fps*blink_time - max_fps//2 - 1, k, 2)
                        log.append(f'{k+1}W@{scores[k]}')
                        log_cursor = max(0, len(log) - 10)
                    else:
                        game_events.add_event(True, 'blink', max_fps*blink_time - max_fps//2 - 1, k, 1)
                        log.append(f'{k+1}F@{scores[k]}')
                        log_cursor = max(0, len(log) - 10)
                game_events.add_event(False, 'clear_score', max_fps*blink_time - max_fps//2 - 1)
                for j in winners:
                    victories[j] += 1
        if i['name'] == 'clear_score':
            scores = [0] * players
    if not changing_score:
        visible_scores = scores.copy()
    if current_ui == "menu":
        ui_menu.draw()
    elif current_ui == 'settings' or current_ui == 'pause':
        ui_settings.draw_global()
    elif current_ui == 'player_edit' or current_ui == 'player_setup':
        ui_settings.draw_player_list()
    elif current_ui == 'setup':
        ui_game.draw_setup()
    elif current_ui == 'game':
        ui_game.draw_game()
        ui_game.process_commands()
    pygame.display.update()
    gametick.tick(max_fps)