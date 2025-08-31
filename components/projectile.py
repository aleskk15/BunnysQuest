# components/projectile.py

import pygame
import math

class Projectile(pygame.sprite.Sprite):
    """
    Represents a single projectile.
    """
    def __init__(self, start_x, start_y, angle, speed, color=(255, 0, 0)):
        super().__init__()

        # For now, a projectile is a small red square.
        self.image = pygame.Surface([10, 10], pygame.SRCALPHA)
        self.image.fill(color)

        self.rect = self.image.get_rect(center=(start_x, start_y))
        self.rect.x = start_x
        self.rect.y = start_y
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed

        self.speed = speed

    def update(self):
        """
        Move the projectile.
        """
        self.rect.x += self.dx
        self.rect.y += self.dy
        # The projectile will be removed if it goes off-screen.
        # This will be handled in the CombatScene.
        if (self.rect.right < 0 or self.rect.left > 800 or
        self.rect.bottom < 0 or self.rect.top > 600):
            self.kill()

    def draw(self, screen):
        """Draw the projectile on the screen."""
        screen.blit(self.image, self.rect)


class PlayerProjectile(Projectile):
    """
    Represents a projectile fired by the player.
    """
    def __init__(self, start_x, start_y):
        # Shoots upwards
        angle = -math.pi / 2
        speed = 10
        super().__init__(start_x, start_y, angle, speed, color=(0, 0, 255))
