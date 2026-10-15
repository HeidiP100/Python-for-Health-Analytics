############################################
# Lab 7 | Linear Regression Analysis Lab   #
# ---------------------------------------- #
# Sabrina Akter | sabrina127@usf.edu       #
# HSC 4933 | Python for Health Analytics   #
# ---------------------------------------- #
# Performs OLS linear regression and       #
# creates scatterplots for selected data.  #
# For educational use only.                #
############################################

# Peer reviewed: no present bugs, code works as needed.

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

# Make sure the columns exist
if x_col not in df.columns or y_col not in df.columns:
    print("Error: One or both column names were not found.")
    raise SystemExit

# Select the X and Y columns
data = df[[x_col, y_col]].copy()

# Remove commas from numeric values
data[x_col] = data[x_col].astype(str).str.replace(",", "", regex=False)
data[y_col] = data[y_col].astype(str).str.replace(",", "", regex=False)

# Convert the selected columns to numeric values
data[x_col] = pd.to_numeric(data[x_col], errors="coerce")
data[y_col] = pd.to_numeric(data[y_col], errors="coerce")

# Remove rows that are missing X or Y values
data = data.dropna()

print(f"\nRows available for regression: {len(data)}")


# Create the scatterplot
fig, ax = plt.subplots(figsize=(8, 6))

ax.scatter(
    data[x_col],
    data[y_col],
    alpha=0.6,
    edgecolor="k",
    linewidth=0.3
)

ax.set_xlabel(x_col)
ax.set_ylabel(y_col)
ax.set_title(f"{y_col} vs. {x_col} (n = {len(data)})")
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


# Perform OLS linear regression
X = sm.add_constant(data[x_col])
model = sm.OLS(data[y_col], X).fit()

# Get the regression results
beta_0 = model.params["const"]
beta_1 = model.params[x_col]
r_squared = model.rsquared

print("\nOLS Regression Results")
print(f"Beta 0 (intercept): {beta_0:.4f}")
print(f"Beta 1 (slope): {beta_1:.4f}")
print(f"R-squared: {r_squared:.4f}")


# Create the regression line
x_line = np.linspace(
    data[x_col].min(),
    data[x_col].max(),
    100
)

y_line = beta_0 + beta_1 * x_line


# Add the regression line to the scatterplot
ax.plot(
    x_line,
    y_line,
    color="crimson",
    linewidth=2,
    label=f"OLS line (R² = {r_squared:.3f})"
)

ax.set_title(
    f"{y_col} vs. {x_col} with OLS line (n = {len(data)})"
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