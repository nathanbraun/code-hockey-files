import pandas as pd
import numpy as np
import math
from textwrap import dedent
import statsmodels.formula.api as smf
from os import path

DATA_DIR = './data'

df = pd.read_csv(path.join(DATA_DIR, 'shots.csv'))

# wrist          3696
# snap           1081
# slap            998
# backhand        602
# tip-in          398
# deflected       158
# wrap-around      70

df['dist_sq'] = df['dist'] ** 2
df['goal'] = df['goal'].astype(int)
df['slap'] = df['shot_type'] == 'slap'
# shots = ['wrist', 'snap', 'slap', 'backhand', 'tip-in', 'deflected', 'wrap-around']

#########################
# holding things constant
#########################

# slap: no effect (p value == 0)
model = smf.ols(formula=
        """
        goal ~ slap
        """, data=df)
results = model.fit()
results.summary2()

df.groupby('slap')['dist'].mean()

# fine but slap shots are far away
model = smf.ols(formula=
        """
        goal ~ slap + dist
        """, data=df)
results = model.fit()
results.summary2()

0.1224 -0.0015*40
0.1224 -0.0015*40 + 0.0238

###############
# fixed effects
###############
pd.get_dummies(df['pos']).head()

model = smf.ols(formula="goal ~ C(shot_type) + dist + dist_sq", data=df)
results = model.fit()
results.summary2()

model = smf.ols(
    formula="goal ~ C(shot_type, Treatment(reference='wrist')) + dist + dist_sq", data=df)
results = model.fit()
results.summary2()

df['shot_type'].value_counts()

####################
# squaring variables
####################

df['dist2'] = df['dist'] ** 2
model = smf.ols(formula="goal ~ dist + dist2", data=df)
results = model.fit()
results.summary2()

# cubed variables
df['dist3'] = df['dist'] ** 3
model = smf.ols(formula="goal ~ dist + dist2 + dist3", data=df)
results = model.fit()
results.summary2()

#############
# natural log
#############
df['ln_dist'] = np.log(df['dist'].apply(lambda x: max(x, 0.5)))

model = smf.ols(formula='goal ~ ln_dist', data=df)
results = model.fit()
results.summary2()

#############
# intractions
#############
df['is_backhand'] = df['shot_type'] == 'backhand'

model = smf.ols(formula=
        """
        goal ~ dist + is_backhand + dist:is_backhand
        """, data=df)
results = model.fit()
results.summary2()

#######
# logit
#######
model = smf.logit(formula=
        """
        goal ~ dist + is_backhand + dist:is_backhand
        """, data=df)
logit_results = model.fit()
logit_results.summary2()

def prob_goal_logit(dist, is_backhand):
    b0, b1, b2, b3  = logit_results.params
    value = (b0 + b1*is_backhand + b2*dist + b3*dist*is_backhand)
    return 1/(1 + math.exp(-value))

prob_goal_logit(20, 1)
prob_goal_logit(100, 0)
prob_goal_logit(100, 1)
