from ._anvil_designer import DashboardFahrerTemplate
from anvil import *
import anvil.server

class DashboardFahrer(DashboardFahrerTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.lade_daten()

  def lade_daten(self):
    daten = anvil.server.call("get_dashboard_fahrer_punkte")

    namen = [d["Name"] for d in daten]
    punkte = [d["Punkte"] for d in daten]

    self.plot_1.data = [{
      "x": namen,
      "y": punkte,
      "type": "bar"
    }]

    self.plot_1.layout = {
      "title": "Top Fahrer nach Punkten"
    }

  def btn_zurueck_click(self, **event_args):
    open_form('MainLayout')