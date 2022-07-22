import pandas as pd
import datetime as dt
import numpy as np
import seaborn as sns
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from os import path

# change this to the directory where the csv files that come with the book are
# stored
# on Windows it might be something like 'C:/mydir'

DATA_DIR = './data'
FIG_DIR = './fig'
# DATA_DIR = '/Users/nathan/fantasybook/data'

# load data
dfs = pd.read_csv(path.join(DATA_DIR, 'shots.csv'))
dfg = pd.read_csv(path.join(DATA_DIR, 'games.csv')).sort_values('date_time_gmt')
dfp = pd.read_csv(path.join(DATA_DIR, 'players.csv'))
dft = pd.read_csv(path.join(DATA_DIR, 'teams.csv'))
dfpg = pd.read_csv(path.join(DATA_DIR, 'player_games.csv'))

# process data
dfs['goal'] = dfs['event'] == 'Goal'
dfs['period_min'] = (60*20 - dfs['period_time_remaining'])//60

dfp.rename(columns={'height_in': 'height'}, inplace=True)
height_split = dfp['height'].str.replace('"', '').str.split("'")
feet = height_split.apply(lambda x: x[0]).astype(int)
inches = height_split.apply(lambda x: x[-1]).astype(int)
dfp['height_in'] = feet*12 + inches

dfp['age'] = (dt.datetime.now() -
    pd.to_datetime(dfp['birth_date'])).dt.days/365

###############
# summary stats
###############

# book picks up here:

# quantile function and describe

dfs['dist'].quantile(.9)
dfs[['dist', 'period']].describe()

dfpg['shots'].value_counts(normalize=True).sort_index().head(10)

##########
# plotting
##########

# basic displot
# all on one line
g = sns.FacetGrid(dfs).map(sns.kdeplot, 'dist', shade=True)

# on seperate lines so it's clearer it's a two step process
g = (sns.FacetGrid(dfs)
     .map(sns.kdeplot, 'dist', shade=True))

# hue - density plot of standard points by goal or not
g = (sns.FacetGrid(dfs, hue='shot_type')
    .map(sns.kdeplot, 'dist', shade=True)
    .add_legend())

# col - goal or not
g = (sns.FacetGrid(dfs, hue='shot_type', col='goal')
    .map(sns.kdeplot, 'dist', shade=True)
    .add_legend())

# reversed
g = (sns.FacetGrid(dfs, hue='goal', col='shot_type')
    .map(sns.kdeplot, 'dist', shade=True)
    .add_legend())

# density plot of standard points by position and week
g = (sns.FacetGrid(dfs, hue='goal', col='shot_type', height=2, col_wrap=3)
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

# book picks up again here:
dfg[['date_time_gmt', 'home_team', 'away_team', 'home_goals',
    'away_goals']].head()  # have this

def home_away_goals_df(df, location):
    df = df[['game_id', 'date_time_gmt', f'{location}_team', f'{location}_goals']]
    df.columns = ['game_id', 'date_time_gmt', 'team', 'goals']
    df['location'] = location
    return df

home_away_goals_df(dfg, 'home').head()

goals_long = pd.concat([
    home_away_goals_df(dfg, loc) for loc in ['home', 'away']],
    ignore_index=True)

g = (sns.FacetGrid(goals_long, hue='location')
     .map(sns.kdeplot, 'goals', shade=True))
g.add_legend()

# jittering
import random

random.uniform()

[random.gauss(0, 1) for _ in range(10)]

goals_long['jgoals'] = (
    goals_long['goals'].apply(lambda x: x + random.gauss(0, 1)))

g = (sns.FacetGrid(goals_long, hue='location')
     .map(sns.kdeplot, 'jgoals', shade=True)
     .add_legend())

#################################
# relationships between variables
#################################

# player weight vs height
sns.relplot(x='weight_lb', y='height_in', data=dfp)

# jitter
dfp['jheight'] = (dfp['height_in']
                      .apply(lambda x: x + random.gauss(0, 1)))

dfp['jweight'] = (dfp['weight_lb']
                      .apply(lambda x: x + random.gauss(0, 1)))

sns.relplot(x='jweight', y='jheight', data=dfp)

# add some hue
sns.relplot(x='jweight', y='jheight', data=dfp, hue='pos')

# cols by pos too
sns.relplot(x='jweight', y='jheight', data=dfp, col='pos',
            hue='pos', col_wrap=4)

# dist more effective?
g = (sns.FacetGrid(dfp, hue='team', col='team', col_wrap=5)
    .map(sns.kdeplot, 'jweight', shade=True))

# try contour
g = (sns.FacetGrid(dfp, col='pos', hue='pos', col_wrap=2)
     .map(sns.kdeplot, 'weight_lb', 'height_in', shade=True))

# without shading
g = (sns.FacetGrid(dfp, col='pos', hue='pos')
     .map(sns.kdeplot, 'weight_lb', 'height_in'))

#############
# correlation
#############

# players['age'] = 2021 - players['birth_date'].str[:4].astype(int)
dfp[['weight_lb', 'height_in', 'age']].corr()

# scatter plot of 0.04 correlation
g = sns.relplot(x='age', y='jheight', data=dfp)

# also good lesson in outliers
dfp.query("name != 'Z. Chara'")[['weight_lb', 'height_in', 'age']].corr()

# scatter plot of 0.705 correlation
g = sns.relplot(x='jweight', y='jheight', data=dfp)
plt.show()

########################
# line plots with python
########################

goals_long['month'] = (goals_long['date_time_gmt']
                       .astype(str).str[:7])

dfgt = (pd.merge(goals_long, dft[['team', 'division', 'conference']])
         .sort_values('month'))

# book picks up again here:

# let's look at scoring by month
g = sns.relplot(x='month', y='goals', kind='line', hue='division', data=dfgt)

dfgt.query("month == '2019-10' & division == 'Atlantic'")[['game_id',
    'date_time_gmt', 'team', 'location', 'month', 'goals']].head()

# just a line
max_goals = (dfgt.groupby(['division', 'month'], as_index=False)['goals'].max())

g = sns.relplot(x='month', y='goals', kind='line', data=max_goals,
                hue='division')

# other line plot
g = sns.relplot(x='period_min', y='dist', kind='line', hue='pos',
                data=dfs.query("period <= 3"), row='period')

##############
# plot options
##############

# basic plot
g = (sns.FacetGrid(dfs, col='shot_type', hue='shot_type')
     .map(sns.kdeplot, 'dist', shade=True))

# wrap columns
g = (sns.FacetGrid(dfs, col='shot_type', hue='shot_type', col_wrap=3)
     .map(sns.kdeplot, 'dist', shade=True))

# adding a title
g.fig.subplots_adjust(top=0.9) # adding a title
g.fig.suptitle('Distribution of Shot Distance by Type')

# modifying options
g.set(xlim=(0, 80))
plt.show()

g.set_xlabels('Distance')
g.set_ylabels('Density')

# saving
g.savefig(path.join(FIG_DIR, 'shot_dist_type_made.png'))
