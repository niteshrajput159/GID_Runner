import pygame
import random
import time
import assets 

lane_positions = [150, 250, 350]

class PowerUps:
    def __init__(self):
        self.coins = []
        self.powerups = []
        self.active_powerups = {}
        self.score = 0
        self.coin_img = assets.get("coin")
        self.shield_img = assets.get("shield")
        self.magnet_img = assets.get("magnet")
        self.dash_img = assets.get("dash")

    def spawn_coin(self, obstacles=None):
        """Spawn coin trails with optimization."""
        if len(self.coins) > 40: 
            return

        pattern = random.choice(["line", "arc", "lane_jump"])
        base_lane = random.choice([0, 1, 2])
        lane_x = lane_positions[base_lane]
        y = -50
        if obstacles:
            for obs in obstacles.obstacles:
                if abs(obs["rect"].centerx - lane_x) < 60 and obs["rect"].y < 250:
                    return
        count = random.randint(4, 6)

        if pattern == "line":
            for i in range(count):
                self.coins.append(pygame.Rect(lane_x - 20, y - (i * 60), 40, 40))

        elif pattern == "arc":
            direction = random.choice([-1, 1])
            for i in range(count):
                offset_x = direction * (i * 10)
                self.coins.append(pygame.Rect(lane_x + offset_x - 20, y - (i * 55), 40, 40))

        elif pattern == "lane_jump":
            lanes = [0, 1, 2]
            random.shuffle(lanes)
            for i, lane in enumerate(lanes[:3]):
                self.coins.append(pygame.Rect(lane_positions[lane] - 20, y - (i * 70), 40, 40))

    def move_coins(self, speed=None):
        if speed is None:
            speed = self.base_speed
        for c in self.coins:
            c.y += speed
        self.coins = [c for c in self.coins if c.y < 800]

    def draw_coins(self, screen):
        if not self.coin_img:
            return
        for c in self.coins:
            screen.blit(self.coin_img, c.topleft)

    def check_coin_collection(self, player):
        player_rect = player.rect
        collected = [c for c in self.coins if player_rect.colliderect(c)]
        for c in collected:
            self.coins.remove(c)
        if collected:
            self.score += len(collected) * 1
            assets.ASSETS["sounds"]["coin"].play() 

    def spawn_powerup(self, obstacles=None):
        if len(self.powerups) > 5: 
            return

        lane = random.choice([0, 1, 2])
        lane_x = lane_positions[lane]
        y = -60

        if obstacles:
            for obs in obstacles.obstacles:
                if abs(obs["rect"].centerx - lane_x) < 60 and obs["rect"].y < 200:
                    return

        type_ = random.choice(["shield", "magnet", "dash", "speed"])
        rect = pygame.Rect(lane_x - 30, y, 60, 60)
        self.powerups.append({"rect": rect, "type": type_})

    def move_powerups(self, speed=None):
        if speed is None:
            speed = self.base_speed
        for p in self.powerups:
            p["rect"].y += speed
        self.powerups = [p for p in self.powerups if p["rect"].y < 800]

    def draw_powerups(self, screen):
        for p in self.powerups:
            img = assets.get(p["type"])
            if img:
                screen.blit(img, p["rect"].topleft)

    def check_powerup_collection(self, player):
        player_rect = player.rect
        collected = [p for p in self.powerups if player_rect.colliderect(p["rect"])]

        if collected:  
            assets.ASSETS["sounds"]["powerup"].play()

        for p in collected:
            self.powerups.remove(p)
            self.activate_powerup(p["type"])

    def activate_powerup(self, type_):
        self.active_powerups[type_] = time.time() + 5 

    def update_active_powerups(self):
        now = time.time()
        self.active_powerups = {k: v for k, v in self.active_powerups.items() if v > now}

    def draw_active_effects(self, screen, player):
        color_map = {
            "shield": (0, 255, 255),
            "dash": (255, 200, 0),
            "magnet": (255, 0, 255),
            "speed": (0, 255, 0),
        }
        for k, color in color_map.items():
            if k in self.active_powerups:
                pygame.draw.circle(screen, color, player.rect.center, 40, 3)

    def apply_magnet_effect(self, player):
        if "magnet" not in self.active_powerups:
            return
        for c in self.coins:
            dx = player.rect.centerx - c.centerx
            dy = player.rect.centery - c.centery
            if abs(dx) < 150 and abs(dy) < 200:
                c.x += 5 if dx > 0 else -5
                c.y += 3