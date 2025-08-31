# components/enemy.py

import pygame
import math
import random
from components.projectile import Projectile as EnemyBullet


class Enemy(pygame.sprite.Sprite):
    """
    Represents an enemy character (a fox).
    """
    def __init__(self, x, y, all_sprites, enemy_bullets, speed=1):
        super().__init__()

        # Load and scale the fox image
        self.image = pygame.image.load("assets/images/Fox.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 50))
        self.rect = self.image.get_rect()
        self.speed = 1
        self.all_sprites = all_sprites
        self.enemy_bullets = enemy_bullets
        self.shoot_delay = 1000
        self.last_shot = pygame.time.get_ticks()
        self.pattern = 'star'


        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed = speed
        self.direction = 1  # 1 for right, -1 for left

    def update(self):
        """Move the enemy side to side."""
        self.rect.x += self.speed * self.direction

        # Reverse direction if it hits the screen edges
        if self.rect.right > 800 or self.rect.left < 0:
            self.direction *= -1

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            self.pattern = random.choice(['star', 'straight', 'spiral'])
            if self.pattern == 'star':
                # Star pattern
                for angle_deg in range(0, 360, 45):  # every 45 degrees
                    angle_rad = math.radians(angle_deg)
                    bullet = EnemyBullet(self.rect.centerx, self.rect.centery, angle_rad, 2)
                    self.all_sprites.add(bullet)
                    self.enemy_bullets.add(bullet)
            elif self.pattern == 'straight':
                # Shoots a burst of 3 bullets straight down
                for i in range(3):
                    bullet = EnemyBullet(self.rect.centerx, self.rect.bottom + i * 20, math.pi / 2, 2)
                    self.all_sprites.add(bullet)
                    self.enemy_bullets.add(bullet)
            elif self.pattern == 'spiral':
                print("spiral")
                bullets = random.randint(50, 100)
                amplitude = random.uniform(0.1, 0.5)
                frequency = random.uniform(0.1, 0.5)

                for i in range(bullets):
                    angle = i * (2 * math.pi / bullets) + pygame.time.get_ticks() * 0.002

                    x_offset = amplitude * math.sin(frequency * i + pygame.time.get_ticks() * 0.005) * 100
                    y_offset = amplitude * math.cos(frequency * i + pygame.time.get_ticks() * 0.005) * 100

                    # Launch angle is changed to be perpendicular to the radius
                    launch_angle = angle + math.pi / 2  

                    bullet = EnemyBullet(self.rect.centerx + x_offset,self.rect.centery + y_offset,launch_angle,1)
                    self.all_sprites.add(bullet)
                    self.enemy_bullets.add(bullet)


    def draw(self, screen):
        """Draw the enemy on the screen."""
        screen.blit(self.image, self.rect)