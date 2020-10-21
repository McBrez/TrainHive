import pygame
import random
import os
import time
from random import choices
from random import randint

LINE_THICKNESS = 4
TRACK_COLOR = (255,255,255)
BASE_VELOCITY = 3
WAIT_CYCLES = 50 

TRACK = [
  pygame.math.Vector2(int(100),int(0)),
  pygame.math.Vector2(int(200),int(0)),
  pygame.math.Vector2(int(400), int(0)),
  pygame.math.Vector2(int(200), int(0)),
  pygame.math.Vector2(int(100), int(0)),
  pygame.math.Vector2(int(100), int(0)) ]



def v2i(vector):
  return (int(vector.x), int(vector.y))

class Controller:
  def __init__(self, screen):
    self.screen = screen
    self.trainList = pygame.sprite.Group()
    self.track = None
  
  def addTrain(self, track, trackIndex, goalIndex):
    newTrain = Train(track)
    newTrain.place(trackIndex)
    newTrain.setGoal(goalIndex)
    # notify all trains about the new train
    for train in self.trainList:
      train.onTrainAdded(newTrain)

    self.trainList.add(newTrain)

    return newTrain

  def addTrack(self, startPoint, trackList):
    self.track = Track(screen = screen, startingPoint = startPoint, vectorList = trackList)
    return self.track

  def update(self):
      key = pygame.key.get_pressed()
      if key[pygame.K_LEFT]:
        for train in self.trainList:
          train.kill()
      elif key[pygame.K_RIGHT]:
        self.addTrain(controller.track, 0, 6)
        self.addTrain(controller.track, 5, 0)
        for train in self.trainList:
          train.startMoving()

      # Call update for held instances
      self.trainList.update()

  def draw(self):
        # Draw stuff.
        self.track.draw()
        self.trainList.draw(self.screen)

# Track class
class Track:
    def __init__(self, screen, startingPoint, vectorList):
      self.vectorList = vectorList
      self.startingPoint = startingPoint
      self.screen = screen

    def draw(self):
      currentEndPos = self.startingPoint + self.vectorList[0]
      pygame.draw.line(self.screen, TRACK_COLOR, self.startingPoint, currentEndPos, LINE_THICKNESS)
      pygame.draw.circle(self.screen, TRACK_COLOR, v2i(self.startingPoint), 10)
      pygame.draw.circle(self.screen, TRACK_COLOR, v2i(currentEndPos), 10)

      for i, vector in enumerate(self.vectorList):
        # Skip the first one, as it already has been drawn.
        if i == 0:
          continue

        nextPos = currentEndPos + vector
        pygame.draw.line(self.screen, TRACK_COLOR, v2i(currentEndPos), v2i(nextPos), LINE_THICKNESS)
        pygame.draw.circle(self.screen, TRACK_COLOR, v2i(nextPos), 10)
        currentEndPos = nextPos

    def getPosOfIndex(self, trackIndex):
      currentPos = self.startingPoint
      for i in range(trackIndex):
        currentPos = currentPos + self.vectorList[i]

      return currentPos

#player class
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
      self.heading = pygame.math.Vector2(int(1), int(0))
      self.latestTrackIndex = 0
      self.state = 0
      self.goalIndex = -1 
      self.waitCycles = 0
      self.trains = []

    def onTrainAdded(self, train):
      self.trains.append(train)

    def onTrainRemoved(self, train):
      self.trains.remove(train)

    def place(self, trackIndex):
      self.latestTrackIndex = trackIndex
      x,y = self.track.getPosOfIndex(trackIndex)
      self.rect.x = x - int(self.rect.centerx)  
      self.rect.y = y - int(self.rect.centery)

    def setGoal(self, goalIndex):
      self.goalIndex = goalIndex
      if self.goalIndex < self.latestTrackIndex:
        self.direction = False
      else:
        self.direction = True

    def startMoving(self):
      self.moving = True

    def stopMoving(self):
      self.moving = False

    def setHeading(self, vector):
      pass

    def update(self):
      if self.state == 0:
        if self.moving:
          # Is train in vicinity of next station?
          if self.direction:
            vecNextStation = self.track.getPosOfIndex(self.latestTrackIndex + 1)
          else:
            vecNextStation = self.track.getPosOfIndex(self.latestTrackIndex - 1)
          vecTrain = pygame.math.Vector2(int(self.rect.centerx), int(self.rect.centery))
          diffVec =  vecNextStation - vecTrain
          if diffVec.magnitude() < 2:
            # Arrived at track index.
            if self.direction:
              self.latestTrackIndex = self.latestTrackIndex + 1
            else:
              self.latestTrackIndex = self.latestTrackIndex - 1

            self.stopMoving()
            # Have we arrived at our goal? 
            if self.latestTrackIndex == self.goalIndex:
              # We arrived at our goal. Remove the train.
              self.kill() # autsch
            else:
              # Wait at station.
              self.state = 1
          else:
            if self.direction:
              self.rect.x = self.rect.x + BASE_VELOCITY
            else:
              self.rect.x = self.rect.x - BASE_VELOCITY

      elif self.state == 1:
        self.waitCycles = self.waitCycles + 1
        if self.waitCycles > WAIT_CYCLES:
          
          # Can i start moving again? 
          # is a train in the next section?
         # currentX = 
         # toBeX =  
         # for train in self.trains:
         #   if train.x  

          self.state = 0
          self.startMoving()
          self.waitCycles = 0

# ------------------------------------------------------------------------------------------------------------- Main --
if __name__ == "__main__":
  # Init pygame
  pygame.init()
  width = 1280
  height = 720
  screen = pygame.display.set_mode((width, height))
  pygame.display.set_caption("TrainHive Simulation")
  clock = pygame.time.Clock()

  # Init Controller
  controller = Controller(screen)
  controller.addTrack(pygame.math.Vector2(int(100), int(height/2)), TRACK)
  controller.addTrain(controller.track, 0, 6)
  controller.addTrain(controller.track, 5, 0)

  # Worker loop
  done = False
  while not done:
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              done = True

      # Do updates
      controller.update()

      #fill the screen
      screen.fill((0, 0, 0))

      # Draw stuff
      controller.draw()

      pygame.display.flip()
      clock.tick(60)

  pygame.quit()