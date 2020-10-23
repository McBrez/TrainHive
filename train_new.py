import pygame

import constants
import train
import textbox


class TrainNew(train.Train):
    def __init__(
        self,
        track,
        pathToImage,
        trainName,
        trainId,
        trainType,
        velocity=constants.BASE_VELOCITY,
        screen=None,
    ):
        super().__init__(track, pathToImage, trainName, velocity)

        self.screen = screen
        self.trainInfoBox = textbox.TextBox(
            pygame.math.Vector2(0, 0), self.screen, 30, 25, color=(0, 0, 0)
        )

        self.trainNameBox = textbox.TextBox(
            pygame.math.Vector2(0, 0), self.screen, 16, 0, color=(0, 0, 0)
        )
        self.trainNameBox.showText(self.trainName)
        self.trainId = trainId
        self.trainType = trainType

    def update(self):
        # Update position of info box.
        self.trainInfoBox.setPosition(
            pygame.math.Vector2(self.rect.x, self.rect.centery - 30)
        )
        self.trainInfoBox.update()
        self.trainNameBox.setPosition(
            pygame.math.Vector2(self.rect.x, self.rect.centery + 30)
        )
        self.trainNameBox.update()

        if self.state == 0:
            if self.moving:
                # Is train in vicinity of next station?
                vecNextStation = self.getPosOfNextTrackIdx()
                vecTrain = pygame.math.Vector2(self.rect.centerx, self.rect.centery)
                diffVec = vecNextStation - vecTrain
                if diffVec.magnitude() < 2:
                    # Arrived at track index. Set the new trackIndex.
                    self.trainInfoBox.showText("3")
                    if self.direction:
                        self.latestTrackIndex = self.latestTrackIndex + 1
                    else:
                        self.latestTrackIndex = self.latestTrackIndex - 1
                    print(
                        self.trainName
                        + " ist in Station "
                        + str(self.latestTrackIndex)
                        + " eingetroffen."
                    )

                    # Park the train at the station.
                    self.rect.center = self.track.enterStation(
                        self, self.latestTrackIndex
                    )

                    # Stop moving.
                    self.stopMoving()

                    # Have we arrived at our goal?
                    if self.latestTrackIndex == self.goalIndex:
                        print(self.trainName + " hat Endstation erreicht und kehrt um.")
                        # We arrived at our goal. Set new goal.
                        if self.goalIndex == constants.TRACK_BEGIN:
                            self.setGoal(constants.TRACK_END)
                        elif self.goalIndex == constants.TRACK_END:
                            self.setGoal(constants.TRACK_BEGIN)

                    # Wait at bit at a station.
                    self.state = 1
                else:
                    # Zug fährt gerade nicht in Station ein. Entscheidung: Darf ich fahren?
                    decision, _ = self.rulebook()
                    if decision:
                        # Move train.
                        moveVector = self.heading * self.velocity
                        self.rect.center = self.rect.center + moveVector

        elif self.state == 1:
            self.waitCycles = self.waitCycles + 1
            self.rect.center = self.track.waitAtStation(self, self.latestTrackIndex)
            if self.waitCycles > constants.WAIT_CYCLES:

                # Can i start moving again?
                # is a train in the next section?
                decision, rule = self.rulebook()
                if decision:
                    if self.direction:
                        nextIdx = self.latestTrackIndex + 1
                    else:
                        nextIdx = self.latestTrackIndex - 1
                    print(
                        self.trainName
                        + " beginnt Anfahrt auf Station "
                        + str(nextIdx)
                        + "."
                        + " Aufgrund von Regel "
                        + rule
                        + "."
                    )
                    # start moving

                    self.state = 0
                    self.startMoving()
                    self.waitCycles = 0
                    self.rect.center = self.track.leaveStation(
                        self, self.latestTrackIndex
                    )

    def rulebook(self):
        # Ist ein Zug im (eingleisigen) Gleisabschnit?
        trainsInNextSection = self._trainsInNextSection()
        if len(trainsInNextSection) > 0:
            # Im eingleisigen Gleisabschnitt ist ein Zug.
            # Fahren Züge in die gleiche Richtung?
            trainsInSameDirection = self._trainsMoveSameDirection(trainsInNextSection)
            if len(trainsInSameDirection) > 0:
                # Alle Züge fahren in die gleiche Richtung.
                # Habe ich genug Abstans?
                if self._enoughDistance(trainsInSameDirection):
                    # 4.1.1 Genug Abstand - Freie Fahrt!
                    self.trainInfoBox.showText("4.1.1")
                    return True, "4.1.1"
                else:
                    # 4.1.2 Zu wenig Abstand - Stop!
                    self.trainInfoBox.showText("4.1.2")
                    return False, "4.1.2"
            else:
                # 4.1.3 Züge fahren nicht in die gleiche Richtung - Stop!
                self.trainInfoBox.showText("4.1.3")
                return False, "4.1.3"
        else:
            # Kein Zug ist im eingleisigen Abschnitt.
            # Bewege ich mich?
            if self.moving == True:
                self.trainInfoBox.showText("5")
                return True, "5"
            else:
                # Möchte noch ein anderer Zug in diesen Abschnitt einfahren?
                relevantTrains = self._claimsToSection()
                if len(relevantTrains) > 0:
                    # 4.2.2 Andere Züge möchten einfahren - Priorisierung.
                    return self._priorityFunction(relevantTrains)
                else:
                    # 4.2.1 Keine vorhandenen Ansprüche - Freie Fahrt.
                    self.trainInfoBox.showText("4.2.1")
                    return True, "4.2.1"

    def _trainsInNextSection(self):
        retList = []

        # Determine the next trackIndex
        if self.direction:
            nextIndex = self.latestTrackIndex + 1
            sectionCoord = (
                self.track.getPosOfIndex(self.latestTrackIndex).x,
                self.track.getPosOfIndex(nextIndex).x,
            )
        else:
            nextIndex = self.latestTrackIndex - 1
            sectionCoord = (
                self.track.getPosOfIndex(nextIndex).x,
                self.track.getPosOfIndex(self.latestTrackIndex).x,
            )

        for otherTrain in self.trains.sprites():
            if otherTrain == self:
                continue
            if (
                otherTrain.rect.centerx > sectionCoord[0]
                and otherTrain.rect.centerx < sectionCoord[1]
            ):
                retList.append(otherTrain)

        return retList

    def _trainsMoveSameDirection(self, trainsInNextSection):
        sameDirTrains = []
        for someTrain in trainsInNextSection:
            if someTrain.direction == self.direction:
                sameDirTrains.append(someTrain)
        return sameDirTrains

    def _enoughDistance(self, trainsInSameDirection):
        for someTrain in trainsInSameDirection:
            # Is train waiting in station?
            if someTrain.state == 1:
                # Train is in station. We do not have to keep distance.
                continue
            # Is train in front of me?
            if self.direction:
                if someTrain.rect.x < self.rect.x:
                    continue
            else:
                if someTrain.rect.x > self.rect.x:
                    continue

                # Is there enough distance?
            if (
                abs(someTrain.rect.x - self.rect.x)
                < constants.MINIMUM_INTER_TRAIN_DISTANCE
            ):
                return False
        return True

    def _claimsToSection(self):
        # Get the trains, that are at the current and the next station.
        currentPos = self.track.getPosOfIndex(self.latestTrackIndex).x
        nextPos = self.getPosOfNextTrackIdx().x

        trainsAtCurrentPos = []
        trainsAtNextPos = []
        for currentTrain in self.trains.sprites():
            if currentTrain == self:
                continue
            if currentTrain.rect.centerx == currentPos:
                trainsAtCurrentPos.append(currentTrain)
            elif currentTrain.rect.centerx == nextPos:
                trainsAtNextPos.append(currentTrain)

        # Which of those want to move into the next sector?
        relevantTrain = []
        for currentTrain in trainsAtCurrentPos:
            if currentTrain.direction == self.direction:
                relevantTrain.append(currentTrain)
        for currentTrain in trainsAtNextPos:
            if currentTrain.direction != self.direction:
                relevantTrain.append(currentTrain)

        return relevantTrain

    def _priorityFunction(self, relevantTrains):
        for currentTrain in relevantTrains:
            # Is the current train of a higher train type?
            if self.trainType > currentTrain.trainType:
                continue
            elif self.trainType == currentTrain.trainType:
                if self._calculatePriority() > currentTrain._calculatePriority():
                    print(
                        self.trainName
                        + " hat eine höhere Priorität als "
                        + currentTrain.trainName
                        + "("
                        + str(self._calculatePriority())
                        + " gegen "
                        + str(currentTrain._calculatePriority())
                        + ")"
                    )
                    continue
                elif self._calculatePriority() == currentTrain._calculatePriority():
                    print(
                        self.trainName
                        + " und "
                        + currentTrain.trainName
                        + " haben gleiche Prioriät. ("
                        + str(self._calculatePriority())
                        + ")"
                    )
                    if self.trainId > currentTrain.trainId:
                        continue
                    else:
                        self.trainInfoBox.showText("4.2.2.2")
                        return False, "4.2.2.2"
                else:
                    print(
                        self.trainName
                        + " hat eine niedrigere Priorität als "
                        + currentTrain.trainName
                        + "("
                        + str(self._calculatePriority())
                        + " gegen "
                        + str(currentTrain._calculatePriority())
                        + ")"
                    )
                    self.trainInfoBox.showText("4.2.2.3")
                    return False, "4.2.2.3"
            else:
                self.trainInfoBox.showText("4.2.2.3")
                return False, "4.2.2.3"

        self.trainInfoBox.showText("4.2.2.1")
        return True, "4.2.2.1"

    def _calculatePriority(self):
        return (self.waitCycles - constants.WAIT_CYCLES) * abs(
            self.latestTrackIndex - self.goalIndex
        )
