import pygame
import assets
lane_positions = [150, 250, 350]
GROUND_Y = 700 - 150
gravity = 1

class Player:
    def __init__(self):
        self.runner_frames = assets.get("runner_frames")

        self.lane = 1
        self.target_lane = 1
        self.rect = pygame.Rect(lane_positions[self.lane] - 25, GROUND_Y, 50, 50)

        self.jumping = False
        self.sliding = False
        self.slide_timer = 0
        self.jump_vel = 0
        self.curr_frame = 0
        self.frame_timer = 0

        self.last_move_time = 0
        self.move_cooldown = 200
        self.move_speed = 15

    def move(self, keys):
        now = pygame.time.get_ticks()

        if now - self.last_move_time > self.move_cooldown:
            if keys[pygame.K_UP]:
                assets.ASSETS["sounds"]["jump"].play()
            if keys[pygame.K_DOWN]:
                assets.ASSETS["sounds"]["slide"].play()
            if keys[pygame.K_LEFT]:
                if self.lane > 0:
                    self.target_lane = self.lane - 1
                    self.last_move_time = now
            elif keys[pygame.K_RIGHT]:
                if self.lane < 2:
                    self.target_lane = self.lane + 1
                    self.last_move_time = now

        target_x = lane_positions[self.target_lane] - 25
        if abs(self.rect.x - target_x) > 3:
            if self.rect.x < target_x:
                self.rect.x += self.move_speed
                if self.rect.x > target_x:
                    self.rect.x = target_x
            elif self.rect.x > target_x:
                self.rect.x -= self.move_speed
                if self.rect.x < target_x:
                    self.rect.x = target_x
        else:
            self.lane = self.target_lane

        if not self.jumping and not self.sliding and keys[pygame.K_UP]:
            self.jumping = True
            self.jump_vel = -18

        if not self.jumping and not self.sliding and keys[pygame.K_DOWN]:
            self.sliding = True
            self.slide_timer = 35
            self.rect.y = GROUND_Y + 20

    def update(self):
        if self.jumping:
            self.rect.y += self.jump_vel
            self.jump_vel += gravity
            if self.rect.y >= GROUND_Y:
                self.rect.y = GROUND_Y
                self.jumping = False

        if self.sliding:
            self.slide_timer -= 1
            if self.slide_timer <= 0:
                self.sliding = False
                self.rect.height = 50
                self.rect.y = GROUND_Y

    def draw(self, screen):
        self.frame_timer += 1
        if self.frame_timer % 5 == 0:
            self.curr_frame = (self.curr_frame + 1) % len(self.runner_frames)

        sprite = self.runner_frames[self.curr_frame]
        if self.jumping:
            sprite = pygame.transform.scale(sprite, (50, 50))
        elif self.sliding:
            sprite = pygame.transform.scale(sprite, (50, 30))

        screen.blit(sprite, self.rect.topleft)