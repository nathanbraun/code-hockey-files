"""
Answers to the end of chapter exercises for Modeling chapter.
"""
import pandas as pd
import random
from pandas import DataFrame, Series
import statsmodels.formula.api as smf
from os import path

DATA_DIR = './data'

###############################################################################
# problem 7.1
###############################################################################

###################
# from 07_01_ols.py
###################
df = pd.read_csv(path.join(DATA_DIR, 'shots.csv'))

# process
df['dist_sq'] = df['dist']**2
df['goal'] = df['goal'].astype(int)

model = smf.ols(formula='goal ~ dist + dist_sq', data=df)
results = model.fit()

def prob_of_goal(dist):
    b0, b1, b2 = results.params
    return (b0 + b1*dist + b2*(dist**2))

df['goal_hat'] = results.predict(df)

#########################
# answers to question 7.1
#########################
# a
df['goal_hat_alt'] = df['dist'].apply(prob_of_goal)

# check whether made_hat and made_hat_alt are within some epsilon
df[['goal_hat', 'goal_hat_alt']].head()

(df['goal_hat_alt'] == df['goal_hat']).all()

import numpy as np
(np.abs(df['goal_hat'] - df['goal_hat_alt']) < .00000001).all()

# b
model_b = smf.ols(
    formula='goal ~ dist + dist_sq + C(period)', data=df)
results_b = model_b.fit()
results_b.summary2()

"""
Most likely to go in in 5th period. Makes sense because these are penalty
shots. Makes sense because NHL OT rules are 5 minutes of sudden death OT (4th
period) then a shootout (5th period).
"""

# c
df['is_2'] = df['period'] == 2
df['is_3'] = df['period'] == 3
df['is_4'] = df['period'] == 4
df['is_5'] = df['period'] == 5

model_d = smf.ols(formula='goal ~ dist + dist_sq + is_2 + is_3 + is_4 + is_5',
                  data=df)
results_d = model_d.fit()
results_d.summary2()

###############################################################################
# problem 7.2
###############################################################################

# a
def run_sim_get_pvalue():
    coin = ['H', 'T']

    # make empty DataFrame
    df = DataFrame(index=range(100))

    # now fill it with a "guess"
    df['guess'] = [random.choice(coin) for _ in range(100)]

    # and flip
    df['result'] = [random.choice(coin) for _ in range(100)]

    # did we get it right or not?
    df['right'] = (df['guess'] == df['result']).astype(int)

    model = smf.ols(formula='right ~ C(guess)', data=df)
    results = model.fit()

    return results.pvalues['C(guess)[T.T]']

# b
sims_1k = Series([run_sim_get_pvalue() for _ in range(1000)])
sims_1k.mean()  # 0.5083

# c
def runs_till_threshold(i, p=0.05):
    pvalue = run_sim_get_pvalue()
    if pvalue < p:
        return i
    else:
        return runs_till_threshold(i+1, p)

sim_time_till_sig_100 = Series([runs_till_threshold(1) for _ in range(100)])

# d

# According to Wikipedia, the mean and median of the Geometric distribution are
# 1/p and -1/log_2(1-p). Since we're working with a p of 0.05, that'd give us:

from math import log
p = 0.05
g_mean = 1/p  # 20
g_median = -1/log(1-p, 2)  # 13.51

g_mean, g_median

sim_time_till_sig_100.mean()
sim_time_till_sig_100.median()

###############################################################################
# problem 7.3
###############################################################################

dfpg = pd.read_csv(path.join(DATA_DIR, 'player_games.csv'))

# a
model_a = smf.ols(formula=
                    """
                    goals ~ time_ice + time_ice_pp + hits + C(pos)
                    """, data=dfpg)
results_a = model_a.fit()
results_a.summary2()


# b
"""
Looking at the coefficients, C is the ommitted position dummy, so we have to
interpret coefficients relative to that.  We can say D scores significantly
less goals than C. There's no significant difference between C's, LW and RW.
"""

# c
"""
Biggest factor in no of goals is prob no of shots. Before (without
shots) ice time and power play time were signifant, but that's probably because
more ice time == more shots, which leads to more goals.

Controlling for no of shots, more ice time (and power play time) probably
doesn't do much. So my guess is those coefficients are no longer significant.

Also: D scores fewer goals, but prob because they take fewer shots. Controlling
for no shots, being a D shouldn't be as big of a deal. Would guess D shots are
lower quality (e.g. further out from the net) so maybe they'll still tend to
score less goals on average, but shouldn't be as big of an impact.

R2 should go up.
"""

model_b = smf.ols(formula=
                    """
                    goals ~ time_ice + time_ice_pp + hits + C(pos) + shots
                    """, data=dfpg)
results_b = model_b.fit()
results_b.summary2()

###############################################################################
# problem 7.4
###############################################################################
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score

xvars = ['shots', 'goals', 'assists', 'hits', 'time_ice', 'pen_min',
    'pp_goals', 'pp_assists', 'fo_wins', 'fo', 'takeaways', 'giveaways',
    'goals_sh', 'assists_sh', 'blocks', 'plus_minus', 'time_ice_even',
    'time_ice_sh', 'time_ice_pp']

yvar = 'pos'

model = RandomForestClassifier(n_estimators=100)

scores = cross_val_score(model, dfpg[xvars], dfpg[yvar], cv=10)
scores.mean()  
scores.min()
scores.max()

# feature important on model
model.fit(dfpg[xvars], dfpg[yvar])  # running model fitting on entire dataset
Series(model.feature_importances_, xvars).sort_values(ascending=False)
