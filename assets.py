import pygame
import os
ASSETS = {}


def load_images():
    global ASSETS
    global menu_bg
    ASSETS = {}

    BASE = os.path.dirname(__file__)
    BG_DIR = os.path.join(BASE, "background")
    CHAR_DIR = os.path.join(BASE, "characters")
    OBS_DIR = os.path.join(BASE, "obstacles")
    POW_DIR = os.path.join(BASE, "powerups")

    SOUND_DIR = os.path.join(BASE, "sounds")

    ASSETS["sounds"] = {
        "coin": pygame.mixer.Sound(os.path.join(SOUND_DIR, "coin.wav")),
        "powerup": pygame.mixer.Sound(os.path.join(SOUND_DIR, "powerup.wav")),
        "game_over": pygame.mixer.Sound(os.path.join(SOUND_DIR, "game_over.wav")),
        "jump": pygame.mixer.Sound(os.path.join(SOUND_DIR, "jump.wav")),
        "slide": pygame.mixer.Sound(os.path.join(SOUND_DIR, "slide.wav")),
    }

    ASSETS["bg_music"] = os.path.join(SOUND_DIR, "bg_music.mp3")
    ASSETS["runner_frames"] = [
        pygame.transform.scale(pygame.image.load(f"runner{i}.png").convert_alpha(), (50, 50))
        for i in range(1, 4)
    ]
    ASSETS["low_obstacle"] = pygame.transform.scale(
        pygame.image.load("low_obstacle.png").convert_alpha(), (50, 40)
    )
    ASSETS["large_obstacle"] = pygame.transform.scale(
        pygame.image.load("train.png").convert_alpha(), (100, 600)
    )
    ASSETS["small_obstacle_frames"] = [
        pygame.transform.scale(
            pygame.image.load(f"small_obstacle{i}.png").convert_alpha(), (100, 100)
        )
        for i in range(1, 6)
    ]
    try:
        ASSETS["coin"] = pygame.transform.scale(pygame.image.load("coin.png").convert_alpha(), (40, 40))
        ASSETS["shield"] = pygame.transform.scale(pygame.image.load("shield.png").convert_alpha(), (60, 60))
        ASSETS["magnet"] = pygame.transform.scale(pygame.image.load("magnet.png").convert_alpha(), (60, 60))
        ASSETS["dash"] = pygame.transform.scale(pygame.image.load("dash.png").convert_alpha(), (60, 60))
        ASSETS["speed"] = pygame.transform.scale(pygame.image.load("speed.png").convert_alpha(), (60, 60))
    except FileNotFoundError:
        print("Some optional powerup images not found — skipping...")
    try:
        ASSETS["background"] = pygame.image.load("background.png").convert()
    except FileNotFoundError:
        print("Background not found — using solid color background.")
    login_bg = pygame.image.load("login_bg.png").convert()
    login_bg = pygame.transform.scale(login_bg, (500, 700))
    ASSETS["login_bg"] = login_bg
    menu_bg = pygame.image.load("menu_bg.png").convert()
    menu_bg = pygame.transform.scale(menu_bg, (500, 700))
    print("Assets loaded successfully!")

# this is the new data
# Hello
def get(name):
    return ASSETS.get(name)