from settings import *
from enum import IntEnum, auto
from pyray import is_key_down, is_key_pressed, KeyboardKey

class Key(IntEnum):
    # Key bindings for WASD keys to support movement for 3 degrees of freedom (forward, backward, left, right)
    FORWARD = KeyboardKey.KEY_W
    BACK = KeyboardKey.KEY_S
    STRAFE_LEFT = KeyboardKey.KEY_A
    STRAFE_RIGHT = KeyboardKey.KEY_D
    MAP = KeyboardKey.KEY_M


class InputHandler:
    # Check current key inputs to call methods of camera movement in camera instance
    def __init__(self, engine):
        self.engine = engine
        self.camera = engine.camera

    def update(self):
        #
        if is_key_down(Key.FORWARD):
            self.camera.step_forward()
        #
        elif is_key_down(Key.BACK):
            self.camera.step_back()

        if is_key_down(Key.STRAFE_RIGHT):
            self.camera.step_right()
        #
        elif is_key_down(Key.STRAFE_LEFT):
            self.camera.step_left()

        if is_key_pressed(Key.MAP):
            self.engine.map_renderer.is_draw_map = not self.engine.map_renderer.is_draw_map
            self.engine.view_renderer.update_screen_tint()