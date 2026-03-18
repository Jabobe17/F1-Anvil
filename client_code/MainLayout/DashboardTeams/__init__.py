from ._anvil_designer import DashboardTeamsTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server

class DashboardTeams(DashboardTeamsTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.lade_daten()

  def lade_daten(self):
    daten = anvil.server.call("get_dashboard_team_punkte")

    teams = [d["Team"] for d in daten]
    punkte = [d["Punkte"] for d in daten]

    self.plot_1.data = [{
      "labels": teams,
      "values": punkte,
      "type": "pie"
    }]

    self.plot_1.layout = {
      "title": "Team Punkte Verteilung 2026"
    }