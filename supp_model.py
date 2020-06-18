# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 23:08:44 2020

@author: jubin
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# choose relevant columns

df_main = pd.read_csv('df_main.csv')

df_main.columns

df_model = df_main[['category', 'brand', 'flavor_simp', 'num_flavors',
       'servings', 'price', 'priceperserving', 'calories', 'fat_g', 'carbs_g', 
       'protein_g', 'cholesterol_mg']]

# get dummy data

df_dum = pd.get_dummies(df_model)

# train test split

from sklearn.model_selection import train_test_split

X = df_dum.drop(['price', 'priceperserving'], axis = 1)
y = df_dum.price.values # .values makes it an array

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size = 0.2, random_state=42)

# multiple linear regression
## stats model

import statsmodels.api as sm

X_sm = X = sm.add_constant(X)
model = sm.OLS(y,X_sm)
model.fit().summary()

## sklearn model

from sklearn.linear_model import LinearRegression, Lasso
from sklearn.model_selection import cross_val_score

lm = LinearRegression()
lm.fit(X_train, y_train)

cross_val_score(lm, X_train, y_train, scoring = 'neg_mean_absolute_error', cv = 3)
np.mean(cross_val_score(lm, X_train, y_train, scoring = 'neg_mean_absolute_error', cv = 3))

# lasso regression

lm_l = Lasso(alpha = 0.02)
lm_l.fit(X_train, y_train)
np.mean(cross_val_score(lm_l, X_train, y_train, scoring = 'neg_mean_absolute_error', cv = 3))

alpha = []
error = []

for i in range(1, 100): 
    alpha.append(i/100)
    lml = Lasso(alpha = (i/100)) 
    error.append(np.mean(cross_val_score(lml, X_train, y_train, scoring = 'neg_mean_absolute_error', cv = 3)))
    
plt.plot(alpha, error)

err = tuple(zip(alpha, error))
df_err = pd.DataFrame(err, columns = ['alpha', 'error'])
df_err[df_err.error == max(df_err.error)]

# random forest

from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor()

cross_val_score(rf, X_train, y_train, scoring = 'neg_mean_absolute_error', cv = 3)
np.mean(cross_val_score(rf, X_train, y_train, scoring = 'neg_mean_absolute_error', cv = 3))

# tune models GridsearchCV

from sklearn.model_selection import GridSearchCV

parameters = {'n_estimators':range(1,10,1), 'criterion':('mse', 'mae'), 'max_features':('auto', 'sqrt', 'log2')}

gs = GridSearchCV(rf, parameters, scoring = 'neg_mean_absolute_error', cv = 3)
gs.fit(X_train, y_train)

gs.best_score_
gs.best_estimator_

# test ensembles

tpred_lm = lm.predict(X_test)
tpred_lml = lm_l.predict(X_test)
tpred_rf = gs.best_estimator_.predict(X_test)

from sklearn.metrics import mean_absolute_error
mean_absolute_error(y_test, tpred_lm)
mean_absolute_error(y_test, tpred_lml)
mean_absolute_error(y_test, tpred_rf)

mean_absolute_error(y_test, (tpred_lml+ tpred_rf)/2)

# productionising the model with flask 

import pickle
pickl = {'model': gs.best_estimator_}
pickle.dump(pickl, open( 'model_file' + ".p", "wb" ))


file_name = "model_file.p"
with open(file_name, 'rb') as pickled:
        data = pickle.load(pickled)
        model = data['model']

X_test.iloc[1,:]

model.predict(X_test.iloc[1,:].values.reshape(1, -1))

list(X_test.iloc[1,:])
