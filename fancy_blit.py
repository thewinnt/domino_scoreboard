import pygame

COLOR_INDEX = {'0': (0, 0, 0),
               '1': (0, 0, 170),
               '2': (0, 170, 0),
               '3': (0, 170, 170),
               '4': (170, 0, 0),
               '5': (170, 0, 170),
               '6': (255, 170, 0),
               '7': (170, 170, 170),
               '8': (85, 85, 85),
               '9': (85, 85, 255),
               'a': (85, 255, 85),
               'b': (85, 255, 255),
               'c': (255, 85, 85),
               'd': (255, 85, 255),
               'e': (255, 255, 85),
               'f': (255, 255, 255)} # these are from minecraft

def fancy_blit(text, font, pos, surface, default_color=(0, 0, 0), background_color=(240, 240, 240)) -> str:
    '''Draws the text and returns it in a normal way (without technical symbols)'''
    divided_text = text.split('§')
    rendered_parts = []
    counter = 0
    for i in divided_text:
        try:
            if i == '' and not len(text):
                continue
            if not i[0] in '0123456789abcdefr' or (text[0] != '§' and not counter):
                raise SyntaxError(f'invalid format code: §{i[0]}')
            if i[0] == 'r':
                rendered_parts.append(font.render(i[1:], 4, default_color, background_color))
            else:
                rendered_parts.append(font.render(i[1:], 4, COLOR_INDEX[i[0]], background_color))
        except:
            if counter:
                rendered_parts.append(font.render('§' + i, 4, default_color, background_color))
            else:
                rendered_parts.append(font.render(i, 4, default_color, background_color))
        counter += 1
    offset = 0
    for i in rendered_parts:
        surface.blit(i, (pos[0] + offset, pos[1]))
        offset += i.get_width()
    normal_text = '' # returning normal text is not tested
    if text:
        counter = 0
        for i in divided_text:
            if counter or text[0] == '§':
                normal_text += i[1:]
            else:
                normal_text += i
        return normal_text
    else:
        return ''