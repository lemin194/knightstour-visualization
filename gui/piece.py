import pygame

class Piece(object):
  def __init__(self):
    self.image = pygame.image.load('data/images/knight_b_neo.png')
    self.scaled_image = self.image
    self.position = (0, 0)
    self.target_position = (0, 0)
  
  def scale_image(self, cell_size):
    self.scaled_image = pygame.transform.smoothscale(
      self.image, (cell_size, cell_size))
  
  def set_position(self, position):
    if (len(position) != 2):
      print('Invalid position')
      return
    self.position = position
    self.target_position = position
  
  def set_target_position(self, position):
    self.target_position = position
  
  def get_rect(self):
    rect = pygame.Rect(self.position[0], self.position[1], 
          self.scaled_image.get_width(), self.scaled_image.get_height())
    return rect
    
  def draw(self, surface):
    surface.blit(self.scaled_image, self.position)
  
  def update(self):
    if (abs(self.target_position[0] - self.position[0]) < 0.5 and
        abs(self.target_position[1] - self.position[1]) < 0.5):
      self.position = self.target_position
      return
    self.position = (
      self.position[0] + (self.target_position[0] - self.position[0]) * 0.8,
      self.position[1] + (self.target_position[1] - self.position[1]) * 0.8,
    )
