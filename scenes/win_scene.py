# scenes/win_scene.py

import pygame
from .base_scene import BaseScene

class WinScene(BaseScene):
    """
    The scene that appears when the player wins the game.
    """
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/images/ganar.png").convert()
        self.image = pygame.transform.scale(self.image, (800, 600))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.switch_to_scene(None)
            

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, (0, 0))