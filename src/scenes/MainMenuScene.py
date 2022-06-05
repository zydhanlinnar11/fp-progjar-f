from scenes.BaseScene import BaseScene
import pygame


class MainMenuScene(BaseScene):
    def __init__(self, display_surface: 'pygame.Surface'):
        super().__init__(display_surface)

    def handle_game_event(self):
        pass

    def handle_game_loop(self):
        pass

    def handle_game_render(self):
        pygame.draw.rect(self._display_surface, (255, 255, 0),
                         pygame.Rect(30, 30, 60, 60),  2)
        pygame.display.flip()

    def get_next_scene(self) -> 'BaseScene':
        return self
