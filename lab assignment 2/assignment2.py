"""
GradeBook Analyzer - Mini Project
Course: Programming for Problem Solving using Python
Student Name: Kunal Yadav
Date: 25 Nov 2025
Description:
    A command-line application that reads student marks (manual/CSV),
    performs statistical analysis, assigns grades, shows pass/fail lists,
    and prints a formatted results table.
"""

import csv
import statistics

# -----------------------------------------------------------
# Task 3: Statistical Functions
# -----------------------------------------------------------
def calculate_average(marks_dict):
    return sum(marks_dict.values()) / len(marks_dict)

def calculate_median(marks_dict):
    return statistics.median(marks_dict.values())

def find_max_score(marks_dict):
    return max(marks_dict.values())

def find_min_score(marks_dict):
    return min(marks_dict.values())

# -----------------------------------------------------------
# Task 4: Grade Assignment
# -----------------------------------------------------------
def assign_grades(marks_dict):
    grades = {}
    for name, score in marks_dict.items():
        if score >= 90:
            grades[name] = "A"
        elif score >= 80:
            grades[name] = "B"
        elif score >= 70:
            grades[name] = "C"
        elif score >= 60:
            grades[name] = "D"
        else:
            grades[name] = "F"
    return grades

def grade_distribution(grades_dict):
    distribution = {"A":0, "B":0, "C":0, "D":0, "F":0}
    for g in grades_dict.values():
        distribution[g] += 1
    return distribution

# -----------------------------------------------------------
# Task 2: Manual or CSV Data Input
# -----------------------------------------------------------
def manual_input():
    marks = {}
    n = int(input("Enter number of students: "))
    for _ in range(n):
        name = input("Enter student name: ")
        score = int(input("Enter marks: "))
        marks[name] = score
    return marks

def load_csv():
    marks = {}
    filename = input("Enter CSV filename (example: data.csv): ")
    try:
        with open(filename, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 2:
                    name = row[0]
                    score = int(row[1])
                    marks[name] = score
        print("CSV loaded successfully!")
    except:
        print("Error: Could not read CSV file.")
    return marks

# -----------------------------------------------------------
# Task 6: Display Table
# -----------------------------------------------------------
def print_results_table(marks, grades):
    print("\nName\t\tMarks\tGrade")
    print("-----------------------------------------")
    for name in marks:
        print(f"{name:12}\t{marks[name]:5}\t{grades[name]}")
    print("-----------------------------------------\n")

# -----------------------------------------------------------
# Task 5: Pass/Fail Using List Comprehensions
# -----------------------------------------------------------
def pass_fail_filter(marks):
    passed = [name for name, score in marks.items() if score >= 40]
    failed = [name for name, score in marks.items() if score < 40]
    return passed, failed

# -----------------------------------------------------------
# Main Program Loop (CLI)
# -----------------------------------------------------------
def main():
    print("\n====================================")
    print("     Welcome to GradeBook Analyzer")
    print("====================================\n")

    while True:
        print("Menu:")
        print("1. Manual Input")
        print("2. Load from CSV")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            marks = manual_input()

        elif choice == "2":
            marks = load_csv()
            if len(marks) == 0:
                print("No data loaded. Try again.")
                continue

        elif choice == "3":
            print("Thank you for using GradeBook Analyzer!")
            break

        else:
            print("Invalid choice! Try again.\n")
            continue

        # Statistical Analysis
        avg = calculate_average(marks)
        med = calculate_median(marks)
        max_score = find_max_score(marks)
        min_score = find_min_score(marks)

        print("\n---- Statistics Summary ----")
        print(f"Average Score: {avg:.2f}")
        print(f"Median Score : {med}")
        print(f"Highest Score: {max_score}")
        print(f"Lowest Score : {min_score}")

        # Grades
        grades = assign_grades(marks)
        dist = grade_distribution(grades)

        print("\n---- Grade Distribution ----")
        for grade, count in dist.items():
            print(f"{grade}: {count}")

        # Pass/Fail
        passed, failed = pass_fail_filter(marks)
        print("\nPassed Students:", passed)
        print("Failed Students:", failed)

        # Final Table
        print_results_table(marks, grades)

        print("Run analysis again?\n")

# Run Program
if __name__ == "__main__":
    main()
