import pygame

import constants


class Train(pygame.sprite.Sprite):
    def __init__(self, track):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("train.png")
        self.image = pygame.transform.scale(self.image, (int(50), int(25)))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.track = track
        self.moving = False
        self.direction = True
        self.heading = pygame.math.Vector2(1.0, 0.0)
        self.latestTrackIndex = 0
        self.state = 0
        self.goalIndex = -1
        self.waitCycles = 0
        self.trains = pygame.sprite.Group()

    def onTrainAdded(self, train):
        self.trains.add(train)

    def onTrainRemoved(self, train):
        self.trains.remove(train)

    def place(self, trackIndex):
        self.latestTrackIndex = trackIndex
        x, y = self.track.getPosOfIndex(trackIndex)
        self.rect.center = (x, y)

    def setGoal(self, goalIndex):
        self.goalIndex = goalIndex
        if self.goalIndex < self.latestTrackIndex:
            self.direction = False
        else:
            self.direction = True

    def startMoving(self):
        # Turn sprite
        directionVec = self.__getDirOfNextTrackIdx().normalize()
        angle = self.heading.angle_to(directionVec)

        self.image = pygame.transform.rotozoom(self.image, -1 * angle, 1)
        self.rect = self.image.get_rect()
        self.rect.center = self.track.getPosOfIndex(self.latestTrackIndex)

        self.heading = directionVec

        # Set moving state.
        self.moving = True

    def stopMoving(self):
        self.moving = False

    def setHeading(self, vector):
        pass

    def update(self):
        if self.state == 0:
            if self.moving:
                # Is train in vicinity of next station?
                vecNextStation = self.__getPosOfNextTrackIdx()
                vecTrain = pygame.math.Vector2(
                    int(self.rect.centerx), int(self.rect.centery)
                )
                diffVec = vecNextStation - vecTrain
                if diffVec.magnitude() < 2:
                    # Arrived at track index. Set the new trackIndex.
                    if self.direction:
                        self.latestTrackIndex = self.latestTrackIndex + 1
                    else:
                        self.latestTrackIndex = self.latestTrackIndex - 1

                    # Move the train directly on top of the station.
                    self.rect.centerx = vecNextStation.x
                    self.rect.centery = vecNextStation.y

                    # Stop moving.
                    self.stopMoving()

                    # Have we arrived at our goal?
                    if self.latestTrackIndex == self.goalIndex:
                        # We arrived at our goal. Remove the train.
                        self.kill()  # autsch
                    else:
                        # Wait at station.
                        self.state = 1
                else:
                    # Move train.
                    moveVector = self.heading * constants.BASE_VELOCITY
                    self.rect.center = self.rect.center + moveVector
                    print(self.rect.center)

        elif self.state == 1:
            self.waitCycles = self.waitCycles + 1
            if self.waitCycles > constants.WAIT_CYCLES:

                # Can i start moving again?
                # is a train in the next section?
                if self.nextSectionFree():
                    # start moving
                    self.state = 0
                    self.startMoving()
                    self.waitCycles = 0

    def __getPosOfNextTrackIdx(self):
        if self.direction:
            return self.track.getPosOfIndex(self.latestTrackIndex + 1)
        else:
            return self.track.getPosOfIndex(self.latestTrackIndex - 1)

    def __getDirOfNextTrackIdx(self):
        return self.track.getDirOfIndex(self.direction, self.latestTrackIndex)

    def nextSectionFree(self):
        # Determine the next trackIndex
        if self.direction:
            nextIndex = self.latestTrackIndex + 1
        else:
            nextIndex = self.latestTrackIndex - 1

        # Check if any trains have nextIndex set and move towards me.
        for otherTrain in self.trains:
            if (
                otherTrain.latestTrackIndex == nextIndex
                and otherTrain.direction != self.direction
            ):
                return False

        return True

    def debug(self):
        print("The center is: ", self.rect.center)
        print("The next trackIndex is: ", self.latestTrackIndex - 1)
        print(
            "Position of next track index: ",
            self.track.getPosOfIndex(self.latestTrackIndex - 1),
        )
        direction = self.track.getDirOfIndex(False, self.latestTrackIndex)
        vec = self.heading * direction.magnitude()
        print("direction vector: ", vec)
