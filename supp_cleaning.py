# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 16:10:08 2020

@author: jubin
"""

import pandas as pd
import numpy as np

df_supp = pd.read_csv("supplements.csv", sep = ",")
df_ing = pd.read_csv("products_w_ing.csv", sep = ",")

pd.set_option("display.max_rows", None, "display.max_columns", None)

# concatenate df_supp with the nutritional info from df_ing

df_ing.drop(df_ing[['Category', 'Name', 'Brand', 'Size', 'Flavor', 'Servings', 'Rating', 'FlavorRating', 'Reviews', 'Price', 'PricePerServing']], axis = 1, inplace = True)

df_merg = pd.concat([df_supp, df_ing], axis=1)

# removing duplicate columns and rows

df_merg = df_merg.loc[:,~df_merg.T.duplicated(keep = 'first')]
df_merg = df_merg.drop_duplicates()

# dropping products with listed with no reviews and no servings

df_merg = df_merg.drop(df_merg[(df_merg.Servings == 0)].index)
df_merg = df_merg.drop(df_merg[(df_merg.Reviews == 0)].index)

# change column to all lower case 

df_merg['Flavor'] = df_merg['Flavor'].str.lower()

# drop size and just keep servings 

df_merg.drop(df_merg[['Size']], axis = 1, inplace = True)

# sorting out the $ in the 'Price' and 'PricePerServing' columns

df_merg.Price = df_merg.Price.apply(lambda x: x.strip('$'))
df_merg.Price = df_merg.Price.astype(float)

df_merg.PricePerServing = df_merg.PricePerServing.apply(lambda x: x.strip('\xa0$'))
df_merg.PricePerServing = df_merg.PricePerServing.astype(float)

# remove columns with only zeros

df_merg = df_merg.loc[:, (df_merg != 0).any(axis = 0)]

df_merg = df_merg.convert_dtypes()

# removing rows with nan

df_merg = df_merg.dropna()

# change all column names to lower case

df_merg.columns = map(str.lower, df_merg.columns)

# some calories have g  

df_merg['calories'] = df_merg['calories'].astype(str).str.replace('g', '')

# saving the final clean df

df_merg.to_csv('df_merg.csv', index = False)

# Total Fat g get rid of 
# CHOLESTEROL mg sort type
# SODIUM mg get rid of 
# TOTAL CARBOHYDRATE g get rid of 
# PROTEIN g sort type
# CALCIUM mg and g there's a mix
# POTASSIUM mg sort type
# DIETARY FIBER g sort type
# IRON mg sort type

df_merg.columns











