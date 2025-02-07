import pygame
import sys
import subprocess
from buttons import ImageButton

# Инициализация Pygame
pygame.init()

# Полноэкранный режим
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Настройки")

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

# Кнопка назад
back_button = ImageButton(WIDTH // 2 - 150, HEIGHT - 150, 300, 80, "", "data/back_b.png", "data/hover_back_b.png")
# Фон настроек
settings_background = pygame.image.load("data/fon_YL.jpg")
settings_background = pygame.transform.scale(settings_background, (WIDTH, HEIGHT))

def settings_menu():
    global current_difficulty

    running = True

    while running:
        # Отображаем фон
        screen.blit(settings_background, (0, 0))

        # Обрабатываем события
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Закрытие игры
                subprocess.run(["python", "main.py"])  # Запуск игры
                sys.exit()

            # Обработка событий для кнопок
            back_button.handle_event(event)



        # Обработка кнопки "Назад"
        back_button.check_hover(pygame.mouse.get_pos())  # Проверка на наведение
        back_button.draw(screen)  # Отображаем кнопку

        # Обновляем экран
        pygame.display.flip()

"""        # Отображаем текст на экране
        text_coord = 50  # Сбрасываем координату текста
        for line in rules:
            string_rendered = font.render(line, 1, pygame.Color(WHITE))
            intro_rect = string_rendered.get_rect()
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)"""

