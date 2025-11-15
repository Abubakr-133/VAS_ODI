import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

df = pd.read_csv("VAS_csv.csv")# loading the VAS data

# Cleaning column names using strip() ,lower() and replace()
df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

# -------------------------------
# IMPROVEMENT CALCULATION:
#   improvement = pre_test_vas - post_test_vas
#   percent_improvement = (improvement / pre_test_vas) * 100
# -------------------------------
df["improvement"] = df["pre_test_vas"] - df["post_test_vas"]
df["percent_improvement"] = ((df["pre_test_vas"] - df["post_test_vas"]) / df["pre_test_vas"]) * 100

# Group-wise summary
summary_table = df.groupby("group")[["pre_test_vas", "post_test_vas", "improvement", "percent_improvement"]].mean()
print("\nGroup-wise Improvement Summary:")
print(summary_table)

# -------------------------------
# GRAPH 1 — BAR GRAPH of pre-test vs post-test VAS grouped based on intervention and control
# -------------------------------
plt.figure(figsize=(8,5))
summary_table[["pre_test_vas", "post_test_vas"]].plot(kind="bar")
plt.title("Pre-test vs Post-test VAS (Group 0 = Intervention, Group 1 = Control)")
plt.xlabel("Group")
plt.ylabel("VAS Score")
plt.tight_layout()
plt.show()
plt.close()


# GRAPH 2 — LINE GRAPH (Individual Change)
# the line graph shows how each individual patient's VAS score changed from Pre-test to Post-test.
plt.figure(figsize=(8,5))
for g, data in df.groupby("group"):
    for _, row in data.iterrows():
        plt.plot([0, 1], [row["pre_test_vas"], row["post_test_vas"]],
                 marker="o", alpha=0.7)
plt.xticks([0, 1], ["Pre Test", "Post Test"])
plt.title("Individual Patient Change (VAS Scores)")
plt.ylabel("VAS Score")
plt.grid(True)
plt.tight_layout()
plt.show()
plt.close()

# -------------------------------
# STATISTICAL TESTING
# -------------------------------
results = {}
for g, data in df.groupby("group"):
    t_val, p_val = stats.ttest_rel(data["pre_test_vas"], data["post_test_vas"], nan_policy="omit")
    results[g] = {"t_value": t_val, "p_value": p_val}
print("\nPaired T-test Results:")
print(results)

# -------------------------------
# RESEARCH-STYLE INTERPRETATION
# if p-value < 0.5 then significant improvement
# if p-value >= 0.5 then No statistically significant improvement
# -------------------------------
for g in results:
    print(f"\n--- Group {g} Interpretation ---")
    t = results[g]["t_value"]
    p = results[g]["p_value"]

    if p < 0.05:
        print(f"Significant improvement (p = {p:.4f}), t = {t:.2f}")
    else:
        print(f"No statistically significant improvement (p = {p:.4f}), t = {t:.2f}")
