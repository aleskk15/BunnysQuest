# components/berry.py

import pygame

class Berry(pygame.sprite.Sprite):
    """
    Represents a berry that the player can collect to regain health.
    """
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/images/Berry.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.heal_amount = 2

    def draw(self, screen, camera_y):
        """Draw the berry on the screen, adjusted for the camera."""
        screen.blit(self.image, self.rect.move(0, camera_y))