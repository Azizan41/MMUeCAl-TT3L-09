def calculate_daily_calories(weight, height, age, gender, activity):
    # Calculate Basal Metabolic Rate (BMR)
    if gender == 'female':
        bmr = 655 + (9.6 * weight) + (1.8 * height) - (4.7 * age)
    else:
        bmr = 66 + (13.7 * weight) + (5 * height) - (6.8 * age)

    # Calculate Total Daily Energy Expenditure (TDEE)
    if activity == 'sedentary':
        tdee = bmr * 1.2
    elif activity == 'lightly active':
        tdee = bmr * 1.375
    elif activity == 'moderately active':
        tdee = bmr * 1.55
    elif activity == 'very active':
        tdee = bmr * 1.725

    return round(tdee)