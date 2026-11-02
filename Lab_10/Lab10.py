##################################
# Heidi Pavka                    #
# hpavka@usf.edu                 #
# Lab10.py                       #
# 11/1/2026                      #
# Kaplan-Meier log-rank test and #
# Cox proportional hazards test  #
# on heart failure datasets      #
##################################

import matplotlib.pyplot as plt
import pandas as pd
from lifelines import KaplanMeierFitter
from lifelines import CoxPHFitter
from lifelines.statistics import logrank_test

# Load Log-Rank dataset
km_file_path = "km_logrank_readmission.csv"
km_df = pd.read_csv(km_file_path)

time_col_km = "time_days"
event_col_km = "readmitted"
group_col_km = "treatment_group"

# Set up Kaplan-Meier model
kmf = KaplanMeierFitter()
fig, ax = plt.subplots(figsize=(10, 6))

groups = km_df[group_col_km].unique()
logrank_result = None

if len(groups) == 2:
    g1_name, g2_name = groups[0], groups[1]
    g1_df = km_df[km_df[group_col_km] == g1_name]
    g2_df = km_df[km_df[group_col_km] == g2_name]

    # Fit and plot group 1
    kmf.fit(durations=g1_df[time_col_km], event_observed=g1_df[event_col_km], label=f"Group: {g1_name}")
    kmf.plot_survival_function(ax=ax, show_censors=True)

    # Fit and plot group 2
    kmf.fit(durations=g2_df[time_col_km], event_observed=g2_df[event_col_km], label=f"Group: {g2_name}")
    kmf.plot_survival_function(ax=ax, show_censors=True)

    # Log-Rank Test
    logrank_result = logrank_test(
        durations_A=g1_df[time_col_km],
        durations_B=g2_df[time_col_km],
        event_observed_A=g1_df[event_col_km],
        event_observed_B=g2_df[event_col_km]
    )

    print(f"Test statistic (chi-square) = {logrank_result.test_statistic:.4f}")
    print(f"p-value = {logrank_result.p_value:.4g}")

# Add Log-Rank P-value on plot
if logrank_result is not None:
    p = logrank_result.p_value
    p_text = "p < 0.001" if p < 0.001 else f"p = {p:.3f}"
    ax.text(
        0.97, 0.97,
        f"Log-rank test\n{p_text}",
        transform=ax.transAxes,
        ha="right", va="top",
        fontsize=11,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
    )

# Plot Formatting
plt.title("Kaplan-Meier Survival Curve", fontsize=14)
plt.xlabel("Time (Days)", fontsize=12)
plt.ylabel("Survival Probability", fontsize=12)
plt.ylim(0, 1.05)
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend(loc="lower left")
plt.tight_layout()

# Save and Display Plot 1
plt.savefig("survival_km.png")
plt.show()

# Load Cox PH Dataset
cox_file_path = "cox_ph_heart_failure_survival.csv"
cox_df = pd.read_csv(cox_file_path)

time_col_cox = "time_months"
event_col_cox = "death"

# Select columns to use as predictors
numeric_covariates = ["age", "bmi", "systolic_bp", "ejection_fraction"]
binary_covariates = ["sex", "diabetes", "smoker", "chronic_kidney_disease", "beta_blocker"]
ordinal_covariates = ["nyha_class"]

# Format binary variables
for col in binary_covariates:
    if cox_df[col].dtype == object or cox_df[col].dtype == bool:
        cox_df[col] = cox_df[col].astype(str).str.strip().str.lower().isin(["true", "1", "yes", "male"]).astype(int)

# Subset model dataframe
model_cols = [time_col_cox, event_col_cox] + numeric_covariates + binary_covariates + ordinal_covariates
model_df = cox_df[model_cols].dropna()

# Fix Cox Proportional Hazards Model
cph = CoxPHFitter()
cph.fit(model_df, duration_col=time_col_cox, event_col=event_col_cox)

# Print summary
cph.print_summary(decimals=3)
print(f"Concordance Index: {cph.concordance_index_:.3f}")

# Hazard Ratios Plot
fig, ax = plt.subplots(figsize=(8, 5))
cph.plot(hazard_ratios=True, ax=ax)
ax.axvline(1, color="gray", linestyle="--")
ax.set_title("Cox PH Model Hazard Ratios", fontsize=14)
ax.set_xlabel("Hazard Ratio", fontsize=12)
plt.tight_layout()

# Save and Display Plot 2
plt.savefig("cox_hazard_ratios.png")
plt.show()