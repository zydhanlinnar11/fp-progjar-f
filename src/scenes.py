import string
from typing import Optional
import pygame
from abc import ABC, abstractmethod
from PodSixNet.Connection import ConnectionListener
import pygame
from elements import Button


class BaseScene(ABC):
    def __init__(self, display_surface: 'pygame.Surface', network_client: 'ConnectionListener'):
        self._display_surface = display_surface
        self._network_client = network_client
        self._scene = self

    @abstractmethod
    def handle_game_event(self, events: 'list[pygame.event.Event]'):
        pass

    @abstractmethod
    def handle_game_loop(self):
        pass

    @abstractmethod
    def handle_game_render(self):
        pass

    @abstractmethod
    def handle_network(self, data):
        pass

    def get_next_scene(self) -> 'BaseScene':
        return self._scene


class MainMenuScene(BaseScene):
    def __init__(self, display_surface: 'pygame.Surface', network_client: 'ConnectionListener'):
        super().__init__(display_surface, network_client)
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
        create_room_button.set_click_handler(self.__handle_create_room)

        join_room_button = Button(
            self._display_surface, button_x_pos, 110, button_width, button_height, 'Join room')
        join_room_button.set_click_handler(self.__handle_join_room)
        self.__buttons.append(join_room_button)

        exit_game_button = Button(
            self._display_surface, button_x_pos, 190, button_width, button_height, 'Exit game')
        exit_game_button.set_click_handler(self.__handle_exit_game)
        self.__buttons.append(exit_game_button)

    def __handle_exit_game(self):
        pygame.quit()

    def __handle_create_room(self):
        self._scene = CreateRoomScene(
            self._display_surface, self._network_client)

    def __handle_join_room(self):
        self._scene = JoinRoomScene(
            self._display_surface, self._network_client)

    def handle_game_event(self, events: 'list[pygame.event.Event]'):
        for button in self.__buttons:
            button.handle_event(events)

    def handle_game_loop(self):
        pass

    def handle_game_render(self):
        for button in self.__buttons:
            button.draw()
        pygame.display.flip()

    def handle_network(self, data):
        pass


class CreateRoomScene(BaseScene):
    def __init__(self, display_surface: 'pygame.Surface', network_client: 'ConnectionListener'):
        super().__init__(display_surface, network_client)
        network_client.Send({'action': 'createroom'})
        self.__buttons: 'list[Button]' = []
        self.__room_id: 'Optional[str]' = None
        self.__font = pygame.font.SysFont('Corbel', 24)
        self.__font_color = (255, 255, 255)
        self.__screen_width = self._display_surface.get_size()[0]
        self.__screen_height = self._display_surface.get_size()[1]
        self.__init_all_buttons()

    def handle_network(self, data: 'dict'):
        if data.get('action') == 'createroomresponse':
            self.__handle_create_room_response(data)
        elif data.get('action') == 'playgame':
            self._scene = InGameScene(
                self._display_surface, self._network_client, self.__room_id)

    def __handle_create_room_response(self, data: 'dict'):
        self.__room_id = data.get('roomid')

    def __init_all_buttons(self):
        button_width = 200
        button_height = 60
        # Align center horizontally
        button_x_pos = (self.__screen_width - button_width) / 2

        back_button = Button(
            self._display_surface, button_x_pos, 190, button_width, button_height, 'Back')
        back_button.set_click_handler(self.__handle_back)
        self.__buttons.append(back_button)

    def __handle_back(self):
        self._network_client.Send(
            {'action': 'deleteroom', 'room_id': self.__room_id})
        self._scene = MainMenuScene(
            self._display_surface, self._network_client)

    def handle_game_event(self, events: 'list[pygame.event.Event]'):
        for button in self.__buttons:
            button.handle_event(events)

    def handle_game_loop(self):
        pass

    def handle_game_render(self):
        for button in self.__buttons:
            button.draw()
        title = self.__font.render('Create room', True, self.__font_color)
        titleRect = title.get_rect()
        titleRect.center = (self.__screen_width / 2, 40)
        self._display_surface.blit(title, titleRect)

        roomId = self.__font.render(
            f'Room ID: {self.__room_id}', True, self.__font_color)
        roomIdRect = roomId.get_rect()
        roomIdRect.center = (self.__screen_width / 2, 130)
        self._display_surface.blit(roomId, roomIdRect)
        pygame.display.flip()


class JoinRoomScene(BaseScene):
    def __init__(self, display_surface: 'pygame.Surface', network_client: 'ConnectionListener'):
        super().__init__(display_surface, network_client)
        self.__buttons: 'list[Button]' = []
        self.__room_id: 'Optional[str]' = None
        self.__font = pygame.font.SysFont('Corbel', 24)
        self.__font_color = (255, 255, 255)
        self.__screen_width = self._display_surface.get_size()[0]
        self.__screen_height = self._display_surface.get_size()[1]
        self.__button_width = 200
        self.__button_height = 60
        self.__room_id: 'str' = ''
        self.__error_text: 'str' = ''
        self.__init_all_buttons()

    def handle_network(self, data: 'dict'):
        if data.get('action') == 'joinroomerror':
            self.__error_text = data.get('message')
        elif data.get('action') == 'playgame':
            self._scene = InGameScene(
                self._display_surface, self._network_client, self.__room_id)

    def __init_all_buttons(self):
        # Align center horizontally
        button_x_pos = (self.__screen_width - self.__button_width) / 2

        join_button = Button(
            self._display_surface, button_x_pos, 190, self.__button_width, self.__button_height, 'Join')
        join_button.set_click_handler(self.__handle_join)
        self.__buttons.append(join_button)

        back_button = Button(
            self._display_surface, button_x_pos, 270, self.__button_width, self.__button_height, 'Back')
        back_button.set_click_handler(self.__handle_back)
        self.__buttons.append(back_button)

    def __handle_join(self):
        if len(self.__room_id) != 6:
            self.__error_text = 'Invalid room code'
            return
        self._network_client.Send(
            {'action': 'joinroom', 'room_id': self.__room_id})

    def __handle_back(self):
        self._network_client.Send(
            {'action': 'deleteroom', 'room_id': self.__room_id})
        self._scene = MainMenuScene(
            self._display_surface, self._network_client)

    def handle_game_event(self, events: 'list[pygame.event.Event]'):
        for button in self.__buttons:
            button.handle_event(events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.__handle_keyboard_input(event)

    def __handle_keyboard_input(self, event: 'pygame.event.Event'):
        unicode: 'str' = event.unicode
        if unicode not in string.ascii_letters and unicode not in string.digits and unicode != '\x08':
            return
        if unicode == '\x08' and len(self.__room_id) == 0:
            return
        if unicode == '\x08':
            self.__room_id = self.__room_id[:-1]
            return
        if len(self.__room_id) == 6:
            return
        self.__room_id += unicode
        self.__room_id = self.__room_id.upper()

    def handle_game_loop(self):
        pass

    def handle_game_render(self):
        for button in self.__buttons:
            button.draw()
        title = self.__font.render('Join room', True, self.__font_color)
        titleRect = title.get_rect()
        titleRect.center = (self.__screen_width / 2, 40)
        self._display_surface.blit(title, titleRect)

        errorText = self.__font.render(self.__error_text, True, (255, 0, 0))
        errorTextRect = errorText.get_rect()
        errorTextRect.center = (self.__screen_width / 2, 70)
        self._display_surface.blit(errorText, errorTextRect)

        input_box = Button(
            self._display_surface, (self.__screen_width - self.__button_width) / 2, 110, self.__button_width, self.__button_height, self.__room_id if self.__room_id else 'Enter Room ID...')
        input_box.draw()

        pygame.display.flip()


class InGameScene(BaseScene):
    def __init__(self, display_surface: 'pygame.Surface', network_client: 'ConnectionListener', room_id: 'str'):
        super().__init__(display_surface, network_client)
        self.__buttons: 'list[Button]' = []
        self.__room_id: 'Optional[str]' = None
        self.__font = pygame.font.SysFont('Corbel', 24)
        self.__font_color = (255, 255, 255)
        self.__screen_width = self._display_surface.get_size()[0]
        self.__screen_height = self._display_surface.get_size()[1]
        self.__button_width = 200
        self.__button_height = 60
        self.__room_id: 'str' = room_id
        self.__error_text: 'str' = ''
        self.__init_all_buttons()

    def handle_network(self, data: 'dict'):
        if data.get('action') == 'joinroomerror':
            self.__error_text = data.get('message')

    def __init_all_buttons(self):
        # Align center horizontally
        button_x_pos = (self.__screen_width - self.__button_width) / 2

        join_button = Button(
            self._display_surface, button_x_pos, 190, self.__button_width, self.__button_height, 'Join')
        join_button.set_click_handler(self.__handle_join)
        self.__buttons.append(join_button)

        back_button = Button(
            self._display_surface, button_x_pos, 270, self.__button_width, self.__button_height, 'Back')
        back_button.set_click_handler(self.__handle_back)
        self.__buttons.append(back_button)

    def __handle_join(self):
        if len(self.__room_id) != 6:
            self.__error_text = 'Invalid room code'
            return
        self._network_client.Send(
            {'action': 'joinroom', 'room_id': self.__room_id})

    def __handle_back(self):
        self._network_client.Send(
            {'action': 'deleteroom', 'room_id': self.__room_id})
        self._scene = MainMenuScene(
            self._display_surface, self._network_client)

    def handle_game_event(self, events: 'list[pygame.event.Event]'):
        for button in self.__buttons:
            button.handle_event(events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.__handle_keyboard_input(event)

    def __handle_keyboard_input(self, event: 'pygame.event.Event'):
        unicode: 'str' = event.unicode
        if unicode not in string.ascii_letters and unicode not in string.digits and unicode != '\x08':
            return
        if unicode == '\x08' and len(self.__room_id) == 0:
            return
        if unicode == '\x08':
            self.__room_id = self.__room_id[:-1]
            return
        if len(self.__room_id) == 6:
            return
        self.__room_id += unicode
        self.__room_id = self.__room_id.upper()

    def handle_game_loop(self):
        pass

    def handle_game_render(self):
        for button in self.__buttons:
            button.draw()
        title = self.__font.render('In Game', True, self.__font_color)
        titleRect = title.get_rect()
        titleRect.center = (self.__screen_width / 2, 40)
        self._display_surface.blit(title, titleRect)

        errorText = self.__font.render(self.__error_text, True, (255, 0, 0))
        errorTextRect = errorText.get_rect()
        errorTextRect.center = (self.__screen_width / 2, 70)
        self._display_surface.blit(errorText, errorTextRect)

        input_box = Button(
            self._display_surface, (self.__screen_width - self.__button_width) / 2, 110, self.__button_width, self.__button_height, self.__room_id if self.__room_id else 'Enter Room ID...')
        input_box.draw()

        pygame.display.flip()
