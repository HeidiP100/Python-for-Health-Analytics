#######################################################
# Heidi Pavka                                         #
# hpavka@usf.edu                                      #
# Lab5_3.py converts Maternal Health Risk csv to xlsx #
# 10/4/2026                                           #
#######################################################

import pandas as pd

# Read original CSV dataset
df = pd.read_csv("Maternal Health Risk Data Set.csv")

# Drop duplicate columns by header
df = df.loc[:, ~df.columns.duplicated()]

# Export to xlsx (excel)
df.to_excel("maternal_health_risk.xlsx", index=False)