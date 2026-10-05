##########################################################
# Heidi Pavka                                            #
# hpavka@usf.edu                                         #
# Lab5_1.py converts Maternal Health Risk csv to parquet #
# 10/4/2026                                              #
##########################################################

import pandas as pd

# Read original CSV dataset
df = pd.read_csv("Maternal Health Risk Data Set.csv")

# Drop duplicate columns by header
df = df.loc[:, ~df.columns.duplicated()]

# Export to parquet
df.to_parquet("maternal_health_risk.parquet", engine="pyarrow", index=False)
