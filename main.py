import pygame
import sys
import os
from buttons import ImageButton

# Инициализация Pygame
pygame.init()

# Полноэкранный режим
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Главное меню")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Шрифт
font = pygame.font.Font(None, 36)

# Громкость звука
volume = 0.5
pygame.mixer.init()
pygame.mixer.music.set_volume(volume)


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


img_play_b = load_image('play_b.png')
img_h_play_b = load_image('hover_play_b.png')
img_exit_b = load_image('exit_b.png')
img_h_exit_b = load_image('hover_exit_b.png')
img_settings_b = load_image('settings_b.png')
img_h_settings_b = load_image('hover_settings_b.png')

# Создание кнопок
play_button = ImageButton(WIDTH // 2 - 100, HEIGHT // 2 - 100, 200, 50, "", img_play_b,
                          img_h_play_b)
exit_button = ImageButton(WIDTH // 2 - 100, HEIGHT // 2, 200, 50, "", img_exit_b,
                          img_h_exit_b)
settings_button = ImageButton(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50, "", img_settings_b,
                             img_h_settings_b)

# Фон главного меню
menu_background = pygame.Surface((WIDTH, HEIGHT))
menu_background.fill(BLACK)


def main_menu():
    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.USEREVENT and event.button == exit_button):
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == play_button:
                exec(open("basic_game.py").read())

            if event.type == pygame.USEREVENT and event.button == settings_button:
                pass

            play_button.handle_event(event)
            exit_button.handle_event(event)
            settings_button.handle_event(event)

        play_button.check_hover(pygame.mouse.get_pos())
        play_button.draw(screen)
        exit_button.check_hover(pygame.mouse.get_pos())
        exit_button.draw(screen)
        settings_button.check_hover(pygame.mouse.get_pos())
        settings_button.draw(screen)
        pygame.display.flip()
