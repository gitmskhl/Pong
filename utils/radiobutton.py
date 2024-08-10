import pygame

pygame.init()

default_rbutton_setup = {
    'font': pygame.font.SysFont('Futura', 30),
    'square_width': 20,
    'square_height': 20,
    'line_width': 3,
    'border_width': 3
}

class RButton:
    def __init__(
            self,
            x,
            y,
            square_width,
            square_height,
            text,
            font,
            color=(255, 255, 255),
            text_color=(255, 255, 255),
            text_bg_color=(0, 0, 0),
            line_width=2,
            line_color=(0, 0, 0),
            border_width=2,
            border_color=(0, 0, 200)
    ):
        self.color = color
        self.line_color = line_color
        self.rect = pygame.rect.Rect(x, y, square_width, square_height)
        self.rect_border = pygame.rect.Rect(x - border_width, y - border_width, square_width + 2 * border_width, square_height + 2 * border_width)
        self.border_color = border_color
        self.text = font.render(text, True, text_color, text_bg_color)
        self.line1 = (x, y, x + square_width, y + square_height)
        self.line2 = (x, y + square_height, x + square_width, y)
        self.line_width = line_width
        self.mouse_over = False
        self.active = False

        self.counter = 0
        self.delay = 10

    def update(self):
        get_pressed = pygame.mouse.get_pressed()[0]
        self.mouse_over = False
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.mouse_over = True
            
        if self.mouse_over and get_pressed:
            self.counter += 1
            if self.counter > self.delay:
                self.active = not self.active
                self.counter = 0
            
        return self.active


    def draw(self, screen):
        if self.mouse_over:
            pygame.draw.rect(screen, self.border_color, self.rect_border)
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text, (self.rect_border.right + 10, self.rect_border.centery -  self.text.get_height() // 2))
        if self.active:
            pygame.draw.line(screen, self.line_color, self.line1[:2], self.line1[2:], self.line_width)
            pygame.draw.line(screen, self.line_color, self.line2[:2], self.line2[2:], self.line_width)


class RadioButton:
    def __init__(self, x_start, y_start, margin=30, options=[], setup=default_rbutton_setup):
        self.x = x_start
        self.y = y_start
        self.setup = setup
        self.buttons = []
        self.margin = margin
        self.names = []
        for option_name in options:
            self.add_button(option_name)
        

    def add_button(self, option_name):
        self.names.append(option_name)
        bheight = self.setup['square_height']
        rbutton = RButton(self.x, self.y, text=option_name, **self.setup)
        self.buttons.append(rbutton)
        self.y += bheight + self.margin

    def update(self):
        results = {
            name: button.update()
            for name, button in zip(self.names, self.buttons)
        }
        return results

    def draw(self, screen):
        for button in self.buttons:
            button.draw(screen)