import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import sqlite3

def _connect():
  db_path = data_files["f1_2026.db"]
  conn = sqlite3.connect(db_path)
  conn.row_factory = sqlite3.Row
  return conn

def _query(sql, params=()):
  with _connect() as conn:
    cur = conn.execute(sql, params)
    rows = cur.fetchall()
    return [dict(r) for r in rows]

@anvil.server.callable
def api_get_drivers():
  return _query("SELECT * FROM Fahrer ORDER BY Nachname, Vorname")

@anvil.server.callable
def api_get_teams():
  return _query("SELECT * FROM Teams ORDER BY Teamname")

@anvil.server.callable
def api_get_races():
  return _query("SELECT * FROM Rennen ORDER BY Datum")

@anvil.server.callable
def api_get_driver_stats():
  return _query("SELECT * FROM Fahrerstatistik ORDER BY Siege DESC, Punkte DESC")

@anvil.server.callable
def api_get_results_for_race(race_id):
  return _query("""
    SELECT * FROM Ergebnisse
    WHERE RennenID = ?
    ORDER BY Position ASC
  """, (race_id,))

  