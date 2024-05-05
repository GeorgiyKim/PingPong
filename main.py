import time
import time as t
from pygame import *

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Ping Pong")
background = transform.scale(image.load('background.jpg'), (700, 500))
app = True
clock = time.Clock()
FPS = 60


class GameSprite(sprite.Sprite):
    # конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)
        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.size_x = size_x
        self.size_y = size_y

    # метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    # класс главного игрока


class Player(GameSprite):
    # метод для управления спрайтом стрелками клавиатуры
    def update_L(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < 400:
            self.rect.y += self.speed

    def update_R(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < 400:
            self.rect.y += self.speed


speed_x = 5
speed_y = 5


class Ball(GameSprite):
    def move(self):
        global speed_x
        global speed_y
        self.rect.x += speed_x
        self.rect.y += speed_y

        if self.rect.colliderect(racket1):
            self.rect.x -= 1
            speed_x *= -1
        if self.rect.colliderect(racket):
            self.rect.x += 1
            speed_x *= -1
        if self.rect.y <= 0:
            self.rect.y += 1
            speed_y *= -1
        if self.rect.y >= win_height - 30:
            self.rect.y -= 1
            speed_y *= -1

        if self.rect.x <= 0:
            self.rect.x = win_width // 2 - 15
            self.rect.y = win_height // 2 - 15
            counter('left')

        if self.rect.x > win_width - 30:
            self.rect.x = win_width // 2 - 15
            self.rect.y = win_height // 2 - 15
            counter('right')


bloody = (239, 5, 5)
ocean = (5, 29, 239)
font.init()
count = font.Font('Duo-quadruple_by_hanbikov_ilyas.otf', 50)

counter_font = font.Font('Duo-quadruple_by_hanbikov_ilyas.otf', 45)

right = 0
left = 0


def counter(side: str):
    global right
    global left
    global points
    if side == 'right':
        left += 1
        points = counter_font.render(f'{left} - {right}', True, (255, 255, 255), (96, 96, 96))
        check = count.render(f'Очко левому игроку!', True, bloody)
        window.blit(check, (90, 150))
        display.update()
        time.delay(1000)

    if side == 'left':
        right += 1
        points = counter_font.render(f'{left} - {right}', True, (255, 255, 255), (96, 96, 96))
        check = count.render(f'Очко правому игроку!', True, ocean)
        window.blit(check, (90, 150))
        display.update()
        time.delay(1000)

    if side == 'game_start':
        check_table = counter_font.render('0 - 0', True, (255, 255, 255), (96, 96, 96))
        return check_table


ball = Ball('tenis_ball.png', win_width // 2 - 15, win_height // 2 - 15, 30, 30, 5)
racket = Player('racket.png', 20, 40, 40, 70, 5)
racket1 = Player('racket.png', 630, 80, 40, 70, 5)

game_over = count.render('GAME OVER', True, (255, 255, 255))

points = counter('game_start')

render = True
game = True
while app:
    # событие нажатия на кнопку “Закрыть”
    for e in event.get():
        if e.type == QUIT:
            app = False

    if game:
        if left >= 5 or right >= 5:
            game = False

        window.blit(background, (0, 0))
        window.blit(points, (win_width // 2 - 50, 1))
        ball.reset()
        racket.reset()
        racket1.reset()
        racket.update_L()
        racket1.update_R()
        ball.move()
        clock.tick(FPS)
        display.update()

    for e in event.get():
        if e.type == QUIT:
            app = False

    if game is not True:
        if render:
            window.fill((0, 0, 0))
            window.blit(game_over, (win_width // 2 - 150, win_height // 2 - 25))
            display.update()
            time.delay(500)
            render = False
        if left >= 5:
            window.fill((0, 0, 0))
            red_win = count.render('ПОБЕДА КРАСНЫХ', True, bloody)
            window.blit(red_win, (win_width // 2 - 200, win_height // 2 - 25))
            display.update()


        if right >= 5:
            window.fill((0, 0, 0))
            blue_win = count.render('ПОБЕДА СИНИХ', True, ocean)
            window.blit(blue_win, (win_width // 2 - 180, win_height // 2 - 25))
            display.update()

