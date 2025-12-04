import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ============================================================
# 1. CREATE SAMPLE DATASET
# ============================================================

data = {
    "Student_ID": range(1, 21),
    "Name": [
        "Aarav", "Vihaan", "Reyansh", "Aditya", "Kabir",
        "Arjun", "Vivaan", "Sai", "Krishna", "Ishaan",
        "Ananya", "Kiara", "Diya", "Eva", "Myra",
        "Aadhya", "Riya", "Saanvi", "Tara", "Meera"
    ],
    "Age": [18, 19, 18, 20, 19, 21, 18, 22, 20, 19, 18, 19, 20, 18, 21, 22, 19, 20, 21, 22],
    "Gender": [
        "Male", "Male", "Male", "Male", "Male",
        "Male", "Male", "Male", "Male", "Male",
        "Female", "Female", "Female", "Female", "Female",
        "Female", "Female", "Female", "Female", "Female"
    ],
    "Marks": [75, 82, 67, 90, 88, 60, 73, 95, 85, 78, 92, 80, 70, 65, 84, 88, 76, 91, 69, 87]
}

df = pd.DataFrame(data)
df.to_csv("student_dataset.csv", index=False)

print("Step 1 Completed: Dataset Created (student_dataset.csv)")

# ============================================================
# 2. DATA CLEANING
# ============================================================

df_clean = df.drop_duplicates()
df_clean = df_clean.dropna()

# Fix incorrect values if any
df_clean["Marks"] = df_clean["Marks"].clip(lower=0, upper=100)

df_clean.to_csv("student_dataset_cleaned.csv", index=False)
print("Step 2 Completed: Cleaned Dataset Saved (student_dataset_cleaned.csv)")

# ============================================================
# 3. DATA ANALYSIS
# ============================================================

mean_marks = df_clean["Marks"].mean()
median_marks = df_clean["Marks"].median()
max_marks = df_clean["Marks"].max()
min_marks = df_clean["Marks"].min()

gender_group = df_clean.groupby("Gender")["Marks"].mean()

print("Step 3 Completed: Analysis Done")

# ============================================================
# 4. VISUALIZATIONS
# ============================================================

# ---- Plot 1: Marks Distribution ----
plt.figure()
plt.hist(df_clean["Marks"])
plt.xlabel("Marks")
plt.ylabel("Count")
plt.title("Marks Distribution")
plt.savefig("plot1_marks_distribution.png")
plt.close()

# ---- Plot 2: Gender vs Average Marks ----
plt.figure()
plt.bar(gender_group.index, gender_group.values)
plt.xlabel("Gender")
plt.ylabel("Average Marks")
plt.title("Average Marks by Gender")
plt.savefig("plot2_gender_vs_marks.png")
plt.close()

# ---- Plot 3: Age vs Marks ----
plt.figure()
plt.scatter(df_clean["Age"], df_clean["Marks"])
plt.xlabel("Age")
plt.ylabel("Marks")
plt.title("Age vs Marks")
plt.savefig("plot3_age_vs_marks.png")
plt.close()

print("Step 4 Completed: All Plots Saved")

# ============================================================
# 5. EXPORT SUMMARY REPORT
# ============================================================

summary = f"""
# Summary Report

## Dataset Overview
- Total Students: {len(df_clean)}
- Males: {sum(df_clean['Gender']=='Male')}
- Females: {sum(df_clean['Gender']=='Female')}

## Marks Analysis
- Mean Marks: {mean_marks:.2f}
- Median Marks: {median_marks:.2f}
- Highest Marks: {max_marks}
- Lowest Marks: {min_marks}

## Average Marks by Gender
{gender_group.to_string()}

## Saved Files
- student_dataset.csv
- student_dataset_cleaned.csv
- plot1_marks_distribution.png
- plot2_gender_vs_marks.png
- plot3_age_vs_marks.png
"""

with open("summary_report.md", "w") as f:
    f.write(summary)

print("Step 5 Completed: Summary Report Created (summary_report.md)")
print("\nALL TASKS COMPLETED SUCCESSFULLY!")
