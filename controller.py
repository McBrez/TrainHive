import pygame

import track
import train


class Controller:
    def __init__(self, screen):
        self.screen = screen
        self.trainList = pygame.sprite.Group()
        self.track = None

    def addTrain(self, track, trackIndex, goalIndex):
        newTrain = train.Train(track)
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
        if key[pygame.K_LEFT]:
            for train in self.trainList:
                train.kill()
        elif key[pygame.K_RIGHT]:
            for train in self.trainList:
                train.startMoving()

        # Call update for held instances
        self.trainList.update()

    def start(self):
        for train in self.trainList:
            train.startMoving()

    def draw(self):
        # Draw stuff.
        self.track.draw()
        self.trainList.draw(self.screen)