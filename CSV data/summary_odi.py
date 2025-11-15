import pandas as pd
import numpy as np
from scipy import stats

df = pd.read_csv("ODI_csv.csv")  #csv data of ODI

# Cleaning of column names using lower() ,strip() and replace()
df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

# Fix table display settings
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1200)   # wide screen
pd.set_option('display.max_colwidth', None)

# Group data by group column (0 as Intervention and 1 control )
groups = df.groupby("group")

summary_rows = []

for grp, data in groups:
    pre = data["pre_test_odi"]
    post = data["post_test_odi"]

    # ---- Summary values ----
    mean_pre = pre.mean() #mean
    median_pre = pre.median() #median
    sd_pre = pre.std() #standard deviation
    se_pre = sd_pre / np.sqrt(len(pre)) # standard Error

    mean_post = post.mean()
    median_post = post.median()
    sd_post = post.std()
    se_post = sd_post / np.sqrt(len(post))

    # ---- Paired T-test ----
    t_value, p_value = stats.ttest_rel(pre, post, nan_policy='omit')

    summary_rows.append({
        "Group": grp,
         "Mean_Pre-test": mean_pre,
        "Mean_Post-test": mean_post,

        "Median_Pre-test": median_pre,
        "Median_Post-test": median_post,

        "Standard_Deviation_Pre-test": sd_pre,
        "Standard_Deviation_Post-test": sd_post,

        "Standard_Error_Pre-test": se_pre,
        "Standard_Error_Post-test": se_post,

        "T_value": t_value,
        "P_value": p_value
    })

# Create summary table
summary_table = pd.DataFrame(summary_rows)

print("\nSummary Table:")
print(summary_table)

from tabulate import tabulate
print("\nTable View:\n")
print(tabulate(summary_table, headers="keys", tablefmt="grid"))
# Save to CSV (optional)
summary_table.to_csv("ODI_summary_table.csv", index=False)
