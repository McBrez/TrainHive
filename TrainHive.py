import pygame

import time

import track
import train
import controller
import constants

if __name__ == "__main__":
    # Init pygame
    pygame.init()
    width = 1280
    height = 720
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("TrainHive Simulation")
    clock = pygame.time.Clock()

    # Init Controller
    controller = controller.Controller(screen)
    controller.addTrack(pygame.math.Vector2(int(100), int(50)), constants.TRACK)

    # controller.addTrain(controller.track, 0, 6)
    controller.addTrain(controller.track, 6, 0)

    controller.start()
    for someTrain in controller.trainList:
        someTrain.debug()
    # Worker loop
    done = False
    firstIteration = True
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # Do updates
        controller.update()

        # fill the screen
        screen.fill((0, 0, 0))

        # Draw stuff
        controller.draw()

        pygame.display.flip()

        if firstIteration:
            firstIteration = False
        else:
            clock.tick(60)

    pygame.quit()
