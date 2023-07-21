from gui.gui import GUI
import packaging
import packaging.version
import packaging.specifiers
import packaging.requirements
import logging


def run():
  window = GUI()

  window.loop()

if (__name__ == '__main__'):
    run()