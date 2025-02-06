import pygame
import sys
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

# Создание кнопок
play_button = ImageButton(WIDTH // 2 - 100, HEIGHT // 2 - 100, 200, 50, "", "play_b.png", "hover_play_b.png",
                          "clic.mp3")
exit_button = ImageButton(WIDTH // 2 - 100, HEIGHT // 2, 200, 50, "", "exite_b.png", "hover_exite_b.png",
                          "clic.mp3")
settings_button = ImageButton(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50, "", "settings.png",
                              "hover_settings_b.png", "clic.mp3")

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


def settings_menu():
    global volume
    increase_button = ImageButton(WIDTH // 2 + 50, HEIGHT // 2 - 50, 50, 50, "", "plus_b.png", "hover_plus_b.png",
                                  "clic.mp3")
    decrease_button = ImageButton(WIDTH // 2 - 100, HEIGHT // 2 - 50, 50, 50, "", "minus_b.png", "hover_minus_b.png",
                                  "clic.mp3")
    back_button = ImageButton(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50, "", "back_b.png", "hover_back_b.png",
                              "clic.mp3")

    run = True
    while run:
        screen.fill(BLACK)

        settings_text = font.render("Настройки", True, WHITE)
        screen.blit(settings_text, (WIDTH // 2 - 80, HEIGHT // 4))

        volume_text = font.render(f"Громкость: {int(volume * 100)}%", True, WHITE)
        screen.blit(volume_text, (WIDTH // 2 - 80, HEIGHT // 2 - 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == increase_button:
                if volume < 1.0:
                    volume += 0.1
                    pygame.mixer.music.set_volume(volume)

            if event.type == pygame.USEREVENT and event.button == decrease_button:
                if volume > 0.0:
                    volume -= 0.1
                    pygame.mixer.music.set_volume(volume)

            if event.type == pygame.USEREVENT and event.button == back_button:
                run = False

            increase_button.handle_event(event)
            decrease_button.handle_event(event)
            back_button.handle_event(event)

        increase_button.check_hover(pygame.mouse.get_pos())
        increase_button.draw(screen)
        decrease_button.check_hover(pygame.mouse.get_pos())
        decrease_button.draw(screen)
        back_button.check_hover(pygame.mouse.get_pos())
        back_button.draw(screen)

        pygame.display.flip()
