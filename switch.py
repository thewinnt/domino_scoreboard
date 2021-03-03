import pygame
class switch(): # a switch that acts like a button, based on the button class
    def __init__(self, x, y, surface, default_color=(0, 204, 204), hover_color=(0, 255, 255), outline_color=(0, 0, 0), enable_color=(47, 194, 0), disable_color=(207, 0, 0)):
        self.x = x
        self.y = y
        self.width = 86
        self.height = 36
        self.surface = surface

        self.theme = [None] * 16
        self.theme[0] = outline_color
        self.theme[8] = hover_color
        self.theme[10] = default_color
        self.theme[14] = enable_color
        self.theme[15] = disable_color

    def draw(self, active, bkp_pos=None):
        #Call this method to draw the button on the screen
        if bkp_pos == None:
            self.pos = pygame.mouse.get_pos()
        else:
            self.pos = bkp_pos
        if self.pos[0] > self.x and self.pos[0] < self.x + self.width and self.pos[1] > self.y and self.pos[1] < self.y + self.height:
            pygame.draw.rect(self.surface, self.theme[8], (self.x, self.y, self.width, self.height), 0, int(self.height / 2))
        else:
            pygame.draw.rect(self.surface, self.theme[10], (self.x, self.y, self.width, self.height), 0, int(self.height / 2))
        pygame.draw.rect(self.surface, self.theme[0], (self.x-2, self.y-2, self.width+4, self.height+4), 4, int(self.height / 2))
        if active:
            pygame.draw.circle(self.surface, self.theme[14], (self.x + 70, self.y + 18), 18)
            pygame.draw.circle(self.surface, self.theme[0], (self.x + 70, self.y + 18), 18, 4)
        else:
            pygame.draw.circle(self.surface, self.theme[15], (self.x + 16, self.y + 18), 18)
            pygame.draw.circle(self.surface, self.theme[0], (self.x + 16, self.y + 18), 18, 4)

    def is_over(self, bkp_pos = None):
        # returns true if mouse is over
        if bkp_pos == None:
            self.pos = pygame.mouse.get_pos()
        else:
            self.pos = bkp_pos
        if self.pos[0] > self.x and self.pos[0] < self.x + self.width and self.pos[1] > self.y and self.pos[1] < self.y + self.height:
            return True
        else:
            return False

    def smart_draw(self, active, bkp_pos = None) -> bool:
        '''Draws the switch and returns its click state'''
        self.draw(active, bkp_pos)
        return self.is_over(bkp_pos) and pygame.mouse.get_pressed()[0]
