import pandas as pd
from os import path
import sqlite3

###############################################
# loading csvs and putting them in a sqlite db
###############################################

# only need to run this section once

# handle directories
DATA_DIR = './data'

# create connection
conn = sqlite3.connect(path.join(DATA_DIR, 'hockey-data.sqlite'))

# load csv data
player_game = pd.read_csv(path.join(DATA_DIR, 'player_games.csv'))
player = pd.read_csv(path.join(DATA_DIR, 'players.csv'))
game = pd.read_csv(path.join(DATA_DIR, 'games.csv'))
team = pd.read_csv(path.join(DATA_DIR, 'teams.csv'))

# and write it to sql
player_game.to_sql('player_game', conn, index=False, if_exists='replace')
player.to_sql('player', conn, index=False, if_exists='replace')
game.to_sql('game', conn, index=False, if_exists='replace')
team.to_sql('team', conn, index=False, if_exists='replace')

#########
# Queries
#########
conn = sqlite3.connect(path.join(DATA_DIR, 'hockey-data.sqlite'))

# return entire player table
df = pd.read_sql(
    """
    SELECT *
    FROM player
    """, conn)
df.head()

# return specific columns from player table + rename on the fly
df = pd.read_sql(
    """
    SELECT player_id, name, birth_date AS bday, team
    FROM player
    """, conn)
df.head()

###########
# filtering
###########

# basic filter, only rows where team is CHI
df = pd.read_sql(
    """
    SELECT player_id, name, nationality, pos
    FROM player
    WHERE team = 'CHI'
    """, conn)
df.head()

# AND in filter
df = pd.read_sql(
    """
    SELECT player_id, name, nationality, pos, team
    FROM player
    WHERE team = 'CHI' AND pos = 'LW'
    """, conn)
df.head()

# OR in filter
df = pd.read_sql(
    """
    SELECT player_id, name, nationality, pos, team
    FROM player
    WHERE team = 'BOS' OR pos = 'LW'
    """, conn)
df.head()

# IN in filter
df = pd.read_sql(
    """
    SELECT player_id, name, nationality, pos, team
    FROM player
    WHERE pos IN ('LW', 'RW', 'C')
    """, conn)
df.head()

# negation with NOT
df = pd.read_sql(
    """
    SELECT player_id, name, nationality, pos
    FROM player
    WHERE nationality NOT IN ('USA', 'CAN')
    """, conn)
df.head()

#########
# joining
#########

# no WHERE so fullcrossjoin
df = pd.read_sql(
    """
    SELECT
        player.name,
        player.pos,
        player.team,
        team.conference,
        team.division
    FROM player, team
    """, conn)
df.head(10)

# add in two team columns to make clearer
df = pd.read_sql(
    """
    SELECT
        player.name,
        player.pos,
        player.team as player_team,
        team.team as team_team,
        team.conference,
        team.division
    FROM player, team
    """, conn)
df.head(10)

# n of rows
df.shape

# works when we add WHERE to filter after crossjoin
df = pd.read_sql(
    """
    SELECT
        player.name,
        player.pos,
        player.team,
        team.conference,
        team.division
    FROM player, team
    WHERE player.team = team.team
    """, conn)
df.head()

# add in team column to make clearer how it works
df = pd.read_sql(
    """
    SELECT
        player.name,
        player.pos,
        player.team as player_team,
        team.team as team_team,
        team.conference,
        team.division
    FROM player, team
    WHERE player.team = team.team
    """, conn)
df.head()

# adding a third table
df = pd.read_sql(
    """
    SELECT
        player.name,
        player.pos,
        team.team,
        team.conference,
        team.division,
        player_game.*
    FROM player, team, player_game
    WHERE
        player.team = team.team AND
        player_game.player_id = player.player_id
    """, conn)
df.head()

# adding a third table - shorthand
df = pd.read_sql(
    """
    SELECT
        p.name,
        p.pos,
        t.team,
        t.conference,
        t.division,
        pg.game_id,
        pg.hits
    FROM player AS p, team AS t, player_game AS pg
    WHERE
        p.team = t.team AND
        pg.player_id = p.player_id
    """, conn)
df.head()

# adding an additional filter
df = pd.read_sql(
    """
    SELECT
        p.name,
        p.pos,
        t.team,
        t.conference,
        t.division,
        pg.game_id,
        pg.shots
    FROM player AS p, team AS t, player_game AS pg
    WHERE
        p.team = t.team AND
        pg.player_id = p.player_id AND
        pg.shots >= 5
    """, conn)
df.head()

###########
# LIMIT/TOP
###########

# SELECT *
# FROM player
# LIMIT 5

# SELECT TOP 5 *
# FROM player

df = pd.read_sql(
    """
    SELECT DISTINCT birth_city AS city, birth_state_prov AS state
    FROM player
    """, conn)
df.head()

# UNION
# SUBQUERIES
# LEFT, RIGHT, OUTER JOINS

# SELECT *
# FROM <left_table>
# LEFT JOIN <right_table> ON <left_table>.<common_column> = <right_table>.<common_column>

df = pd.read_sql(
    """
    SELECT a.*, b.shots, b.assists, b.goals, b.time_ice
    FROM
        (SELECT game_id, home_team_id AS team, player_id, name
        FROM game, player
        WHERE game.home_team_id = player.team_id
        UNION
        SELECT game_id, away_team_id AS team, player_id, name
        FROM game, player
        WHERE game.away_team_id = player.team_id) AS a
    LEFT JOIN player_game AS b ON a.game_id = b.game_id AND a.player_id = b.player_id
    """, conn)

df.loc[df['name'] == 'S. Crosby']

# game = pd.read_sql(
#     """
#     SELECT *
#     FROM game
#     """
#     , conn)

# game.loc[[11, 0, 1, 2, 3]]

# game.query("home == 'GB'")
