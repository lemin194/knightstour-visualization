import random
import os
from os import listdir, linesep
from os.path import isfile, join, basename, splitext
import pygame
import pygame_gui
from collections import deque

from pygame_gui.elements import UIWindow
from pygame_gui.elements import UITextBox
from pygame_gui.elements import UILabel
from pygame_gui.elements import UIPanel
from pygame_gui.elements import UIButton

from pygame_gui.windows import UIMessageWindow

import math


class ReadmeWindow(UIWindow):
  def __init__(
    self, rect, manager, window_display_title='',
    resizable=False, visible=1, draggable=True,
    html_text="",
  ):
    UIWindow.__init__(
      self,
      rect=rect,
      manager=manager,
      window_display_title=window_display_title,
      object_id="#readme_window",
      resizable=resizable,
      visible=visible,
      draggable=draggable,
    )


    self.manager = manager

    home_button_top = 3
    home_button_size = 29
    text_box_rect_top = home_button_size + 2 * home_button_top
    self.text_box_rect = pygame.Rect(
      rect.width * 0.02, text_box_rect_top, 
      rect.width * 0.96, rect.height * 0.9 - self.title_bar_height - text_box_rect_top)
    dismiss_btn_width = 96
    dismiss_btn_height = 28
    dismiss_btn_rect = pygame.Rect(
      rect.width // 2 - dismiss_btn_width / 2, rect.height - dismiss_btn_height - self.title_bar_height - 4,
      dismiss_btn_width, dismiss_btn_height
    )


    
    self.home_button = pygame_gui.elements.UIButton(
      pygame.Rect((24, home_button_top),
                  (home_button_size, home_button_size)),
      '',
      manager=manager,
      container=self,
      parent_element=self,
      object_id='#home_button')


    self.pages = {}
    page_path = 'data/readme_window/'
    file_paths = [join(page_path, f) for f in listdir(page_path) if isfile(join(page_path, f))]
    for file_path in file_paths:
      with open(file_path, 'r') as page_file:
        file_id = splitext(basename(file_path))[0]
        file_data = ""
        for line in page_file:
          line = line.rstrip(linesep).lstrip()
          if len(line) > 0:
            if line[-1] != '>':
              line += '\n'
            file_data += line
        self.pages[file_id] = file_data
    index_page = self.pages['index']

    self.create_text_box(index_page)

    self.dismiss_btn = UIButton(
      relative_rect=dismiss_btn_rect,
      text="Dismiss",
      manager=manager,
      container=self,
      object_id='#dismiss',
    )


  def create_text_box(self, html_text: str):
    
    self.text_box = UITextBox(
      html_text=html_text,
      relative_rect=self.text_box_rect,
      manager=self.manager,
      object_id='#text_box',
      container=self,
    )

  def process_event(self, event):
    handled = super().process_event(event)

    if event.type == pygame_gui.UI_TEXT_BOX_LINK_CLICKED:
      self.open_new_page(event.link_target)
      handled = True
    
    if event.type == pygame_gui.UI_BUTTON_PRESSED:
      if event.ui_object_id == '#readme_window.#home_button':
        self.open_new_page('index')
        handled = True
      
    return handled
  
  def open_new_page(self, page_link: str):
    if self.text_box: self.text_box.kill()
    self.text_box = None
    if page_link in self.pages:
      text = self.pages[page_link]

      self.create_text_box(text)
