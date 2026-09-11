import pandas as pd
import matplotlib.pyplot as plt

from pricing_functions import calculate_premium, load_mortality_table

gender="Male"
mortality_table = load_mortality_table(gender)

mortality_scenarios=[0.8,0.9,1.0,1.1,1.2]
interest_scenarios=[0.01,0.02,0.03,0.04,0.05]

results=[]

for multiplier in mortality_scenarios:
    total_PV,r,N,G=calculate_premium(30,1000000,20,0.03,mortality_table,multiplier)
    results.append({"Mortality multiplier":multiplier,
                    "Net Premium":round(N,2),
                    "Gross Premium":round(G,2)})

interest_result=[]
for i in interest_scenarios:
    total_PV,r,N,G=calculate_premium(30,1000000,20,i,mortality_table,1)
    interest_result.append({"Interest rate":i,
                    "Net Premium":round(N,2),
                    "Gross Premium":round(G,2)})

results_df = pd.DataFrame(results)
results_df["Gross Premium"].is_monotonic_increasing, \
    "Gross premium should increase as mortality increases."
results_df.to_csv("mortality_sensitivity.csv", index=False)

plt.plot(
    results_df["Mortality multiplier"],
    results_df["Gross Premium"],
    marker="o"
)
plt.xlabel("Mortality Multiplier")
plt.ylabel("Gross Premium")
plt.title("Mortality Sensitivity Analysis")
plt.xticks(
    results_df["Mortality multiplier"],
    [f"{x:.0%}" for x in results_df["Mortality multiplier"]]
)
plt.grid(True, alpha=0.3)
plt.savefig("mortality_sensitivity.png")
plt.show()

interest_results_df = pd.DataFrame(interest_result)
assert interest_results_df["Gross Premium"].is_monotonic_decreasing, \
    "Gross premium should decrease as interest rate increases."
interest_results_df.to_csv("interest_sensitivity.csv", index=False)
plt.plot(
    interest_results_df["Interest rate"],
    interest_results_df["Gross Premium"],
    marker="o"
)
plt.xlabel("Interest rate")
plt.ylabel("Gross Premium")
plt.title("Interest Rate Sensitivity Analysis")
plt.xticks(
    interest_results_df["Interest rate"],
    [f"{x:.0%}" for x in interest_results_df["Interest rate"]]
)
plt.grid(True, alpha=0.3)
plt.savefig("interest_sensitivity.png")
plt.show()
