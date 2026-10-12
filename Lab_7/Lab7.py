####################################
# Heidi Pavka                      #
# hpavka@usf.edu                   #
# Lab7.py                          #
# 10/11/2026                       #
# Performs OLS regression          #
# and plotting for a given dataset #
####################################

# Imports
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

# Prompt user for dataset and load dataset
csv_path = input("Enter the dataset filename: ")
df = pd.read_csv(csv_path)

# Clean column names to lowercase and replaces spaces with underscores
df.columns = df.columns.str.lower().str.replace(" ", "_")

# List available columns
print("Columns:")
print(df.columns)

# Prompt user for X and Y variables
x_col = input("Enter X variable column name: ")
y_col = input("Enter Y variable column name: ")

# Remove missing rows from X or Y columns
data = df[[x_col, y_col]].dropna()

# Create plain scatterplot
fig, ax = plt.subplots(figsize = (8, 6))
ax.scatter(data[x_col], data[y_col], alpha = 0.6, edgecolor = "k", linewidth = 0.3)
ax.set_xlabel(x_col)
ax.set_ylabel(y_col)
ax.set_title(f"{y_col} vs. {x_col} (n = {len(data)})")
ax.grid(alpha = 0.3)
fig.tight_layout()

# Ask user if they want to save the plain scatterplot
save_plain = input("Would you like to save this scatterplot? (y/n): ")
if save_plain == "y":
    scatter_file = input("Enter custom filename: ")
    fig.savefig(scatter_file, dpi = 300)
    print(f"Saved scatterplot -> {scatter_file}")

# Calculate OLS regression line
X = sm.add_constant(data[x_col])
model = sm.OLS(data[y_col], X).fit()

# Print regression regression line on scatterplot
x_line = np.linspace(data[x_col].min(), data[x_col].max(), 100)
y_line = model.params["const"] + model.params[x_col] * x_line
ax.plot(x_line, y_line, color="purple", linewidth = 2, label = f"OLS line (R^2 = {model.rsquared:.3f})")
ax.set_title(f"{y_col} vs. {x_col} with OLS line (n = {len(data)})")
ax.legend()

# Ask user if they want to save the OLS scatterplot
save_ols = input("Would you like to save this scatterplot with OLS regression line? (y/n): ")
if save_ols == "y":
    ols_file = input("Enter custom filename: ")
    fig.savefig(ols_file, dpi=300)
    print(f"Saved scatterplot with OLS line -> {ols_file}")

# Display OLS regression line
plt.show()
