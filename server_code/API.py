import anvil.server
import sqlite3
from anvil.files import data_files

DB_NAME = "F1_Anvil.db"


def get_connection():
  conn = sqlite3.connect(data_files[DB_NAME])
  conn.row_factory = sqlite3.Row
  return conn


def run_query(sql, params=()):
  conn = get_connection()
  cur = conn.cursor()
  cur.execute(sql, params)
  rows = cur.fetchall()
  conn.close()
  return [dict(row) for row in rows]


@anvil.server.callable
def get_fahrer():
  sql = """
        SELECT FahrerNr, Name, Nation, Geburtsdatum, Debutjahr
        FROM Fahrer
        ORDER BY Name
    """
  return run_query(sql)


@anvil.server.callable
def get_fahrerstatistik():
  sql = """
        SELECT
            f.Name,
            fs.Pole_Position,
            fs.Punkte,
            fs.Siege,
            fs.DNF,
            fs.Podium
        FROM Fahrerstatistik fs
        JOIN Fahrer f ON f.FahrerNr = fs.FahrerNr
        ORDER BY fs.Punkte DESC, f.Name
    """
  return run_query(sql)


@anvil.server.callable
def get_teams():
  sql = """
        SELECT team_id, name, Abkuerzung, Standort
        FROM Team
        ORDER BY name
    """
  return run_query(sql)


@anvil.server.callable
def get_fahrer_weltmeister():
  sql = """
        SELECT
            wm.Jahr,
            f.Name AS Fahrer,
            t.name AS Team,
            wm.Punkte,
            wm.Siege
        FROM FahrerWM wm
        JOIN Fahrer f ON f.FahrerNr = wm.FahrerNr
        JOIN Team t ON t.team_id = wm.team_id
        ORDER BY wm.Jahr DESC
    """
  return run_query(sql)


@anvil.server.callable
def get_konstrukteur_weltmeister():
  sql = """
        SELECT
            wm.Jahr,
            t.name AS Team,
            (
                SELECT f.Name
                FROM Fahrer_Team ft
                JOIN Fahrer f ON f.FahrerNr = ft.FahrerNr
                WHERE ft.team_id = wm.team_id
                  AND ft.Jahr = wm.Jahr
                ORDER BY f.Name
                LIMIT 1
            ) AS Fahrer1,
            (
                SELECT f.Name
                FROM Fahrer_Team ft
                JOIN Fahrer f ON f.FahrerNr = ft.FahrerNr
                WHERE ft.team_id = wm.team_id
                  AND ft.Jahr = wm.Jahr
                ORDER BY f.Name
                LIMIT 1 OFFSET 1
            ) AS Fahrer2,
            wm.Punkte,
            wm.Siege
        FROM KonstrukteurWM wm
        JOIN Team t ON t.team_id = wm.team_id
        ORDER BY wm.Jahr DESC
    """
  return run_query(sql)


@anvil.server.callable
def get_dashboard_fahrer_punkte():
  sql = """
        SELECT
            f.Name,
            fs.Punkte
        FROM Fahrerstatistik fs
        JOIN Fahrer f ON f.FahrerNr = fs.FahrerNr
        ORDER BY fs.Punkte DESC
        LIMIT 10
    """
  return run_query(sql)


@anvil.server.callable
def get_dashboard_team_punkte():
  sql = """
        SELECT
            t.name AS Team,
            SUM(fs.Punkte) AS Punkte
        FROM Fahrer_Team ft
        JOIN Fahrerstatistik fs ON fs.FahrerNr = ft.FahrerNr
        JOIN Team t ON t.team_id = ft.team_id
        WHERE ft.Jahr = 2026
        GROUP BY t.name
        ORDER BY Punkte DESC
    """
  return run_query(sql)


@anvil.server.callable
def get_strecken_liste():
  sql = """
        SELECT Name
        FROM strecken
        ORDER BY Name
    """
  rows = run_query(sql)
  return [row["Name"] for row in rows]


@anvil.server.callable
def get_strecke_details(name):
  sql = """
        SELECT
            Name,
            Land,
            Kordinaten,
            Laenge_km,
            Rundenrekord,
            Letzter_Gewinner
        FROM strecken
        WHERE Name = ?
    """
  rows = run_query(sql, (name,))

  if not rows:
    return None

  row = rows[0]

  return {
    "Name": row["Name"],
    "Land": row["Land"],
    "Kordinaten": row["Kordinaten"],
    "Laenge_km": row["Laenge_km"],
    "Rekordzeit": row["Rundenrekord"],
    "Letzter_Sieger": row["Letzter_Gewinner"]
  }