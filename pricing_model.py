import pandas as pd
from pricing_functions import calculate_premium, load_mortality_table

#Gender
gender=input("Enter gender(Male/Female):").capitalize()
while gender not in ["Male","Female"]:
    print("Invalid gender, please enter Male or Female.")
    gender=input("Enter gender(Male/Female):").capitalize()

mortality_table = load_mortality_table(gender)

#Age
while True:
    try:
        age=int(input("Enter entry age:"))
        if 0<=age<=110:
            break
        print("Invalid age, please enter an age between 0 and 110.")
    except ValueError:
        print("Invalid input. Please enter a whole number.")

#Sum Assured
while True:
    try:
        sum_assured = float(input("Enter sum assured:"))
        if sum_assured>0:
            break
        print("Invalid sum assured. Please enter a positive amount.")
    except ValueError:
        print("Invalid input. Please enter a number.")

#Term
while True:
    try:
        term=int(input("Enter term:"))
        if term>0 and age+term-1<=110:
            break
        print("Invalid term. The term must be positive and the attained age cannot exceed 110.")
    except ValueError:
        print("Invalid input. Please enter a whole number.")

#interest rate
while True:
    try:
        interest_rate = float(input("Enter interest rate (%):"))
        if interest_rate>-100:
            i=interest_rate/100
            break
        print("Invalid interest rate. Please enter a rate greater than -100.")
    except ValueError:
        print("Invalid input. Please enter a number.")

#Mortality multiplier
while True:
    try:
        mortality_multiplier = float(input("Enter mortality multiplier: "))
        if mortality_multiplier<=0:
            print("Invalid mortality multiplier. Please enter a positive number.")
            continue

        valid_multiplier=True
        for current_age in range(age,age+term):
            mortality_rate=mortality_table[current_age]*mortality_multiplier
            if mortality_rate>1:
                valid_multiplier=False
        if valid_multiplier:
            break
        print("Invalid mortality multiplier. Mortality rate cannot exceed 100%.")

    except ValueError:
        print("Invalid input. Please enter a number.")

total_PV, r, N, G=calculate_premium(age, sum_assured, term, i, mortality_table, mortality_multiplier)
assert G > N, "Gross premium should be greater than net premium."

# print("\n--- Pricing Result ---")
# print("Gender:", gender)
# print("Entry Age:", age)
# print("Sum Assured:", f"{sum_assured:,.0f}")
# print("Term:", term, "years")
# print("Interest Rate:", f"{i:.2%}")
# print("Mortality Multiplier:", mortality_multiplier)
print("Net Premium:", round(N, 2))
print("Gross Premium:", round(G, 2))

result=pd.DataFrame([{
    "Gender":gender,
    "Entry age":age,
    "Sun Assured":sum_assured,
    "Term":term,
    "Interest Rate":i,
    "Mortality Multiplier":mortality_multiplier,
    "Net Premium":round(N,2),
    "Gross Premium":round(G,2)
}])
result.to_csv("pricing_result.csv",index=False)
