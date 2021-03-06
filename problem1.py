# -*- coding: utf-8 -*-
"""problem1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Vf4PD2wbm41-eVobIL9RNiqaae4bWbTC
"""

import numpy as np
import pandas as pd

"""# New Section"""

from google.colab import drive
drive.mount('/content/drive')

df = pd.read_csv("adult.csv")

df

import seaborn as sns

#sns.pairplot(df)

df.loc[df['salary']==df['salary'][32557]]

#sns.pairplot(df.loc[df['salary']==df['salary'][32557]])

df.isna().sum()
#no missing value

from sklearn import preprocessing
label_encoder = preprocessing.LabelEncoder()

df['salary'] = label_encoder.fit_transform(df['salary'])

df.head(1)

categ = ['workclass','education','marital-status','occupation','relationship','race','sex','country']

# Encode Categorical Columns

df[categ] = df[categ].apply(label_encoder.fit_transform)
from scipy import stats
df = df[(np.abs(stats.zscore(df)) < 3).all(axis=1)]
df.drop_duplicates(inplace=True)
df

df_arr = df.to_numpy()

X = df_arr[:,0:14]
y = df_arr[:,14]
X
y

import matplotlib.pyplot as plt

#!pip3 install xgboost

from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_wine

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)



model = XGBClassifier(use_label_encoder=False, eval_metric='mlogloss')

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

y_pred

accuracy = accuracy_score(y_test, y_pred)
accuracy



#accuracytrain = accuracy_score(y_train, x_pred)
#accuracytrain
# accuracy suggests that it is not overfitting

#from sklearn.linear_model import LogisticRegression
#model = LogisticRegression()
#model.fit(X_train,y_train)
#using regression type classifier gives us less accuracy

#model.score(X_train,y_train)

from hyperopt import STATUS_OK, Trials, fmin, hp, tpe

space={'max_depth': hp.quniform("max_depth", 3, 18, 1),
        'gamma': hp.uniform ('gamma', 1,9),
        'reg_alpha' : hp.quniform('reg_alpha', 40,180,1),
        'reg_lambda' : hp.uniform('reg_lambda', 0,1),
        'colsample_bytree' : hp.uniform('colsample_bytree', 0.5,1),
        'min_child_weight' : hp.quniform('min_child_weight', 0, 10, 1),
        'n_estimators': 180,
        'seed': 0
    }

import xgboost as xgb
def objective(space):
    clf=xgb.XGBClassifier(
                    n_estimators =space['n_estimators'], max_depth = int(space['max_depth']), gamma = space['gamma'],
                    reg_alpha = int(space['reg_alpha']),min_child_weight=int(space['min_child_weight']),
                    colsample_bytree=int(space['colsample_bytree']))
    
    evaluation = [( X_train, y_train), ( X_test, y_test)]
    
    clf.fit(X_train, y_train,
            eval_set=evaluation, eval_metric="auc",
            early_stopping_rounds=10,verbose=False)
    pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, pred>0.5)
    print ("SCORE:", accuracy)
    return {'loss': -accuracy, 'status': STATUS_OK }

trials = Trials()

best_hyperparams = fmin(fn = objective,
                        space = space,
                        algo = tpe.suggest,
                        max_evals = 100,
                        trials = trials)

best_hyperparams

model_with_hyper = XGBClassifier(colsample_bytree= 0.6985112260818864,
 gamma= 6.2050849899764255,
 max_depth= 4.0,
 min_child_weight= 9.0,
 reg_alpha= 40.0,
 reg_lambda= 0.3321709497064385,eval_metric='mlogloss')

model.fit(X_train, y_train)

y_pred = model.predict(X_train)

accuracy_with_hyper = accuracy_score(y_train,y_pred)

accuracy_with_hyper



