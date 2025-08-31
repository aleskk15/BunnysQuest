# scenes/game_scene.py

import pygame
from .base_scene import BaseScene
from components.player import Player
from .combat_scene import CombatScene
from components.enemy import Enemy
from components.berry import Berry
from components.cave import Cave
from .boss_cinematic_scene import BossCinematicScene
import random

class GameScene(BaseScene):
    """
    The scene for the main exploration gameplay.
    """
    def __init__(self):
        super().__init__()
        self.all_sprites = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.player = Player(start_x=385, start_y=500, speed=2.5, health=10)
        self.all_sprites.add(self.player)

        # Define path boundaries
        self.path_width = 100
        self.path_x = (800 - self.path_width) / 2 # Assuming screen width is 800

        self.enemies = pygame.sprite.Group()
        self.set_enemies()

        self.berries = pygame.sprite.Group()
        self.set_berries()

        self.cave = Cave(x=325, y=-3000)
        self.all_sprites.add(self.cave)

        # Camera offset
        self.camera_y = 0
    
    def set_enemies(self):
        # Place enemies at various positions along the path
        for i in range(5):
            enemy = Enemy(x=375, y= -i * 600, all_sprites=self.all_sprites, enemy_bullets=self.enemy_bullets)
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)

    def set_berries(self):
        for i in range(20):
            # Place berries randomly within the path
            x = self.path_x + random.randint(0, self.path_width - 15)
            y = -i * 200
            berry = Berry(x, y)
            self.berries.add(berry)
            self.all_sprites.add(berry)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.switch_to_scene(None)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # For now, pressing ESC will quit the game.
                    # Later, this might go back to a menu.
                    self.switch_to_scene(None)

    def update(self):
        self.handle_player_movement()

        # Keep player on the path
        if self.player.rect.left < self.path_x:
            self.player.rect.left = self.path_x
        if self.player.rect.right > self.path_x + self.path_width:
            self.player.rect.right = self.path_x + self.path_width
        
        # Keep player on screen vertically
        if self.player.rect.top < 0:
            self.player.rect.top = 0
        if self.player.rect.bottom > 600:
            self.player.rect.bottom = 600

        # Check for collision
        for enemy in self.enemies:
            # Create a temporary rect for the enemy that is adjusted for the camera
            adjusted_enemy_rect = enemy.rect.move(0, self.camera_y)
            if self.player.rect.colliderect(adjusted_enemy_rect):
                print("Player collided with enemy! Starting combat...")
                self.enemies.remove(enemy)
                self.switch_to_scene(CombatScene(self, player=self.player))
                return
        
        # Check for berry collision
        for berry in self.berries:
            adjusted_berry_rect = berry.rect.move(0, self.camera_y)
            if self.player.rect.colliderect(adjusted_berry_rect):
                self.player.heal(berry.heal_amount)
                self.berries.remove(berry)
                self.all_sprites.remove(berry)
                print(f"Player collected a berry! Current health: {self.player.health}")

        # Check for cave collision
        adjusted_cave_rect = self.cave.rect.move(0, self.camera_y)
        if self.player.rect.colliderect(adjusted_cave_rect):
            self.switch_to_scene(BossCinematicScene(self))
            return


    def draw(self, screen):
        # Draw the background
        background = pygame.image.load("assets/images/Grass.png").convert()
        background = pygame.transform.scale(background, (800, 600))
        screen.blit(background, (0, 0))
        # Draw the path
        path_color = (139, 69, 19)  # Brown
        # We need to draw a much longer path to scroll through
        # Draw the path starting from off-screen to give the illusion of a continuous world
        path_length = 5000
        screen_height = 600
        start_y = self.camera_y - (path_length - screen_height)
        pygame.draw.rect(screen, path_color, [self.path_x, start_y, self.path_width, path_length])

        # Draw sprites with camera offset
        for enemy in self.enemies:
            screen.blit(enemy.image, (enemy.rect.x, enemy.rect.y + self.camera_y))
        
        for berry in self.berries:
            berry.draw(screen, self.camera_y)

        self.cave.draw(screen, self.camera_y)

        screen.blit(self.player.image, self.player.rect)

        # Draw the UI
        self.draw_ui(screen)

    def handle_player_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move(-self.player.speed, 0)
        if keys[pygame.K_RIGHT]:
            self.player.move(self.player.speed, 0)
        if keys[pygame.K_UP]:
            # If player is at the top of the screen, scroll the camera
            if self.player.rect.top < 100:
                self.camera_y += self.player.speed
                self.player.update()

            else:
                self.player.move(0, -self.player.speed)
        if keys[pygame.K_DOWN]:
            # If player is at the bottom of the screen, scroll the camera
            if self.player.rect.bottom > 500:
                self.camera_y -= self.player.speed
                self.player.update()
            else:
                self.player.move(0, self.player.speed)

    def draw_ui(self, screen):
        # Health bar
        health_bar_width = 200
        health_bar_height = 20
        health_bar_x = 10
        health_bar_y = 10

        current_health_width = (self.player.health / self.player.max_health) * health_bar_width
        pygame.draw.rect(screen, (255, 0, 0), [health_bar_x, health_bar_y, health_bar_width, health_bar_height])
        pygame.draw.rect(screen, (0, 255, 0), [health_bar_x, health_bar_y, current_health_width, health_bar_height])

        # Ememy defeat counter (placeholder)
        font = pygame.font.SysFont('Arial', 24)
        enemy_text = font.render(f"Enemies Left: {len(self.enemies)}", True, (0, 0, 0))
        screen.blit(enemy_text, (10, 40))