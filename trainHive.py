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
    controller.addTrack(pygame.math.Vector2(int(100), int(height/2)), constants.TRACK)
    controller.addTrain(controller.track, constants.TRACK_BEGIN, constants.TRACK_END, "./res/train_red.png", "Zug Rot", 2)
    controller.addTrain(controller.track, constants.TRACK_END, constants.TRACK_BEGIN, "./res/train_green.png", "Zug Grün", 3)
    controller.start()



    # Worker loop
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # fill the screen
        screen.fill((0, 0, 0))

        # Do updates
        controller.update()

        # Draw stuff
        controller.draw()

        pygame.display.update()
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
