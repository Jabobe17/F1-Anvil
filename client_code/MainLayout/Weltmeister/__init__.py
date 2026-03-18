from ._anvil_designer import WeltmeisterTemplate
from anvil import *
import anvil.server

class Weltmeister(WeltmeisterTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    self.repeating_panel_1.items = anvil.server.call("get_fahrer_weltmeister")
    self.repeating_panel_2.items = anvil.server.call("get_konstrukteur_weltmeister")

  @handle("button_1", "click")
  def button_1_click(self, **event_args):
    open_form('MainLayout')
    pass
