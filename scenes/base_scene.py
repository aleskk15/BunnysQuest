# scenes/base_scene.py

class BaseScene:
    """
    A template for all scenes in the game.
    """
    def __init__(self):
        self.next_scene = self
        self.is_active = True

    def handle_events(self, events):
        """Handle all events coming from pygame."""
        raise NotImplementedError

    def update(self):
        """Update the scene's state."""
        raise NotImplementedError

    def draw(self, screen):
        """Draw the scene to the screen."""
        raise NotImplementedError

    def switch_to_scene(self, next_scene):
        """Set the next scene."""
        self.is_active = False
        self.next_scene = next_scene