from ._anvil_designer import TeamsTemplate
from anvil import *
import anvil.server

class Teams(TeamsTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.repeating_panel_1.items = anvil.server.call("get_teams")

  @handle("button_1", "click")
  def button_1_click(self, **event_args):
    open_form('MainLayout')
    pass

  @handle("btn_dashboard_teams", "click")
  def btn_dashboard_teams_click(self, **event_args):
    open_form('MainLayout.DashboardTeams')
    pass
