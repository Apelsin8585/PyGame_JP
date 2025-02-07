import pygame
import sys
import subprocess

# Инициализация Pygame
pygame.init()

# Полноэкранный режим
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Настройки")

# Правила игры
rules = ["Управление:",
         "ESC - выход",
         "A/D - движение влево/вправо",
         "Space - прыжок",
         "ЛКМ - стрельба"]
font = pygame.font.Font(None, 72)
text_coord = 50  # Начальная координата для текста

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Фон настроек
settings_background = pygame.image.load("data/fon_YL.jpg")
settings_background = pygame.transform.scale(settings_background, (WIDTH, HEIGHT))

def settings_menu():
    running = True

    while running:
        # Отображаем фон
        screen.blit(settings_background, (0, 0))

        # Обрабатываем события
        for event in pygame.event.get():
            if event.type == pygame.QUIT \
            or event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                pygame.quit()  # Закрытие игры
                subprocess.run(["python", "main.py"])  # Запуск игры
                sys.exit()

        # Отображаем текст на экране
        text_coord = 50  # Сбрасываем координату текста
        for line in rules:
            string_rendered = font.render(line, 1, pygame.Color(WHITE))
            intro_rect = string_rendered.get_rect()
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        # Обновление экрана
        pygame.display.flip()






