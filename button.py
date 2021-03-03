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
