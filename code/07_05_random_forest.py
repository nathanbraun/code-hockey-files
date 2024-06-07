import pandas as pd
import numpy as np
from patsy import dmatrices
from pandas import DataFrame, Series
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from os import path

DATA_DIR = './data'

df = pd.read_csv(path.join(DATA_DIR, 'shots.csv'))
df = df.loc[df['shot_type'].notnull()]

cont_vars = ['dist', 'st_x', 'st_y', 'period_time_remaining', 'empty']
cat_vars = ['pos', 'hand', 'period']

# replace periods 1, 2, 3 ... with P1, P2, P3 ...
# this is so that when we turn them into dummy variables the column names are
# P1, P2, ... and not just 1, 2, which can cause issues
df['period'] = 'P' + df['period'].astype(str)

df_cat = pd.concat([pd.get_dummies(df[x]) for x in cat_vars], axis=1)

df_all = pd.concat([df[cont_vars], df_cat], axis=1)
df_all['shot_type'] = df['shot_type']
df_all.sample(10)

yvar = 'shot_type'
xvars = cont_vars + list(df_cat.columns)
xvars

train, test = train_test_split(df_all, test_size=0.20)

model = RandomForestClassifier(n_estimators=100)
model.fit(train[xvars], train[yvar])

test['shot_type_hat'] = model.predict(test[xvars])
test['correct'] = (test['shot_type_hat'] == test['shot_type'])
test['correct'].mean()

model.predict_proba(test[xvars])

probs = DataFrame(model.predict_proba(test[xvars]),
                  index=test.index,
                  columns=model.classes_)
probs.head()
probs.columns = ['pmiss', 'pmake']

results = pd.concat([test[['shot_type', 'shot_type_hat',
    'correct']], probs], axis=1)


results.groupby('shot_type')[['correct', 'backhand', 'deflected', 'slap',
    'snap', 'tip-in', 'wrap-around', 'wrist']].mean().round(2)

# cross validation
model = RandomForestClassifier(n_estimators=100)
scores = cross_val_score(model, df_all[xvars], df_all[yvar], cv=10)

scores
scores.mean()

# feature importance
model = RandomForestClassifier(n_estimators=100)
model.fit(df_all[xvars], df_all[yvar])  # running model fitting on entire dataset
Series(model.feature_importances_, xvars).sort_values(ascending=False)

# homework: add in some player info?

# vs logit model
df['ln_dist'] = np.log(df['dist'].apply(lambda x: max(x, 0.5)))
df['goal'] = df['goal'].astype(int)
y, X = dmatrices('goal ~ dist', df)

model = LogisticRegression()
scores = cross_val_score(model, X, y, cv=10)

scores
scores.mean()
