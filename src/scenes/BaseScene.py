import pygame
from abc import ABC, abstractmethod


class BaseScene(ABC):
    def __init__(self, display_surface: 'pygame.Surface'):
        self._display_surface = display_surface
        self._scene = self

    @abstractmethod
    def handle_game_event(self):
        pass

    @abstractmethod
    def handle_game_loop(self):
        pass

    @abstractmethod
    def handle_game_render(self):
        pass

    def get_next_scene(self) -> 'BaseScene':
        return self._scene
