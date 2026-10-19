############################################
# Lab 7 | Linear Regression Analysis Lab   #
# ---------------------------------------- #
# Sabrina Akter | sabrina127@usf.edu       #
# HSC 4933 | Python for Health Analytics   #
# ---------------------------------------- #
# Performs OLS linear regression and       #
# creates scatterplots for selected data.  #
# For educational use only.                #
# ---------------------------------------- #
# Modified by Heidi Pavka (hpavka@usf.edu) #
# 10/18/2026:                              #
# filtered regression by chosen range and  #
# graphed two dependent variables against  #
# an independent variable                  #
############################################

# Imports
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm


# Ask the user which dataset to use
csv_path = input("Enter the dataset filename: ")

# Load the dataset
df = pd.read_csv(csv_path)

# Clean the column names
df.columns = df.columns.str.lower().str.replace(" ", "_")

# Show the available columns
print("\nAvailable columns:")
for column in df.columns:
    print(column)


# Ask the user to choose the X and Y variables
x_col = input("\nEnter the column name for the X variable: ").lower()
y_col = input("Enter the column name for the Y variable: ").lower()
y2_col = input("Enter the column name for the second Y variable (for dual plotting): ").lower()

# Make sure the columns exist
if x_col not in df.columns or y_col not in df.columns:
    print("Error: One or both column names were not found.")
    raise SystemExit

# MODIFICATION: filter regression by chosen range
filter_choice = input(f"\nWould you like to filter data by a specific range? (yes/no): ").lower()
if filter_choice == "yes":
    print(f"Available columns to filter: {x_col}, {y_col}, {y2_col}")
    f_col = input("Enter column name to filter by: ").lower()
    min_val = float(input("Enter minimum value: "))
    max_val = float(input("Enter maximum value: "))

    # Clean and filter
    df[f_col] = pd.to_numeric(df[f_col].astype(str).str.replace(",", "", regex=False), errors="coerce")
    df = df[(df[f_col] >= min_val) & (df[f_col] <= max_val)]
    print(f"Rows remaining after range filter [{min_val} - {max_val}]: {len(df)}")


# Select the X and Y1, and Y2 columns
data = df[[x_col, y_col, y2_col]].copy()

# Remove commas from numeric values
data[x_col] = data[x_col].astype(str).str.replace(",", "", regex=False)
data[y_col] = data[y_col].astype(str).str.replace(",", "", regex=False)
data[y2_col] = data[y2_col].astype(str).str.replace(",", "", regex=False)

# Convert the selected columns to numeric values
data[x_col] = pd.to_numeric(data[x_col], errors="coerce")
data[y_col] = pd.to_numeric(data[y_col], errors="coerce")
data[y2_col] = pd.to_numeric(data[y2_col], errors="coerce")

# Remove rows that are missing X or Y values
data = data.dropna()

print(f"\nRows available for regression: {len(data)}")

# MODIFICATION: Create the scatterplot with both Y variables
fig, ax = plt.subplots(figsize=(8, 6))

ax.scatter(
    data[x_col],
    data[y_col],
    alpha=0.6,
    edgecolor="k",
    linewidth=0.3
)

ax.scatter(
    data[x_col],
    data[y2_col],
    alpha=0.6,
    edgecolor="k",
    linewidth=0.3,
    marker="s"
)

ax.set_xlabel(x_col)
ax.set_ylabel(f"{y_col} and {y2_col}")
ax.set_title(f"{y_col} and {y2_col} vs. {x_col} (n = {len(data)})")
ax.grid(alpha=0.3)
fig.tight_layout()


# Ask the user if they want to save the scatterplot
save_scatter = input(
    "\nWould you like to save the scatterplot? (yes/no): "
).lower()

if save_scatter == "yes":
    scatter_file = input("Enter the file name for the scatterplot: ")

    if not scatter_file.endswith(".png"):
        scatter_file += ".png"

    fig.savefig(scatter_file, dpi=300)
    print(f"Saved scatterplot -> {scatter_file}")


# Perform OLS linear regression for both variables
X = sm.add_constant(data[x_col])

# MODICIATION: Model 1 (Y1)
model1 = sm.OLS(data[y_col], X).fit()
beta_0_1 = model1.params["const"]
beta_1_1 = model1.params[x_col]
r_squared_1 = model1.rsquared

print("\nOLS Regression Results")
print(f"Beta 0 (intercept): {beta_0_1:.4f}")
print(f"Beta 1 (slope): {beta_1_1:.4f}")
print(f"R-squared: {r_squared_1:.4f}")

# MODIFICATION: Model 2 (Y2)
model2 = sm.OLS(data[y2_col], X).fit()
beta_0_2 = model2.params["const"]
beta_1_2 = model2.params[x_col]
r_squared_2 = model2.rsquared

print("\nOLS Regression Results")
print(f"Beta 0 (intercept): {beta_0_2:.4f}")
print(f"Beta 1 (slope): {beta_1_2:.4f}")
print(f"R-squared: {r_squared_2:.4f}")

# Create the regression line
x_line = np.linspace(
    data[x_col].min(),
    data[x_col].max(),
    100
)

y_line_1 = beta_0_1 + beta_1_1 * x_line
y_line_2 = beta_0_2 + beta_1_2 * x_line



# Add both of the the regression lines to the scatterplot
ax.plot(
    x_line,
    y_line_1,
    color="crimson",
    linewidth=2,
    label=f"{y_col}OLS line (R² = {r_squared_1:.3f})"
)

ax.plot(
    x_line,
    y_line_2,
    color="blue",
    linewidth=2,
    label=f"{y2_col} OLS line (R² = {r_squared_2:.3f})"
)

ax.set_title(
    f"{y_col} and {y2_col} vs. {x_col} with OLS line (n = {len(data)})"
)

ax.legend()
fig.tight_layout()


# Ask the user if they want to save the OLS scatterplot
save_ols = input(
    "\nWould you like to save the scatterplot with the OLS regression line? (yes/no): "
).lower()

if save_ols == "yes":
    ols_file = input("Enter the file name for the OLS scatterplot: ")

    if not ols_file.endswith(".png"):
        ols_file += ".png"

    fig.savefig(ols_file, dpi=300)
    print(f"Saved OLS scatterplot -> {ols_file}")


# Show the final graph
plt.show()