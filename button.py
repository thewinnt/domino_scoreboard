import pygame
class button():
    def __init__(self, color,x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,outline=None,font_color=(0, 0, 0),font_size=60):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)

        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)

        if self.text != '':
            font = pygame.font.Font('assets/denhome.otf', font_size)
            text = font.render(self.text, 1, font_color)
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, bkp_pos=None):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if bkp_pos == None:
            self.pos = pygame.mouse.get_pos()
        else:
            self.pos = bkp_pos
        if self.pos[0] > self.x and self.pos[0] < self.x + self.width and self.pos[1] > self.y and self.pos[1] < self.y + self.height:
            return True
        else:
            return False

    def smart_draw(self, surface, font_size = 60, bkp_pos = None, default_color=(0, 204, 204), hover_color=(0, 255, 255), click_color=(0, 102, 102), text_color=(0, 0, 0), outline_color=(0, 0, 0)) -> bool:
        '''Draws the button and returns its click state'''
        to_return = False
        if self.isOver(bkp_pos):
            self.color = hover_color
            if pygame.mouse.get_pressed()[0]:
                self.color = click_color
                pygame.event.clear()
                to_return = True
        if not self.isOver(bkp_pos) and not pygame.mouse.get_pressed()[0]:
            self.color = default_color
        self.draw(surface, outline_color, text_color, font_size)
        return to_return
