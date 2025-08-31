# main.py - The entry point for Bunny's Quest

import pygame

from scenes.intro_scene import IntroScene

def main():
   """Main function to run the game."""
   pygame.init()

   screen_width = 800
   screen_height = 600
   screen = pygame.display.set_mode((screen_width, screen_height))
   pygame.display.set_caption("Bunny's Quest")

   # Scene management
   active_scene = IntroScene()

   while active_scene is not None:
       # Handle events
       active_scene.handle_events(pygame.event.get())

       # Update scene
       active_scene.update()

       # Draw to screen only if the scene is active
       if active_scene.is_active:
           active_scene.draw(screen)
           pygame.display.flip()

       # Switch to the next scene if needed
       if active_scene.next_scene is not active_scene:
           if active_scene.next_scene is not None:
               active_scene.next_scene.is_active = True
       active_scene = active_scene.next_scene

   pygame.quit()

if __name__ == '__main__':
    main()