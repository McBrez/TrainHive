import pygame


def v2i(vector):
    return (int(vector.x), int(vector.y))


ARG_CONV = "conventional"
ARG_NEW = "newConcept"
LINE_THICKNESS = 4
TRACK_COLOR = (255, 255, 255)
BASE_VELOCITY = 3
WAIT_CYCLES = 75
TRACK = [
    pygame.math.Vector2(int(150), int(0)),
    pygame.math.Vector2(int(225), int(0)),
    pygame.math.Vector2(int(300), int(0)),
    pygame.math.Vector2(int(225), int(0)),
    pygame.math.Vector2(int(125), int(0)),
    pygame.math.Vector2(int(375), int(0)),
    pygame.math.Vector2(int(150), int(0)),
]
TRACK_BEGIN = 0
TRACK_END = len(TRACK)
TEXTBOX_POS = pygame.math.Vector2(int(50), int(50))
MINIMUM_INTER_TRAIN_DISTANCE = 110

IMG_RAILJET = "./res/railjet.png"
IMG_BUS = "./res/bus.png"
IMG_CITYJET = "./res/cityjet.png"


REGIONAL_ZUG = 1
REGIONAL_EXPRESS = 2
RAIL_JET = 3