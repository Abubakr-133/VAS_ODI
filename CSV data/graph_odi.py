import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

df = pd.read_csv("ODI_csv.csv")  # loading the ODI data

# Cleaning column names
df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

# -------------------------------
# IMPROVEMENT CALCULATION:
#   improvement = pre_test_odi - post_test_odi
#   percent_improvement = (improvement / pre_test_odi) * 100
# -------------------------------
df["improvement"] = df["pre_test_odi"] - df["post_test_odi"]
df["percent_improvement"] = ((df["pre_test_odi"] - df["post_test_odi"]) / df["pre_test_odi"]) * 100

# Group-wise summary
summary_table = df.groupby("group")[["pre_test_odi", "post_test_odi", "improvement", "percent_improvement"]].mean()
print("\nGroup-wise Improvement Summary:")
print(summary_table)

# -------------------------------
# GRAPH 1 — BAR GRAPH (Pre-test vs Post-test ODI)
# -------------------------------
plt.figure(figsize=(8,5))
summary_table[["pre_test_odi", "post_test_odi"]].plot(kind="bar")
plt.title("Pre-test vs Post-test ODI (Group 0 = Intervention, Group 1 = Control)")
plt.xlabel("Group")
plt.ylabel("ODI Score")
plt.tight_layout()
plt.show()
plt.close()

# -------------------------------
# GRAPH 2 — LINE GRAPH (Individual Changes)
# -------------------------------
plt.figure(figsize=(8,5))
for g, data in df.groupby("group"):
    for _, row in data.iterrows():
        plt.plot([0, 1], [row["pre_test_odi"], row["post_test_odi"]],
                 marker="o", alpha=0.7)
plt.xticks([0, 1], ["Pre Test", "Post Test"])
plt.title("Individual Patient Change (ODI Scores)")
plt.ylabel("ODI Score")
plt.grid(True)
plt.tight_layout()
plt.show()
plt.close()

# -------------------------------
# STATISTICAL TESTING — PAIRWISE T-TEST
# -------------------------------
results = {}
for g, data in df.groupby("group"):
    t_val, p_val = stats.ttest_rel(data["pre_test_odi"], data["post_test_odi"], nan_policy="omit")
    results[g] = {"t_value": t_val, "p_value": p_val}
print("\nPaired T-test Results:")
print(results)

# -------------------------------
# RESEARCH INTERPRETATION
# -------------------------------
for g in results:
    print(f"\n--- Group {g} Interpretation ---")
    t = results[g]["t_value"]
    p = results[g]["p_value"]

    if p < 0.05:
        print(f"Significant improvement (p = {p:.4f}), t = {t:.2f}")
    else:
        print(f"No statistically significant improvement (p = {p:.4f}), t = {t:.2f}")
