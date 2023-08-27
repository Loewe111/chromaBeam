import random
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

      pygame.draw.circle(self.screen, self.color, (int(center.x + position.x), int(center.y + position.y)), int(self.width * 100))

class EffectStars():
  def __init__(self, screen):
    self.screen = screen
    self.frame = 0

    self.speed = 1
    self.color = [255, 255, 255]
    self.seed = 0.5
    self.width = 0.5

    self.stars = []
    self.size = 3000
    for i in range(0, 1000):
      self.stars.append(pygame.Vector2(random.randint(0, self.size), random.randint(0, self.size)))

  def getScreenSize(self):
    size = {}
    size["x"] = self.screen.get_width()
    size["y"] = self.screen.get_height()
    return size
  
  def draw(self):
    screen = self.getScreenSize()
    center = pygame.Vector2(screen["x"] / 2, screen["y"] / 2)

    self.frame += self.speed
    if self.frame > 360:
      self.frame = 0

    radius = int(self.frame)

    for star in self.stars:
      position = pygame.Vector2()
      position = star - pygame.Vector2(self.size / 2, self.size / 2)
      position.as_polar()

      newpos = pygame.Vector2()
      newpos.from_polar((position.length(), position.angle_to(center) + radius))
      # scale by seed
      newpos.scale_to_length(position.length() * (self.seed + 0.5))
      # move to center
      newpos += center

      pygame.draw.circle(self.screen, self.color, (int(newpos.x), int(newpos.y)), int(self.width * 10))

class EffectGridSquares():
  def __init__(self, screen):
    self.screen = screen

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
    num_squares = int(self.seed * 10) + 1
    square_areas = pygame.Vector2(screen["x"] / num_squares, screen["y"] / num_squares)
    square_sizes = pygame.Vector2(square_areas.x * self.width, square_areas.y * self.width)
    square_positions = pygame.Vector2((square_areas.x - square_sizes.x) / 2, (square_areas.y - square_sizes.y) / 2)

    for i in range(0, num_squares):
      for j in range(0, num_squares):
        pygame.draw.rect(self.screen, self.color, (i * square_areas.x + square_positions.x, j * square_areas.y + square_positions.y, square_sizes.x, square_sizes.y), border_radius= 10)

