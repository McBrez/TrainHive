import time
import sys

import pygame

import track
import train
import controller
import constants

if __name__ == "__main__":
    # Get command line argument
    simulationType = sys.argv[1]

    # Init pygame
    pygame.init()
    width = 1800
    height = 720
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("TrainHive Simulation")
    clock = pygame.time.Clock()

    # Init Controller
    controller = controller.Controller(screen)
    controller.addTrack(pygame.math.Vector2(int(100), int(height / 2)), constants.TRACK)

    if simulationType == constants.ARG_CONV:
        print("Starte konventionelle Simulation")
        controller.addTrain(
            controller.track,
            constants.TRACK_BEGIN,
            constants.TRACK_END,
            "./res/train_red.png",
            "Zug Rot",
            2,
        )
        controller.addTrain(
            controller.track,
            constants.TRACK_END,
            constants.TRACK_BEGIN,
            "./res/train_green.png",
            "Zug Grün",
            3,
        )
        controller.addTrain(
            controller.track,
            constants.TRACK_END - 1,
            constants.TRACK_BEGIN,
            "./res/train_blue.png",
            "Zug Blau",
            1,
        )
    elif simulationType == constants.ARG_NEW:
        controller.addNewTrain(
            controller.track,
            constants.TRACK_BEGIN,
            constants.TRACK_END,
            constants.IMG_CITYJET,
            "CityJet",
            constants.REGIONAL_EXPRESS,
            2,
        )
        controller.addNewTrain(
            controller.track,
            constants.TRACK_END,
            constants.TRACK_BEGIN,
            constants.IMG_RAILJET,
            "RailJet",
            constants.RAIL_JET,
            3,
        )
        controller.addNewTrain(
            controller.track,
            constants.TRACK_END - 1,
            constants.TRACK_BEGIN,
            constants.IMG_BUS,
            "Regional Zug",
            constants.REGIONAL_ZUG,
            1,
        )
        print("Starte 'new concept' Simulation")
    else:
        quit()

    controller.start()

    # Worker loop
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # fill the screen
        screen.fill((230, 230, 230))

        # Do updates
        controller.update()

        # Draw stuff
        controller.draw()

        pygame.display.update()
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
