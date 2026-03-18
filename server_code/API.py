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
            2026 AS Jahr,
            f.Name AS Fahrer,
            t.name AS Team,
            fs.Punkte,
            fs.Siege
        FROM Fahrerstatistik fs
        JOIN Fahrer f ON f.FahrerNr = fs.FahrerNr
        JOIN Fahrer_Team ft ON ft.FahrerNr = fs.FahrerNr
        JOIN Team t ON t.team_id = ft.team_id
        WHERE ft.Jahr = 2026
        ORDER BY fs.Punkte DESC, fs.Siege DESC, f.Name ASC
        LIMIT 1
    """
  return run_query(sql)

@anvil.server.callable
def get_konstrukteur_weltmeister():
  sql = """
        WITH team_stats AS (
            SELECT
                ft.team_id,
                ft.Jahr,
                t.name AS Team,
                SUM(fs.Punkte) AS Punkte,
                SUM(fs.Siege) AS Siege
            FROM Fahrer_Team ft
            JOIN Fahrerstatistik fs ON fs.FahrerNr = ft.FahrerNr
            JOIN Team t ON t.team_id = ft.team_id
            WHERE ft.Jahr = 2026
            GROUP BY ft.team_id, ft.Jahr, t.name
        ),
        best_team AS (
            SELECT team_id, Jahr, Team, Punkte, Siege
            FROM team_stats
            ORDER BY Punkte DESC, Siege DESC, Team ASC
            LIMIT 1
        )
        SELECT
            bt.Jahr,
            bt.Team,
            (
                SELECT f.Name
                FROM Fahrer_Team ft
                JOIN Fahrer f ON f.FahrerNr = ft.FahrerNr
                WHERE ft.team_id = bt.team_id
                  AND ft.Jahr = bt.Jahr
                ORDER BY f.Name
                LIMIT 1
            ) AS Fahrer1,
            (
                SELECT f.Name
                FROM Fahrer_Team ft
                JOIN Fahrer f ON f.FahrerNr = ft.FahrerNr
                WHERE ft.team_id = bt.team_id
                  AND ft.Jahr = bt.Jahr
                ORDER BY f.Name
                LIMIT 1 OFFSET 1
            ) AS Fahrer2,
            bt.Punkte,
            bt.Siege
        FROM best_team bt
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
        SELECT Name, Land, Kordinaten, Laenge_km
        FROM strecken
        WHERE Name = ?
    """
  rows = run_query(sql, (name,))

  if not rows:
    return None

  return rows[0]