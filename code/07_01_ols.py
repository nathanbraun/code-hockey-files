import pandas as pd
import statsmodels.formula.api as smf
from os import path

DATA_DIR = './data'

###################
# linear regression
###################

# load
df = pd.read_csv(path.join(DATA_DIR, 'shots.csv'))

# process
df['dist_sq'] = df['dist']**2
df['goal'] = df['goal'].astype(int)

df[['goal', 'dist', 'dist_sq']].head()

model = smf.ols(formula='goal ~ dist + dist_sq', data=df)
results = model.fit()

results.summary2()

def prob_of_goal(dist):
    b0, b1, b2 = results.params
    return (b0 + b1*dist + b2*(dist**2))

prob_of_goal(5)
prob_of_goal(20)
prob_of_goal(40)

df['goal_hat'] = results.predict(df)
df[['goal', 'goal_hat']].head()
