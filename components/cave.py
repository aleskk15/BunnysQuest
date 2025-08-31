# components/cave.py

import pygame

class Cave(pygame.sprite.Sprite):
    """
    Represents the cave entrance that leads to the boss.
    """
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((150, 150))
        self.image.fill((50, 50, 50))  # Dark grey color for the cave
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen, camera_y):
        """Draws the cave"""
        screen.blit(self.image, self.rect.move(0, camera_y))