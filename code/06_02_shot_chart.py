
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from os import path

# change this to the directory where the csv files that come with the book are
# stored
# on Windows it might be something like 'C:/mydir'

%matplotlib qt
DATA_DIR = './data'

# load data
dfs = pd.read_csv(path.join(DATA_DIR, 'shots.csv'))

# process data
dfs['goal'] = dfs['event'] == 'Goal'
dfs['period_min'] = (60*20 - dfs['period_time_remaining'])//60

# book picks up here

dfs[['name', 'dist', 'shot_type', 'goal', 'st_x', 'st_y']].head(5)

# shot data
g = sns.relplot(data=dfs, x='st_x', y='st_y', kind='scatter', s=10)
g.set(yticks=[], xticks=[], xlabel=None, ylabel=None)
g.despine(left=True, bottom=True)

map_img = mpimg.imread(path.join(DATA_DIR, 'hockey_rink.png'))

# scatter plot with rink overlay
g = sns.relplot(data=dfs, x='st_x', y='st_y', kind='scatter', s=10)
g.set(yticks=[], xticks=[], xlabel=None, ylabel=None)
g.despine(left=True, bottom=True)

for ax in g.fig.axes:
    ax.imshow(map_img, zorder=0, extent=[-110, 110, -42, 42])

# how about a bit of jitter
dfs['xj'] = np.random.uniform(dfs['st_x'] - 0.5, dfs['st_x'] + 0.5)
dfs['yj'] = np.random.uniform(dfs['st_y'] - 0.5, dfs['st_y'] + 0.5)

g = sns.relplot(data=dfs, x='xj', y='yj', kind='scatter', s=10)
for ax in g.fig.axes:
    ax.imshow(map_img, zorder=0, extent=[-100, 100, -42, 42])
g.set(yticks=[], xticks=[], xlabel=None, ylabel=None)
g.despine(left=True, bottom=True)

def shot_chart(df, **kwargs):
    g = sns.relplot(data=df, x='xj', y='yj', kind='scatter', **kwargs)
    g.set(yticks=[], xticks=[], xlabel=None, ylabel=None)
    g.despine(left=True, bottom=True)

    for ax in g.fig.axes:
        ax.imshow(map_img, zorder=0, extent=[-110, 110, -42, 42])

    return g

# kwargs
def add2(num1, num2):
    return num1 + num2

# commented out because it throws an error
# add2(num1=4, num2=5, num3=1)

def add2_flexible(num1, num2, **kwargs):
    return num1 + num2

add2_flexible(num1=4, num2=5, num3=1, num4=4)

g = shot_chart(dfs, hue='goal', style='goal', s=20, height=8, legend=False)

# then can set title etc with g

# contour plots
g = (sns.FacetGrid(dfs, col='goal', row='shot_type', hue='goal')
     .map(sns.kdeplot, 'xj', 'yj', alpha=0.5, shade=True))
g.set(yticks=[], xticks=[], xlabel=None, ylabel=None)
g.despine(left=True, bottom=True)
for ax in g.fig.axes:
    ax.imshow(map_img, zorder=0, extent=[-110, 110, -42, 42])

# without shading
g = (sns.FacetGrid(dfs, col='goal', row='pos', hue='goal')
     .map(sns.kdeplot, 'xj', 'yj', alpha=0.5))
g.set(yticks=[], xticks=[], xlabel=None, ylabel=None)
g.despine(left=True, bottom=True)
for ax in g.fig.axes:
    ax.imshow(map_img, zorder=0, extent=[-110, 110, -42, 42])

