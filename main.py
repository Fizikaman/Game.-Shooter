# необходимые импорты
import sys
from random import randint
import pygame

# инициализация игры
pygame.init()

game_font = pygame.font.Font(None, 30)  # Шрифт текста

# параметры экрана
screen_width, screen_height = 800, 600
screen_fill_color = (32, 52, 71)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("!!!Fucking Mega Shooter Game!!!")

FIGHTER_STEP = 0.5  # шаг смещения
BALL_STEP = 0.5  # скорость ракеты

fighter_image = pygame.image.load('png_files/fighter.png')  # параметры изображения: загрузка изображения,
fighter_width, fighter_height = fighter_image.get_size()  # координаты верх. левого угла
fighter_x, fighter_y = screen_width / 2 - fighter_width / 2, screen_height - fighter_height

ball_image = pygame.image.load('png_files/ball.png')  # загрузка изображения ракет
ball_width, ball_height = ball_image.get_size()  # размер изображения
ball_x, ball_y = fighter_x + fighter_width / 2 - ball_width / 2, fighter_y - ball_height
ball_was_fired = False

alien_image = pygame.image.load('png_files/alien.png')  # загрузка изображения инопланетянена
alien_width, alien_height = alien_image.get_size()  # размеры изображения
ALIEN_STEP = 0.05  # Шаг смешения по y
alien_speed = ALIEN_STEP
alien_x, alien_y = randint(0, screen_width - alien_width), 0  # стартовые координаты

fighter_is_moving_left, fighter_is_moving_right = False, False  # Флаги для непрерывного нажатия

game_is_running = True
game_score = 0

while game_is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # условие закрытия окна
            sys.exit()
        if event.type == pygame.KEYDOWN:  # смещение изображения корабля
            if event.key == pygame.K_LEFT:
                fighter_is_moving_left = True  # меняем состояние кнопки

            if event.key == pygame.K_RIGHT:
                fighter_is_moving_right = True
                fighter_x += FIGHTER_STEP
            if event.key == pygame.K_SPACE:  # выстрел ракетой
                ball_was_fired = True
                ball_x = fighter_x + fighter_width / 2 - ball_width / 2
                ball_y = fighter_y - ball_height

        if event.type == pygame.KEYUP:  # возвращение кнопок "влево/вправо" в исходное положение
            if event.key == pygame.K_LEFT:
                fighter_is_moving_left = False
            if event.key == pygame.K_RIGHT:
                fighter_is_moving_right = False
    if fighter_is_moving_left and fighter_x >= FIGHTER_STEP:  # непрерывное перемещение корабля
        fighter_x -= FIGHTER_STEP
    if fighter_is_moving_right and fighter_x <= screen_width - fighter_width - FIGHTER_STEP:
        fighter_x += FIGHTER_STEP

    alien_y += alien_speed

    if ball_was_fired and ball_y + ball_height < 0:
        ball_was_fired = False

    if ball_was_fired:
        ball_y -= BALL_STEP

    screen.fill(screen_fill_color)  # заливка экрана цветом
    screen.blit(fighter_image, (fighter_x, fighter_y))  # размещение изображения корабля на экран
    screen.blit(alien_image, (alien_x, alien_y))

    if ball_was_fired:
        screen.blit(ball_image, (ball_x, ball_y))

    game_score_text = game_font.render(f"Your score is: {game_score}", True, 'white')  # вывод счета
    screen.blit(game_score_text, (20, 20))

    pygame.display.update()  # применение изменений

    if alien_y + alien_height > fighter_y:  # Условие проигрыша
        game_is_running = False

    if ball_was_fired and \
            alien_x < ball_x < alien_x + alien_width and \
            alien_y < ball_y < alien_y + alien_height - ball_height:  # проверка попадания по пришельцу ракетой
        ball_was_fired = False  # скрываем ракету
        alien_x, alien_y = randint(0, screen_width - alien_width), 0  # возвращаем пришельца на начало экрана после попадания
        alien_speed += 0.01
        game_score += 1

game_over_text = game_font.render("Game Over!!!", True, 'white')  # Надпись после проигрыша
game_over_rectangle = game_over_text.get_rect()  # В прямоугольнике
game_over_rectangle.center = (screen_width / 2, screen_height / 2)  # по центру
screen.blit(game_over_text, game_over_rectangle)  # Вывод на экран
pygame.display.update()
pygame.time.wait(5000)
pygame.quit()

# for event in pygame.event.get():
#     if event.type == pygame.KEYDOWN:
#         if event.key == pygame.K_y:
#             game_is_running = True
#         else:
#
