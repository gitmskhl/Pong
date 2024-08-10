import pygame
from config import *
import config
from menu import *
from math import sin, cos, pi
from random import randint


pygame.init()


class Board:
    def __init__(self, width, height, speed, isLeft=True, ai=False, level='easy', color=(255, 255, 255)):
        self.width = width
        self.height = height
        self.speed = speed
        self.isLeft = isLeft
        self.ai = ai
        self.level = level
        self.color = color
        left = 0 if isLeft else SCREEN_WIDTH - width
        top = (SCREEN_HEIGHT - height) >> 1 
        self.rect = pygame.rect.Rect(
            left,
            top,
            width,
            height
        )
        self.inner_rect = pygame.rect.Rect(
            left,
            top + height // 4,
            width,
            height // 2
        )
        self.moveDown = False
        self.moveUp = False


    def update(self, ball):
        if self.ai:
            ball_data = ball.rect.x, ball.rect.y, ball.speedx, ball.speedy
            if self.level == 'easy': self.ai_easy(*ball_data)
            elif self.level == 'normal': self.ai_normal(*ball_data)
            elif self.level == 'hard': self.ai_hard(*ball_data)
            elif self.level == 'ultimate': self.ai_ultimate(*ball_data)
        if self.moveDown:
            self.rect.y += self.speed
        if self.moveUp:
            self.rect.y -= self.speed
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        
    def _move_to(self, y_dest=SCREEN_HEIGHT >> 1):
        self.inner_rect.center = self.rect.center
        x = self.inner_rect.centerx
        if self.inner_rect.collidepoint(x, y_dest):
            self.moveDown = self.moveUp = False
            return
        if self.inner_rect.y < y_dest:
            self.moveDown = True
            self.moveUp = False
        else:
            self.moveUp = True
            self.moveDown = False


    def ai_easy(self, ballx, bally, ballvelx, ballvely):
        x = self.rect.centerx
        t = (x - ballx) / ballvelx
        y = bally + ballvely * t
        self._move_to(y)

    def ai_normal(self, ballx, bally, ballvelx, ballvely):
        if self.isLeft:
            if ballvelx < 0: self.ai_easy(ballx, bally, ballvelx, ballvely)
            else: self._move_to()
        else:
            if ballvelx > 0: self.ai_easy(ballx, bally, ballvelx, ballvely)
            else: self._move_to()

    def ai_bithard(self, ballx, bally, ballvelx, ballvely):
        x = self.rect.centerx
        t = (x - ballx) / ballvelx
        y_predicted = bally + ballvely * t
        if y_predicted < 0: self._move_to(-y_predicted)
        elif y_predicted > SCREEN_HEIGHT: self._move_to(2 * SCREEN_HEIGHT - y_predicted)
        else: self._move_to(y_predicted)

    def ai_hard(self, ballx, bally, ballvelx, ballvely):
        if self.isLeft:
            if ballvelx < 0: self.ai_bithard(ballx, bally, ballvelx, ballvely)
            else: self._move_to()
        else:
            if ballvelx > 0: self.ai_bithard(ballx, bally, ballvelx, ballvely)
            else: self._move_to()

    def ultimate_predict_coordinate(self, ballx, bally, ballvelx, ballvely):
        while True:
            x = self.rect.centerx
            t = (x - ballx) / ballvelx
            y_predicted = bally + ballvely * t
            if y_predicted < 0:
                y_next = 0
            elif y_predicted > SCREEN_HEIGHT:
                y_next = SCREEN_HEIGHT
            else:
                return y_predicted
            t_next = (y_next - bally) / ballvely
            x_next = ballx + ballvelx * t_next
            ballx, bally = x_next, y_next
            ballvely = Ball._update_speed(ballvely)

    def ai_ultimate(self, ballx, bally, ballvelx, ballvely):
        if self.isLeft:
            if ballvelx < 0:
                y_predicted = self.ultimate_predict_coordinate(ballx, bally, ballvelx, ballvely)
                self._move_to(y_predicted)
            else: 
                self._move_to()
        else:
            if ballvelx > 0:
                y_predicted = self.ultimate_predict_coordinate(ballx, bally, ballvelx, ballvely)
                self._move_to(y_predicted)
            else: self._move_to()
        


    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)


class Ball:
    def __init__(self, radius, speed, color=(255, 255, 255), logic='simple'):
        self.radius = radius
        self.color = color
        left = (SCREEN_WIDTH >> 1) - radius
        top = (SCREEN_HEIGHT >> 1) - radius 
        self.rect = pygame.rect.Rect(left, top, 2 * radius, 2 * radius)
        r = randint(0, 300) / 100
        self.speedx = speed * cos(r)
        self.speedy = speed * sin(r)

        self.ticks = 0
        self.increase_speed_ticks = 1
        self.increase_delta_speed = .1

    def update(self, left_board, right_board):
        if self.ticks >= self.increase_speed_ticks:
            if self.speedx > 0:
                self.speedx += self.increase_delta_speed
            else:
                self.speedx -= self.increase_delta_speed
            if self.speedy > 0:
                self.speedy += self.increase_delta_speed
            else:
                self.speedy -= self.increase_delta_speed
            self.ticks = 0

        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top < 0:
            self.rect.top = 0
            self.speedy = Ball._update_speed(self.speedy)
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.speedy = Ball._update_speed(self.speedy)
        
        if left_board.rect.colliderect(self.rect):
            self.rect.left = left_board.rect.right
            self.speedx = Ball._update_speed(self.speedx)
            self.ticks += 1
            if config.PLAY_SOUND:
                collide_sound.play()
        if right_board.rect.colliderect(self.rect):
            self.rect.right = right_board.rect.left
            self.speedx = Ball._update_speed(self.speedx)
            self.ticks += 1
            if config.PLAY_SOUND:
                collide_sound.play()

        if self.rect.left < 0: return 1
        if self.rect.right > SCREEN_WIDTH: return -1
        return 0


    def _update_speed(oldSpeed):
        return -oldSpeed

    def draw(self):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)


class App:
    def __init__(self, max_points=10, level=level, logic=logic):
        self.leftBoard = Board(BOARD_WIDTH, BOARD_HEIGHT, BOARD_SPEED, level=config.level, ai=False, color=BOARD_COLOR)
        self.rightBoard = Board(BOARD_WIDTH, BOARD_HEIGHT, BOARD_SPEED, False, ai=True, level=config.level, color=BOARD_COLOR)
        self.ball = Ball(BALL_RADIUS, BALL_SPEED, BALL_COLOR, logic)
        self.run = True
        self.max_points = max_points
        self.leftPoints = 0
        self.rightPoints = 0

        self.last_ai = config.USE_AI

        self.font = pygame.font.SysFont('Futura', 60)

        
    def new_round(self):
        self.leftBoard = Board(BOARD_WIDTH, BOARD_HEIGHT, BOARD_SPEED, level=config.level, color=BOARD_COLOR)
        self.rightBoard = Board(BOARD_WIDTH, BOARD_HEIGHT, BOARD_SPEED, False, True, config.level, BOARD_COLOR)
        self.ball = Ball(BALL_RADIUS, BALL_SPEED, BALL_COLOR, logic)

    def update(self):
        if not config.USE_AI and self.last_ai:
            self.leftBoard.ai = False
            self.leftBoard.moveDown = False
            self.leftBoard.moveUp = False
        self.last_ai = config.USE_AI
        
        if not self.run: return
        
        self.leftBoard.update(self.ball)
        self.rightBoard.update(self.ball)
        result = self.ball.update(self.leftBoard, self.rightBoard)
        if result == 1:
            self.rightPoints += 1
            self.new_round()
        elif result == -1:
            self.leftPoints += 1
            self.new_round()
        if self.leftPoints == config.MAX_POINTS:
            config.round_finished = True
            config.win = True
        elif self.rightPoints == config.MAX_POINTS:
            config.round_finished = True
            config.win = False


    def draw(self):
        screen.fill(BG_COLOR)
        if DRAW_LINE:
            pygame.draw.line(screen, LINE_COLOR, (SCREEN_WIDTH >> 1, 0), (SCREEN_WIDTH >> 1, SCREEN_HEIGHT), LINE_WIDTH)
        if DRAW_CIRCLE:
            pygame.draw.circle(screen, CIRCLE_COLOR, (SCREEN_WIDTH >> 1, SCREEN_HEIGHT >> 1), CIRCLE_RADIUS, width=CIRCLE_WIDTH)
        lefttext = font.render(str(self.leftPoints), True, FONT_COLOR)
        righttext = font.render(str(self.rightPoints), True, FONT_COLOR)
        screen.blit(lefttext, (SCREEN_WIDTH >> 2, 10))
        screen.blit(righttext, (SCREEN_WIDTH - (SCREEN_WIDTH >> 2), 10))
        self.leftBoard.draw()
        self.rightBoard.draw()
        self.ball.draw()
        if config.round_finished:
            text = 'You won!'
            color = GREEN
            if not config.win:
                text = 'You lost!'
                color = RED
            text = self.font.render(text, True, color, BLACK)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 50))

config.mainMenu = MainMenu(
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    topmargin=150,
    margin=50
)

config.settingsMenu = CommonSettingsMenu(
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
)

config.menu = config.mainMenu

while not config.game_over:
    clock.tick(FPS)
    if config.new_game:
        app = App()
        config.new_game = False
        config.round_finished = False
        config.win = False
    if config.pause:
        config.menu.update()
        config.menu.draw(screen)
    else:
        if not config.round_finished:
            app.update()
        app.draw()
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            config.game_over = True
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                app.leftBoard.moveUp = True
            if event.key == pygame.K_DOWN:
                app.leftBoard.moveDown = True
            if event.key == pygame.K_SPACE and config.USE_AI:
                app.leftBoard.ai = not app.leftBoard.ai

            if event.key == pygame.K_ESCAPE:
                config.pause = not pause

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                app.leftBoard.moveUp = False
            if event.key == pygame.K_DOWN:
                app.leftBoard.moveDown = False

    pygame.display.update()
    
    

pygame.quit()