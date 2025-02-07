import pygame
import sys
import os
import subprocess
from buttons import ImageButton
from settings import settings_menu

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


play_button = ImageButton(WIDTH // 3 + 100, HEIGHT // 2 - 120, 400, 100, "",
                          "data/play_b.png", "data/hover_play_b.png")
exit_button = ImageButton(WIDTH // 3 + 100, HEIGHT // 2, 400, 100, "",
                          "data/exit_b.png", "data/hoverr_exit_b.png")
settings_button = ImageButton(WIDTH // 2 - 300, HEIGHT // 2 - 100, 75, 200, "",
                              "data/settings_b.png", "data/hover_settings_b.png")


# Фон главного меню
background = pygame.image.load("data/fon_YL_text.png")  # Загружаем фон
background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # Масштабируем под размер окна


def main_menu():
    running = True
    while running:
        screen.blit(background, (0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.USEREVENT and event.button == exit_button):
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == play_button:
                pygame.quit()  # Закрываем главное меню
                subprocess.run(["python", "basic_game.py"])  # Запускаем игру
                sys.exit()  # Полностью закрываем меню

            if event.type == pygame.USEREVENT and event.button == settings_button:
                settings_menu()

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

if __name__ == "__main__":
    main_menu()
