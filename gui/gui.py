import pygame
import pygame_gui
from pygame_gui.elements import UIButton
from pygame_gui.elements import UIWindow

from gui.knightstour_gui import KnightsTourGUI
from knightstour.knightstour import KnightsTour
from gui.control_panel import ControlPanel
from gui.readme_window import ReadmeWindow
import json
import os

class GUI(object):
  def __init__(self):
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Knight's tour visualization")

    self.window_width = 960
    self.window_height = 720

    #Theme
    self.theme_file = 'data/theme.json'
    self.theme_object = None
    self.background_color = '#202124'


    print(os.getcwd())


    self.screen = pygame.display.set_mode((self.window_width, self.window_height))
    
    self.fps = 60

    self.load_media()


    #GUI
    nmin, nmax, ndefault = 5, 12, 8
    self.chessboard_space = (0, 0, int(self.window_width * 0.7), self.window_height)
    self.panel_space = (self.chessboard_space[2], 0, self.window_width - self.chessboard_space[2] + 15, self.window_height)
    self.knightstour_gui = KnightsTourGUI(
      self.chessboard_space, self.m_font, ndefault)
    self.control_panel = ControlPanel(pygame.Rect(self.panel_space), self.manager, nmin, nmax, ndefault)

    self.algorithm_list = ["Brute force", "Warnsdorff's rule"]
    self.algorithm_name = self.algorithm_list[0]

    self.control_panel.set_algorithm_list(self.algorithm_list, 0)

    self.readme_btn = UIButton(pygame.Rect(24, self.window_height - 54, 96, 32),
                                "Read me",
                                manager=self.manager)

    self.create_readme_window()

  def create_readme_window(self):
    self.readme_window = ReadmeWindow(
        rect = pygame.Rect((self.window_width * 0.1, self.window_height * 0.1),
                    (int(500), int(self.window_height * 0.7))),
        manager=self.manager,
        window_display_title='Readme',
        resizable=False,
        )
  
  def load_media(self):
    self.window_icon = pygame.image.load('data/images/icon_knight_b_neo.png')
    pygame.display.set_icon(self.window_icon)

    loader = pygame_gui.core.IncrementalThreadedResourceLoader()

    self.manager = pygame_gui.UIManager((self.window_width, self.window_height), resource_loader=loader)

    self.m_font = pygame.font.Font('data/fonts/Roboto-Medium.ttf', 18)

    self.manager.add_font_paths('Roboto',
        regular_path='data/fonts/Roboto-Regular.ttf',
          bold_path='data/fonts/Roboto-Medium.ttf')
    clock = pygame.time.Clock()
    load_time_1 = clock.tick()
    self.manager.preload_fonts([
                                {'name': 'Roboto', 'html_size': 4.5, 'style': 'regular'},
                                {'name': 'Roboto', 'html_size': 6, 'style': 'bold'}
                              ])

    
    loader.start()
    finished_loading = False
    while not finished_loading:
        finished_loading, progress = loader.update()
    load_time_2 = clock.tick()
    print('Font load time taken:', (load_time_2 - load_time_1)/1000.0, 'seconds.')

    self.manager.get_theme().load_theme(self.theme_file)

    #Load theme
    with open(self.theme_file) as f:
      self.theme_object = json.load(f)
    self.load_theme()


  def load_theme(self):
    if not self.theme_object:
      return
    
    if 'main_window' not in self.theme_object:
      return
    
    main_window_theme = self.theme_object['main_window']

    self.background_color = main_window_theme.setdefault('background_color', '#202124')
  




  def change_board_size(self, board_n):
    self.knightstour_gui.change_board_size(board_n)

  def change_phase(self, phase_number):
    self.knightstour_gui.change_phase(phase_number)
    self.knightstour_gui.reset_algorithm()
  
  def set_algorithm(self, name):
    if name in self.algorithm_list:
      self.algorithm_name = name
      self.control_panel.set_algorithm(name)
      self.knightstour_gui.set_algorithm(name)
  
  def change_algorithm_speed(self, speed):
    self.knightstour_gui.change_algorithm_speed(speed)


  def draw(self):
    self.screen.fill(pygame.Color(self.background_color))

    self.knightstour_gui.draw(self.screen)

    
    self.manager.draw_ui(self.screen)

    pygame.display.update()
  

  def loop(self):
    clock = pygame.time.Clock()
    run = True

    while run:
      time_delta = clock.tick(self.fps) / 1000.0

      

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          run = False
          break
        
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
          if event.ui_element == self.readme_btn:
            if not self.readme_window:
              self.create_readme_window()
            else:
              self.readme_window.kill()
              self.readme_window = None
            

          if event.ui_object_id in ['#readme_window.#close_button',
                                    '#readme_window.#dismiss']:
            self.readme_window.kill()
            self.readme_window = None
        self.manager.process_events(event)
        self.control_panel.handle_event(event, self)
        self.knightstour_gui.handle_event(event)
      
      if (not run):
        break
      
      
      self.manager.update(time_delta)
      self.control_panel.update(self)


      self.draw()
  
      
  def __del__(self):
    pygame.quit()

