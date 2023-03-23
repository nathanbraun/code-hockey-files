import pandas as pd
from os import path

# change this to the directory where the csv files that come with the book are
# stored
# on Windows it might be something like 'C:/mydir'

DATA_DIR = './data'

# load player-game data
pg = pd.read_csv(path.join(DATA_DIR, 'player_games.csv'))

# book picks up here:

# creating and modifying columns
pg['penalty_time'] = 2
pg[['name', 'shots', 'goals', 'penalty_time']].head()

pg['penalty_time'] = 5
pg[['name', 'shots', 'goals', 'penalty_time']].head()

# math and number columns
pg['net_penalty_min'] = (pg['time_ice_pp'] - pg['time_ice_sh'])

pg[['name', 'game_id', 'net_penalty_min']].head()

import numpy as np  # note: normally you'd import this at the top of the file

pg['biggest_impact'] = np.abs(pg['plus_minus'])

pg['ln_min'] = np.log(pg['time_ice'])

pg['rink_width'] = 85

pg[['name', 'game_id', 'rink_width']].sample(5)

# string Columns
pg['name'].str.upper().sample(5)

pg['name'].str.replace('. ', '-').sample(5)

(pg['name'] + ', ' + pg['pos'] + ' - ' + pg['team']).sample(5)

pg['name'].str.replace('.', '').str.lower().sample(5)

# boolean columns
pg['is_defender'] = (pg['pos'] == 'D')
pg[['name', 'is_defender']].sample(5)

pg['is_a_w'] = (pg['pos'] == 'LW') | (pg['pos'] == 'RW')
pg['balanced_off'] = (pg['goals'] > 0) & (pg['assists'] > 0)
pg['is_not_a_w'] = ~((pg['pos'] == 'LW') | (pg['pos'] == 'RW'))

(pg[['goals', 'assists']] > 0).sample(5)

# Applying functions to columns
def is_e_metro(team):
  """
  Takes some string named team ('WSH', 'CHI' etc) and checks whether they're in
  the Metropolitan division.
  """
  return team in ['WSH', 'NYI', 'PIT', 'CAR', 'CBJ', 'PHI', 'NYR', 'NJD']

pg['is_e_metro'] = pg['team'].apply(is_e_metro)

pg[['name', 'team', 'is_e_metro']].sample(5)

pg['is_e_metro_alternate'] = pg['team'].apply(
    lambda x: x in ['WSH', 'NYI', 'PIT', 'CAR', 'CBJ', 'PHI', 'NYR', 'NJD'])

# Dropping Columns
pg.drop('is_e_metro_alternate', axis=1, inplace=True)

# Renaming Columns
pg.columns = [x.upper() for x in pg.columns]

pg.head()

pg.columns = [x.lower() for x in pg.columns]

pg.rename(columns={'fo': 'faceoffs'}, inplace=True)

# missing data
pg['shot_pct'] = pg['goals']/pg['shots']
pg[['name', 'team', 'goals', 'shots', 'shot_pct']].sample(5)

pg['shot_pct'].isnull().head(10)
pg['shot_pct'].notnull().head(10)

pg['shot_pct'].fillna(-99).head(10)

# Changing column types
pg['date'].sample(5)

date = '20200215'

year = date[0:4]
month = date[4:6]
day = date[6:8]

year
month
day

# pg['month'] = pg['date'].str[4:6]  # commented out since it gives an error

pg['month'] = pg['date'].astype(str).str[4:6]
pg[['name', 'team', 'month', 'date']].sample(5)

pg['month'].astype(int).sample(5)

pg.dtypes.head()
