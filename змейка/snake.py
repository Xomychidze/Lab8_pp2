import pygame
import sys
import random as ran
import classGame  

pygame.init()
pygame.mixer.init()

# Музыка
monetka = pygame.mixer.Sound("змейка/z_uki-dlya-_ideo-z_uk-monetok-mario.mp3")

# Константы       
WIDTH, HEIGHT = 1500, 800
BLACK = (0, 0, 0)
CELL_SIZE = 20
SPEED = 5
HAS_FOOD_SCREEN = False
INTERVAL = 2000

# Переменные
tick_speed = 13
level_up = True
play_game = True
food = False
monetka_music = False
time_set = 0
special_food = False

# Экран
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Simple Snake')
start_time = pygame.time.get_ticks()

# Цвета
GREEN = (0, 255, 0)
WHITE = (255,255,255)

# Массивы игры
obstacles = []
snake_pos = [100, 100]
snake_body = [[100, 100], [80, 100], [60, 100]]
direction = 'RIGHT'
change_to = direction

# UI
ui = classGame.UI_Count(WIDTH - 100, 20, 80, 40, (50, 50, 50), 36)
clock = pygame.time.Clock()

# Загрузка изображения головы змеи
snake_head_img = pygame.image.load("змейка/man.jpg")
snake_head_img = pygame.transform.scale(snake_head_img, (CELL_SIZE, CELL_SIZE))

running = True
while running:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and direction != 'DOWN':
                change_to = 'UP'
            elif event.key == pygame.K_s and direction != 'UP':
                change_to = 'DOWN'
            elif event.key == pygame.K_d and direction != 'LEFT':
                change_to = 'RIGHT'
            elif event.key == pygame.K_a and direction != 'RIGHT':
                change_to = 'LEFT'

        elif event.type == pygame.MOUSEBUTTONUP:
            if not play_game: 
                pos = event.pos
                if button_exit.rect.collidepoint(pos):
                    running = False
                if button_replay.rect.collidepoint(pos):
                    tick_speed = 13
                    level_up = True
                    play_game = True
                    food = False
                    obstacles = []
                    snake_pos = [100, 100]
                    snake_body = [[100, 100], [80, 100], [60, 100]]
                    direction = 'RIGHT'
                    change_to = direction
                    ui = classGame.UI_Count(WIDTH - 100, 20, 80, 40, (50, 50, 50), 36)

    # Проверка на столкновение с собой
    for i in range(1, len(snake_body)):
        if snake_body[0][0] == snake_body[i][0] and snake_body[0][1] == snake_body[i][1]:
            play_game = False
            pygame.mixer.music.load("змейка/mario-smert.mp3")
            pygame.mixer.music.play()

    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load("змейка/super-mario-saundtrek.mp3")
        pygame.mixer.music.play()

    direction = change_to

    # Создание еды
    if current_time - start_time >= INTERVAL:
        if not food: 
            food_x = ran.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
            food_y = ran.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
            choose = ran.randint(1, 3)
            if choose == 1:
                food = classGame.GameObject(food_x, food_y, CELL_SIZE, CELL_SIZE, (255, 255, 255), 1)
            elif choose == 2:
                food = classGame.GameObject(food_x, food_y, CELL_SIZE, CELL_SIZE, (255, 255, 255), 2)
            elif choose == 3: 
                food = classGame.GameObject(food_x, food_y, CELL_SIZE, CELL_SIZE, (255, 0, 0), 3)
                line_time = pygame.Rect(700, 30, 300, 10)
                special_food = True
            obstacles.append(food)
            food = True
        time_set += 1

    # Столкновение с едой
    player = pygame.Rect(snake_pos[0], snake_pos[1], CELL_SIZE, CELL_SIZE)
    for obstacle in obstacles[:]:
        if player.colliderect(obstacle.rect):
            obj: classGame.GameObject = obstacle
            ui.count_more(obj.get_weight()) 
            obstacles.remove(obstacle)
            snake_body.insert(0, list(snake_pos))
            special_food = False
            line_time = None
            level_up = True
            monetka.play()
            monetka_music = True
            food = False

    # Отключение звука монетки
    if time_set % 10 == 0:
        monetka_music = False
    if not monetka_music:
        monetka.stop()

    # Таймер для специальной еды
    if special_food:
        line_time.width -= 5
        if line_time.width <= 0: 
            obstacles.clear()
            special_food = False
            line_time = None
            food = False

    # Повышение уровня
    if ui.num % 5 == 0 and ui.num != 0 and level_up: 
        level_up = False
        tick_speed += 0.5

    # Движение змейки
    if direction == 'UP':
        snake_pos[1] -= CELL_SIZE 
    elif direction == 'DOWN':
        snake_pos[1] += CELL_SIZE 
    elif direction == 'LEFT':
        snake_pos[0] -= CELL_SIZE 
    elif direction == 'RIGHT':
        snake_pos[0] += CELL_SIZE 

    # Переход через границы экрана
    if (
    snake_pos[0] < 0 or 
    snake_pos[0] >= WIDTH or 
    snake_pos[1] < 0 or 
    snake_pos[1] >= HEIGHT):
        play_game = False
        pygame.mixer.music.load("змейка/mario-smert.mp3")
        pygame.mixer.music.play()

    snake_body.insert(0, list(snake_pos))
    snake_body.pop()

    screen.fill(BLACK)

    # Отрисовка игры
    if play_game: 
        for i in range(1, len(snake_body)):
            pygame.draw.rect(screen, GREEN, pygame.Rect(snake_body[i][0], snake_body[i][1], CELL_SIZE, CELL_SIZE))
        for obstacle in obstacles: 
            obstacle.draw(screen)    

        # Рисуем голову змейки как изображение
        screen.blit(snake_head_img, (snake_pos[0], snake_pos[1]))

        if special_food:
            pygame.draw.rect(screen, (255, 255, 255), line_time)
        ui.draw(screen)
    else: 
        game_over = classGame.UI_level(0, 0, WIDTH, HEIGHT, (200, 0, 0), 80, "Game Over! Loshara")
        button_replay = classGame.Button(580, 450, 150, 60, (0, 0, 0), "Replay", (255, 255, 255), 5)
        button_exit = classGame.Button(780, 450, 150, 60, (0, 0, 0), "Exit", (255, 255, 255), 5)        
        game_over.draw(screen)
        button_exit.draw(screen)
        button_replay.draw(screen)

    pygame.display.flip()
    clock.tick(tick_speed)

pygame.quit()
sys.exit()
