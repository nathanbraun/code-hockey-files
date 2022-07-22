"""
Answers to the end of chapter exercises for Summary Stats and Visualization
chapter.
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from os import path

# change this to the directory where the csv files that come with the book are
# stored
# on Windows it might be something like 'C:/mydir'

# DATA_DIR = '/Users/nathan/fantasybook/data'
DATA_DIR = './data'

dfpg = pd.read_csv(path.join(DATA_DIR, 'player_games.csv'))  

###############################################################################
# 6.1a
###############################################################################

g = (sns.FacetGrid(dfpg)
     .map(sns.kdeplot, 'time_ice_pp', shade=True))
g.fig.subplots_adjust(top=0.9)
g.fig.suptitle('Distribution of Power Play Time')
g.savefig('./solutions-to-exercises/6-1a.png')

# 6.1b
g = (sns.FacetGrid(dfpg, hue='pos')
    .map(sns.kdeplot, 'time_ice_pp', shade=True))
g.fig.subplots_adjust(top=0.9)
g.fig.suptitle('Distribution of Power Play Time by Position B')
g.savefig('./solutions-to-exercises/6-1b.png')

# 6.1c
g = (sns.FacetGrid(dfpg, col='pos', col_wrap=3)
    .map(sns.kdeplot, 'time_ice_pp', shade=True))
g.fig.subplots_adjust(top=0.8)
g.fig.suptitle('Distribution of Power Play Time by Position C')
g.savefig('./solutions-to-exercises/6-1c.png')

# 6.1d
g = (sns.FacetGrid(dfpg, col='pos', hue='pos', col_wrap=3)
    .map(sns.kdeplot, 'time_ice_pp', shade=True))
g.fig.subplots_adjust(top=0.8)
g.fig.suptitle('Distribution of Power Play Time by Position D')
g.savefig('./solutions-to-exercises/6-1d.png')

# 6.1e
g = (sns.FacetGrid(dfpg, col='team', col_wrap=6)
    .map(sns.kdeplot, 'time_ice_pp', shade=True))
g.fig.subplots_adjust(top=0.9)
g.fig.suptitle('Distribution of Power Play Time by Team D')
g.savefig('./solutions-to-exercises/6-1e.png')

# #### 6.2
# 6.2a
g = sns.relplot(x='time_ice_pp', y='time_ice_sh', data=dfpg)
g.fig.subplots_adjust(top=0.9)
g.fig.suptitle('Power Play vs. Short Handed Time')
g.savefig('./solutions-to-exercises/6-2a.png')

# 6.2b
dfpg[['time_ice_pp', 'time_ice_sh']].corr()

