📘 GradeBook Analyzer – Mini Project

Course: Programming for Problem Solving using Python
Student: Kunal Yadav
Submission Date: 25 Nov 2025

🧩 Project Overview

GradeBook Analyzer is a Python-based Command Line Interface (CLI) tool that automates the process of analyzing student marks.
It allows instructors to input or import student data, calculates essential statistics, assigns letter grades, identifies pass/fail students, and prints a formatted results table.

This project demonstrates the use of modular programming, file handling, statistics functions, control flow, loops, and list comprehensions.

📝 Learning Objectives

Through this project, you will practice:

Reading data manually or from a CSV file

Using Python dictionaries & lists

Implementing statistical functions (average, median, min, max)

Assigning letter grades with conditional logic

Filtering data using list comprehensions

Looping menus for repeated actions

Formatting tabular output

📂 Project Structure
gradebook_analyzer/
│
├── gradebook.py       # Main CLI program
└── README.md          # Documentation

🚀 Features Implemented
✅ 1. Manual Input & CSV Import

The program allows two input methods:

Manual entry of names and marks

Loading data from a CSV file (Name,Marks format)

✅ 2. Statistical Analysis

After loading data, the system computes:

Average Score

Median Score

Highest Score

Lowest Score

These functions are modular and reusable.

✅ 3. Grade Assignment

Grades are assigned using the following scale:

Marks	Grade
90+	A
80-89	B
70-79	C
60-69	D
<60	F

A grade distribution summary (A–F count) is also displayed.

✅ 4. Pass/Fail Filtering (List Comprehension)

The program uses Python list comprehensions to find:

passed_students → Marks ≥ 40

failed_students → Marks < 40

Both lists are printed.✅ 5. Formatted Results Table

A clean tabular output is displayed:

Name            Marks      Grade
---------------------------------------
Alice             78         C
Bob               92         A

✅ 6. CLI Menu Loop

The program runs inside a while loop, allowing users to:

Input new data

Load a CSV

Re-run analysis

Exit the program

🔧 How to Run the Program
1. Open Terminal / VS Code

Navigate to the project folder:

cd gradebook_analyzer

2. Run the Python Script
python gradebook.py

📄 CSV File Format

Your CSV file must follow this structure:

Alice,78
Bob,92
Charlie,67
David,55
Eva,89

🧪 Testing Requirements

Your project must be tested with:

✔ At least 5 students’ data entered manually

✔ At least 1 CSV file

🌟 Bonus (Optional)

Add a feature to export the final table to a CSV file.

📌 Submission Checklist
Requirement	Status
gradebook.py created	✔
Manual + CSV input implemented	✔
Statistics functions implemented	✔
Grade assignment + distribution	✔
Pass/Fail filtering	✔
Formatted table output	✔
Menu loop	✔
Tested with sample data	✔
README.md included	✔
📬 Contact

For academic queries: sameer.farooq@krmangalam.edu.in

👍 Final Note

This project demonstrates real-world data processing, modular programming, and Python CLI development.
Feel free to modify, extend, or enhance it for future use!
