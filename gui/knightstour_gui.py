import pygame
import pygame_gui
from pygame_gui.elements import UILabel
import math
from gui.piece import Piece
from knightstour.knightstour import KnightsTour
import time


class KnightsTourGUI(object):
  def __init__(self, window_space, m_font : pygame.font.Font, ndefault=8):
    self.board_size = int(window_space[2] * 0.8)
    self.board_pos = (
      window_space[0] + window_space[2] / 2 - self.board_size / 2,
      window_space[1] + window_space[3] / 2 - self.board_size / 2,
    )
    self.knight_image = pygame.image.load('data/images/knight_b_neo.png')
    self.knight = Piece()
    self.dragging = False
    self.knightstour = KnightsTour(ndefault)
    self.board_n = self.knightstour.board_n
    self.cell_size = self.board_size / self.board_n
    knight_pos = self.knightstour.knight_pos
    knight_coord = (
      self.board_pos[0] + knight_pos[1] * self.cell_size, 
      self.board_pos[1] + knight_pos[0] * self.cell_size)
    self.knight.set_position(knight_coord)

    self.phase_number = 0
    self.algorithm_name = 'Brute force'


    self.m_font = m_font
    self.move_order_labels = []
    for i in range(144):
      self.move_order_labels.append(
        self.m_font.render(str(i + 1),
          True,
          (12, 16, 14)
        )
      )

    self.algorithm_timing = time.time()
    self.algorithm_delay = 0.01
    self.solving = False


  def set_algorithm(self, name):
    self.algorithm_name = name

  def handle_event(self, event):
    if self.phase_number == 0:
      self.handle_phase_0(event)
    else:
      self.handle_phase_1(event)

  def handle_phase_0(self, event):
    self.handle_dragging(event)
  
  def handle_phase_1(self, event):
    # if self.algorithm_name == 'Brute force':
    #   self.handle_brute_force(event)
    # elif self.algorithm_name == "Warnsdorff's rule":
    #   self.handle_warnsdorff(event)
    pass
    
  def handle_brute_force(self, event):
    pass


  def start_algorithm(self):
    self.solving = True

  def reset_algorithm(self):
    self.pause_algorithm()
    self.knightstour.reset_states()
  
  def pause_algorithm(self):
    self.solving = False
  
  def change_algorithm_speed(self, speed):
    if speed < 1: speed = 1
    if speed > 15: speed = 15
    self.algorithm_delay = (31 - 2 * speed) * 0.01
  
  def algorithm_next_step(self):
    if self.algorithm_name == 'Brute force':
      return self.brute_force_next_step()
    elif self.algorithm_name == "Warnsdorff's rule":
      return self.warnsdorff_next_step()

  
  def algorithm_prev_step(self):
    if self.algorithm_name == 'Brute force':
      return self.brute_force_prev_step()
    elif self.algorithm_name == "Warnsdorff's rule":
      return self.warnsdorff_prev_step()


  def brute_force_next_step(self):
    return self.knightstour.brute_force_next_step()
    # steps = 0
    # while not self.knightstour.brute_force_next_step():
    #   time.sleep(0.01)
    #   steps += 1
    #   if steps % 1000 == 0: print(f'# steps: {steps}')
    #   continue

  def brute_force_prev_step(self):
    return self.knightstour.brute_force_prev_step()
    
  
  def warnsdorff_next_step(self):
    return self.knightstour.warnsdorff_next_step()
    
  
  def warnsdorff_prev_step(self):
    return self.knightstour.warnsdorff_prev_step()
    
  def change_board_size(self, board_n):
    self.board_n = board_n
    self.cell_size = self.board_size / self.board_n
    self.knightstour.change_board_size(board_n)
    
  
  def change_phase(self, phase_number):
    self.phase_number = phase_number
    if self.phase_number == 1:
      self.knightstour.set_starting_pos(self.knightstour.knight_pos)
      self.dragging = False

  def handle_dragging(self, event):
    if (event.type == pygame.MOUSEBUTTONDOWN):
      if (not pygame.mouse.get_pressed()[0]): return
      mouse_pos = pygame.mouse.get_pos()
      knight_rect = self.knight.get_rect()
      if (knight_rect.collidepoint(mouse_pos[0], mouse_pos[1])) :
        self.dragging = True
    elif (event.type == pygame.MOUSEBUTTONUP):
      if (self.dragging):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos_relative = (mouse_pos[0] - self.board_pos[0],
                              mouse_pos[1] - self.board_pos[1])
        cell_pos = (mouse_pos_relative[0] // self.cell_size, 
                    mouse_pos_relative[1] // self.cell_size)
        
        self.knightstour.set_knight_pos((cell_pos[1], cell_pos[0]))
        
        self.dragging = False

  def update(self):
    if (self.dragging):
      mouse_pos = pygame.mouse.get_pos()
      self.knight.set_position((
        mouse_pos[0] - self.cell_size // 2, mouse_pos[1] - self.cell_size // 2))
    else:
      knight_pos = self.knightstour.knight_pos
      knight_coord = (
        self.board_pos[0] + knight_pos[1] * self.cell_size, 
        self.board_pos[1] + knight_pos[0] * self.cell_size)
      self.knight.set_target_position(knight_coord)

    if not self.solving: self.algorithm_timing = time.time()
    else:
      passed_time = time.time() - self.algorithm_timing
      if passed_time > self.algorithm_delay:
        self.algorithm_timing = time.time()
        done = self.algorithm_next_step()
        if done:
          self.pause_algorithm()
    
    
    self.knight.update()

  def draw(self, surface):

    self.draw_board(surface)

    if self.phase_number == 1:
      self.highlight_possible_moves(surface)
      self.draw_move_order(surface)


    self.draw_board_border(surface)


    self.knight.scale_image(self.cell_size)

    self.knight.draw(surface)

    
    self.update()

  def get_cell_rect(self, i, j):
    (x, y) = (int(self.board_pos[0] + int(self.cell_size * j)),
            int(self.board_pos[1] + int(self.cell_size * i)))
    csize = int(math.ceil(self.cell_size))
    return pygame.Rect(x, y, csize, csize)

  def draw_board(self, surface):
    light_square_color = (238, 238, 210)
    dark_square_color = (118, 150, 86)



    for i in range(self.board_n):
      for j in range(self.board_n):
        pygame.draw.rect(
          surface, 
          light_square_color if ((i + j + self.board_n) % 2 == 0) else dark_square_color,
          self.get_cell_rect(i, j),
          0
        )
  def draw_board_border(self, surface):
    border_weight = 4
    border_color = (64, 64, 64)
    if (border_weight > 0):
      pygame.draw.rect(
        surface, border_color, 
        pygame.Rect(self.board_pos[0], self.board_pos[1], self.board_size, self.board_size),
        border_weight
      )
  
  def highlight_possible_moves(self, surface):
    highlight_move_color = (0, 220, 128, 64)
    possible_moves = self.knightstour.get_possible_moves()
    for i in range(self.board_n):
      for j in range(self.board_n):
        if (i, j) not in possible_moves: continue
        cell_rect = self.get_cell_rect(i, j)
        s = pygame.Surface((cell_rect.width,
                            cell_rect.height),
                            pygame.SRCALPHA
                            )
        s.fill(highlight_move_color)
        surface.blit(s, (cell_rect.left, cell_rect.top))
  
  def draw_move_order(self, surface):
    move_stack = self.knightstour.move_stack
    for ind, move in enumerate(move_stack):
      i, j = move
      (cx, cy) = (int(self.board_pos[0] + self.cell_size * j) + self.cell_size // 2,
                int(self.board_pos[1] + self.cell_size * i) + self.cell_size // 2)
      text = self.move_order_labels[ind]
      textRect = text.get_rect()
      textRect.center = (cx, cy)
      surface.blit(text, textRect)
 