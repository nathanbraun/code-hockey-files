from os import path
import pandas as pd

# change this to the directory where the csv files that come with the book are
# stored
# on Windows it might be something like 'C:/mydir'

BB = '/Users/nathanbraun/fantasymath/basketball/nba_api/data'
SO = '/Users/nathanbraun/fantasymath/soccer/worldcup/data'
HY = '/Users/nathanbraun/fantasymath/hockey/data'

##############
# Loading data
##############
shots = pd.read_csv(path.join(HY, 'shots.csv'))

type(shots)

##################################
# DataFrame methods and attributes
##################################
shots.head()

shots.columns

shots.shape

#################################
# Working with subsets of columns
#################################
# A single column
shots['name'].head()

type(shots['name'])

shots['name'].to_frame().head()
type(shots['name'].to_frame().head())

# Multiple columns
shots[['name', 'pos', 'hand', 'goal']].head()

type(shots[['name', 'pos', 'hand', 'goal']])

# shots['name', 'pos', 'hand', 'goal'].head() # commented out because it throws an error

##########
# Indexing
##########
shots[['name', 'pos', 'hand', 'goal']].head()

shots.set_index('play_id').head()

# Copies and the inplace argument
shots.head()  # note: player_id not the index, even though we just set it

shots.set_index('play_id', inplace=True)
shots.head()  # now player_id is index

# alternate to using inplace, reassign adp
# reload shots with default 0, 1, ... index
shots = pd.read_csv(path.join(HY, 'shots.csv'))
shots = shots.set_index('play_id')
shots.head()  # now player_id is index

shots.reset_index().head()

#############################
# Indexes keep things aligned
#############################
shots_ot = shots.loc[shots['period_type'] == 'OVERTIME', ['name', 'hand', 'goal']]
shots_ot.head()

shots_ot.sort_values('name', inplace=True)
shots_ot.head()

# assigning a new column
shots_ot['pos'] = shots['pos']
shots_ot.head()

# has the same index as shots_ot and shots['pos']
shots['pos'].head()

#################
# Outputting data
#################
shots_ot.to_csv(path.join(HY, 'shots_ot.csv'))

shots_ot.to_csv(path.join(HY, 'shots_ot_no_index.csv'), index=False)

