import pygame
import assets

font = pygame.font.Font(None, 40)

bg_scroll_y = 0
BG_SCROLL_SPEED = 4 

def draw_background(screen, game_over=False):
    global bg_scroll_y

    bg = assets.get("background")
    if bg:
        if not game_over:
            bg_scroll_y += BG_SCROLL_SPEED
            if bg_scroll_y >= 700:
                bg_scroll_y = 0

        screen.blit(bg, (0, bg_scroll_y - 700))
        screen.blit(bg, (0, bg_scroll_y))
    else:
        screen.fill((30, 30, 30))

def show_score(screen, score, coins, high_score=0, total_coins=0):
    font = pygame.font.Font(None, 40)
    score_text = font.render(f"Score: {int(score)}", True, (255, 255, 255))
    coin_text = font.render(f"Coins: {coins}", True, (255, 255, 0))
    high_text = font.render(f"High: {high_score}", True, (255, 200, 200))
    total_text = font.render(f"Total: {total_coins}", True, (200, 255, 200))

    screen.blit(score_text, (20, 40))
    screen.blit(coin_text, (20, 80))
    screen.blit(high_text, (350, 40))
    screen.blit(total_text, (350, 80))

def show_game_over(screen):
    over = font.render("GAME OVER", True, (255, 0, 0))
    restart = font.render("Press SPACE to Restart", True, (255, 255, 255))
    screen.blit(over, (250 - 90, 700//2 - 40))
    screen.blit(restart, (250 - 160, 700//2))