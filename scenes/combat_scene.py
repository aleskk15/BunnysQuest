# scenes/combat_scene.py

import pygame
import random
import math
from .base_scene import BaseScene
from components.player import Player
from components.enemy import Enemy
from components.projectile import Projectile, PlayerProjectile
from components.boss import Boss
from .win_scene import WinScene
from .game_over_scene import GameOverScene


class CombatScene(BaseScene):
    """
    The scene for the bullet-hell combat.
    """
    def __init__(self, previous_scene, player, is_boss_fight=False):
        super().__init__()
        self.previous_scene = previous_scene
        self.is_active = True
        self.is_boss_fight = is_boss_fight
        
        # Create the player, enemy, and projectile groups
        self.all_sprites = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.player = player
        self.player_projectiles = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        if self.is_boss_fight:
            self.enemy = Boss(x=340, y=50, all_sprites=self.all_sprites, enemy_bullets=self.enemy_bullets)
        else:
            self.enemy = Enemy(x=375, y=50, all_sprites=self.all_sprites, enemy_bullets=self.enemy_bullets, speed=1)
        
        self.all_sprites.add(self.enemy)
        self.max_health = player.max_health

        # Combat parameters
        self.fire_rate = 250  # Milliseconds (Faster firing)
        self.last_shot = pygame.time.get_ticks()

        
        # Timer (only for non-boss fights)
        self.combat_duration = 10000 if self.is_boss_fight else 5000  # 10s for boss, 5s for normal
        self.start_time = pygame.time.get_ticks()
        
        # Define the player's movement area
        self.player_bounds = pygame.Rect(200, 400, 400, 150)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.switch_to_scene(None)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.switch_to_scene(self.previous_scene)

    def update(self):
        if not self.is_active:
            return

        # Check for win condition
        if self.is_boss_fight:
            if self.enemy.health <= 0:
                self.is_active = False
                self.switch_to_scene(WinScene())
                return
        elif pygame.time.get_ticks() - self.start_time > self.combat_duration:
            self.is_active = False
            self.switch_to_scene(self.previous_scene)
            return

        # Update player and projectiles
        self.handle_player_movement()
        self.enemy.update()
        self.enemy_bullets.update()
        self.player_projectiles.update()

        # Keep player within the bounds
        self.player.rect.clamp_ip(self.player_bounds)

        # Time to fire a new projectile?
        self.enemy.shoot()

        # Check for collisions
        # Check for collisions between player and enemy bullets
        if pygame.sprite.spritecollide(self.player, self.enemy_bullets, True):
            print("Player Hit!")
            if self.player.damage(1):
                print("You lose!")
                self.is_active = False
                if self.is_boss_fight:
                    self.switch_to_scene(GameOverScene(image_path="assets/images/perderCueva.png"))
                else:
                    self.switch_to_scene(GameOverScene(image_path="assets/images/pierdesBosque.png"))
                return
        
        # Check for collisions between player projectiles and enemy
        if self.is_boss_fight:
            if pygame.sprite.spritecollide(self.enemy, self.player_projectiles, True):
                if self.enemy.damage(1):
                    self.is_active = False
                    self.switch_to_scene(WinScene())
                    return

    def handle_player_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move(-self.player.speed, 0)
        if keys[pygame.K_RIGHT]:
            self.player.move(self.player.speed, 0)
        if keys[pygame.K_UP]:
            self.player.move(0, -self.player.speed)
        if keys[pygame.K_DOWN]:
            self.player.move(0, self.player.speed)
        if keys[pygame.K_SPACE]:
            if self.is_boss_fight:
                new_projectile = self.player.shoot()
                if new_projectile:
                    self.all_sprites.add(new_projectile)
                    self.player_projectiles.add(new_projectile)

    def draw(self, screen):
        screen.fill((0, 0, 0))  # Black background
        
        # Draw the bounding box for debugging
        pygame.draw.rect(screen, (0, 255, 0), self.player_bounds, 2)

        self.player.draw(screen)
        self.enemy.draw(screen)
        self.enemy_bullets.draw(screen)
        self.player_projectiles.draw(screen)
        self.draw_combat_ui(screen)

    def draw_combat_ui(self, screen):
        # Health bar
        health_bar_width = 200
        health_bar_height = 20
        health_bar_x = 10
        health_bar_y = 10
        current_health_width = (self.player.health / self.max_health) * health_bar_width

        pygame.draw.rect(screen, (255, 0, 0), [health_bar_x, health_bar_y, health_bar_width, health_bar_height])
        pygame.draw.rect(screen, (0, 255, 0), [health_bar_x, health_bar_y, current_health_width, health_bar_height])

        font = pygame.font.SysFont('Arial', 24)
        if self.is_boss_fight:
            # Boss health bar
            boss_health_bar_width = 400
            boss_health_bar_height = 20
            boss_health_bar_x = (screen.get_width() - boss_health_bar_width) / 2 + 100
            boss_health_bar_y = 10
            boss_current_health_width = (self.enemy.health / self.enemy.max_health) * boss_health_bar_width
            
            pygame.draw.rect(screen, (255, 0, 0), [boss_health_bar_x, boss_health_bar_y, boss_health_bar_width, boss_health_bar_height])
            pygame.draw.rect(screen, (0, 255, 0), [boss_health_bar_x, boss_health_bar_y, boss_current_health_width, boss_health_bar_height])

            font = pygame.font.SysFont('Arial', 24)
            enemy_text = font.render("Defeat the boss with SPACE!!", True, (255, 255, 255)
            )
            screen.blit(enemy_text, (40, 560))

        # Timer
        if not self.is_boss_fight:
            time_left = (self.combat_duration - (pygame.time.get_ticks() - self.start_time)) / 1000
            timer_text = font.render(f"Survive: {int(time_left)}s", True, (255, 255, 255))
            screen.blit(timer_text, (screen.get_width() - 150, 10))