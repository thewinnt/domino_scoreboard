import pygame
class text_field:
    def __init__(self, x, y, width, height, text, font, surface, type_='string', outline_color_active=(0, 0, 0), outline_color_inactive=(50, 50, 50), field_color=(240, 240, 240)):
        '''A text field class that can automatically draw and update itself'''
        self.width = width
        self.height = height

        self.x = x
        self.y = y

        self.text = str(text)
        self.font = font

        self.outline_color_active = outline_color_active
        self.outline_color_inactive = outline_color_inactive
        self.field_color = field_color

        self.surface = surface
        self.active = False
        
        self.number_chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-']
        self.float_chars = self.number_chars + ['.']

        self.type = type_

        self.was_clicked = False

    def _is_over(self, bkp_pos = None) -> bool:
        # returns true if mouse is over
        if bkp_pos == None:
            self.pos = pygame.mouse.get_pos()
        else:
            self.pos = bkp_pos
        if self.pos[0] > self.x and self.pos[0] < self.x + self.width and self.pos[1] > self.y and self.pos[1] < self.y + self.height:
            return True
        else:
            return False

    def _update(self) -> str:
        '''Update the contents of the box and return the new value'''
        self.was_clicked = pygame.mouse.get_pressed()[0]
        if self.type == 'int':
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.was_clicked = True
                        break
                    if event.key == pygame.K_BACKSPACE:
                        try:
                            self.text = str(self.text)[:-1]
                        except:
                            pass
                    try:
                        lol = int(event.unicode + '1')
                    except ValueError:
                        lol = 5
                    else:
                        self.text = str(self.text) + event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.was_clicked = True
        elif self.type == 'float':
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.was_clicked = True
                        break
                    if event.key == pygame.K_BACKSPACE:
                        try:
                            self.text = str(self.text)[:-1]
                        except:
                            pass
                    try:
                        lol = float('1' + event.unicode)
                    except ValueError:
                        lol = 5
                    else:
                        self.text = str(self.text) + event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.was_clicked = True
        else:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.was_clicked = True
                        break
                    if event.key == pygame.K_BACKSPACE:
                        try:
                            self.text = str(self.text)[:-1]
                        except:
                            pass
                    else:
                        self.text += event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.was_clicked = True

    def draw(self, update=True, text_color=(0, 0, 0)) -> str:
        '''Usage: 'temp = field_name.draw(...); if not temp is False: target = temp' where target is the string you want to get as user input'''
        self.was_clicked = pygame.mouse.get_pressed()[0]
        if self.active and update:
            outline_color = self.outline_color_active
            outline_width = 4
            self._update()
        else:
            outline_color = self.outline_color_inactive
            outline_width = 2

        pygame.draw.rect(self.surface, self.field_color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(self.surface, outline_color, (self.x, self.y, self.width, self.height), outline_width)

        text = self.font.render(str(self.text), 4, outline_color)
        self.surface.blit(text, (self.x + 5, self.y))

        if update and self.was_clicked:
            self.was_clicked = False
            temp = self.active
            self.active = self._is_over()
            if temp == self.active or self.active:
                return False
            if not self.active:
                if self.type == 'string':
                    return self.text
                elif self.type == 'float':
                    return float(self.text)
                elif self.type == 'int':
                    return int(self.text)
                else:
                    raise SyntaxError(f"Invalid type of value to return: {self.type}, it must be either 'int', 'float' or 'string' (default)")
        else:
            return False
