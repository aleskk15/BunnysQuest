# components/player.py

import pygame
import random
from components.projectile import PlayerProjectile
class Player(pygame.sprite.Sprite):
    """
    Represents the player character (the bunny).
    """
    def __init__(self, start_x, start_y, speed=1, health=10):
        super().__init__()

        # Load the player image (Bunny)
        self.image = pygame.image.load("assets/images/Bunny.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 50))
        self.rect = self.image.get_rect()
        self.max_health = health
        self.health = health 
        self.rect.x = start_x
        self.rect.y = start_y

        self.speed = speed

        self.sprites = [
            pygame.transform.scale(pygame.image.load("assets/images/Bunny.png").convert_alpha(),(40, 50)),
            pygame.transform.scale(pygame.image.load("assets/images/Bunny2.png").convert_alpha(),(40, 50)),
            pygame.transform.scale(pygame.image.load("assets/images/Bunny3.png").convert_alpha(),(40, 50))
            ]
        self.current_sprite = 0
        self.projectiles = pygame.sprite.Group()
        self.last_shot = pygame.time.get_ticks()
        self.fire_rate = 250


    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.fire_rate:
            self.last_shot = now
            projectile = PlayerProjectile(self.rect.centerx, self.rect.top)
            self.projectiles.add(projectile)
            return projectile
        return None

    def damage(self, amount):
        """
        Damage the player by a given amount.
        """
        self.health = max(0, self.health - amount)
        return self.health <= 0  #  Return True if the player is dead

    def heal(self, amount):
        """
        Heal the player by a given amount.
        """
        self.health = min(self.max_health, self.health + amount)

    def update(self):
        """
        Updating the player sprites
        """
        self.current_sprite += 1
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        
    def move(self, dx, dy):
        """
        Move the player by a given amount.
        """
        self.rect.x += dx
        self.update()
        self.rect.y += dy
        self.update()

    def draw(self, screen):
        """Draw the player on the screen."""
        screen.blit(self.image, self.rect)
