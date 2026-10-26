###########################################
# Heidi Pavka                             #
# hpavka@usf.edu                          #
# 10/25/2026                              #
# Lab9.py logistic and count-variable     #
# regression. Cleans column headers,      #
# calculates confusion matrices and VIF,  #
# and saves summary outputs to text files.#
###########################################

import os
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools import add_constant

# Prompt the user for a specific dataset and load it
file_name = input("Enter the dataset filename: ")
df = pd.read_csv(file_name)

# Clean column names to snake_case format
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# List available column names
print("Available column names:")
for col in df.columns:
    print(col)

# Prompt the user for regression type (Logistic or Poisson)
print("Select Regression Type:")
print("1. Logistic Regression")
print("2. Poisson Regression")
reg_type = input("Enter 1 or 2: ").strip()

# Prompt user for response amd predictor variables
response_var = input("Enter the response variable name: ").strip().lower()
predictors_input = input("Enter predictor column names separated by commas: ").strip()
predictors = [p.strip().lower() for p in predictors_input.split(",")]

# Remove rows missing any of the values used for the regression
needed_cols = predictors + [response_var]
df_clean = df[needed_cols].dropna()

# Build R-style formula using string
formula = f"{response_var} ~ " + " + ".join(predictors)

output_text = ""

# Calculate model based on choice
if reg_type == "1":
    # Logistic regression
    model = smf.logit(formula, data=df_clean)
    result = model.fit()

    # Calculate confusion matrix using a 0.5 threshold
    predicted_probs = result.predict(df_clean)
    predicted_classes = (predicted_probs >= 0.5).astype(int)
    actual_classes = df_clean[response_var].astype(int)
    confusion_mat = pd.crosstab(actual_classes, predicted_classes, rownames=['Actual'], colnames=['Predicted'])

    print("Logistic Regression Output")
    print(result.summary())
    print("Confusion Matrix:")
    print(confusion_mat)

else:
    # Poisson Regression
    model = smf.poisson(formula, data=df_clean)
    result = model.fit()

    # VIF calculation
    X = add_constant(df_clean[predictors])
    vif_df = pd.DataFrame()
    vif_df["Feature"] = X.columns
    vif_df["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]

    print("Poisson Regression Output")
    print(result.summary())
    print("Variance Inflation Factor (VIF):")
    print(vif_df.to_string(index=False))

# Ask user if they would like to save the output to a .txt file
save_choice = input("Would you like to save the output to a .txt file? (y/n): ").strip().lower()
if save_choice == 'y':
    custom_filename = input("Enter custom file name: ").strip()
    if not custom_filename.endswith(".txt"):
        custom_filename += ".txt"

    with open(custom_filename, "w", encoding = "utf-8") as f:
        f.write(str(result.summary()))
        if reg_type == "1":
            f.write("Confusion Matrix:" + str(confusion_mat))
        else:
            f.write("Variance Inflation Factor (VIF):" + str(vif_df.to_string(index=False)))

    print(f"Output successfully saved to {custom_filename}")
else:
    print("Output not saved.")
