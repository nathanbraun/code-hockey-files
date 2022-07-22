"""
Answers to the end of chapter exercises for SQL chapter.

Note: this assumes you've already created/populated the SQL database as
outlined in the book and ./code/04_sql.py.
"""
import pandas as pd
from os import path
import sqlite3

DATA_DIR = './data'

conn = sqlite3.connect(path.join(DATA_DIR, 'hockey-data.sqlite'))

###############################################################################
# 4.1
###############################################################################
df  = pd.read_sql(
    """
    SELECT
        date, player_game.name, shots, goals, time_ice AS time_ice_sec
    FROM
        player_game, team
    WHERE
        team.team = player_game.team AND
        team.division = 'Atlantic'
    """, conn)

###############################################################################
# 4.2
###############################################################################
df  = pd.read_sql(
    """
    SELECT
        date, pg.name, shots, goals, time_ice AS time_ice_sec, nationality
    FROM
        player_game AS pg,
        team AS t,
        player AS p
    WHERE
        t.team = pg.team AND
        t.division = 'Central' AND
        p.player_id = pg.player_id
    """, conn)
