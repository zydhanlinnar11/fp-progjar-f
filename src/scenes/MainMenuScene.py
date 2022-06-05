from elements import Button
from scenes.BaseScene import BaseScene
import pygame


class MainMenuScene(BaseScene):
    def __init__(self, display_surface: 'pygame.Surface'):
        super().__init__(display_surface)
        self.__buttons: 'list[Button]' = []
        self.__init_all_buttons()

    def __init_all_buttons(self):
        (screen_width, screen_height) = self._display_surface.get_size()
        button_width = 200
        button_height = 60
        # Align center horizontally
        button_x_pos = (screen_width - button_width) / 2

        create_room_button = Button(
            self._display_surface, button_x_pos, 30, button_width, button_height, 'Create room')
        self.__buttons.append(create_room_button)

        join_room_button = Button(
            self._display_surface, button_x_pos, 110, button_width, button_height, 'Join room')
        self.__buttons.append(join_room_button)

        exit_game_button = Button(
            self._display_surface, button_x_pos, 190, button_width, button_height, 'Exit game')
        exit_game_button.set_click_handler(self.__handle_exit_game)
        self.__buttons.append(exit_game_button)

    def __handle_exit_game(self):
        pygame.quit()

    def handle_game_event(self, events: 'list[pygame.event.Event]'):
        for button in self.__buttons:
            button.handle_event(events)

    def handle_game_loop(self):
        pass

    def handle_game_render(self):
        for button in self.__buttons:
            button.draw()
        pygame.display.flip()
