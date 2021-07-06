# init
import os
import json
import random
import config
if __name__ == '__main__':
    import pygame
    import button
    import switch
    import tkinter
    import hyperlink
    import text_field
    import fancy_blit
    import dropdown_list
    import event_handler
    import multiprocessing
    from tkinter import filedialog
    multiprocessing.set_start_method('spawn')

global_config = config.config({}, 'config_global.json') # load the config file
global_config.load('config_global.json')
global_config.get('voice', True)
global_config.get('victories', True)
global_config.get('progress', True)
global_config.get('blink_time', 5) # for each setting we need, check if it's there and if it's not, set it to default value
global_config.get('max_fps', 60)
global_config.get('lang', 'en') # this is the only reason i moved this here
global_config.get('image_scale', 1)
lang_type = global_config.get('lang')
scale = global_config.get('image_scale')

try:
    with open(f'assets/lang/{lang_type}.json', 'r', -1, 'utf-8') as lang_file:
        lang = json.load(lang_file)
except:
    try:
        print(f'File error: language file "assets/lang/{lang_type}.json" not found, gotta use English')
        with open('assets/lang/en.json', 'r', -1, 'utf-8') as lang_file:
            lang = json.load(lang_file)
        lang_type = 'en'
        global_config.set('lang', 'en')
    except:
        print('File error: ENGLISH LANGUAGE FILE (assets/lang/en.json) NOT FOUND')
        input('Cannot start the program, press Enter to exit...')
        exit(-1)

try:
    import gtts
except ModuleNotFoundError:
    print(lang['err_lib_not_installed'].format(lib='gtts'))
    allow_tts = False
else:
    allow_tts = True

try: 
    import playsound
except ModuleNotFoundError:
    print(lang['err_lib_not_installed'].format(lib='playsound'))
    allow_tts = False
else:
    allow_tts = True

# speak code in case this isn't the main process
def speak(my_text, lang):
    rand = random.randint(-2147483648, 2147483647)
    gtts.gTTS(text=my_text, lang=lang).save(f'temp{rand}.mp3')
    playsound.playsound(f'temp{rand}.mp3', True)
    os.remove(f'temp{rand}.mp3')
    
if __name__ != '__main__':
    with open('temp.txt', 'r') as file:
        to_speak = file.read()
    try:
        os.remove('temp.txt')
    except:
        pass
    rand_num = speak(to_speak, lang['google_lang_code'])
    exit()

useless = tkinter.Tk()
useless.withdraw()

pygame.init()
pygame.mixer.init()

gametick = pygame.time.Clock()
game_events = event_handler.EventHandler()

icon = pygame.image.load("assets/window.png")
pygame.display.set_icon(icon)
final_window = pygame.display.set_mode((int(1280 * scale), int(720 * scale)))
window = pygame.Surface((1280, 720))
def upd_win_caption(): # otherwise i will forget to change the value in settings
    pygame.display.set_caption(f"{lang['program_name']} (v. 1.0 release candidate 5)")
upd_win_caption()
game_version = "v. 1.0-rc5"

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
    global was_pressed_esc
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
    was_pressed_esc = False
    is_updating = False

    message = lang['enter_command']

    try:
        with open(f'assets/command_help_{lang_type}.txt', 'r', -1, 'utf-8') as help_file:
            command_help = help_file.read()
    except:
        print(lang['err_no_translated_help'].format(lang=lang_type))
        try:
            with open('assets/command_help_en.txt', 'r', -1, 'utf-8') as help_file:
                command_help = help_file.read()
        except:
            command_help = lang['no_help']
            print(lang['err_no_help'])

predefine_variables()
available_lang_ids = os.listdir('assets/lang')
available_langs = []
available_lang_names = []
for i in range(len(available_lang_ids)):
    available_lang_ids[i] = available_lang_ids[i][:-5]
    with open(f'assets/lang/{available_lang_ids[i]}.json', 'r', -1, 'utf-8') as file:
        available_langs.append(json.load(file))
        available_lang_names.append(available_langs[i]['lang_name'])

# utility functions
def draw_rect(x1, y1, x2, y2, fill_color = (0, 204, 204), outline=3, outline_color = (0, 0, 0), surface=pygame.display.get_surface()):
    '''A utility function that draws a rectangle with just one line'''
    if x1 > x2 or y1 > y2:
        raise ValueError("first set of coordinates must represent top left corner")
    dx = x2 - x1
    dy = y2 - y1
    pygame.draw.rect(surface, fill_color, (x1, y1, dx, dy))
    pygame.draw.rect(surface, outline_color, (x1, y1, dx, dy), outline)
def blit(text, font, pos, center=False, color=(0, 0, 0), surface=pygame.display.get_surface()):
    '''Blits some text to a chosen surface with only one line instead of two'''
    j = font.render(text, 1, color)
    if center is True:
        pos = (pos[0]-j.get_width() / 2, pos[1])
    elif center == 'back':
        pos = (pos[0]-j.get_width(), pos[1])
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
def narrate(text):
    if allow_tts and voice:
        with open('temp.txt', 'w') as file:
            file.write(text)
        p = multiprocessing.Process(target=speak)
        p.start()

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

        self.btn_new_file = button.Button(color_board_outline, 490, 250, 300, 75, self.surface, lang['btn_new_file'])
        self.btn_import = button.Button(color_board_outline, 490, 335, 300, 75, self.surface, lang['btn_open'])
        self.btn_settings = button.Button(color_board_outline, 490, 420, 300, 75, self.surface, lang['btn_settings'])

        self.btn_continue = button.Button(color_board_outline, 490, 195, 300, 75, self.surface, lang['btn_continue'])

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
            if self.btn_continue.smart_draw(72, bkp_pos) and pygame.event.get(pygame.MOUSEBUTTONDOWN):
                current_ui = 'game'
        else:
            self.btn_new_file.y = 250
            self.btn_import.y = 335
            self.btn_settings.y = 420
        if self.btn_import.smart_draw(72, bkp_pos) and pygame.event.get(pygame.MOUSEBUTTONDOWN):
            game_conf_file = filedialog.askopenfilename(title='Load game', filetypes=[('Game file', '*.json'), ('All files', '*.*')])
            try:
                with open(game_conf_file, 'r', -1, 'utf-8') as file:
                    game_config = json.load(file)
            except FileNotFoundError:
                return
            try:
                game_name = game_config['game_name']
            except KeyError:
                game_name = lang['no_game_name']
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
                print(lang['err_cannot_load_game'])
                return
            if players % 3:
                max_page = players // 3
            else:
                max_page = players // 3 - 1
            field_colors = [0] * players
            visible_scores = scores.copy()
            is_game_running = True
            current_ui = 'game'
        if self.btn_settings.smart_draw(72, bkp_pos) and pygame.event.get(pygame.MOUSEBUTTONDOWN):
            ui_settings.blink_time.text = str(blink_time)
            ui_settings.game_name.text = game_name
            ui_settings.score_lim.text = str(score_limit)
            current_ui = 'settings'
        if self.btn_new_file.smart_draw(72, bkp_pos) and pygame.event.get(pygame.MOUSEBUTTONDOWN):
            predefine_variables() # we don't want to reload the previous game
            ui_game.__init__() # that is needed too
            current_ui = 'setup'
        blit(game_version, font_40, (10, 680), surface=self.surface)


class settings:
    def __init__(self):
        self.surface = window
        # global settings
        if allow_tts:
            self.voice_enabled = switch.Switch(1180, 100, self.surface) ## note: a switch is 86x36 pixels
        else:
            self.voice_enabled = switch.Switch(1180, 100, self.surface, (102, 204, 204), outline_color=(127, 127, 127), disable_color=(206, 206, 206))
        self.show_victories = switch.Switch(1180, 150, self.surface)
        self.show_goal_progress = switch.Switch(1180, 200, self.surface)
        self.blink_time = text_field.TextField(1070, 250, 200, 45, blink_time, font_50, self.surface, 'int')
        self.language = dropdown_list.DropdownList(available_lang_names, available_lang_ids.index(lang_type), (1270, 300), font_50, self.surface, 200,
                                                   False, 6, color_board_outline, (0, 232, 232), color_scroll=(0, 63, 63),
                                                   color_hover_base=(0, 240, 240), color_hover_origin=color_bg,
                                                   color_hover_scroll=(0, 0, 0))
        self.scale = text_field.TextField(1070, 355, 200, 45, str(scale), font_50, self.surface, 'float')
        self.fps = text_field.TextField(1070, 405, 200, 45, str(max_fps), font_50, self.surface, 'int')
        # game settings
        self.game_name = text_field.TextField(1070, 480, 200, 45, game_name, font_50, self.surface)
        self.score_lim = text_field.TextField(1070, 530, 200, 45, score_limit, font_50, self.surface, 'int')
        self.score_mode = switch.Switch(1180, 580, self.surface)
        self.filename = button.Button(color_board_outline, 1120, 630, 150, 40, self.surface, lang['btn_change_file'])
        self.goto_player_name = button.Button(color_board_outline, 20, 680, 150, 35, self.surface, lang['btn_edit_player_names'], font_40)
        self.go_menu = button.Button(color_board_outline, 175, 680, 150, 35, self.surface, lang['btn_menu'], font_40)
        # player names
        self.player_names = []
        for i in range(18):
            self.player_names.append(text_field.TextField(20+415*(i%3) + 175, (i//3) * 100 + 100, 220, 50, '', font_50, self.surface))
        # utility stuff
        self.go_back = hyperlink.Hyperlink((0, 0, 0), 10, 0, lang['link_back'])
        ## note: everything in self is not the settings, but the tool used to change them
    
    def draw_global(self):
        global current_ui
        global voice
        global show_victories
        global show_progress
        global blink_time
        global lang_type
        global lang
        global was_pressed_esc
        global message
        global command_help
        global scale
        global final_window
        global max_fps
        if not was_pressed_esc and pygame.key.get_pressed()[pygame.K_ESCAPE]:
            was_pressed_esc = True
            is_clicked = True
        elif was_pressed_esc and pygame.key.get_pressed()[pygame.K_ESCAPE]:
            was_pressed_esc = True
            is_clicked = False
        else:
            was_pressed_esc = False
            is_clicked = False
        self.surface.fill(color_bg)
        if self.go_back.smart_draw(self.surface, bkp_pos=bkp_pos) or is_clicked:
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
        blit(lang['global_settings'], font_40, (20, 50), False, (100, 100, 100), self.surface)
        if allow_tts:
            blit(lang['narrator'], font_72, (20, 80), surface=self.surface)
        else:
            blit(lang['narrator'], font_72, (20, 80), False, (127, 127, 127), self.surface)
        blit(lang['show_player_victories'], font_72, (20, 130), surface=self.surface)
        blit(lang['show_goal_progress'], font_72, (20, 180), surface=self.surface)
        blit(lang['blink_time'], font_72, (20, 230), surface=self.surface)
        blit(lang['language'], font_72, (20, 280), surface=self.surface)
        blit(lang['image_scale'], font_72, (20, 335), surface=self.surface)
        blit(lang['framerate'], font_72, (20, 385), surface=self.surface)
        if allow_tts:
            if self.voice_enabled.smart_draw(global_config.get('voice'), bkp_pos=bkp_pos):
                voice = not voice
                global_config.set('voice', voice)
        else:
            self.voice_enabled.draw(False, (0, 0))
        if self.show_victories.smart_draw(global_config.get('victories'), bkp_pos=bkp_pos):
            show_victories = not show_victories
            global_config.set('victories', show_victories)
        if self.show_goal_progress.smart_draw(global_config.get('progress'), bkp_pos=bkp_pos):
            show_progress = not show_progress
            global_config.set('progress', show_progress)
        temp_blink_time = self.blink_time.draw(bkp_pos=bkp_pos)
        if temp_blink_time is not False:
            if temp_blink_time >= 0:
                blink_time = temp_blink_time
                global_config.set('blink_time', temp_blink_time)
            else:
                blink_time = 0
                self.blink_time.text = '0'
                global_config.set('blink_time', 0)
        if is_game_running:
            self._draw_game()
        temp = self.scale.draw(bkp_pos=bkp_pos)
        if temp is not False:
            if temp < 0.25:
                temp = 0.25
                self.scale.text = '0.25'
            scale = temp
            final_window = pygame.display.set_mode((int(1280 * scale), int(720 * scale)))
            global_config.set('image_scale', scale)
        temp = self.fps.draw(bkp_pos=bkp_pos)
        if temp is not False:
            if temp > 5:
                max_fps = temp
            else:
                max_fps = 5 # anything below 5 fps is pretty much unusable
        temp = self.language.update(bkp_pos=bkp_pos)
        if temp is not None:
            lang_type = available_lang_ids[temp]
            lang = available_langs[temp]
            self.__init__()
            ui_menu.__init__()
            ui_game.__init__() # we need to update all the buttons since they are defined once in __init__ and don't update immediately
            global_config.set('lang', lang_type)
            upd_win_caption()
            message = lang['enter_command']
            try:
                with open(f'assets/command_help_{lang_type}.txt', 'r', -1, 'utf-8') as help_file:
                    command_help = help_file.read()
            except:
                print(lang['err_no_translated_help'].format(lang=lang_type))
                try:
                    with open('assets/command_help_en.txt', 'r', -1, 'utf-8') as help_file:
                        command_help = help_file.read()
                except:
                    command_help = lang['no_help']
                    print(lang['err_no_help'])

    def _draw_game(self):
        global current_ui
        global game_name
        global score_limit
        global game_conf_file
        global inverted_victory_mode
        global is_game_running
        blit(lang['game_settings'], font_40, (20, 435), False, (100, 100, 100), surface=self.surface)
        blit(lang['game_name'], font_72, (20, 460), surface=self.surface)
        blit(lang['score_limit'], font_72, (20, 510), surface=self.surface)
        blit(lang['victory_mode'], font_72, (20, 560), surface=self.surface)
        blit(lang['save_file'], font_72, (20, 610), surface=self.surface)
        blit(lang['game_will_be_saved'], font_40, (330, 680), False, (85, 85, 85), surface=self.surface)
        blit(game_conf_file, font_50, (1115, 625), 'back', surface=self.surface)
        if self.goto_player_name.smart_draw(66, bkp_pos=bkp_pos):
            for i in range(players):
                self.player_names[i].text = names[i]
            if current_ui == 'pause':
                current_ui = 'player_edit'
        if self.go_menu.smart_draw(66, bkp_pos=bkp_pos):
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
        temp = self.game_name.draw(bkp_pos=bkp_pos)
        if temp is not False:
            game_name = temp
        temp = self.score_lim.draw(bkp_pos=bkp_pos)
        if temp is not False:
            if temp > 0:
                score_limit = temp
            else:
                score_limit = 1
                self.score_lim.text = '1'
        if self.score_mode.smart_draw(inverted_victory_mode, bkp_pos=bkp_pos):
            inverted_victory_mode = not inverted_victory_mode
        if self.filename.smart_draw(bkp_pos=bkp_pos):
            temp = filedialog.asksaveasfilename(defaultextension = '.json', filetypes = [('JSON files', '*.json'), ('All files', '*.*')], title = 'Save game data')
            if temp != '':
                game_conf_file = temp

    def draw_player_list(self):
        global current_ui
        global was_pressed_esc
        if not was_pressed_esc and pygame.key.get_pressed()[pygame.K_ESCAPE]:
            was_pressed_esc = True
            is_clicked = True
        elif was_pressed_esc and pygame.key.get_pressed()[pygame.K_ESCAPE]:
            was_pressed_esc = True
            is_clicked = False
        else:
            was_pressed_esc = False
            is_clicked = False
        self.surface.fill(color_bg)
        for i in range(players):
            blit(lang['player_name_desc'].format(num=i+1), font_72, (20+415*(i%3), (i//3) * 100 + 100), surface=self.surface)
            temp = self.player_names[i].draw()
            if temp is not False:
                names[i] = temp
                game_config['names'][i] = temp
        if self.go_back.smart_draw(self.surface, bkp_pos=bkp_pos) or is_clicked:
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
        self.game_name = text_field.TextField(800, 90, 460, 65, game_name, font_72, self.surface)
        self.player_count = text_field.TextField(800, 160, 460, 65, players, font_72, self.surface, 'int')
        self.score_lim = text_field.TextField(800, 230, 460, 65, score_limit, font_72, self.surface, 'int')
        self.set_player_names = button.Button(color_board_outline, 20, 300, 400, 65, self.surface, lang['btn_set_player_names'])
        self.start = button.Button(color_board_outline, 950, 630, 310, 75, self.surface, lang['btn_save'])
        self.go_menu = hyperlink.Hyperlink((0, 0, 0), 10, 0, lang['link_menu'])
        self.start_no_file = button.Button(color_board_outline, 585, 630, 350, 75, self.surface, lang['btn_start_no_save'])

        self.no_file = button.Button((168, 0, 0), 425, 375, 200, 60, self.surface, lang['btn_continue'])
        self.try_again = button.Button(color_board_outline, 655, 375, 200, 60, self.surface, lang['btn_back'])

        self.color_index = [color_board_bg, color_red, color_green]

        self.command_line = text_field.TextField(10, 660, 950, 50, command, font_cmd, self.surface)
        self.cmd_desc = {'score': '§fscore <add|remove|set|limit> ...',
                         'double': '§fdouble §b<0|6> §6<player: int>',
                         'rename': '§frename §b<player: int|game> §6<name: str>',
                         'menu': '§fmenu §c[no_save]',
                         'file': '§ffile <set|reload|save> ...',
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

        self.operator_desc = {'+': lang['operator_plus'],
                              '-': lang['operator_minus'],
                              '*': lang['operator_mult'],
                              '/': lang['operator_div']}

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
        global visible_scores
        global was_pressed
        global was_pressed_esc
        self.surface.fill(color_bg)
        if not was_pressed_esc and pygame.key.get_pressed()[pygame.K_ESCAPE]:
            was_pressed_esc = True
            is_clicked = True
        elif was_pressed_esc and pygame.key.get_pressed()[pygame.K_ESCAPE]:
            was_pressed_esc = True
            is_clicked = False
        else:
            was_pressed_esc = False
            is_clicked = False
        blit(lang['new_game'], font_96, (640, 10), True, surface=self.surface)
        blit(lang['game_name'], font_72, (20, 80), surface=self.surface)
        blit(lang['player_amount'], font_72, (20, 150), surface=self.surface)
        blit(lang['score_limit_desc'], font_72, (20, 220), surface=self.surface)
        error_messages = []
        if players < 2:
            error_messages.append(lang['err_not_enough_players'])
        if players > 18:
            error_messages.append(lang['err_too_many_players'])
        if score_limit <= 0:
            error_messages.append(lang['err_negative_limit'])
        if error_messages:
            j = 0
            for i in error_messages:
                blit(i, font_50, (20, j*50 + 370), False, (200, 0, 0), surface=self.surface)
                j += 1
        temp = self.game_name.draw(fancy_format=False, bkp_pos=bkp_pos)
        if temp is not False:
            game_name = temp
            game_config['game_name'] = temp
        temp = self.player_count.draw(bkp_pos=bkp_pos)
        if temp is not False:
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
        temp = self.score_lim.draw(bkp_pos=bkp_pos)
        if temp is not False:
            score_limit = temp
            game_config['score_limit'] = temp
        if self.go_menu.smart_draw(self.surface, bkp_pos=bkp_pos) or is_clicked:
            current_ui = 'menu'
        if self.set_player_names.smart_draw(72, bkp_pos=bkp_pos) and players <= 18:
            for i in range(players):
                ui_settings.player_names[i].text = names[i]
            try:
                names[players-1]
                game_config['names'][players-1]
            except:
                names = ['Player'] * players
                game_config['names'] = ['player'] * players
            current_ui = 'player_setup'
        if self.start_no_file.smart_draw(72, bkp_pos=bkp_pos) and not error_messages:
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
        if self.start.smart_draw(72, bkp_pos=bkp_pos):
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
                    draw_rect(410, 270, 870, 450, surface=self.surface)
                    draw_rect(410, 270, 870, 300, color_bg, surface=self.surface)
                    blit(lang['warn_no_file_title'], font_28, (640, 270), True, surface=self.surface)
                    blit(lang['warn_no_file_line1'], font_40, (640, 300), True, surface=self.surface)
                    blit(lang['warn_no_file_line2'], font_40, (640, 330), True, surface=self.surface)
                    while True:
                        if self.no_file.smart_draw(60, bkp_pos, (168, 30, 30), (220, 45, 45), (128, 15, 15)):
                            break
                        if self.try_again.smart_draw(bkp_pos=bkp_pos):
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
        global was_pressed_esc
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
            if eval(goals[first]) != 0:
                goal_first = str(eval(goals[first]) - victories[first]) + lang['goal_left_ext'] + str(round(victories[first] / eval(goals[first]) * 100, 1)) + '%)'
            else:
                goal_first = f'{str(eval(goals[first]) - victories[first])}{lang["goal_left"]}'
            try:
                if eval(goals[second]) != 0:
                    goal_second = str(eval(goals[second]) - victories[second]) + lang['goal_left_ext'] + str(round(victories[second] / eval(goals[second]) * 100, 1)) + '%)'
                else:
                    goal_second = f'{str(eval(goals[second]) - victories[second])}{lang["goal_left"]}'
                if eval(goals[third]) != 0:
                    goal_third = str(eval(goals[third]) - victories[third]) + lang['goal_left_ext'] + str(round(victories[third] / eval(goals[third]) * 100, 1)) + '%)'
                else:
                    goal_third = f'{str(eval(goals[first]) - victories[first])}{lang["goal_left"]}'
            except:
                pass
        else:
            if eval(goals[first]) != '0':
                goal_first = str(eval(goals[third]) - victories[third]) + lang["goal_left"]
            else:
                goal_first = '0'
            try:
                if eval(goals[second]) != '0':
                    goal_second = str(eval(goals[second]) - victories[second]) + lang["goal_left"]
                else:
                    goal_second = '0'
                if eval(goals[third]) != '0':
                    goal_third = str(eval(goals[third]) - victories[third]) + lang["goal_left"]
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
        blit(lang['ui_score_limit'], font_40, (1170, 618), 'back', surface=self.surface)
        blit(lang['ui_game_name'], font_40, (970, 622), False, (255, 255, 255), surface=self.surface)

        # draw the log
        # draw the outline
        pygame.draw.rect(self.surface, color_log_fill, (1073, 10, 205, 600), 0, 8)
        pygame.draw.rect(self.surface, (255, 255, 255), (1073, 10, 205, 40), 0, 8, 8, 8, 0, 0)
        pygame.draw.rect(self.surface, (255, 255, 255), (1073, 570, 205, 40), 0, 8, 0, 0, 8, 8)
        pygame.draw.rect(self.surface, color_info_outline, (1073, 10, 205, 600), 3, 8)
        # draw the info
        blit(lang['ui_log'], font_log, (1175, 20), True, color_log_index, surface=self.surface)
        blit(lang['log_len'].format(number=len(log)), font_log, (1175, 577), True, color_log_index, surface=self.surface)
        # draw the entries
        for i in range(min(len(log) - log_cursor, 10)):
            blit(str(i + 1 + log_cursor), font_log, (1079, 65 + 50*i), False, color_log_index, surface=self.surface)
            pygame.draw.rect(self.surface, color_log_background, (1095 + 10*(len(str(i + 1 + log_cursor)) - 1), 55 + 50*i, 177 - 10*(len(str(i + 1 + log_cursor)) - 1), 45), 0, 8)
            pygame.draw.rect(self.surface, color_log_outline, (1095 + 10*(len(str(i + 1 + log_cursor)) - 1), 55 + 50*i, 177 - 10*(len(str(i + 1 + log_cursor)) - 1), 45), 3, 8)
            blit(log[i + log_cursor], font_data, (1100 + 10*(len(str(i + 1 + log_cursor)) - 1), 60 + 50*i), False, (255, 255, 255), surface=self.surface)
        
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
        if not was_pressed_esc and pygame.key.get_pressed()[pygame.K_ESCAPE]:
            was_pressed_esc = True
            ui_settings.blink_time.text = str(blink_time)
            ui_settings.game_name.text = game_name
            ui_settings.score_lim.text = str(score_limit)
            is_updating = False
            current_ui = 'pause'
        elif was_pressed_esc and pygame.key.get_pressed()[pygame.K_ESCAPE]:
            was_pressed_esc = True
        else:
            was_pressed_esc = False

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
            message = lang['enter_command']
        if pygame.event.get(pygame.MOUSEBUTTONDOWN):
            if is_updating:
                is_updating = False
            elif self.command_line.is_over(bkp_pos=bkp_pos):
                pygame.event.get()
                is_updating = not is_updating
        pygame.draw.rect(self.surface, (240, 240, 240), (10, 660, 950, 50))
        if is_updating:
            command = self.command_line.update()
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
                            message = '§fgoal §b<player: int> §frelative §6<player: int|most|least> §a[<operation: +|-|/|*> §d<value: float>]'
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
                        if args[2] != 'all':
                            try: # i know it's a bit messy, but no one's gonna read this part anyway =)
                                int(args[3])
                            except:
                                success = False
                            else:
                                success = True
                            if success:
                                visible[3] = '§6' + visible[3] + '§7'
                        elif len(args) == 3 + players:
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
                                success = int(args[3]) > 0
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
                            game_events.add_event(False, 'score_change', max_fps + 10)
                        else:
                            scores[int(args[2]) - 1] += int(args[3])
                            game_events.add_event(True, 'increase_player', max_fps, int(args[2]) - 1, int(args[3]) / max_fps)
                            game_events.add_event(False, 'score_change', max_fps*(5 if voice else 0.5))
                            log.append(f'P{int(args[2])}+{int(args[3])}')
                            log_cursor = max(0, len(log) - 10)
                            narrate(lang['narrator_add_points'].format(amount=args[3],player=names[int(args[2]) - 1]))
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
                            game_events.add_event(False, 'score_change', max_fps + 10)
                        else:
                            scores[int(args[2]) - 1] -= int(args[3])
                            game_events.add_event(True, 'increase_player', max_fps, int(args[2]) - 1, -int(args[3]) / max_fps)
                            game_events.add_event(False, 'score_change', max_fps*(5 if voice else 0.5))
                            log.append(f'P{int(args[2])}-{int(args[3])}')
                            log_cursor = max(0, len(log) - 10)
                            narrate(lang['narrator_take_points'].format(amount=args[3],player=names[int(args[2]) - 1]))
                    elif args[1] == 'set': ## SET ARGUMENT
                        scores[int(args[2]) - 1] = int(args[3]) # won't be smooth
                        game_events.add_event(False, 'score_change', max_fps*(4 if voice else 0.5))
                        log.append(f'P{int(args[2])}={int(args[3])}')
                        log_cursor = max(0, len(log) - 10)
                        narrate(lang['narrator_set_points'].format(amount=args[3],player=names[int(args[2]) - 1]))
                    elif args[1] == 'limit': ## LIMIT ARGUMENT
                        if args[2] == 'set':
                            score_limit = int(args[3])
                            log.append(f'SL={int(args[3])}')
                            log_cursor = max(0, len(log) - 10)
                            narrate(lang['narrator_set_limit'].format(value=args[3]))
                        elif args[2] == 'mode':
                            if args[3] == 'least':
                                inverted_victory_mode = False
                                log.append('LM=LEAST')
                                log_cursor = max(0, len(log) - 10)
                                narrate(lang['narrator_limit_mode_least'])
                            else:
                                inverted_victory_mode = True
                                log.append('LM=MOST')
                                log_cursor = max(0, len(log) - 10)
                                narrate(lang['narrator_limit_mode_most'])
                else:
                    print(lang['err_incomplete_command'].format(command=command))
            elif args[0] == 'double': ## DOUBLE COMMAND
                if len(args) > 2:
                    if args[1] == '0':
                        log.append(f'{int(args[2])}E0')
                        log_cursor = max(0, len(log) - 10)
                        victories[int(args[2]) - 1] += 1
                        game_events.add_event(True, 'blink', max_fps*blink_time - max_fps//2 + 1, int(args[2]) - 1, 2)
                        narrate(lang['narrator_end_0'].format(name=names[int(args[2]) - 1]))
                    elif args[1] == '6':
                        log.append(f'{int(args[2])}E6')
                        log_cursor = max(0, len(log) - 10)
                        for i in range(players):
                            if i != int(args[2]) - 1:
                                scores[i] += 50
                                game_events.add_event(True, 'increase_player', max_fps, i, 50 / max_fps)
                                game_events.add_event(True, 'blink', max_fps*blink_time - max_fps//2 + 1, i, 1)
                        narrate(lang['narrator_end_6'].format(name=names[int(args[2]) - 1]))
                        game_events.add_event(False, 'score_change', max_fps*(6.5 if voice else 0.5))
                else:
                    print(lang['err_incomplete_command'].format(command=command))
            elif args[0] == 'rename':
                try:
                    if args[1] == 'game':
                        game_name = command[12:]
                        log.append(f'GN={args[2]}')
                        log_cursor = max(0, len(log) - 10)
                        narrate(lang['narrator_rename_game'].format(new_name=command[12:]))
                    else:
                        if players < 10:
                            names[int(args[1]) - 1] = command[9:]
                            log.append(f'P{int(args[1])}N={command[9:]}')
                            log_cursor = max(0, len(log) - 10)
                            narrate(lang['narrator_player_rename'].format(player=args[1], new_name=command[9:]))
                        else:
                            names[int(args[1]) - 1] = command[10:]
                            log.append(f'P{int(args[1])}N={command[10:]}')
                            log_cursor = max(0, len(log) - 10)
                            narrate(lang['narrator_player_rename'].format(player=args[1], new_name=command[9:]))
                except:
                    print(lang['err_incomplete_command'].format(command=command))
            elif args[0] == 'menu':
                log.append('exit')
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
                            log.append(f'F={game_conf_file}')
                            log_cursor = max(0, len(log) - 10)
                            narrate(lang['narrator_set_save'].format(new_file=game_conf_file))
                        else:
                            temp = filedialog.asksaveasfilename(defaultextension = '.json', filetypes = [('JSON files', '*.json'), ('All files', '*.*')], title = 'Save game data')
                            if temp:
                                game_conf_file = temp
                                log.append(f'F={game_conf_file}')
                                log_cursor = max(0, len(log) - 10)
                                narrate(lang['narrator_set_save'].format(new_file=game_conf_file))
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
                        narrate(lang['narrator_save_game'])
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
                        narrate(lang['narrator_reload_save'])
            elif args[0] == 'help':
                print(command_help)
                narrate(lang['narrator_help_printed'])
            elif args[0] == 'log':
                if len(args) > 2:
                    if args[1] == 'add':
                        log.append(command[8:])
                        log_cursor = max(0, len(log) - 10)
                        narrate(lang['narrator_add_log'].format(entry=command[8:]))
                    elif args[1] == 'remove':
                        if len(args) > 3:
                            del log[int(args[2])-1 : int(args[3])]
                            narrate(lang['narrator_remove_log_range'].format(start=args[2], finish=args[3]))
                        else:
                            del log[int(args[2]) - 1]
                            narrate(lang['narrator_remove_log_single'].format(number=args[2]))
                else:
                    print(lang['err_incomplete_command'].format(command=command))
            elif args[0] == 'goal':
                if len(args) > 3:
                    if args[2] == 'fixed':
                        goals[int(args[1]) - 1] = args[3]
                        log.append(f'{args[1]}G={args[3]}')
                        log_cursor = max(0, len(log) - 10)
                        narrate(lang['narrator_set_fixed_goal'].format(player=names[int(args[1]) - 1], goal=args[3]))
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
                            if args[3] in ['least', 'most']:
                                log.append(f'{args[1]}G=[{args[3].upper()}]{args[4]}{args[5]}')
                            else:
                                log.append(f'{args[1]}G=[{args[3].upper()}]{args[4]}{args[5]}')
                            if args[3] == 'least':
                                narrate(lang['narrator_set_goal_relative_lowest'].format(player=names[int(args[1]) - 1], operation=self.operator_desc[args[4]], value=args[5]))
                            elif args[3] == 'most':
                                narrate(lang['narrator_set_goal_relative_highest'].format(player=names[int(args[1]) - 1], operation=self.operator_desc[args[4]], value=args[5]))
                            else:
                                narrate(lang['narrator_set_goal_relative_player'].format(player=names[int(args[1]) - 1], target=names[int(args[3]) - 1], operation=self.operator_desc[args[4]], value=args[5]))
                        else:
                            log.append(f'{args[1]}G=[{args[3].upper()}]')
                            if args[3] == 'least':
                                narrate(lang['narrator_set_goal_lowest'].format(player=names[int(args[1]) - 1]))
                            elif args[3] == 'most':
                                narrate(lang['narrator_set_goal_highest'].format(player=names[int(args[1]) - 1]))
                            else:
                                narrate(lang['narrator_set_goal_player'].format(player=names[int(args[1]) - 1], target=names[int(args[3]) - 1]))
                        log_cursor = max(0, len(log) - 10)
                else:
                    print(lang['err_incomplete_command'].format(command=command))
            elif args[0] == 'victory':
                if len(args) > 2:
                    victories[int(args[1]) - 1] = int(args[2])
                    log.append(f'{args[1]}V={args[2]}')
                    log_cursor = max(0, len(log) - 10)
                    narrate(lang['narrator_set_victory'].format(player=names[int(args[1]) - 1], value=args[2]))
                else:
                    print(lang['err_incomplete_command'].format(command=command))
            command = ''
            self.command_line.text = ''
            is_updating = False
            return
        
ui_menu = menu()
ui_settings = settings()
ui_game = game()

while True:
    bkp_pos0 = pygame.mouse.get_pos()
    bkp_pos = (int(bkp_pos0[0] / scale), int(bkp_pos0[1] / scale))
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
        global_config.save()
        pygame.quit()
        exit(0)
    changing_score = False
    for i in game_events.tick():
        if i['name'] == 'increase_player': # arg1 is the player, arg2 is the score
            visible_scores[i['arg1']] += i['arg2']
            changing_score = True
        if i['name'] == 'blink' and blink_time > 0: # arg1 is the player, arg2 is the color
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
                        game_events.add_event(True, 'blink', max_fps*blink_time - max_fps//2 + 1, k, 2)
                        log.append(f'{k+1}W@{scores[k]}')
                        log_cursor = max(0, len(log) - 10)
                    else:
                        game_events.add_event(True, 'blink', max_fps*blink_time - max_fps//2 + 1, k, 1)
                        log.append(f'{k+1}F@{scores[k]}')
                        log_cursor = max(0, len(log) - 10)
                game_events.add_event(False, 'clear_score', max_fps*blink_time - max_fps//2 - 1)
                win_names = []
                for m in winners:
                    victories[m] += 1
                    win_names.append(names[m])
                if len(winners) > 1:
                    win_final_names = ''
                    for m in range(len(winners) - 1):
                        win_final_names += f'{win_names[m]}, '
                    win_final_names += f' and {win_names[-1]}'
                    narrate(lang['narrator_victory_multiple'].format(players=win_final_names, score=j))
                else:
                    win_final_names = win_names[0]
                    narrate(lang['narrator_victory_single'].format(player=win_final_names, score=j))
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
    transformed = pygame.transform.smoothscale(window, (int(1280*scale), int(720*scale)))
    final_window.blit(transformed, (0, 0))
    pygame.display.update()
    gametick.tick(max_fps)
