from ._anvil_designer import FahrerTemplate
from anvil import *
import anvil.server

class Fahrer(FahrerTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.repeating_panel_1.items = anvil.server.call("get_fahrer")

  @handle("button_1", "click")
  def button_1_click(self, **event_args):
    open_form('MainLayout')
    pass
