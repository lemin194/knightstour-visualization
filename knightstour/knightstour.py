import numpy as np


def create_2d_list_of_object(r, c, obj) :
  ret = []
  for i in range(r):
    curr_row = []
    for j in range(c):
      curr_row.append(obj.copy())
    ret.append(curr_row.copy())
  return ret

class KnightsTour(object):
  def __init__(self, board_n):
    self.board_n = board_n
    self.starting_pos = (1, 2)
    
    self.possible_dirs = [(-1, -2), (-2, -1),
                      (-2, 1), (-1, 2),
                      (1, 2), (2, 1),
                      (2, -1), (1, -2),
                      ]

    self.reset_states()

  def set_knight_pos(self, knight_pos):
    pos = (int(knight_pos[0]), int(knight_pos[1]))
    if (len(pos) != 2):
      print("Invalid position!")
      return
    if (pos[0] not in range(self.board_n) or
        pos[1] not in range(self.board_n)):
      return
    self.knight_pos = (int(pos[0]), int(pos[1]))
  def change_board_size(self, board_n):
    self.board_n = board_n
    ki, kj = self.knight_pos
    if ki >= board_n: ki = board_n - 1
    if kj >= board_n: kj = board_n - 1
    self.knight_pos = (ki, kj)

  def set_starting_pos(self, starting_pos):
    self.starting_pos = starting_pos

  def reset_states(self):
    self.move_stack = []
    self.possible_moves = create_2d_list_of_object(self.board_n, self.board_n, [])
    self._marking_possible_moves = create_2d_list_of_object(self.board_n, self.board_n, set())
    self._marking_moves = np.zeros((self.board_n, self.board_n))
    self.history = []
    
    self.knight_pos = self.starting_pos
    self.init_states()

  def init_states(self):
    self.move_stack = [self.knight_pos]
    self._marking_moves[self.knight_pos] = 1
    
    for i in range(self.board_n):
      for j in range(self.board_n):
        self.calc_possible_moves_at_cell(i, j)
  
  def calc_possible_moves_at_cell(self, i, j):
    n = self.board_n
    cnt = 0
    for curr_dir in self.possible_dirs:
      new_i, new_j = i + curr_dir[0], j + curr_dir[1]
      if new_i < 0 or new_i >= n or new_j < 0 or new_j >= n:
        continue
      cnt += 1
      self.possible_moves[i][j].append((new_i, new_j))

  
  def precheck_stuck(self):
    reachable_moves = self.get_possible_moves()
    if (len(reachable_moves) == 0): return 1
    for i in range(self.board_n):
      for j in range(self.board_n):
        if self._marking_moves[(i, j)] == 1 or (i, j) in reachable_moves: continue
        possible_moves = self.get_possible_moves((i, j))
        if len(possible_moves) == 0:
          print(f'Stuck at {i}, {j}!')
          return 1
    return 0

  def get_possible_moves(self, pos=None):
    if not pos: pos = self.knight_pos
    ret = [move for move in 
      self.possible_moves[pos[0]][pos[1]]
      if self._marking_moves[move] == 0]
    return ret
  
  def count_accessibility_dist(self, pos):
    i, j = pos
    n = self.board_n
    center = (n // 2, n // 2)
    dist = abs(center[0] - i) ** 2 + abs(center[1] - j) ** 2
    ac = 0
    for curr_dir in self.possible_dirs:
      new_i, new_j = i + curr_dir[0], j + curr_dir[1]
      if new_i < 0 or new_i >= n or new_j < 0 or new_j >= n:
        continue
      if self._marking_moves[(new_i, new_j)] == 0:
        ac += 1
    return (ac, -dist)

  def brute_force_next_step(self):
    if len(self.move_stack) == self.board_n * self.board_n:
      print('Done!')
      return 1
    stuck = self.precheck_stuck()
    if not stuck:
      ki, kj = self.knight_pos
      possible_moves = self.get_possible_moves()
      for move in possible_moves:
        i, j, ret = *move, self.count_accessibility_dist(move)
      for move in possible_moves:
        if move not in self._marking_possible_moves[ki][kj]:
          self._marking_possible_moves[ki][kj].add(move)
          self.move_stack.append(move)
          self.knight_pos = move
          self._marking_moves[move] = 1
          self.history.append((
            1,
            move,
            (ki, kj)
          ))
          return 0
      stuck = 1
    if stuck:

      move = self.move_stack.pop()
      self.knight_pos = self.move_stack[-1]

      self.history.append((
        0,
        move,
        self._marking_possible_moves[move[0]][move[1]].copy()
      ))
      self._marking_possible_moves[move[0]][move[1]].clear()
      self._marking_moves[move] = 0
      
    return 0

  def brute_force_prev_step(self):
    if len(self.history) == 0: return
    state_type = self.history[-1][0]
    if state_type == 1:
      state_type, prev_move, prev_kpos = self.history.pop()
      self._marking_possible_moves[prev_kpos[0]][prev_kpos[1]].remove(prev_move)
      self.move_stack.remove(prev_move)
      self.knight_pos = prev_kpos
      self._marking_moves[prev_move] = 0
      return
    if state_type == 0:
      state_type, prev_move, prev_possible_states = self.history.pop()

      self.move_stack.append(prev_move)
      self.knight_pos = prev_move
      self._marking_possible_moves[prev_move[0]][prev_move[1]] = prev_possible_states
      self._marking_moves[prev_move] = 1
  
  
  def warnsdorff_next_step(self):
    if len(self.move_stack) == self.board_n * self.board_n:
      print('Done!')
      return 1
    
    stuck = self.precheck_stuck()
    if not stuck:
      ki, kj = self.knight_pos
      possible_moves_sorted = self.get_possible_moves()
      possible_moves_sorted.sort(key=self.count_accessibility_dist)
      for move in possible_moves_sorted:
        i, j, ret = *move, self.count_accessibility_dist(move)
      for move in possible_moves_sorted:
        if move not in self._marking_possible_moves[ki][kj]:
          self._marking_possible_moves[ki][kj].add(move)
          self.move_stack.append(move)
          self.knight_pos = move
          self._marking_moves[move] = 1
          self.history.append((
            1,
            move,
            (ki, kj)
          ))
          return 0
      stuck = 1
    if stuck:
      move = self.move_stack.pop()
      self.knight_pos = self.move_stack[-1]
      self.history.append((
        0,
        move,
        self._marking_possible_moves[move[0]][move[1]].copy()
      ))
    
      self._marking_possible_moves[move[0]][move[1]].clear()
      self._marking_moves[move] = 0
    return 0
  
  def warnsdorff_prev_step(self):
    
    if len(self.history) == 0: return
    state_type = self.history[-1][0]
    if state_type == 1:
      state_type, prev_move, prev_kpos = self.history.pop()
      self._marking_possible_moves[prev_kpos[0]][prev_kpos[1]].remove(prev_move)
      self.move_stack.remove(prev_move)
      self.knight_pos = prev_kpos
      self._marking_moves[prev_move] = 0
      return
    if state_type == 0:
      state_type, prev_move, prev_possible_states = self.history.pop()

      self.move_stack.append(prev_move)
      self.knight_pos = prev_move
      self._marking_possible_moves[prev_move[0]][prev_move[1]] = prev_possible_states
      self._marking_moves[prev_move] = 1