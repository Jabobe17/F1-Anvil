from ._anvil_designer import MainLayoutTemplate
from anvil import *
import plotly.graph_objects as go
from anvil import GoogleMap
from .DashboardFahrer import DashboardFahrer
from .DashboardTeams import DashboardTeams
from .Fahrer import Fahrer
from .Fahrerstatistik import Fahrerstatistik
from .Teams import Teams
from .Weltmeister import Weltmeister


class MainLayout(MainLayoutTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    # Karte initialisieren
    self.zeige_interlagos()

  def zeige_interlagos(self):
    center_lat = -23.7014
    center_lng = -46.6969

    self.map_1.center = GoogleMap.LatLng(center_lat, center_lng)
    self.map_1.zoom = 15

    # Marker
    marker = GoogleMap.Marker(
      position=GoogleMap.LatLng(center_lat, center_lng),
      title="Interlagos"
    )
    self.map_1.add_component(marker)



  def zeige_form(self, form_klasse):
    self.column_panel_1.clear()
    self.column_panel_1.add_component(form_klasse())

  @handle("btn_fahrer", "click")
  def btn_fahrer_click(self, **event_args):
    self.zeige_form(Fahrer)

  @handle("btn_statistik", "click")
  def btn_fahrerstatistik_click(self, **event_args):
    self.zeige_form(Fahrerstatistik)

  @handle("btn_teams", "click")
  def btn_teams_click(self, **event_args):
    self.zeige_form(Teams)

  @handle("btn_weltmeister", "click")
  def btn_weltmeister_click(self, **event_args):
    self.zeige_form(Weltmeister)

  @handle("btn_dashboard_fahrer", "click")
  def btn_dashboard_fahrer_click(self, **event_args):
    self.zeige_form(DashboardFahrer)

  @handle("btn_dashboard_teams", "click")
  def btn_dashboard_teams_click(self, **event_args):
    self.zeige_form(DashboardTeams)