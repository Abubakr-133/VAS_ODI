import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

df = pd.read_csv("VAS_csv.csv")#loading the dataset with VAS data

# Cleaning column names
df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

# Extracting post-test VAS values and separating intervention and control group
group0 = df[df["group"] == 0]["post_test_vas"]
group1 = df[df["group"] == 1]["post_test_vas"]

# Independent T-test
t_val, p_val = stats.ttest_ind(group0, group1, equal_var=False)

print("Comparison of Post-Test VAS Between Group 0 and Group 1")
print("-------------------------------------------------------")
print(f"T-value = {t_val:.3f}")
print(f"P-value = {p_val:.4f}")

if p_val < 0.05:
    print("Result: Statistically significant difference between Group 0 and Group 1.")
else:
    print("Result: No statistically significant difference between Group 0 and Group 1.")

# Graph for visual comparison
plt.figure(figsize=(6,5))
plt.boxplot([group0, group1], labels=["Group 0", "Group 1"])
plt.title("Post-Test VAS Comparison Between Groups")
plt.ylabel("VAS Score")
plt.grid(True)
plt.show()
