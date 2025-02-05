

import sys
import pygame
import random

# Инициализация Pygame
pygame.init()

# Полноэкранный режим
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Игра с фиксированной стрельбой")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Часы для управления FPS
clock = pygame.time.Clock()
FPS = 60

# Гравитация
GRAVITY = 0.5

# Группы спрайтов
all_sprites = pygame.sprite.Group()
walls = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Счетчик убийств
kill_count = 0

class Player(pygame.sprite.Sprite):
    """Класс для игрока."""
    def init(self):
        super().init(all_sprites)
        self.image = pygame.Surface((40, 60))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.vel_y = 0
        self.vel_x = 0
        self.on_ground = False

    def update(self):
        """Обновляет состояние игрока."""
        # Гравитация
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        # Проверка на землю
        if self.rect.bottom >= HEIGHT - 50:
            self.rect.bottom = HEIGHT - 50
            self.vel_y = 0
            self.on_ground = True

        # Управление
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:  # Движение влево
            self.vel_x = -5
        elif keys[pygame.K_d]:  # Движение вправо
            self.vel_x = 5
        else:
            self.vel_x = 0

        # Движение по X
        self.rect.x += self.vel_x

        # Проверка коллизий со стенами
        self.check_collisions()

        # Проверка границ экрана
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def check_collisions(self):
        """Проверяет коллизии со стенами."""
        hits = pygame.sprite.spritecollide(self, walls, False)
        for hit in hits:
            if self.vel_x > 0:  # Движение вправо
                self.rect.right = hit.rect.left
            elif self.vel_x < 0:  # Движение влево
                self.rect.left = hit.rect.right
            if self.vel_y > 0:  # Падение вниз
                self.rect.bottom = hit.rect.top
                self.vel_y = 0
                self.on_ground = True
            elif self.vel_y < 0:  # Прыжок вверх
                self.rect.top = hit.rect.bottom
                self.vel_y = 0

    def shoot(self):
        """Стрельба вверх."""
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Wall(pygame.sprite.Sprite):
    """Класс для стен."""
    def init(self, x, y, width, height):
        super().init(all_sprites, walls)
        self.image = pygame.Surface((width, height))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Enemy(pygame.sprite.Sprite):
    """Класс для врагов."""
    def init(self, x, y):
        super().init(all_sprites, enemies)
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_x = random.choice([-2, 2])
        self.hiding = False

    def update(self):
        """Обновляет состояние врага."""
        # Движение врага
        self.rect.x += self.vel_x

        # Проверка коллизий со стенами
        if pygame.sprite.spritecollideany(self, walls):
            self.vel_x *= -1
            self.hiding = True  # Враг прячется за стеной
        else:
            self.hiding = False

        # Проверка границ экрана
        if self.rect.left < 0:
            self.rect.left = 0
            self.vel_x *= -1
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.vel_x *= -1
# Стрельба в сторону игрока
        if not self.hiding and random.randint(1, 100) == 1:
            self.shoot()

    def shoot(self):
        """Стрельба врага."""
        bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Bullet(pygame.sprite.Sprite):
    """Класс для пуль игрока."""
    def init(self, x, y):
        super().init(all_sprites)
        self.image = pygame.Surface((10, 20))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

    def update(self):
        """Обновляет состояние пули."""
        self.rect.y -= 10  # Пуля движется вверх
        if self.rect.bottom < 0:
            self.kill()
        # Проверка коллизий со стенами
        if pygame.sprite.spritecollideany(self, walls):
            self.kill()

class EnemyBullet(pygame.sprite.Sprite):
    """Класс для пуль врагов."""
    def init(self, x, y):
        super().init(all_sprites)
        self.image = pygame.Surface((10, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y

    def update(self):
        """Обновляет состояние пули."""
        self.rect.y += 10
        if self.rect.top > HEIGHT:
            self.kill()
        # Проверка коллизий со стенами
        if pygame.sprite.spritecollideany(self, walls):
            self.kill()

def load_level(level):
    """Загружает уровень."""
    global kill_count
    kill_count = 0  # Сброс счетчика убийств

    # Очистка предыдущих спрайтов
    all_sprites.empty()
    walls.empty()
    enemies.empty()
    bullets.empty()

    # Создание игрока
    player = Player()

    # Создание стен
    if level == 1:
        Wall(200, 400, 200, 20)
        Wall(400, 300, 200, 20)
        for _ in range(3):
            enemy = Enemy(random.randint(0, WIDTH - 40), random.randint(0, HEIGHT // 2))
    elif level == 2:
        Wall(100, 500, 200, 20)
        Wall(500, 200, 200, 20)
        for _ in range(7):
            enemy = Enemy(random.randint(0, WIDTH - 40), random.randint(0, HEIGHT // 2))

    return player

# Загрузка первого уровня
current_level = 1
player = load_level(current_level)

# Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Выход по ESC
                running = False
            if event.key == pygame.K_SPACE and player.on_ground:  # Прыжок
                player.vel_y = -15
                player.on_ground = False
        elif event.type == pygame.MOUSEBUTTONDOWN:  # Стрельба по левой кнопке мыши
            if event.button == 1:  # Левая кнопка мыши
                player.shoot()  # Стрельба вверх

    # Обновление спрайтов
    all_sprites.update()

    # Проверка коллизий пуль с врагами
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        kill_count += 1
        print(f"Убийств: {kill_count}")
        if current_level == 1 and kill_count >= 7:  # Переход на второй уровень
            current_level = 2
            player = load_level(current_level)
        else:
            enemy = Enemy(random.randint(0, WIDTH - 40), random.randint(0, HEIGHT // 2))

    # Проверка коллизий игрока с врагами
    if pygame.sprite.spritecollide(player, enemies, False):
        print("Игрок убит!")
        running = False

    # Проверка коллизий игрока с пулями врагов
    if pygame.sprite.spritecollide(player, bullets, True):
        print("Игрок ранен!")

    # Отрисовка
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()