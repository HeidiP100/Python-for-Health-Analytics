#######################################################
# Heidi Pavka                                         #
# hpavka@usf.edu                                      #
# Lab5_2.py converts Maternal Health Risk csv to json #
# 10/4/2026                                           #
#######################################################

import pandas as pd

# Read original CSV dataset
df = pd.read_csv("Maternal Health Risk Data Set.csv")

# Drop duplicate columns by header
df = df.loc[:, ~df.columns.duplicated()]

# Export to json
df.to_json("maternal_health_risk.json", orient="records", indent=2)