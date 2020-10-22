import pygame


def v2i(vector):
    return (int(vector.x), int(vector.y))


LINE_THICKNESS = 4
TRACK_COLOR = (255, 255, 255)
BASE_VELOCITY = 3
WAIT_CYCLES = 50
TRACK = [
    pygame.math.Vector2(int(100), int(0)),
    pygame.math.Vector2(int(200), int(100)),
    pygame.math.Vector2(int(400), int(0)),
    pygame.math.Vector2(int(200), int(200)),
    pygame.math.Vector2(int(100), int(100)),
    pygame.math.Vector2(int(100), int(200)),
]