import pygame

import constants


class Track:
    def __init__(self, screen, startingPoint, vectorList):
        self.vectorList = vectorList
        self.startingPoint = startingPoint
        self.screen = screen

        # Create a list of list. It shall have as much entries as there are stations.
        self.parkedTrains = []
        self.parkedTrains.append(list())
        for _ in vectorList:
            self.parkedTrains.append(list())

    def draw(self):
        currentEndPos = self.startingPoint + self.vectorList[0]
        pygame.draw.line(
            self.screen,
            constants.TRACK_COLOR,
            self.startingPoint,
            currentEndPos,
            constants.LINE_THICKNESS,
        )
        pygame.draw.circle(
            self.screen, constants.TRACK_COLOR, constants.v2i(self.startingPoint), 10
        )
        pygame.draw.circle(
            self.screen, constants.TRACK_COLOR, constants.v2i(currentEndPos), 10
        )

        for i, vector in enumerate(self.vectorList):
            # Skip the first one, as it already has been drawn.
            if i == 0:
                continue

            nextPos = currentEndPos + vector
            pygame.draw.line(
                self.screen,
                constants.TRACK_COLOR,
                constants.v2i(currentEndPos),
                constants.v2i(nextPos),
                constants.LINE_THICKNESS,
            )
            pygame.draw.circle(
                self.screen, constants.TRACK_COLOR, constants.v2i(nextPos), 10
            )
            currentEndPos = nextPos

    def getPosOfIndex(self, trackIndex):
        currentPos = self.startingPoint
        for i in range(trackIndex):
            currentPos = currentPos + self.vectorList[i]

        return currentPos

    def getDirOfIndex(self, direction, trackIndex):
        if direction:
            return self.vectorList[trackIndex]
        else:
            return self.vectorList[trackIndex - 1] * -1

    def enterStation(self, train, trackIndex):
        self.parkedTrains[trackIndex].append(train)
        pos = self.getPosOfIndex(trackIndex)
        pos.y += (
            -1
            * (len(self.parkedTrains[trackIndex]) - 1)
            * constants.STATION_DISPLACEMENT
        )
        return pos

    def leaveStation(self, train, trackIndex):
        self.parkedTrains[trackIndex].remove(train)
        return self.getPosOfIndex(trackIndex)

    def waitAtStation(self, train, trackIndex):
        idx = self.parkedTrains[trackIndex].index(train)
        pos = self.getPosOfIndex(trackIndex)
        pos.y += -1 * idx * constants.STATION_DISPLACEMENT
        return pos
