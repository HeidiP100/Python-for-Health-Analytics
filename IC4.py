################################################
# Heidi Pavka                                  #
# hpavka@usf.edu                               #
# IC4.py                                       #
# Data Cleaning and Summarization with Pandas  #
################################################

import pandas as pd

# Load Dataset
df = pd.read_csv("eye_health_behavioral_risk_factors_dataset_2022_brfss.csv")

# Remove duplicate rows
df = df.drop_duplicates()

# Summary statistics
print("Overall statistics:")
print(df.describe())

# Summary for states
print("State Averages:")
print(df.groupby("LocationAbbr")["Data_Value"].mean())

# Summary for sex
print("Averages by sex:")
print(df.groupby("Sex")["Data_Value"].mean())

# Summary for Age
print("Age averages:")
print(df.groupby("Age")["Data_Value"].mean())


