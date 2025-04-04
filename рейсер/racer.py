import pygame, sys
from pygame.locals import *
import random, time

# Инициализация Pygame
pygame.init()

# Основные настройки
FPS = 60
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FramePerSec = pygame.time.Clock()

# Цвета
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Шрифты
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)

# Экран
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game")

# Задний фон
background = pygame.image.load("рейсер\\AnimatedStreet.png")
        
global SCORE
# Класс кнопки
class Button:
    def __init__(self, x, y, width, height, color, text, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font = pygame.font.Font(None, 24)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Класс врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("рейсер\\Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
        self.speed = 5
        self.inc = False

    def move(self):

        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
            self.inc = True

    def increase_speed(self):
        if SCORE % 10 == 0 and self.inc:
            self.speed += 1
            self.inc = False

# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("рейсер\\Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        keys = pygame.key.get_pressed()
        if self.rect.left > 0 and keys[K_a]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH and keys[K_d]:
            self.rect.move_ip(5, 0)

# Класс объекта (монета)
class GameObject:
    def __init__(self, image, weight):
        original_image = pygame.image.load(image)
        self.image = pygame.transform.scale(original_image, (30, 30))  # Уменьшили размер
        self.rect = self.image.get_rect()
        self.weight = weight
        self.speed = 5
        self.rect.center = (random.randint(30, SCREEN_WIDTH - 30), 0)

    def move(self):
        self.rect.move_ip(0, self.speed)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Основная функция игры
def main():
    global SCORE
    SCORE = 0
    INTERVAL = 4000
    MONEY = False
    start_time = pygame.time.get_ticks()
    money_list = []

    # Кнопки
    replay_button = Button(120, 400, 80, 40, BLACK, "Replay", WHITE)
    exit_button = Button(220, 400, 80, 40, BLACK, "Exit", WHITE)

    # Спрайты
    P1 = Player()
    E1 = Enemy()
    enemies = pygame.sprite.Group()
    enemies.add(E1)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(P1, E1)

    running = True
    game_over = False

    while running:
        DISPLAYSURF.blit(background, (0, 0))
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and game_over:
                if replay_button.is_clicked(event.pos):
                    main()
                    return
                elif exit_button.is_clicked(event.pos):
                    pygame.quit()
                    sys.exit()

        if not game_over:
            # Создание новой монеты
            if current_time - start_time >= INTERVAL:
                if not MONEY:
                    weight = random.randint(1, 2)
                    money = GameObject("рейсер\monetka.png", weight)
                    money_list.append(money)
                    MONEY = True
                    start_time = current_time

            # Отображение счёта
            score_text = font_small.render(f"Score: {SCORE}", True, BLACK)
            DISPLAYSURF.blit(score_text, (10, 10))

            # Отрисовка и движение спрайтов
            for entity in all_sprites:
                entity.move()
                DISPLAYSURF.blit(entity.image, entity.rect)
                if isinstance(entity, Enemy):
                    entity.increase_speed()

            # Отрисовка и движение монет
            for mon in money_list[:]:
                mon.move()
                mon.draw(DISPLAYSURF)

                # Сбор монеты
                if P1.rect.colliderect(mon.rect):
                    SCORE += mon.weight
                    money_list.remove(mon)
                    MONEY = False

                # Удаление, если вышла за экран
                elif mon.rect.top > SCREEN_HEIGHT:
                    money_list.remove(mon)
                    MONEY = False

            # Проверка столкновений с врагом
            if pygame.sprite.spritecollideany(P1, enemies):
                pygame.mixer.Sound('рейсер\\crash.wav').play()
                DISPLAYSURF.fill(RED)
                over_text = font.render("Game Over", True, BLACK)
                DISPLAYSURF.blit(over_text, (30, 250))
                replay_button.draw(DISPLAYSURF)
                exit_button.draw(DISPLAYSURF)
                pygame.display.update()
                game_over = True

        pygame.display.update()
        FramePerSec.tick(FPS)

# Запуск
if __name__ == "__main__":
    main()
