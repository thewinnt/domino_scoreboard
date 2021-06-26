import pygame

# default colors
COLOR_ORIGIN = (240, 240, 240)
COLOR_BASE = (230, 230, 230)
COLOR_TEXT = (0, 0, 0)
COLOR_OUTLINE = (0, 0, 0)
COLOR_SCROLLER = (40, 40, 40)
COLOR_HOVER_ORIGIN = (255, 255, 255)
COLOR_HOVER_BASE = (240, 240, 240)
COLOR_HOVER_SCROLLER = (80, 80, 80)

class DropdownList:
    def __init__(self, options, chosen, pos, font, surface, min_width=150, require_hover=False, max_len=6, color_base=COLOR_BASE, color_origin=COLOR_ORIGIN, color_text=COLOR_TEXT, color_outline=COLOR_OUTLINE, color_scroll=COLOR_SCROLLER, color_hover_base=COLOR_HOVER_BASE, color_hover_origin=COLOR_HOVER_ORIGIN, color_hover_scroll=COLOR_HOVER_SCROLLER):
        self.x = pos[0] # this is the right side
        self.y = pos[1]
        self.max_len = max_len
        self.font = font
        self.surface = surface

        self.color_base = color_base
        self.color_origin = color_origin
        self.color_text = color_text
        self.color_outline = color_outline
        self.color_scroller = color_scroll
        self.color_hover_base = color_hover_base
        self.color_hover_origin = color_hover_origin
        self.color_hover_scroll = color_hover_scroll

        self.options = options
        self.open = False
        self.chosen_option_index = chosen # aka origin
        self.scroll_offset = 0 # 0 <= scroll_offset <= len(options) - max_len
        self.require_hover = require_hover # whether the list will be closed when mouse cursor isn't at it

        self.min_width = min_width

        self.was_pressed = False
        self.scrolling = False
        self.start_y = None
        self.start_offset = None

        self.cache()

    def cache(self):
        '''Prepares the sizes of the list - must be run every time the options change! (unless you redefine the list)'''
        self.height = int(self.font.size('*Ёy,gj')[1] * 1.1) # this should do the trick
        option_sizes = []
        for i in self.options:
            option_sizes.append(self.font.size(i)[0] + int(self.height))
        self.width = max(max(option_sizes), self.min_width)
        self.hitbox_closed = [(self.x - self.width, self.y), (self.x, self.y + self.height)] # the corners of the list when it's closed
        self.hitbox_open = [(self.x - self.width, self.y), (self.x, self.y + self.height * (min(len(self.options), self.max_len) + 1))]
        self.hitbox_options = [] # format: self.hitbox_options[option][corner: top left or bottom right][coordinate: x or y]
        for i in range(min(len(self.options), self.max_len)):
            self.hitbox_options.append([(self.x - self.width, self.y + self.height * (i+1)), (self.x, self.y + self.height * (i+2))])
        self.ren_chosen = self.font.render(self.options[self.chosen_option_index], 1, self.color_text)
        self.ren_opt = []
        for i in self.options:
            self.ren_opt.append(self.font.render(i, 1, self.color_text))

    def update(self, bkp_pos=None) -> int:
        '''Draws the list, updates it and returns the last clicked value'''
        hbo = self.hitbox_options # this is much shorter

        ## gather events
        if bkp_pos:
            pos = bkp_pos
        else:
            pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] and not self.was_pressed:
            self.was_pressed = True
            if self.open:
                if hbo[0][1][0] - self.height*0.2 < pos[0] < hbo[0][1][0] and self.y+self.height+self.scroll_pos < pos[1] < self.y+self.height+self.scroll_pos+self.scroll_len:
                    self.scrolling = True
                    self.start_y = pos[1]
                    self.start_offset = self.scroll_offset
                elif not (hbo[0][1][0] - self.height*0.2 < pos[0] < hbo[0][1][0] and hbo[0][0][1] < pos[1] < self.hitbox_open[1][1]):
                    self.open = False
                    for i in range(len(hbo)):
                        if hbo[i][0][0] < pos[0] < hbo[i][1][0] - self.height*0.2 and hbo[i][0][1] < pos[1] < hbo[i][1][1]:
                            return i + self.scroll_offset
            elif not self.open and self.x - self.width < pos[0] < self.x and self.y < pos[1] < self.y + self.height:
                self.open = True
        elif pygame.mouse.get_pressed()[0] and self.was_pressed: 
            self.was_pressed = True
        else:
            self.was_pressed = False
        if self.open and self.require_hover and not self.scrolling:
            if not (self.hitbox_open[0][0] < pos[0] < self.hitbox_open[1][0] and self.hitbox_open[0][1] < pos[1] < self.hitbox_open[1][1]):
                self.open = False
        if len(self.options) > self.max_len:
            event = pygame.event.get(pygame.MOUSEWHEEL)
            if event:
                self.scroll_offset -= event[0].y
                if self.scroll_offset < 0:
                    self.scroll_offset = 0
                elif self.scroll_offset > len(self.options) - self.max_len:
                    self.scroll_offset = len(self.options) - self.max_len

        ## calculate scroll bar position
        if len(self.options) > self.max_len:
            self.scroll_len = max(self.height, min(self.height * len(self.options) / (len(self.options) - self.max_len), self.height * (self.max_len - 1)))
            self.scroll_step = (self.height * self.max_len - self.scroll_len) / (len(self.options) - self.max_len) 
            self.scroll_pos = self.scroll_step * self.scroll_offset

            ## proces scrolling
            if self.scrolling:
                if not pygame.mouse.get_pressed()[0]:
                    self.scrolling = False
                else:
                    self.scroll_offset = self.start_offset + int((pos[1] - self.start_y) // self.scroll_step)
                    if self.scroll_offset < 0:
                        self.scroll_offset = 0
                    elif self.scroll_offset > len(self.options) - self.max_len:
                        self.scroll_offset = len(self.options) - self.max_len
            if (hbo[0][1][0] - self.height*0.2 < pos[0] < hbo[0][1][0] and self.y+self.height+self.scroll_pos < pos[1] < self.y+self.height+self.scroll_pos+self.scroll_len) or self.scrolling:
                is_scroller_hovered = True
            else:
                is_scroller_hovered = False
        
        ## draw origin
        if self.hitbox_closed[0][0] < pos[0] < self.hitbox_closed[1][0] and self.hitbox_closed[0][1] < pos[1] < self.hitbox_closed[1][1]:
            pygame.draw.rect(self.surface, self.color_hover_origin, (self.x - self.width, self.y, self.width, self.height))
        else:
            pygame.draw.rect(self.surface, self.color_origin, (self.x - self.width, self.y, self.width, self.height))

        pygame.draw.polygon(self.surface, self.color_outline, ([self.x - self.height * 0.3, self.y + self.height * 0.3],
                                                               [self.x - self.height * 0.7, self.y + self.height * 0.3],
                                                               [self.x - self.height * 0.5, self.y + self.height * 0.7]))
        self.surface.blit(self.ren_chosen, (self.x - self.width + self.height * 0.15, self.y))
        pygame.draw.rect(self.surface, self.color_outline, (self.x - self.width, self.y, self.width, self.height), 2)

        ## draw base
        if self.open:
            for i in range(min(len(self.options), self.max_len)):
                if hbo[i][0][0] < pos[0] < hbo[i][1][0] - self.height * 0.2 and hbo[i][0][1] < pos[1] < hbo[i][1][1]:
                    pygame.draw.rect(self.surface, self.color_hover_base, (hbo[i][0][0], 
                                                                           hbo[i][0][1], 
                                                                           hbo[i][1][0] - hbo[i][0][0], 
                                                                           hbo[i][1][1] - hbo[i][0][1])) # the line is too long
                else:
                    pygame.draw.rect(self.surface, self.color_base, (hbo[i][0][0], 
                                                                     hbo[i][0][1], 
                                                                     hbo[i][1][0] - hbo[i][0][0], 
                                                                     hbo[i][1][1] - hbo[i][0][1]))
                self.surface.blit(self.ren_opt[i + self.scroll_offset], (hbo[i][0][0] + self.height * 0.1, hbo[i][0][1]))
            pygame.draw.rect(self.surface, self.color_outline, (self.hitbox_open[0][0],
                                                                self.hitbox_open[0][1],
                                                                self.hitbox_open[1][0] - self.hitbox_open[0][0],
                                                                self.hitbox_open[1][1] - self.hitbox_open[0][1]), 2)
            if len(self.options) > self.max_len:
                if is_scroller_hovered:
                    pygame.draw.rect(self.surface, self.color_hover_scroll, (self.x - self.height * 0.2,
                                                                             self.y + self.scroll_pos + self.height,
                                                                             self.height * 0.2,
                                                                             self.scroll_len))
                else:
                    pygame.draw.rect(self.surface, self.color_scroller, (self.x - self.height * 0.2,
                                                                         self.y + self.scroll_pos + self.height,
                                                                         self.height * 0.2,
                                                                         self.scroll_len))