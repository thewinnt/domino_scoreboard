import pygame
class hyperlink:
    def __init__(self, color, x, y, text):
        '''Not really a link, just a button that looks like one'''
        self.color = color
        self.x = x
        self.y = y
        self.text = text
        self.was_pressed = False

    def draw(self,surface,font_size=60):
        '''Simply draws the link'''
        font = pygame.font.Font('assets/denhome.otf', font_size)
        self.rendered_text = font.render(self.text, 1, self.color)
        surface.blit(self.rendered_text, (self.x, self.y))

    def is_over(self, bkp_pos=None) -> bool:
        '''Returns true, if the cursor is pointing at the link'''
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
        self.draw(surface, font_size)
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