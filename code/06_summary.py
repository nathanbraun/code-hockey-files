import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from os import path

# change this to the directory where the csv files that come with the book are
# stored
# on Windows it might be something like 'C:/mydir'

DATA_DIR = '/Users/nathanbraun/fantasymath/hockey/data'
FIG_DIR = '/Users/nathanbraun/fantasymath/hockey'
# DATA_DIR = '/Users/nathan/fantasybook/data'

df = pd.read_csv(path.join(DATA_DIR, 'shots.csv'))
df['goal'] = df['event'] == 'Goal'

###############
# summary stats
###############

# book picks up here:

# quantile function and describe

df['dist'].quantile(.9)
df[['dist', 'st_y']].describe()

##########
# plotting
##########

# basic displot
g = (sns.FacetGrid(df)
     .map(sns.kdeplot, 'dist', shade=True))
plt.show()


# all on one line
g = sns.FacetGrid(df).map(sns.kdeplot, 'dist', shade=True)
plt.show()

# on seperate lines so it's clearer it's a two step process
g = (sns.FacetGrid(df)
     .map(sns.kdeplot, 'dist', shade=True))

# density plot of standard points by goal or not
g = (sns.FacetGrid(df, hue='goal')
     .map(sns.kdeplot, 'dist', shade=True)
     .add_legend())
plt.show()

# density plot of standard points by position and week
g = (sns.FacetGrid(df, hue='goal', col='shot_type', height=2, col_wrap=3)
     .map(sns.kdeplot, 'dist', shade=True)
     .add_legend())
g.set(xlim=(0, 80), ylim=(0, 0.15))
plt.show()

#########################
# processing for plotting
#########################

# example of reshaping data to get it into the shape we want

# thinking about seaborn: specify seperate columns for columns, hue (color),
# thing we're plotting (points)
# so we need points in one column, then another type for scoring type

games = pd.read_csv(path.join(DATA_DIR, 'games.csv'))

# book picks up again here:
games[['home_team', 'away_team', 'home_goals', 'away_goals']].head()  # have this

def home_away_goals_df(_df, location):
    _df = _df[['game_id', 'date_time_gmt', f'{location}_team', f'{location}_goals']]
    _df.columns = ['game_id', 'date', 'team', 'goals']
    _df['location'] = location
    return _df

home_away_goals_df(games, 'home').head()

goals_long = pd.concat([
    home_away_goals_df(games, loc) for loc in ['home', 'away']],
    ignore_index=True)

# now can plot points by scoring system and position
g = (sns.FacetGrid(goals_long, hue='location')
     .map(sns.kdeplot, 'goals', shade=True))
g.add_legend()
plt.show()

#################################
# relationships between variables
#################################

players = pd.read_csv(path.join(DATA_DIR, 'players.csv'))
players.rename(columns={'height_in': 'height'}, inplace=True)

height_split = players['height'].str.replace('"', '').str.split("'")

feet = height_split.apply(lambda x: x[0]).astype(int)
inches = height_split.apply(lambda x: x[-1]).astype(int)
players['height_in'] = feet*12 + inches

# player weight vs height
sns.relplot(x='weight_lb', y='height_in', data=players)
plt.show()

# jitter
players['height_j'] = np.random.uniform(
    players['height_in'] - 0.5, players['height_in'] + 0.5)
players['weight_j'] = np.random.uniform(
    players['weight_lb'] - 0.5, players['weight_lb'] + 0.5)

sns.relplot(x='weight_j', y='height_j', data=players)
plt.show()

# add some hue
sns.relplot(x='weight_j', y='height_j', data=players, hue='pos')
plt.show()

# cols by pos too
sns.relplot(x='weight_j', y='height_j', data=players, col='pos',
            hue='pos', col_wrap=4)
plt.show()

# try contour
sns.displot(x='weight_lb', y='height_in', data=players, col='pos', hue='pos',
            kind='kde')
plt.show()

#############
# correlation
#############

import datetime as dt

# players['age'] = 2021 - players['birth_date'].str[:4].astype(int)
players['age'] = (dt.datetime.now() - pd.to_datetime(players['birth_date'])).dt.days/365

players[['weight_lb', 'height_in', 'age']].corr()

# scatter plot of 0.04 correlation
g = sns.relplot(x='age', y='height_j', data=players)
plt.show()

# also good lesson in outliers
players.query("name != 'Z. Chara'")[['weight_lb', 'height_in', 'age']].corr()

# scatter plot of 0.705 correlation
g = sns.relplot(x='weight_j', y='height_j', data=players)
plt.show()

# scatter plot of -0.975 correlation
df[['st_x', 'st_y', 'dist']].corr()

g = sns.relplot(x='st_x', y='dist', data=df)
plt.show()

########################
# line plots with python
########################

teams = pd.read_csv(path.join(DATA_DIR, 'teams.csv'))

goals_long['month'] = (goals_long['date']
                       .astype(str).str[:7])

df_gt = (pd.merge(goals_long, teams[['team', 'division', 'conference']])
         .sort_values('month'))

# let's look at scoring by month
g = sns.relplot(x='month', y='goals', kind='line', data=df_gt)
plt.show()

# add hue
g = sns.relplot(x='month', y='goals', kind='line', data=df_gt, hue='conference')
plt.show()

# just a line
max_pts = (df_gt.groupby(['conference', 'month'], as_index=False)['goals'].max())

g = sns.relplot(x='month', y='goals', kind='line', data=max_pts,
                hue='conference')

##############
# plot options
##############

# basic plot
g = (sns.FacetGrid(df, hue='goal', col='shot_type')
     .map(sns.kdeplot, 'dist', shade=True))
plt.show()


# wrap columns
g = (sns.FacetGrid(df, hue='goal', col='shot_type', col_wrap=3)
     .map(sns.kdeplot, 'dist', shade=True))
plt.show()

# adding a title
g.fig.subplots_adjust(top=0.9) # adding a title
g.fig.suptitle('Distribution of Shot Distances by Type, Made')

# modifying options
g.set(xlim=(0, 80), ylim=(0, 0.15))
plt.show()

g.set_xlabels('Distance')
g.set_ylabels('Density')

# saving
g.savefig(path.join(FIG_DIR, 'shot_dist_type_made.png'))

#############
# shot charts
#############

map_img = mpimg.imread(path.join(FIG_DIR, 'hockey_rink.png'))

# scatter plot with rink overlay
g = sns.relplot(data=df, x='st_x', y='st_y', kind='scatter', s=10)
for ax in g.fig.axes:
    ax.imshow(map_img, zorder=0, extent=[-110, 110, -42, 42])
g.set(yticks=[], xticks=[], xlabel=None, ylabel=None)
g.despine(left=True, bottom=True)
plt.show()

# how about a bit of jitter
df['x_j'] = np.random.uniform(df['st_x'] - 0.5, df['st_x'] + 0.5)
df['y_j'] = np.random.uniform(df['st_y'] - 0.5, df['st_y'] + 0.5)

g = sns.relplot(data=df, x='x_j', y='y_j', kind='scatter', s=10)
for ax in g.fig.axes:
    ax.imshow(map_img, zorder=0, extent=[-100, 100, -42, 42])
g.set(yticks=[], xticks=[], xlabel=None, ylabel=None)
g.despine(left=True, bottom=True)
plt.show()

# add some hue
df['goal'] = df['event'] == 'Goal'

g = sns.relplot(data=df, x='x_j', y='y_j', kind='scatter', hue='goal',
                style='goal', s=10)
for ax in g.fig.axes:
    ax.imshow(map_img, zorder=0, extent=[-105, 105, -42, 42])
g.set(yticks=[], xticks=[], xlabel=None, ylabel=None)
g.despine(left=True, bottom=True)
plt.show()

# and columns
g = sns.relplot(data=df, x='x_j', y='y_j', kind='scatter', hue='goal',
                style='goal', col='shot_type', col_wrap=3, s=10)
for ax in g.fig.axes:
    ax.imshow(map_img, zorder=0, extent=[-105, 105, -42, 42])
g.set(yticks=[], xticks=[], xlabel=None, ylabel=None)
g.despine(left=True, bottom=True)
plt.show()

# or teams
g = sns.relplot(data=df, x='x_j', y='y_j', kind='scatter', hue='goal',
                style='goal', col='team', col_wrap=5, s=10)
for ax in g.fig.axes:
    ax.imshow(map_img, zorder=0, extent=[-105, 105, -42, 42])
g.set(yticks=[], xticks=[], xlabel=None, ylabel=None)
g.despine(left=True, bottom=True)
plt.show()
g.savefig(path.join(FIG_DIR, 'shot_chart_teams.png'))

# now let's try a contour plot
g = (sns.FacetGrid(df)
     .map(sns.kdeplot, 'st_x', 'st_y', alpha=0.5)
     .add_legend())
for ax in g.fig.axes:
    ax.imshow(map_img, zorder=0, extent=[-105, 105, -42, 42])
g.set(yticks=[], xticks=[], xlabel=None, ylabel=None)
g.despine(left=True, bottom=True)
plt.show()

# add some rows, columns
g = (sns.FacetGrid(df, row='shot_type', col='hand', hue='hand')
     .map(sns.kdeplot, 'st_x', 'st_y', alpha=0.5)
     .add_legend())
for ax in g.fig.axes:
    ax.imshow(map_img, zorder=0, extent=[-105, 105, -42, 42])
g.set(yticks=[], xticks=[], xlabel=None, ylabel=None)
g.despine(left=True, bottom=True)
plt.show()

