import pandas as pd
import numpy as np
from patsy import dmatrices
from pandas import DataFrame, Series
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from os import path

DATA_DIR = '/Users/nathanbraun/fantasymath/hockey/data'

df = pd.read_csv(path.join(DATA_DIR, 'shots.csv'))


cont_vars = ['dist', 'st_x', 'st_y', 'period_time_remaining', 'empty']

cat_vars = ['pos', 'hand', 'shot_type', 'period']

df_cat = pd.concat([pd.get_dummies(df[x]) for x in cat_vars], axis=1)

df = pd.concat([df, df_cat], axis=1)

df['ln_dist'] = np.log(df['dist'].apply(lambda x: max(x, 0.5)))

xvars = cont_vars + list(df_cat.columns)
yvar = 'goal'

train, test = train_test_split(df, test_size=0.20)

model = RandomForestClassifier(n_estimators=100)
model.fit(train[xvars], train[yvar])

test['goal_hat'] = model.predict(test[xvars])
test['correct'] = (test['goal_hat'] == test['goal'])
test['correct'].mean()

model.predict_proba(test[xvars])

probs = DataFrame(model.predict_proba(test[xvars]),
                  index=test.index,
                  columns=model.classes_)
probs.head()
probs.columns = ['pmiss', 'pmake']

results = pd.concat([
    test[['name', 'shot_type', 'dist', 'goal', 'goal_hat',
          'correct']],
    probs[['pmake']]], axis=1)


results.sample(5)

results.groupby(['shot_type', 'goal'])['correct'].mean().to_frame().unstack()

results['pmake_bin'] = pd.cut(results['pmake'], 10)

results.groupby('pmake_bin')['goal'].mean()

# cross validation
model = RandomForestClassifier(n_estimators=100)
scores = cross_val_score(model, df[xvars], df[yvar], cv=10)

scores
scores.mean()

# feature importance
model.fit(df[xvars], df[yvar])  # running model fitting on entire dataset
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
