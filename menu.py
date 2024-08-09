import pygame
from config import *
import config

def load_image(path, scale=1):
    image = pygame.image.load(path).convert_alpha()
    w, h = image.get_width() * scale, image.get_height() * scale
    return pygame.transform.scale(image, (w, h))


class Button:
    def __init__(self, text, x, y, width, height):
        self.name = text
        self.text = font.render(text, True, BUTTON_TEXT_COLOR, BUTTON_BG_COLOR)
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.rect_border = pygame.rect.Rect(
            x - BUTTON_BORDER,
            y - BUTTON_BORDER,
            width + 2 * BUTTON_BORDER,
            height + 2 * BUTTON_BORDER
        )
        self.text_x = self.rect.centerx - self.text.get_width() // 2
        self.text_y = self.rect.centery - self.text.get_height() // 2
        self.mouse_over = False
        self.clicked = False

    def update(self):
        self.mouse_over = False
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.mouse_over = True
        
        if pygame.mouse.get_pressed()[0] == 1:
            if self.mouse_over:
                self.clicked = True
                return True
        self.clicked = False
        return False
    
    def draw(self, screen):
        if self.mouse_over:
            pygame.draw.rect(screen, BUTTON_BORDER_COLOR, self.rect_border)
        pygame.draw.rect(screen, BUTTON_BG_COLOR, self.rect)
        screen.blit(self.text, (self.text_x, self.text_y))



class Menu:
    def __init__(self, screen_width, screen_height, topmargin=0, margin=100):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.topmargin = topmargin
        self.margin = margin
        self.buttons = []
        self._sum_heights = 0
    
    def add_button(self, text, width, height):
        x = (SCREEN_WIDTH - width) >> 1
        y = self.topmargin + len(self.buttons) * self.margin + self._sum_heights
        button = Button(text, x, y, width, height)
        self.buttons.append(button)
        self._sum_heights += height

    def update(self):
        return {
            button.name: button.update()
            for button in self.buttons
        }
    
    def draw(self, screen):
        screen.fill(MENU_BG_COLOR)
        for button in self.buttons:
            button.draw(screen)



class MainMenu(Menu):
    def __init__(self, screen_width, screen_height, topmargin=100, margin=100):
        super().__init__(screen_width, screen_height, topmargin, margin)
        self.add_button('start', BUTTON_WIDTH, BUTTON_HEIGHT)
        self.add_button('new game', BUTTON_WIDTH, BUTTON_HEIGHT)
        self.add_button('settings', BUTTON_WIDTH, BUTTON_HEIGHT)
        self.add_button('exit', BUTTON_WIDTH, BUTTON_HEIGHT)


    def update(self):
        results = super().update()
        if results['start']:
            config.pause = False
        elif results['new game']:
            config.new_game = True
            config.pause = False
        elif results['settings']:
            pass
        elif results['exit']:
            config.game_over = True


