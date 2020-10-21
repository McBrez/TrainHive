import pygame
import random
import os
import time
from random import choices
from random import randint

LINE_THICKNESS = 4
TRACK_COLOR = (255,255,255)


# Track class
class Track:
    def __init__(self, screen, startingPoint, vectorList):
      self.vectorList = vectorList
      self.startingPoint = startingPoint
      self.screen = screen

    def draw(self):
      currentEndPos = (self.startingPoint[0] + self.vectorList[0][0], self.startingPoint[1] + self.vectorList[0][1])
      pygame.draw.line(self.screen, TRACK_COLOR, self.startingPoint, currentEndPos, LINE_THICKNESS)
      pygame.draw.circle(self.screen, TRACK_COLOR, self.startingPoint, 10)
      pygame.draw.circle(self.screen, TRACK_COLOR, currentEndPos, 10)

      for i, vector in enumerate(self.vectorList):
        # Skip the first one, as it already has been drawn.
        if i == 0:
          continue

        nextPos = (currentEndPos[0] + vector[0], currentEndPos[1] + vector[1] )
        pygame.draw.line(self.screen, TRACK_COLOR, currentEndPos, nextPos, LINE_THICKNESS)
        pygame.draw.circle(self.screen, TRACK_COLOR, nextPos, 10)
        currentEndPos = nextPos

    def getPosOfIndex(self, trackIndex):
      currentPos = []
      
      return currentPos

#player class
class Train(pygame.sprite.Sprite):
    def __init__(self, track):
      pygame.sprite.Sprite.__init__(self)
      self.image = pygame.image.load("train.png") 
      self.image = pygame.transform.scale(self.image, (int(50), int(25)))
      self.rect = self.image.get_rect()
      self.rect.x = width / 2
      self.rect.y = height / 2
      self.track = track

    def place(self, trackIndex):
      self.x, self.y = self.track.getPosOfIndex(trackIndex) 

    def update(self):
      self.vx = 0
      self.vy = 0
      key = pygame.key.get_pressed()
      if key[pygame.K_LEFT]:
        self.vx = -5
        self.vy = 0
      elif key[pygame.K_RIGHT]:
        self.vx = 5
        self.vy = 0
      if key[pygame.K_UP]:
        self.vy = -5
        self.vx = 0
      elif key[pygame.K_DOWN]:
        self.vy = 5
        self.vx = 0
      self.rect.x = self.rect.x + self.vx
      self.rect.y = self.rect.y + self.vy

# ------------------------------------------------------------------------------------------------------------- Main --
if __name__ == "__main__":
  # Init pygame
  pygame.init()
  width = 1280
  height = 720
  screen = pygame.display.set_mode((width, height))
  pygame.display.set_caption("TrainHive Simulation")

  clock = pygame.time.Clock()
  WHITE = (255,255,255)
  RED = (255,0,0)
  change_x = 0
  change_y = 0
  HW = width / 2
  HH = height / 2

  # Init track
  track = Track(screen = screen, startingPoint = (100,int(height/2)), vectorList = [(400,0), (600, 0)])
  track.draw()

  #player sprite group
  sprites = pygame.sprite.Group()
  player = Train(track)
  sprites.add(player)
  all_trains = (player,)



  # Worker loop
  done = False
  while not done:
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              done = True

      sprites.update()

      #collision between player and and walls
      if player.rect.collidelist(all_trains) > 0:
        print("Collision !!")
        player.rect.x = player.rect.x - player.vx
        player.rect.y = player.rect.y - player.vx

      #fill the screen
      screen.fill((0, 0, 0))
      #screen.blit(background,(x,y))

      #draw the sprites
      sprites.draw(screen)
      track.draw()

      pygame.display.flip()
      clock.tick(60)

  pygame.quit()