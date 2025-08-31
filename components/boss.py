# components/boss.py

import pygame
import math
import random
from components.projectile import Projectile as EnemyBullet


class Boss(pygame.sprite.Sprite):
    """
    Represents the boss character.
    """
    def __init__(self, x, y, all_sprites, enemy_bullets, speed=1, health=20):
        super().__init__()

        # Load and scale the boss image
        self.image = pygame.image.load("assets/images/bossFox.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (120, 100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.all_sprites = all_sprites
        self.enemy_bullets = enemy_bullets
        self.shoot_delay = 500  # Shoots faster than regular enemies
        self.last_shot = pygame.time.get_ticks()

        self.speed = speed
        self.direction = 1  # 1 for right, -1 for left
        self.max_health = health
        self.health = health
        self.pattern = 'random'

    def damage(self, amount):
        """
        Reduce la salud del jefe.
        """
        self.health = max(0, self.health - amount)
        return self.health <= 0

    def update(self):
        """Move the boss side to side."""
        self.rect.x += self.speed * self.direction

        # Reverse direction if it hits the screen edges
        if self.rect.right > 800 or self.rect.left < 0:
            self.direction *= -1

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now

            self.pattern = random.choice(['burst', 'random'])

            # More complex shooting pattern
            if self.pattern == 'burst':
                # Shoots a burst of 5 bullets in a spread
                for angle_deg in range(-30, 31, 15):  # from -30 to +30 degrees
                    angle_rad = math.radians(angle_deg + 90)
                    bullet = EnemyBullet(self.rect.centerx, self.rect.bottom, angle_rad, 1.5)
                    self.all_sprites.add(bullet)
                    self.enemy_bullets.add(bullet)
            elif self.pattern == 'random':
                for i in range(4):
                    angle_deg = (now / 5 + i * 90) % 360
                    angle_rad = math.radians(angle_deg)
                    bullet = EnemyBullet(self.rect.centerx, self.rect.centery, angle_rad, 1)
                    self.all_sprites.add(bullet)
                    self.enemy_bullets.add(bullet)

            

    def draw(self, screen):
        """Draw the boss on the screen."""
        screen.blit(self.image, self.rect)
