# scenes/intro_scene.py

import pygame
from .base_scene import BaseScene
from .menu_scene import MenuScene

class IntroScene(BaseScene):
    """
    The first scene that tells the story's opening.
    """
    def __init__(self):
        super().__init__()
        # Load images
        self.happy_bunny_img = pygame.image.load("assets/images/happyBunny.png").convert()
        self.kidnapping_img = pygame.image.load("assets/images/kidnapping.png").convert()

        # Scale images to fit the screen
        self.happy_bunny_img = pygame.transform.scale(self.happy_bunny_img, (800, 600))
        self.kidnapping_img = pygame.transform.scale(self.kidnapping_img, (800, 600))

        # Font and Text
        self.font = pygame.font.SysFont('Arial', 40)
        self.text = self.font.render("Oh no! The foxes took my sister...", True, (255, 255, 255))
        self.text_rect = self.text.get_rect(center=(400, 550)) # Position text at the bottom

        # Timer for the scene
        self.start_time = pygame.time.get_ticks()
        self.duration = 6000  # 6 seconds total, 3 for each image

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.switch_to_scene(None)
            # Allow skipping with a key press
            if event.type == pygame.KEYDOWN:
                self.switch_to_scene(MenuScene())

    def update(self):
        # Check if the scene duration has passed
        if pygame.time.get_ticks() - self.start_time > self.duration:
            self.switch_to_scene(MenuScene())

    def draw(self, screen):
        screen.fill((0, 0, 0))  # Black background
        
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.start_time

        if elapsed_time < self.duration / 2:
            # Show the first image
            screen.blit(self.happy_bunny_img, (0, 0))
        else:
            # Show the second image
            screen.blit(self.kidnapping_img, (0, 0))

        # Draw the text over the image
        screen.blit(self.text, self.text_rect)