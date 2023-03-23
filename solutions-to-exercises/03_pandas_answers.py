"""
Answers to the end of chapter exercises for Pandas chapter.

Questions with written (not code) answers are inside triple quotes.
"""
###############################################################################
# PANDAS BASICS
###############################################################################

#######
# 3.0.1
#######
import pandas as pd
from os import path

DATA_DIR = './data'
games = pd.read_csv(path.join(DATA_DIR, 'games.csv'))

#######
# 3.0.2
#######
games50 = games.sort_values('date_time_gmt').head(50)

#######
# 3.0.3
#######
games.sort_values('home_goals', ascending=False, inplace=True)
games.head()

# Note: if this didn't work when you printed it on a new line in the REPL you
# probably forgot the `inplace=True` argument.

#######
# 3.0.4
#######
type(games.sort_values('home_goals'))  # it's a DataFrame

#######
# 3.0.5
#######
# a
game_simple = games[['date_time_gmt', 'home_team', 'away_team', 'home_goals',
    'away_goals']]

# b
game_simple = game_simple[['home_team', 'away_team', 'date_time_gmt',
    'home_goals', 'away_goals']]

# c
game_simple['game_id'] = games['game_id']

# d
games.to_csv(path.join(DATA_DIR, 'game_simple.txt'), sep='|')

###############################################################################
# COLUMNS
###############################################################################

#######
# 3.1.1
#######
import pandas as pd
from os import path

DATA_DIR = './data'
pg = pd.read_csv(path.join(DATA_DIR, 'player_games.csv'))

#######
# 3.1.2
#######
pg['net_takeaways'] = pg['takeaways'] - pg['giveaways']
pg['net_takeaways'].head()

#######
# 3.1.3
#######
pg['player_desc'] = pg['name'] + ' is the ' + pg['team'] + ' ' + pg['pos']
pg['player_desc'].head()

#######
# 3.1.4
#######
pg['is_pkiller'] = pg['time_ice_sh'] > pg['time_ice_pp']
pg['is_pkiller'].head()

#######
# 3.1.5
#######
pg['len_last_name'] = (pg['name']
                       .apply(lambda x: len(x.split('.')[-1])))
pg['len_last_name'].head()

#######
# 3.1.6
#######
pg['game_id'] = pg['game_id'].astype(str)

#######
# 3.1.7
#######
# a
pg.columns = [x.replace('_', ' ') for x in pg.columns]
pg.head()

# b
pg.columns = [x.replace(' ', '_') for x in pg.columns]
pg.head()

#######
# 3.1.8
#######
# a
pg['shooting_percentage'] = pg['goals']/pg['shots']
pg['shooting_percentage'].sample(5)

# b
"""
`'shooting_percentage'` is goals divided by shots. Since you can't divide by 0,
`shooting_percentage` is missing whenever a player had 0 shots.
"""

# To replace all the missing values with `-99`:
pg['shooting_percentage'].fillna(-99, inplace=True)
pg['shooting_percentage'].sample(5)

#######
# 3.1.9
#######
pg.drop('shooting_percentage', axis=1, inplace=True)
pg.head()

"""
If you forget the `axis=1` Pandas will try to drop the *row* with the
index value `'shooting_percentage'`. Since that doesn't exist, it'll throw an
error.

Without the `inplace=True`, Pandas just returns a new copy of `pg` without the
`'shooting_percentage'` column. Nothing happens to the original `pg`, though we
could reassign it if we wanted like this:
"""

# alternative to inplace=True
# pg = pg.drop('shooting_percentage', axis=1)


###############################################################################
# BUILT-IN FUNCTIONS
###############################################################################
#######
# 3.2.1
#######
import pandas as pd
from os import path

DATA_DIR = './data'
pg = pd.read_csv(path.join(DATA_DIR, 'player_games.csv'))

#######
# 3.2.2
#######
pg['pts1'] = pg['goals'] + pg['assists']

pg['pts2'] = pg[['goals', 'assists']].sum(axis=1)

(pg['pts1'] == pg['pts2']).all()

#######
# 3.2.3
#######

# a
pg[['shots', 'goals', 'time_ice']].mean()

# shots         1.770278
# goals         0.161111
# time_ice    991.306111

# b
((pg['goals'] >= 3) & (pg['pen_min'] == 0)).sum()  # 6

# c
(((pg['goals'] >= 3) & (pg['pen_min'] == 0)).sum())/pg.shape[0]  # 0.17%

# d
pg['goals_sh'].sum()  # 9

# e
pg['team'].value_counts()  # TBL - 216 times, DAL - 18 times

###############################################################################
# FILTERING
###############################################################################
#######
# 3.3.1
#######
import pandas as pd
from os import path

DATA_DIR = './data'
dfp = pd.read_csv(path.join(DATA_DIR, 'players.csv'))

#######
# 3.3.2
#######
# a
dfp_can1 = dfp.loc[dfp['nationality'] == 'CAN',
                ['name', 'pos', 'birth_city', 'birth_state_prov']]
dfp_can1.head()

# b
dfp_can2 = dfp.query("nationality == 'CAN'")[['name', 'pos', 'birth_city',
    'birth_state_prov']]
dfp_can2.head()

#######
# 3.3.3
#######
dfp_no_can = dfp.loc[dfp['nationality'] != 'CAN', ['name', 'pos', 'birth_city',
    'birth_state_prov', 'nationality']]
dfp_no_can.head()

#######
# 3.3.4
#######

# a
dfp[['team', 'birth_city', 'birth_state_prov']].duplicated().any()  # yes there are
dfp[['team', 'birth_city', 'birth_state_prov']].duplicated().sum()  # 34

# b
# flags ALL dups (not just 2nd) because passing keep=False
dups = dfp[['team', 'birth_city', 'birth_state_prov']].duplicated(keep=False)

dfp_dups = dfp.loc[dups]
dfp_nodups = dfp.loc[~dups]

#######
# 3.3.5
#######
import numpy as np

dfp['height_description'] = np.nan
dfp.loc[dfp['height_cm'] > 190, 'height_description'] = 'tall'
dfp.loc[dfp['height_cm'] < 180, 'height_description'] = 'short'
dfp[['height_cm', 'height_description']].sample(5)

#######
# 3.3.6
#######
# a
dfp_no_desc1 = dfp.loc[dfp['height_description'].isnull()]

# b
dfp_no_desc2 = dfp.query("height_description.isnull()")

###############################################################################
# GRANULARITY
###############################################################################
#######
# 3.4.1
#######
"""
Usually you can only shift your data from more (play by play) to less (game)
granular, which necessarily results in a loss of information. If I go from
knowing whether or not Crosby made any particiular shot to just knowing how
many goals he scored total, that's a loss of information.
"""

#######
# 3.4.2
#######

# a
import pandas as pd
from os import path

DATA_DIR = './data'
dfpg = pd.read_csv(path.join(DATA_DIR, 'player_games.csv'))

# b
dfpg.groupby('player_id')['shots', 'goals'].mean()

# c
player_ave = dfpg.groupby('player_id')['shots', 'goals'].mean()

(player_ave['shots'] > 4).mean()  # 1.45%

#######
# 3.4.3
#######

# a
dftg = dfpg.groupby(['team', 'game_id']).agg(
    total_goals = ('goals', 'sum'),
    total_assists = ('assists', 'sum'),
    total_shots = ('shots', 'sum'),
    nplayed = ('player_id', 'count'))

dftg.head()

# b
dftg.reset_index(inplace=True)

# c
dftg['no_goals'] = dftg['total_goals'] == 0
dftg.groupby('no_goals')['total_shots'].mean()

# d
dftg.groupby('team')['game_id'].count()
dftg.groupby('team')['game_id'].sum()

"""
Count counts the number of non missing (non `np.nan`) values. This is different
than `sum` which adds up the values in all of the columns. The only time
`count` and `sum` would reliably return the same thing is if you had a column
filled with 1s without any missing values.

We want to use count. Sum doesn't make any sense.
"""

#######
# 3.4.4
#######
"""
Stacking is when you change the granularity in your data, but shift information
from rows to columns (or vis versa) so it doesn't result in any loss on
information.
"""

###############################################################################
# COMBINING DATAFRAMES
###############################################################################
#######
# 3.5.1
#######
# a
import pandas as pd
from os import path

DATA_DIR = './data'
df_name = pd.read_csv(path.join(DATA_DIR, 'problems/combine1', 'name.csv'))
df_fo = pd.read_csv(path.join(DATA_DIR, 'problems/combine1', 'fo.csv'))
df_poss = pd.read_csv(path.join(DATA_DIR, 'problems/combine1', 'poss.csv'))
df_shot = pd.read_csv(path.join(DATA_DIR, 'problems/combine1', 'shot.csv'))

# b
df_comb1 = pd.merge(df_name, df_fo, how='left')
df_comb1 = pd.merge(df_comb1, df_poss, how='left')
df_comb1 = pd.merge(df_comb1, df_shot, how='left')

df_comb1 = df_comb1.fillna(0)

# c
df_comb2 = pd.concat([df_name.set_index(['player_id', 'game_id']),
                      df_fo.set_index(['player_id', 'game_id']),
                      df_poss.set_index(['player_id', 'game_id']),
                      df_shot.set_index(['player_id', 'game_id'])], join='outer',
                     axis=1)

df_comb2 = df_comb2.fillna(0)

# d
"""
Which is better is somewhat subjective, but I generally prefer `concat` when
combining three or more DataFrames because you can do it all in one step.

Note `merge` gives a little more fine grained control over how you merge (left,
or outer) vs `concat`, which just gives you inner vs outer.

Note also we have to set the index equal to game and player id before
concating.
"""

########
# 3.5.2a
########
import pandas as pd
from os import path

DATA_DIR = './data'
df_c = pd.read_csv(path.join(DATA_DIR, 'problems/combine2', 'c.csv'))
df_d = pd.read_csv(path.join(DATA_DIR, 'problems/combine2', 'd.csv'))
df_lw = pd.read_csv(path.join(DATA_DIR, 'problems/combine2', 'lw.csv'))
df_rw = pd.read_csv(path.join(DATA_DIR, 'problems/combine2', 'rw.csv'))

# b
df = pd.concat([df_c, df_d, df_lw, df_rw], ignore_index=True)

#######
# 3.5.3
#######
# a
import pandas as pd
from os import path

DATA_DIR = './data'
dft = pd.read_csv(path.join(DATA_DIR, 'teams.csv'))

# b
for conf in ['Eastern', 'Western']:
    (dft
        .query(f"conference == '{conf}'")
        .to_csv(path.join(DATA_DIR, f'dft_{conf}.csv'), index=False))

# c
df = pd.concat([pd.read_csv(path.join(DATA_DIR, f'dft_{conf}.csv'))
    for conf in ['Eastern', 'Western']], ignore_index=True)

