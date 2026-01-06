import pygame, sys, random, time
pygame.init()

WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Great Indian Dash")

import assets
assets.load_images()
pygame.mixer.music.load(assets.ASSETS["bg_music"])
pygame.mixer.music.set_volume(0.6)
pygame.mixer.music.play(-1)

from save_system import (
    load_data, save_data, update_high_score, add_coins, get_high_score, get_total_coins,
    create_user, login_user, get_current_user, get_all_users
)
from player import Player
from obstacles import ObstacleManager
from powerups import PowerUps
from ui import draw_background, show_score, show_game_over
from menu import draw_menu, handle_menu_input 

clock = pygame.time.Clock()
SPAWN_EVENT = pygame.USEREVENT + 1
COIN_EVENT = pygame.USEREVENT + 2
POWERUP_EVENT = pygame.USEREVENT + 3
pygame.time.set_timer(SPAWN_EVENT, 1200)
pygame.time.set_timer(COIN_EVENT, 1500)
pygame.time.set_timer(POWERUP_EVENT, 8000)

player = Player()
obstacles = ObstacleManager()
powerups = PowerUps()
game_over = False
score = 0
game_over_updated = False 
# This is the one
game_state = "login"
username = ""
menu_selected = 0

def reset_game():
    global player, obstacles, powerups, score, game_over
    player = Player()
    obstacles = ObstacleManager()
    powerups = PowerUps()
    score = 0
    game_over = False

while True:
    events = pygame.event.get()
    keys = pygame.key.get_pressed()

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if game_state == "login":
        screen.blit(assets.ASSETS["login_bg"], (0, 0))

        font = pygame.font.Font(None, 50)
        prompt_text = font.render("Enter Username: " + username, True, (255, 255, 255))
        screen.blit(prompt_text, (50, HEIGHT // 2))

        font_small = pygame.font.Font(None, 30)
        info_text = font_small.render("Press ENTER to continue", True, (200, 200, 200))
        screen.blit(info_text, (50, HEIGHT // 2 + 60))

        pygame.display.flip()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if username.strip() != "":
                        if username not in get_all_users():
                            create_user(username)
                        else:
                            login_user(username)
                        high_score = get_high_score()
                        total_coins = get_total_coins()
                        game_state = "menu"
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += event.unicode

        continue 

    if game_state == "menu":
        for event in events:
            menu_selected, chosen = handle_menu_input(event, menu_selected)
            if chosen:
                if menu_selected == 0:
                    reset_game()
                    game_state = "playing"
                elif menu_selected == 1:
                    pygame.quit()
                    sys.exit()
        draw_menu(screen, menu_selected)
        pygame.display.flip()
        clock.tick(60)
        continue

    if game_state == "playing":
        for event in events:
            if event.type == SPAWN_EVENT and not game_over:
                obstacles.spawn()
            if event.type == COIN_EVENT and not game_over:
                powerups.spawn_coin(obstacles)
            if event.type == POWERUP_EVENT and not game_over:
                powerups.spawn_powerup(obstacles)

        draw_background(screen, game_over)

        if not game_over:
            player.move(keys)
            player.update()
            base_speed = 8
            speed_active = "speed" in powerups.active_powerups
            movement_multiplier = 1.7 if speed_active else 1  
            score_multiplier = 2 if speed_active else 1        

            obstacles.move(base_speed * movement_multiplier)
            powerups.move_coins(base_speed * movement_multiplier)
            powerups.move_powerups(base_speed * movement_multiplier)
            powerups.update_active_powerups()
            
            powerups.check_coin_collection(player)
            powerups.check_powerup_collection(player)
            powerups.apply_magnet_effect(player)

            collided = obstacles.check_collision(player)
            if collided:
                if "shield" in powerups.active_powerups:
                    del powerups.active_powerups["shield"]
                elif "dash" in powerups.active_powerups:
                    pass
                else:
                    assets.ASSETS["sounds"]["game_over"].play()
                    game_over = True
                    game_over_updated = False
            else:
                score += 0.2 * score_multiplier

        draw_background(screen)
        obstacles.draw(screen)
        powerups.draw_coins(screen)
        powerups.draw_powerups(screen)
        player.draw(screen)
        powerups.draw_active_effects(screen, player)

        show_score(screen, score, powerups.score, high_score, total_coins)
        font = pygame.font.Font(None, 30)
        user_text = font.render(f"User: {get_current_user()}", True, (255,255,255))
        screen.blit(user_text, (20,10))

        if game_over:
            if not game_over_updated:
                update_high_score(score)
                add_coins(powerups.score)
                high_score = get_high_score()
                total_coins = get_total_coins()
                game_over_updated = True
            show_game_over(screen)
            if keys[pygame.K_SPACE]:
                reset_game()
                game_state = "menu"

        pygame.display.flip()
        clock.tick(60)