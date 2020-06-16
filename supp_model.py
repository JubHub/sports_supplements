# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 23:08:44 2020

@author: jubin
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# choose relevant columns

df = pd.read_csv('df_merg.csv')

df.columns

df_model = df[['category', 'name', 'brand', 'flavor', 'servings', 'rating', 
               'flavorrating', 'reviews', 'price', 'priceperserving', 'calories']]

# get dummy data

df_dum = pd.get_dummies(df_model)

# train test split

from sklearn.model_selection import train_test_split

X = df_dum.drop(['price', 'priceperserving'], axis = 1)
y = df_dum.price.values # .values makes it an array

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# multiple linear regression
## stats model

import statsmodels.api as sm

X_sm = X = sm.add_constant(X)
model = sm.OLS(y,X_sm)
model.fit().summary()