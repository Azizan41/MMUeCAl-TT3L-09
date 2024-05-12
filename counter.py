def float_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")

def int_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter an integer.")

def gender_input(prompt):
    while True:
        gender = input(prompt).lower()
        if gender == "male" or gender == "female":
            return gender
        else:
            print("Invalid input. Please enter 'male' or 'female'.")

def activity_level_input(prompt):
    while True:
        activity_level = input(prompt).lower()
        if activity_level == "sedentary" or activity_level == "lightly active" or activity_level == "moderately active" or activity_level == "very active":
            return activity_level
        else:
            print("Invalid input. Please enter 'sedentary', 'lightly active', 'moderately active', or 'very active'.")

def calculate_bmr(weight, height, age, gender):
    if gender == "male":
        bmr = 66 + (6.3 * weight) + (12.9 * height) - (6.8 * age)
    else:
        bmr = 655 + (4.3 * weight) + (4.7 * height) - (4.7 * age)
    return bmr

def calculate_daily_calories(bmr, activity_level):
    if activity_level == "sedentary":
        calories = bmr * 1.2
    elif activity_level == "lightly active":
        calories = bmr * 1.375
    elif activity_level == "moderately active":
        calories = bmr * 1.55
    else:
        calories = bmr * 1.725
    return calories

def daily_calorie_needs_and_count_calories():
    weight = float_input("Enter your weight in kilograms: ")
    height = float_input("Enter your height in centimetres: ")
    age = int_input("Enter your age: ")
    gender = gender_input("Enter your gender (male or female): ")
    activity_level = activity_level_input("Enter your activity level (sedentary, lightly active, moderately active, very active): ")

    bmr = calculate_bmr(weight, height, age, gender)
    daily_calories = calculate_daily_calories(bmr, activity_level)

    print("Your daily calorie needs are: ", daily_calories)

    print("Please input your meal. If there is nothing more type 'done'.")
    total_calories = 0
    while True:
        meal_input = input("Meal: ")
        if meal_input.lower() == "done":
            break

        quantity_input = input("Quantity: ")
        try:
            quantity = float(quantity_input)
        except ValueError:
            print("Invalid quantity. Please enter a number.")
            continue

        # Assign calories based on meal name
        if meal_input.lower() == "pizza":
            calories = 285 * quantity
        elif meal_input.lower() == "burger":
            calories = 354 * quantity
        elif meal_input.lower() == "fries":
            calories = 230 * quantity
        else:
            print(f"Calories for {meal_input} not found. Assigning 0 calories.")
            calories = 0

        total_calories += calories

    print(f"\nThanks for using the Calories Counter! Here's your calorie count:\n\n---")
    print(f"Total Calories: {total_calories} (out of {daily_calories} daily needs)")

if __name__ == "__main__":
    daily_calorie_needs_and_count_calories()