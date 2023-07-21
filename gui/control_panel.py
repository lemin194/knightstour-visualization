import random
import os
import pygame
import pygame_gui
from collections import deque

from pygame_gui import UIManager, PackageResource

from pygame_gui.elements import UIWindow
from pygame_gui.elements import UIButton
from pygame_gui.elements import UIHorizontalSlider
from pygame_gui.elements import UITextEntryLine
from pygame_gui.elements import UIDropDownMenu
from pygame_gui.elements import UIScreenSpaceHealthBar
from pygame_gui.elements import UILabel
from pygame_gui.elements import UIImage
from pygame_gui.elements import UIPanel
from pygame_gui.elements import UISelectionList

from pygame_gui.windows import UIMessageWindow

import math


class ControlPanel(object):
  def __init__(self, rect:pygame.Rect, manager, nmin=5, nmax=12, ndefault=8):
    self.ui_space = rect
    self.manager = manager
    self.nmin = nmin
    self.nmax = nmax
    self.ndefault = ndefault
    self.recreate_ui()
  
  def recreate_ui(self):
    rect = self.ui_space
    manager = self.manager
    self.panel = UIPanel(rect,
                          manager=manager)
    
    self.ui_set = [set(), set()]
    self.phase_number = 0
    
    self.ui_width = rect.width * 0.8
    self.ui_left = (rect.width - self.ui_width) // 2


    self.create_ui_phase_0()
    self.create_ui_phase_1()
    
    for ui in self.ui_set[self.phase_number]:
      ui.show()


  
  def create_ui_phase_0(self):
    
    rect = self.ui_space
    manager = self.manager
    # From top
    next_top = 10
    next_height = 30
    vertical_spacing = 30

    self.header_1 = UILabel(pygame.Rect(self.ui_left, next_top, self.ui_width, next_height),
                            'Control Panel',
                            container=self.panel,
                            visible=0,)
    self.ui_set[0].add(self.header_1)


    next_top += next_height + vertical_spacing
    next_height = 30
    vertical_spacing = 10
    
    self.board_size_label = UILabel(
                          pygame.Rect(self.ui_left, next_top, self.ui_width, next_height),
                          'N:',
                          container=self.panel,
                          object_id='#option_label',
                          visible=0,)
    self.ui_set[0].add(self.board_size_label)


    next_top += next_height + vertical_spacing
    next_height = 30
    vertical_spacing = 10
    

    next_left = self.ui_left
    next_width = int(self.ui_width * 0.8)
    horizontal_spacing = 4
    self.board_size_slider = UIHorizontalSlider(
                          pygame.Rect(next_left, next_top, next_width, next_height),
                          8, (5, 12),
                          container=self.panel,
                          click_increment=1,
                          visible=0,
                        )
    self.ui_set[0].add(self.board_size_slider)

    next_left += next_width + horizontal_spacing
    next_width = int(self.ui_width - next_left + 10)
    self.board_size_slider_label = UILabel(
                          pygame.Rect(next_left, next_top, next_width, next_height),
                          str(int(round(self.board_size_slider.get_current_value()))),
                          container=self.panel,
                          object_id='#option_label',
                          visible=0,
                          )
    self.ui_set[0].add(self.board_size_slider_label)


    next_top += next_height + vertical_spacing
    next_height = 30
    vertical_spacing = 10
    
    self.algorithm_label = UILabel(
                          pygame.Rect(self.ui_left, next_top, self.ui_width, next_height),
                          'Algorithm:',
                          container=self.panel,
                          object_id='#option_label',
                          visible=0,)
    self.ui_set[0].add(self.algorithm_label)


    next_top += next_height + vertical_spacing
    next_height = 25
    vertical_spacing = 10

    self.algorithm_drop_down = UIDropDownMenu(
                          ["Brute force", "Warnsdorff's rule"],
                          "Brute force",
                          pygame.Rect(self.ui_left, next_top, self.ui_width, next_height),
                          container=self.panel,
                          visible=0,
                          )
    self.ui_set[0].add(self.algorithm_drop_down)


    next_top += next_height + vertical_spacing
    next_height = 25
    vertical_spacing = 10

    # From bottom
    next_top = rect.height - 100
    next_height = 50
    vertical_spacing = 10
    self.ready_button = UIButton(
                        pygame.Rect(self.ui_left, rect.height - 100, self.ui_width, 50),
                        'Start',
                        manager=manager,
                        container=self.panel,
                        object_id='#ready_button',
                        visible=0,
                        )
    self.ui_set[0].add(self.ready_button)
  
  def create_ui_phase_1(self):
    rect = self.ui_space
    manager = self.manager

    # From top
    next_top = 10
    next_height = 30
    vertical_spacing = 30

    self.header_2 = UILabel(pygame.Rect(self.ui_left, next_top, self.ui_width, next_height),
                            'Control Panel',
                            container=self.panel,
                            visible=0,
                            )
    self.ui_set[1].add(self.header_2)


    next_top += next_height + vertical_spacing
    next_height = 30
    vertical_spacing = 10
    
    self.speed_label = UILabel(
                          pygame.Rect(self.ui_left, next_top, self.ui_width, next_height),
                          'Speed:',
                          container=self.panel,
                          object_id='#option_label',
                          visible=0,)
    self.ui_set[1].add(self.speed_label)


    next_top += next_height + vertical_spacing
    next_height = 30
    vertical_spacing = 10

    next_left = self.ui_left
    next_width = int(self.ui_width * 0.8)
    horizontal_spacing = 4
    self.speed_slider = UIHorizontalSlider(
                          pygame.Rect(next_left, next_top, next_width, next_height),
                          8, (1, 15),
                          container=self.panel,
                          click_increment=1,
                          visible=0,
                        )
    self.ui_set[1].add(self.speed_slider)

    next_left += next_width + horizontal_spacing
    next_width = int(self.ui_width - next_left + 10)
    self.speed_slider_label = UILabel(
                          pygame.Rect(next_left, next_top, next_width, next_height),
                          str(int(round(self.speed_slider.get_current_value()))),
                          container=self.panel,
                          object_id='#option_label',
                          visible=0,
                          )
    self.ui_set[1].add(self.speed_slider_label)


    # From bottom
    next_top = rect.height - 100
    next_height = 50
    vertical_spacing = 30
    self.clear_button = UIButton(
                        pygame.Rect(self.ui_left, rect.height - 100, self.ui_width, 50),
                        'Clear',
                        manager=manager,
                        container=self.panel,
                        object_id='#clear_button',
                        visible=0,
                        )
    self.ui_set[1].add(self.clear_button)

    next_height = 30
    next_top -= next_height + vertical_spacing
    vertical_spacing = 10

    next_left = self.ui_left
    next_width = self.ui_width // 2
    self.prev_button = UIButton(
                        pygame.Rect(next_left, next_top, next_width, next_height),
                        '<-Prev',
                        container=self.panel,
                        object_id='#normal_button',
                        visible=0,
                      )
    self.ui_set[1].add(self.prev_button)

    next_left += next_width
    self.next_button = UIButton(
                        pygame.Rect(next_left, next_top, next_width, next_height),
                        'Next->',
                        container=self.panel,
                        object_id='#normal_button',
                        visible=0,
                      )
    self.ui_set[1].add(self.next_button)

    
    next_height = 50
    next_top -= next_height + vertical_spacing
    vertical_spacing = 30

    next_left = self.ui_left
    next_width = self.ui_width // 2
    self.start_button = UIButton(
                        pygame.Rect(next_left, next_top, next_width, next_height),
                        'Start',
                        container=self.panel,
                        object_id='#normal_button',
                        visible=0,
                      )
    self.ui_set[1].add(self.start_button)

    next_left += next_width
    self.reset_button = UIButton(
                        pygame.Rect(next_left, next_top, next_width, next_height),
                        'Reset',
                        container=self.panel,
                        object_id='#normal_button',
                        visible=0,
                      )
    self.ui_set[1].add(self.reset_button)
  

  def set_algorithm_list(self, algorithm_list, default):
    self.algorithm_drop_down.remove_options(
      self.algorithm_drop_down.options_list)
    self.algorithm_drop_down.add_options(algorithm_list)
    self.algorithm_drop_down.selected_option = algorithm_list[default]
    
  def set_algorithm(self, name):
    self.header_2.set_text(name)

  def update(self, gui):
    if self.phase_number == 0: self.update_phase_0(gui)
    elif self.phase_number == 1: self.update_phase_1(gui)
    
  
  def update_phase_0(self, gui):
    self.board_size_slider.set_current_value(
        int(round(self.board_size_slider.get_current_value())))
    self.board_size_slider_label.set_text(str(
        int(self.board_size_slider.get_current_value())))
  
  def update_phase_1(self, gui):
    if gui.knightstour_gui.solving:
      self.start_button.set_text('Pause')
    else:
      self.start_button.set_text('Start')
    self.speed_slider.set_current_value(
      int(round(self.speed_slider.get_current_value())))
    self.speed_slider_label.set_text(str(
        int(self.speed_slider.get_current_value())))
        
    gui.change_algorithm_speed(int(round(self.speed_slider.get_current_value())))

  def change_phase(self, phase_number):
    if phase_number not in range(2):
      return
    
    if phase_number == self.phase_number:
      return
    
    for ui in self.ui_set[self.phase_number]:
      ui.hide()
    for ui in self.ui_set[phase_number]:
      ui.show()
    
    self.phase_number = phase_number

  
  def handle_event(self, event, gui):
    if self.phase_number == 0: self.handle_phase_0(event, gui)
    elif self.phase_number == 1: self.handle_phase_1(event, gui)

  def handle_phase_0(self, event, gui):
    if event.type == pygame_gui.UI_BUTTON_PRESSED:
      if event.ui_element == self.ready_button:
        self.change_phase(1)
        gui.change_phase(1)
      
    
    if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
      if event.ui_element == self.algorithm_drop_down:
        algorithm_name = event.text
        gui.set_algorithm(algorithm_name)
        self.set_algorithm(gui.algorithm_name)

    if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
      if event.ui_element == self.board_size_slider:
        gui.change_board_size(int(round(self.board_size_slider.get_current_value())))


  def handle_phase_1(self, event, gui):
    if event.type == pygame_gui.UI_BUTTON_PRESSED:
        
      if event.ui_element == self.clear_button:
        self.change_phase(0)
        gui.change_phase(0)
      
      elif event.ui_element == self.next_button:
        gui.knightstour_gui.algorithm_next_step()
      elif event.ui_element == self.prev_button:
        gui.knightstour_gui.algorithm_prev_step()
      
      elif event.ui_element == self.start_button:
        if not gui.knightstour_gui.solving:
          gui.knightstour_gui.start_algorithm()
        else:
          gui.knightstour_gui.pause_algorithm()

      elif event.ui_element == self.reset_button:
        gui.knightstour_gui.reset_algorithm()
    
    if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
      if event.ui_element == self.speed_slider:
        gui.change_algorithm_speed(int(round(self.speed_slider.get_current_value())))