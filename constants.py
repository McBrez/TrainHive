import pygame


def v2i(vector):
    return (int(vector.x), int(vector.y))


LINE_THICKNESS = 4
TRACK_COLOR = (255, 255, 255)
BASE_VELOCITY = 3
WAIT_CYCLES = 75
TRACK = [
    pygame.math.Vector2(int(100), int(0)),
    pygame.math.Vector2(int(150), int(0)),
    pygame.math.Vector2(int(200), int(0)),
    pygame.math.Vector2(int(150), int(0)),
    pygame.math.Vector2(int(100), int(0)),
    pygame.math.Vector2(int(250), int(0)),
    pygame.math.Vector2(int(100), int(0)),
]
TRACK_BEGIN = 0
TRACK_END = len(TRACK)
TEXTBOX_POS =  pygame.math.Vector2(int(50), int(50))