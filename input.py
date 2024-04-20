import pygame


class Keyboard:
    def __init__(self):
        self.curr_keys = None
        self.prev_keys = None

    def process(self):
        self.prev_keys = self.curr_keys
        self.curr_keys = pygame.key.get_pressed()

    def key_down(self, key):
        return self.curr_keys[key] == True

    def key_pressed(self, key):
        return self.curr_keys[key] == True and self.prev_keys[key] == False

    def key_released(self, key):
        if self.curr_keys is None or self.prev_keys is None:
            return False
        return self.curr_keys[key] == False and self.prev_keys[key] == True


class InputStream:
    def __init__(self):
        self.keyboard = Keyboard()

    def process(self):
        self.keyboard.process()
