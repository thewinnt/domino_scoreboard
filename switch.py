import pygame
class Switch:
    def __init__(self, x, y, surface, default_color=(0, 204, 204), hover_color=(0, 255, 255), outline_color=(0, 0, 0), enable_color=(47, 194, 0), disable_color=(207, 0, 0)):
        '''A switch that acts like a button, based on the button class'''
        self.x = x
        self.y = y
        self.width = 86
        self.height = 36
        self.surface = surface

        self.theme = [None] * 16
        self.outline_color = outline_color
        self.hover_color = hover_color
        self.default_color = default_color
        self.enable_color = enable_color
        self.disable_color = disable_color

        self.was_pressed = False

    def draw(self, active, bkp_pos=None, is_over=False):
        '''Simply draw the switch'''
        if bkp_pos == None:
            self.pos = pygame.mouse.get_pos()
        else:
            self.pos = bkp_pos
        if is_over:
            pygame.draw.rect(self.surface, self.hover_color, (self.x, self.y, self.width, self.height), 0, int(self.height / 2))
        else:
            pygame.draw.rect(self.surface, self.default_color, (self.x, self.y, self.width, self.height), 0, int(self.height / 2))
        pygame.draw.rect(self.surface, self.outline_color, (self.x-2, self.y-2, self.width+4, self.height+4), 4, int(self.height / 2))
        if active:
            pygame.draw.circle(self.surface, self.enable_color, (self.x + 70, self.y + 18), 18)
            pygame.draw.circle(self.surface, self.outline_color, (self.x + 70, self.y + 18), 18, 4)
        else:
            pygame.draw.circle(self.surface, self.disable_color, (self.x + 16, self.y + 18), 18)
            pygame.draw.circle(self.surface, self.outline_color, (self.x + 16, self.y + 18), 18, 4)

    def is_over(self, bkp_pos=None) -> bool:
        '''Returns true if mouse is over'''
        if bkp_pos == None:
            self.pos = pygame.mouse.get_pos()
        else:
            self.pos = bkp_pos
        if self.pos[0] > self.x and self.pos[0] < self.x + self.width and self.pos[1] > self.y and self.pos[1] < self.y + self.height:
            return True
        else:
            return False

    def smart_draw(self, active, bkp_pos=None) -> bool:
        '''Draws the switch and returns if it's been clicked at recently'''
        self.draw(active, bkp_pos, self.is_over(bkp_pos))
        if not self.was_pressed and pygame.mouse.get_pressed()[0]:
            self.was_pressed = True
            is_clicked = True
        elif self.was_pressed and pygame.mouse.get_pressed()[0]:
            self.was_pressed = True
            is_clicked = False
        else:
            self.was_pressed = False
            is_clicked = False
        return self.is_over(bkp_pos) and is_clicked