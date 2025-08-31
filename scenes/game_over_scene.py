# scenes/game_over_scene.py

import pygame
from .base_scene import BaseScene

class GameOverScene(BaseScene):
    """
    The scene that appears when the player loses.
    """
    def __init__(self, image_path="assets/images/pierdesBosque.png"):
        super().__init__()
        self.image = pygame.image.load(image_path).convert()
        self.image = pygame.transform.scale(self.image, (800, 600))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.switch_to_scene(None)
           

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, (0, 0))