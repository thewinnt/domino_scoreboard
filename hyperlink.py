from abc import abstractmethod
import pygame
class hyperlink:
    def __init__(self, color, x, y, text):
        '''Not really a link, just a button that looks like one'''
        self.color = color
        self.x = x
        self.y = y
        self.text = text

    def _draw(self,surface,font_size=60):
        font = pygame.font.Font('assets/denhome.otf', font_size)
        self.rendered_text = font.render(self.text, 1, self.color)
        surface.blit(self.rendered_text, (self.x, self.y))

    def _is_over(self, bkp_pos=None) -> bool:
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if bkp_pos == None:
            self.pos = pygame.mouse.get_pos()
        else:
            self.pos = bkp_pos
        if self.pos[0] > self.x and self.pos[0] < self.x + self.rendered_text.get_width() and self.pos[1] > self.y and self.pos[1] < self.y + self.rendered_text.get_height():
            return True
        else:
            return False

    def smart_draw(self, surface, font_size = 60, bkp_pos = None) -> bool:
        '''Draws the link and returns its click state'''
        self._draw(surface, font_size)
        return self._is_over(bkp_pos) and pygame.mouse.get_pressed()[0]