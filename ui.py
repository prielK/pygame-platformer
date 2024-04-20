import draw
import globalVars


class Button:
    def __init__(self, key, text, x, y):
        self.key = key
        self.text = text
        self.x = x
        self.y = y
        self.pressed = False
        self.on = False
        self.timer = 30

    def update(self, input_stream):
        self.pressed = input_stream.keyboard.key_pressed(self.key)
        if self.pressed:
            self.on = True
        if self.on:
            self.timer -= 1
            if self.timer <= 0:
                self.on = False
                self.timer = 30

    def draw(self, screen, alpha=255):
        if self.on:
            color = globalVars.GREEN
        else:
            color = globalVars.WHITE
        draw.draw_text(screen, self.text, color, self.x, self.y, alpha)
