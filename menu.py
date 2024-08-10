import pygame
from config import *
import config
from utils.radiobutton import RadioButton

pygame.init()

menu_over = pygame.mixer.Sound('audio/menu_select.mp3')

def load_image(path, scale=1):
    image = pygame.image.load(path).convert_alpha()
    w, h = image.get_width() * scale, image.get_height() * scale
    return pygame.transform.scale(image, (w, h))


class Button:
    def __init__(self, text, x, y, width, height, borderColor=BUTTON_BORDER_COLOR):
        self.name = text
        self.text = font.render(text, True, BUTTON_TEXT_COLOR, BUTTON_BG_COLOR)
        self.borderColor = borderColor
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
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if not self.mouse_over:
                menu_over.play()
            self.mouse_over = True
        else:
            self.mouse_over = False            

        if pygame.mouse.get_pressed()[0] == 1:
            if self.mouse_over:
                self.clicked = True
                return True
        self.clicked = False
        return False
    
    def draw(self, screen):
        if self.mouse_over:
            pygame.draw.rect(screen, self.borderColor, self.rect_border)
        pygame.draw.rect(screen, BUTTON_BG_COLOR, self.rect)
        screen.blit(self.text, (self.text_x, self.text_y))



class Menu:
    def __init__(self, screen_width, screen_height, topmargin=0, margin=100, borderColor=BUTTON_BORDER_COLOR):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.topmargin = topmargin
        self.margin = margin
        self.borderColor = borderColor
        self.buttons = []
        self._sum_heights = 0

        self.counter = 0
        self.delay = 10
    
    def add_button(self, text, width, height, x=None):
        if x is None:
            x = (SCREEN_WIDTH - width) >> 1
        y = self.topmargin + len(self.buttons) * self.margin + self._sum_heights
        button = Button(text, x, y, width, height, self.borderColor)
        self.buttons.append(button)
        self._sum_heights += height

    def update(self):
        self.counter += 1
        return {
            button.name: button.update()
            for button in self.buttons
        }
    
    def draw(self, screen, fillBackground=True):
        if fillBackground:
            screen.fill(MENU_BG_COLOR)
        for button in self.buttons:
            button.draw(screen)

class DifficultyMenu(Menu):
    def __init__(self, screen_width, screen_height, x=None, topmargin=100, margin=100):
        super().__init__(screen_width, screen_height, topmargin, margin, BLUE)
        self.add_button('easy', BUTTON_WIDTH, BUTTON_HEIGHT, x=x)
        self.add_button('normal', BUTTON_WIDTH, BUTTON_HEIGHT, x=x)
        self.add_button('hard', BUTTON_WIDTH, BUTTON_HEIGHT, x=x)
        self.add_button('ultimate', BUTTON_WIDTH, BUTTON_HEIGHT, x=x)
        if config.level == 'easy':
            self.selected = 0
        elif config.level == 'normal':
            self.selected = 1
        elif config.level == 'hard':
            self.selected = 2
        elif config.level == 'ultimate':
            self.selected = 3
        

    def update(self):
        results = super().update()
        if self.counter < self.delay: return
        self.counter = 0
        if results['easy']:
            config.level = 'easy'
            self.selected = 0
        elif results['normal']:
            config.level = 'normal'
            self.selected = 1
        elif results['hard']:
            config.level = 'hard'
            self.selected = 2
        elif results['ultimate']:
            config.level = 'ultimate'
            self.selected = 3

    def draw(self, screen, fillBackground=True):
        self.buttons[self.selected].mouse_over = True
        super().draw(screen, fillBackground)

class CommonSettingsMenu(Menu):
    def __init__(self, screen_width, screen_height):
        super().__init__(screen_width, screen_height, 250, 50)
        self.add_button('difficulty', BUTTON_WIDTH, BUTTON_HEIGHT)
        self.add_button('back', BUTTON_WIDTH, BUTTON_HEIGHT)
        self.soundRB = RadioButton(
            self.buttons[0].rect.x,
            50,
            margin=40,
            options=['play sound', 'Use Ai'],
        )
        for b in self.soundRB.buttons:
            b.active = True

        self.difficultyMenu = DifficultyMenu(
            screen_width,
            screen_height,
            self.buttons[0].rect.right + 30,
            topmargin=100,
            margin=20
        )
        self.visible = False        

    def draw(self, screen):
        super().draw(screen)
        self.soundRB.draw(screen)
        if self.visible:
            self.difficultyMenu.draw(screen, False)


    def update(self):
        if self.visible:
            self.difficultyMenu.update()
        radioResults = self.soundRB.update()
        config.PLAY_SOUND = radioResults['play sound']
        config.USE_AI = radioResults['Use Ai']
        results = super().update()
        if self.counter < self.delay: return
        self.counter = 0
        if results['difficulty']:
            self.visible = not self.visible
        elif results['back']:
            config.menu = config.mainMenu
            self.visible = False


class MainMenu(Menu):
    def __init__(self, screen_width, screen_height, topmargin=100, margin=100):
        super().__init__(screen_width, screen_height, topmargin, margin)
        self.add_button('start', BUTTON_WIDTH, BUTTON_HEIGHT)
        self.add_button('new game', BUTTON_WIDTH, BUTTON_HEIGHT)
        self.add_button('settings', BUTTON_WIDTH, BUTTON_HEIGHT)
        self.add_button('exit', BUTTON_WIDTH, BUTTON_HEIGHT)


    def update(self):
        results = super().update()
        if self.counter < self.delay: return
        self.counter = 0
        if results['start']:
            config.pause = False
        elif results['new game']:
            config.new_game = True
            config.pause = False
        elif results['settings']:
            config.menu = config.settingsMenu
        elif results['exit']:
            config.game_over = True


