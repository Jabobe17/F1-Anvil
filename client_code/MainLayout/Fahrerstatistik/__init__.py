from ._anvil_designer import FahrerstatistikTemplate
from anvil import *
import anvil.server

class Fahrerstatistik(FahrerstatistikTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.repeating_panel_1.items = anvil.server.call("get_fahrerstatistik")

  @handle("button_1", "click")
  def button_1_click(self, **event_args):
    open_form('MainLayout')    
    pass

  @handle("btn_dashboard_fahrer", "click")
  def btn_dashboard_fahrer_click(self, **event_args):
    open_form('MainLayout.DashboardFahrer')
    pass
