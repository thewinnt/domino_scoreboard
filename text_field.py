import pygame
class text_field:
    def __init__(self, width, height, text, font, surface, type='string', outline_color_active=(0, 0, 0), outline_color_inactive=(50, 50, 50), field_color=(240, 240, 240)):
        '''A text field class that can automatically draw and update itself'''
        self.width = width
        self.height = height

        self.text = text
        self.font = font

        self.outline_color_active = outline_color_active
        self.outline_color_inactive = outline_color_inactive
        self.field_color = field_color

        self.surface = surface
        self.active = False

    def _update(self) -> str:
        '''Update the contents of the box and return the new value'''
        pass  #to be done

    def draw(self, x, y, update=True, text_color=(0, 0, 0)) -> str:
        '''Usage: 'desired_string = field_name.draw(...)' where desired_string is the string you want to get as user input'''
        if self.active:
            outline_color = self.outline_color_active
            self._update()
        else:
            outline_color = self.outline_color_inactive

        pygame.draw.rect(self.surface, (x, y, self.width, self.height), self.field_color)
        pygame.draw.rect(self.surface, (x, y, self.width, self.height), outline_color)

        text = self.font.render(self.text, 1, outline_color)
        self.surface.blit(text, (x + 2, y))