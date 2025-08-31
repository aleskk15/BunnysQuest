# scenes/boss_cinematic_scene.py

import pygame
from .base_scene import BaseScene
from .combat_scene import CombatScene
from components.boss import Boss

class BossCinematicScene(BaseScene):
    """
    A cinematic scene that plays before the boss fight.
    """
    def __init__(self, previous_scene):
        super().__init__()
        self.previous_scene = previous_scene
        self.image = pygame.image.load("assets/images/bossFight.png").convert()
        self.image = pygame.transform.scale(self.image, (800, 600))
        
        # Timer for the scene
        self.start_time = pygame.time.get_ticks()
        self.duration = 3000  # 3 seconds

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.switch_to_scene(None)
            # Allow skipping with a key press
            if event.type == pygame.KEYDOWN:
                self.start_boss_fight()

    def update(self):
        # Check if the scene duration has passed
        if pygame.time.get_ticks() - self.start_time > self.duration:
            self.start_boss_fight()

    def draw(self, screen):
        screen.blit(self.image, (0, 0))

    def start_boss_fight(self):
        self.switch_to_scene(CombatScene(self.previous_scene, player=self.previous_scene.player, is_boss_fight=True))