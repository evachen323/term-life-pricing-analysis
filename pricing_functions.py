import pandas as pd

def load_mortality_table(gender):
    mortality_data = pd.read_csv("mortality_table.csv")

    gender_column = gender + "_qx"

    mortality_table = dict(
        zip(mortality_data["Age"], mortality_data[gender_column])
    )

    return mortality_table

def calculate_premium(age, sum_assured, term, i, mortality_table, mortality_multiplier):
    total_PV=0
    survival_probability=1
    r=1

    for year in range(1, term + 1):
        current_age = age + year - 1
        mortality_rate = mortality_table[current_age]*mortality_multiplier

        expected_claim = sum_assured * survival_probability * mortality_rate

        discount_factor = 1 / (1 + i) ** year
        PV = expected_claim * discount_factor
        total_PV += PV

        survival_rate = 1 - mortality_rate
        survival_probability *= survival_rate

        if year < term:
            r += survival_probability * discount_factor

    annual_expense=100
    expense_PV=annual_expense*r
    net_premium=total_PV/r
    gross_premium=(total_PV+expense_PV)/r

    return total_PV,r,net_premium,gross_premium
