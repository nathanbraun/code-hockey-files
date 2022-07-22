import pandas as pd
from os import path

# change this to the directory where the csv files that come with the book are
# stored
# on Windows it might be something like 'C:/mydir'

DATA_DIR = './data'

# TODO standardize pp/sh terminology

pg = pd.read_csv(path.join(DATA_DIR, 'player_games.csv'))  # player-game
games = pd.read_csv(path.join(DATA_DIR, 'games.csv'))  # game info
player = pd.read_csv(path.join(DATA_DIR, 'players.csv')) # player info

# player game data
pg[['player_id', 'game_id', 'name', 'team', 'shots', 'goals']].head(5)

# player table
player[['player_id', 'name', 'team', 'hand']].head()

# Merge Question 1. What columns are you joining on?
pd.merge(pg, player[['player_id', 'hand']], on='player_id').head()

pp_df = pg[['game_id', 'player_id', 'pp_goals', 'time_ice_pp']]
sh_df = pg[['game_id', 'player_id', 'goals_sh', 'time_ice_sh']]

combined = pd.merge(pp_df, sh_df, on=['player_id', 'game_id'])
combined.head()

# Merge Question 2. Are you doing a 1:1, 1:many (or many:1), or many:many
# join?player.head()

player['player_id'].duplicated().any()

combined['player_id'].duplicated().any()

pd.merge(combined, player[['player_id', 'name', 'team', 'hand']]).head()

# pd.merge(combined, player, validate='1:1')  # this will fail since it's 1:m

# Merge Question 3. What are you doing with unmatched observations?
pp_df = pg.loc[pg['time_ice_pp'] > 0,
       ['game_id', 'player_id', 'pp_goals', 'time_ice_pp']]

sh_df = pg.loc[pg['time_ice_sh'] > 0,
          ['game_id', 'player_id', 'goals_sh', 'time_ice_sh']]

pp_df.shape
sh_df.shape

comb_inner = pd.merge(pp_df, sh_df)
comb_inner.shape

comb_left = pd.merge(pp_df, sh_df, how='left')
comb_left.shape

comb_left.head()

comb_outer = pd.merge(pp_df, sh_df, how='outer', indicator=True)
comb_outer.shape

comb_outer['_merge'].value_counts()

# More on pd.merge
# left_on and right_on
pp_df = pg.loc[pg['time_ice_pp'] > 0,
       ['game_id', 'player_id', 'pp_goals', 'time_ice_pp']]
pp_df.columns = ['game_id', 'pp_player_id', 'pp_goals', 'time_ice_pp']

sh_df = pg.loc[pg['time_ice_sh'] > 0,
          ['game_id', 'player_id', 'goals_sh', 'time_ice_sh']]
sh_df.columns = ['game_id', 'sh_player_id', 'goals_sh', 'time_ice_sh']

pd.merge(pp_df, sh_df, left_on=['game_id', 'pp_player_id'],
    right_on=['game_id', 'sh_player_id']).head()

# merging on index
max_pp_df = (pp_df
               .groupby('pp_player_id')
               .agg(max_pp_time = ('time_ice_pp', 'max'),
                    max_pp_goals =  ('pp_goals', 'max')))

max_pp_df.head()

pd.merge(pp_df, max_pp_df, left_on='pp_player_id', right_index=True).head()

#############
# pd.concat()
#############
pp_df = (pg.loc[pg['time_ice_pp'] > 0,
               ['game_id', 'player_id', 'time_ice_pp']]
         .set_index(['game_id', 'player_id']))

sh_df = (pg.loc[pg['time_ice_sh'] > 0,
          ['game_id', 'player_id', 'time_ice_sh']]
         .set_index(['game_id', 'player_id']))

pp_df.head()

pd.concat([pp_df, sh_df], axis=1).head()

even_df = (pg.loc[pg['time_ice_even'] > 0,
                  ['game_id', 'player_id', 'time_ice_even']]
         .set_index(['game_id', 'player_id']))

pd.concat([pp_df, sh_df, even_df], axis=1).head()

#### Combining DataFrames Vertically
centers = pg.loc[pg['pos'] == 'C']
wings = pg.loc[(pg['pos'] == 'LW') | (pg['pos'] == 'RW')]

centers.shape
wings.shape

pd.concat([centers, wings]).shape

centers_reset = centers.reset_index(drop=True)
wings_reset = wings.reset_index(drop=True)

centers_reset.head()

pd.concat([centers_reset, wings_reset]).sort_index().head()

pd.concat([centers_reset, wings_reset], ignore_index=True).sort_index().head()
