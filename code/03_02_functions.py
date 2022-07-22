import pandas as pd
from os import path

# change this to the directory where the csv files that come with the book are
# stored
# on Windows it might be something like 'C:/mydir'

DATA_DIR = './data'

# load adp data
pg = pd.read_csv(path.join(DATA_DIR, 'player_games.csv'))

pg[['game_id', 'player_id', 'date']] = (
    pg[['game_id', 'player_id', 'date']].astype(str))

# book picks up here:

pg.mean()
pg.max()

# Axis
pg[['shots', 'goals', 'assists', 'hits']].mean(axis=0)
pg[['shots', 'goals', 'assists', 'hits']].mean(axis=1).head()

# Summary functions on boolean columns
pg['defender_scored'] = (pg['pos'] == 'D') & (pg['goals'] > 0)

pg['defender_scored'].mean()
pg['defender_scored'].sum()

(pg['pen_min'] > 20).any()
(pg['time_ice'] > 0).all()

pg['time_ice'].min()

(pg[['goals', 'assists']] > 2).any(axis=1)

(pg[['goals', 'assists']] > 2).any(axis=1).sum()

(pg[['time_ice_sh', 'time_ice_pp']] == 0).all(axis=1).sum()

# Other misc built-in summary functions
pg['pos'].value_counts()

pg['pos'].value_counts(normalize=True)

pd.crosstab(pg['team'], pg['pos']).head()
