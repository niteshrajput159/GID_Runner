import pygame
import random
import assets  

lane_positions = [150, 250, 350]
base_speed = 8

class ObstacleManager:
    def __init__(self):
        self.low_ob = assets.get("low_obstacle")
        self.large_ob = assets.get("large_obstacle")
        self.small_ob_frames = assets.get("small_obstacle_frames")

        self.obs_frm_index = 0
        self.obs_frm_timer = 0
        self.obstacles = []

    def spawn(self):
        available_lanes = [0, 1, 2]

        if random.random() < 0.3:
            blocked = random.sample(available_lanes, 2)
            for lane in blocked:
                if self.is_lane_free(lane):
                    self.add_obstacle(lane)
        else:
            lane = random.choice(available_lanes)
            if self.is_lane_free(lane):
                self.add_obstacle(lane)

    def is_lane_free(self, lane):
        lane_x = lane_positions[lane]
        for obs in self.obstacles:
            if abs(obs["rect"].centerx - lane_x) < 60 and obs["rect"].bottom > -300:
                return False
        return True

    def add_obstacle(self, lane):
        lane_x = lane_positions[lane]
        choice = random.choice(["small", "low", "train"])

        if choice == "small":
            rect = pygame.Rect(lane_x - 25, -100, 100, 100)
        elif choice == "train":
            rect = pygame.Rect(lane_x - 50, -600, 100, 600)
        else:
            rect = pygame.Rect(lane_x - 25, -40, 50, 40)

        self.obstacles.append({"rect": rect, "type": choice})

    def move(self, speed=None):
        if speed is None:
            speed = self.base_speed
        for ob in self.obstacles:
            ob["rect"].y += speed
        self.obstacles = [o for o in self.obstacles if o["rect"].top < 700 + 1000]

    def draw(self, screen):
        self.obs_frm_timer += 1
        if self.obs_frm_timer % 5 == 0:
            self.obs_frm_index = (self.obs_frm_index + 1) % len(self.small_ob_frames)

        for obs in self.obstacles:
            if obs["type"] == "small":
                screen.blit(self.small_ob_frames[self.obs_frm_index], obs["rect"].topleft)
            elif obs["type"] == "train":
                screen.blit(self.large_ob, obs["rect"].topleft)
            else:
                screen.blit(self.low_ob, obs["rect"].topleft)

    def check_collision(self, player):
        for obs in self.obstacles:
            if player.rect.colliderect(obs["rect"]):
                if obs["type"] == "small" and player.jumping:
                    continue
                if obs["type"] == "low" and player.sliding:
                    continue
                return True
        return False