import pygame
from pygame.locals import *
import assets

pygame.init()

font = pygame.font.Font(None, 60)
small_font = pygame.font.Font(None, 40)

WHITE = (255, 255, 255)
YELLOW = (255, 215, 0)

def draw_menu(screen, selected_index):
    screen.blit(assets.menu_bg, (0, 0))

    overlay = pygame.Surface((500, 700))
    overlay.set_alpha(120)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    title = font.render("Great Indian Dash", True, YELLOW)
    screen.blit(title, (100, 150))
    options = ["Start Game", "Quit"]
    for i, text in enumerate(options):
        color = YELLOW if i == selected_index else WHITE
        option = small_font.render(text, True, color)
        screen.blit(option, (160, 280 + i * 60))

    pygame.display.flip()


def handle_menu_input(event, selected_index):
    if event.type == KEYDOWN:
        if event.key == K_UP:
            selected_index = (selected_index - 1) % 2
        elif event.key == K_DOWN:
            selected_index = (selected_index + 1) % 2
        elif event.key in (K_RETURN, K_SPACE):
            return selected_index, True
    return selected_index, False