import pandas as pd
import numpy as np
from os import path

# change this to the directory where the csv files that come with the book are
# stored
# on Windows it might be something like 'C:/mydir'

DATA_DIR = './data'

# note: we're passing the index_col argument, which immediately setting the
# index to be the player_id column
dfp = pd.read_csv(path.join(DATA_DIR, 'players.csv'), index_col='player_id')

# Filtering

ovechkin_id = 8471214
dfp.loc[ovechkin_id]

oilers_ids = [8478402, 8477492, 8475197]

dfp.loc[oilers_ids]
dfp.loc[oilers_ids, ['name', 'height_in', 'height_cm', 'hand']]
dfp.loc[oilers_ids, 'name']

# Boolean Indexing
is_a_rw = dfp['pos'] == 'RW'

is_a_rw.head()

dfp_rw = dfp.loc[is_a_rw]

dfp_rw[['name', 'nationality', 'pos', 'hand']].head()

dfp_lw = dfp.loc[dfp['pos'] == 'LW']
dfp_lw[['name', 'nationality', 'pos', 'hand']].head()

is_a_d = dfp['pos'] == 'D'

dfp_not_d = dfp.loc[~is_a_d]

dfp_not_d[['name', 'nationality', 'pos', 'hand']].head()

# Duplicates
dfp.drop_duplicates(inplace=True)

dfp.drop_duplicates('pos')[['name', 'nationality', 'pos', 'hand']]

dfp.duplicated().head()

dfp['pos'].duplicated().head()

# Combining filtering with changing columns
dfp['height_local'] = np.nan
dfp.loc[dfp['nationality'] == 'USA', 'height_local'] = dfp['height_in']
dfp.loc[dfp['nationality'] != 'USA', 'height_local'] = dfp['height_cm']

dfp[['name', 'nationality', 'height_local', 'height_in', 'height_cm']].sample(5)

# Query
dfp.query("pos == 'C'").head()

dfp['is_a_d'] = dfp['pos'] == 'D'

dfp.query("is_a_d").head()

dfp.query("birth_state_prov.isnull()")[['name', 'nationality', 'birth_state_prov']].head()

# note: if getting an error on line above, try it with engine='python' like
# this
dfp.query("birth_state_prov.isnull()", engine='python')[['name', 'nationality', 'birth_state_prov']].head()
