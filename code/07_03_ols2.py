import pandas as pd
import numpy as np
import math
from textwrap import dedent
import statsmodels.formula.api as smf
from os import path

DATA_DIR = '/Users/nathanbraun/fantasymath/hockey/data'

df = pd.read_csv(path.join(DATA_DIR, 'shots.csv'))

# wrist          3696
# snap           1081
# slap            998
# backhand        602
# tip-in          398
# deflected       158
# wrap-around      70

df['goal'] = df['goal'].astype(int)
shots = ['wrist', 'snap', 'slap', 'backhand', 'tip-in', 'deflected', 'wrap-around']

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

# fine but slap shots are far away
model = smf.ols(formula=
        """
        goal ~ slap + dist
        """, data=df)
results = model.fit()
results.summary2()

###############
# fixed effects
###############
pd.get_dummies(df['shot_type']).head()

model = smf.ols(formula="goal ~ C(shot_type) + dist", data=df)
results = model.fit()
results.summary2()

model = smf.ols(
    formula="goal ~ C(shot_type, Treatment(reference='wrist')) + dist", data=df)
results = model.fit()
results.summary2()

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
model = smf.ols(formula=
        """
        goal ~ C(shot_type) + ln_dist + ln_dist:slap
        """, data=df)
results = model.fit()
results.summary2()

#######
# logit
#######
model = smf.logit(formula=
        """
        goal ~ slap + ln_dist + ln_dist:slap
        """, data=df)
logit_results = model.fit()
logit_results.summary2()

def prob_made(dist, is_slap):
    b0, b1, b2, b3 = logit_results.params
    value = (b0 + b1*is_slap + b2*np.log(dist) + b3*np.log(dist)*is_slap)
    return 1/(1 + math.exp(-value))

prob_made(20, 1)
prob_made(100, 0)
prob_made(100, 1)
