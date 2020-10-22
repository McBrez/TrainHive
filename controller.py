import pygame

import track
import train
import textbox
import constants

class Controller:
    def __init__(self, screen):
        self.screen = screen
        self.trainList = pygame.sprite.Group()
        self.track = None
        self.lastPressedKey = {}
        self.textbox = textbox.TextBox(constants.TEXTBOX_POS, self.screen)

    def addTrain(self, track, trackIndex, goalIndex, pathToImage, trainName, velocity = constants.BASE_VELOCITY):
        newTrain = train.Train(track, pathToImage, trainName, velocity)
        newTrain.place(trackIndex)
        newTrain.setGoal(goalIndex)
        newTrain.trains = self.trainList

        # notify all trains about the new train
        for knownTrain in self.trainList:
            knownTrain.onTrainAdded(newTrain)

        self.trainList.add(newTrain)

        return newTrain

    def addTrack(self, startPoint, trackList):
        self.track = track.Track(
            screen=self.screen, startingPoint=startPoint, vectorList=trackList
        )
        return self.track

    def update(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] == True and self.lastPressedKey[pygame.K_LEFT] == False:
            self.trainList.sprites()[0].prioritize()
            self.textbox.showText( self.trainList.sprites()[0].trainName + " wurde manuell priorisiert.")
        elif key[pygame.K_RIGHT] == True and self.lastPressedKey[pygame.K_RIGHT] == False:
            self.trainList.sprites()[1].prioritize()
            self.textbox.showText( self.trainList.sprites()[1].trainName + " wurde manuell priorisiert.")

        self.lastPressedKey[pygame.K_LEFT] = key[pygame.K_LEFT]
        self.lastPressedKey[pygame.K_RIGHT] = key[pygame.K_RIGHT]

        # Call update for held instances
        self.trainList.update()
        self.textbox.update()

    def start(self):
        for train in self.trainList:
            train.startMoving()

    def draw(self):
        # Draw stuff.
        self.track.draw()
        self.trainList.draw(self.screen)