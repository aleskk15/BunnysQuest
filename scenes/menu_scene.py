# scenes/menu_scene.py

import pygame
from .base_scene import BaseScene
from .game_scene import GameScene

class MenuScene(BaseScene):
    """
    The scene for the main menu.
    """
    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont('Arial', 56)
        self.text = self.font.render("Bunny's Quest", True, (255, 255, 255))
        self.text_rect = self.text.get_rect(center=(400, 250))

        self.sub_font = pygame.font.SysFont('Arial', 32)
        self.sub_text = self.sub_font.render("Press SPACE to Start", True, (200, 200, 200))
        self.sub_text_rect = self.sub_text.get_rect(center=(400, 350))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                # To exit the game, we set the next_scene to None
                self.switch_to_scene(None)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("Switching to game scene...")
                    self.switch_to_scene(GameScene())

    def update(self):
        # The menu scene doesn't have much state to update
        pass

    def draw(self, screen):
        screen.fill((0, 0, 0))  # Black background
        screen.blit(self.text, self.text_rect)
        screen.blit(self.sub_text, self.sub_text_rect)