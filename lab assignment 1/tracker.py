# Name = Kunal Yadav , date = 28/10/2025 , Roll no.=2501730146
''' Stay on top of your health goals with ease. This tool helps you track your daily calorie intake, monitor meals, and balance your nutrition throughout the day. Simply log what you eat, and we’ll calculate your total calories to help you stay within your target.
 Start tracking today and take control of your fitness journey! 💪'''
 # 🍎 Daily Calorie Tracker

print("Welcome to Daily Calorie Tracker!")
print("Track your meals and stay within your daily calorie goal.\n")

# ----- Task 2: Input & Data Collection -----
meal_names = []
calories = []

num_meals = int(input("How many meals do you want to enter? "))

for i in range(num_meals):
    meal = input(f"\nEnter meal name #{i+1}: ")
    cal = float(input(f"Enter calories for {meal}: "))
    meal_names.append(meal)
    calories.append(cal)

# ----- Task 3: Calorie Calculations -----
total_calories = sum(calories)
average_calories = total_calories / num_meals

daily_limit = float(input("\nEnter your daily calorie limit: "))

# ----- Task 4: Exceed Limit Warning System -----
print("\n-------------------- RESULT --------------------")

if total_calories > daily_limit:
    print("⚠️ Warning: You have exceeded your daily calorie limit!")
else:
    print("✅ Great job! You are within your daily calorie limit.")

# ----- Task 5: Neatly Formatted Output -----
print("\nMeal Name\tCalories")
print("--------------------------------")

for i in range(num_meals):
    print(f"{meal_names[i]:<15}\t{calories[i]}")

print("--------------------------------")
print(f"Total:\t\t{total_calories}")
print(f"Average:\t{average_calories:.2f}")

print("\nThank you for using the Daily Calorie Tracker! 🥗")
