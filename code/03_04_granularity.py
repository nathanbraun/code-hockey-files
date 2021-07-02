import pandas as pd
from os import path

# change this to the directory where the csv files that come with the book are
# stored
# on Windows it might be something like 'C:/mydir'

BB = '/Users/nathanbraun/fantasymath/basketball/nba_api/data'
SO = '/Users/nathanbraun/fantasymath/soccer/worldcup/data'
HY = '/Users/nathanbraun/fantasymath/hockey/data'

shots = pd.read_csv(path.join(HY, 'shots.csv'))  # shot data

# Granularity

# Grouping
shots.groupby('game_id').sum()

shots['attempt'] = 1

sum_cols = ['goal', 'attempt', 'missed_net']
shots.groupby('game_id').sum()[sum_cols]

shots.groupby('game_id').agg({
    'goal': 'sum',
    'attempt': 'count',
    'dist': ['mean', 'median']
})

shots.groupby('game_id').agg(
    goal = ('goal', 'sum'),
    attempt = ('attempt', 'count'),
    ave_dist = ('dist', 'mean'),
    med_dist = ('dist', 'median'))

shots_team = shots.groupby(['game_id', 'team']).agg(
    goal = ('goal', 'sum'),
    attempt = ('attempt', 'count'),
    ave_dist = ('dist', 'mean'),
    med_dist = ('dist', 'median'))

shots_team

# A note on multilevel indexing
shots_team.loc[[(2019020007, 'BUF'), (2019030001, 'BOS')]]

# Stacking and unstacking data
gd = shots.groupby(['game_id', 'team', 'goal'])['dist'].mean().reset_index()

gd_reshaped = gd.set_index(['game_id', 'team', 'goal']).unstack()
gd_reshaped.columns = ['no_goal', 'goal']

(gd_reshaped['no_goal'] - gd_reshaped['goal']).mean()

gd_reshaped_undo = gd_reshaped.stack()
gd_reshaped_undo.head()
