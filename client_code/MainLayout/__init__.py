from ._anvil_designer import MainLayoutTemplate
from anvil import *
import anvil.server
import plotly.graph_objects as go
from anvil import GoogleMap

from .DashboardFahrer import DashboardFahrer
from .DashboardTeams import DashboardTeams
from .Fahrer import Fahrer
from .Fahrerstatistik import Fahrerstatistik
from .Teams import Teams
from .Weltmeister import Weltmeister


class MainLayout(MainLayoutTemplate):
  def __init__(self, start_form=None, **properties):
    self.init_components(**properties)

    self.marker_strecke = None

    self.lade_strecken()
    self.starte_mit_erster_strecke()

    if start_form is not None:
      self.zeige_form(start_form)

  def lade_strecken(self):
    strecken = anvil.server.call("get_strecken_liste")
    self.drop_down_1.items = strecken

  def starte_mit_erster_strecke(self):
    if not self.drop_down_1.items:
      return

    erste_strecke = self.drop_down_1.items[0]
    self.drop_down_1.selected_value = erste_strecke
    self.zeige_strecke(erste_strecke)

  def zeige_strecke(self, streckenname):
    daten = anvil.server.call("get_strecke_details", streckenname)

    if not daten:
      alert("Keine Streckendaten gefunden.")
      return

    koord_string = daten["Kordinaten"]

    try:
      lat_str, lng_str = koord_string.split(",")
      lat = float(lat_str.strip())
      lng = float(lng_str.strip())
    except Exception:
      alert(f"Koordinaten ungültig: {koord_string}")
      return

    pos = GoogleMap.LatLng(lat, lng)

    self.map_1.center = pos
    self.map_1.zoom = 15

    if self.marker_strecke is None:
      self.marker_strecke = GoogleMap.Marker(
        position=pos,
        title=daten["Name"]
      )
      self.map_1.add_component(self.marker_strecke)
    else:
      self.marker_strecke.position = pos
      self.marker_strecke.title = daten["Name"]

    self.repeating_panel_1.items = [{
      "Name": daten["Name"],
      "Land": daten["Land"],
      "Laenge_km": f'{daten["Laenge_km"]} km'
    }]

  @handle("drop_down_1", "change")
  def drop_down_1_change(self, **event_args):
    streckenname = self.drop_down_1.selected_value
    if streckenname:
      self.zeige_strecke(streckenname)

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