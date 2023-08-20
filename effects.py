import pygame

class EffectScrollingLine():
  def __init__(self, screen):
    self.screen = screen
    self.frame = 0

    self.speed = 1
    self.color = [255, 255, 255]
    self.seed = 0
    self.width = 0.5

  def getScreenSize(self):
    size = {}
    size["x"] = self.screen.get_width()
    size["y"] = self.screen.get_height()
    return size

  def draw(self):
    screen = self.getScreenSize()
    width = screen["x"] - self.width * 100

    self.frame += self.speed * 50
    if self.frame > width * 2:
      self.frame = 0

    pos = int(self.frame) + self.seed * width
    pos = pos % (2 * width)
    pos = pos if pos < width else int(2 * width - pos)

    pygame.draw.rect(self.screen, self.color, (pos, 0, self.width * 100, screen["y"]))

class EffectDots():
  def __init__(self, screen):
    self.screen = screen
    self.frame = 0

    self.speed = 1
    self.color = [255, 255, 255]
    self.seed = 0.5
    self.width = 0.5

  def getScreenSize(self):
    size = {}
    size["x"] = self.screen.get_width()
    size["y"] = self.screen.get_height()
    return size
  
  def draw(self):
    screen = self.getScreenSize()
    center = pygame.Vector2(screen["x"] / 2, screen["y"] / 2)

    self.frame += self.speed * 5
    if self.frame > 360:
      self.frame = 0

    radius = int(self.frame)
    distance = self.seed * screen["x"] / 2

    for i in range(0, 360, 30):
      position = pygame.Vector2()
      position.from_polar((distance, i + radius))

      pygame.draw.circle(self.screen, self.color, (int(center.x + position.x), int(center.y + position.y)), self.width * 100)
