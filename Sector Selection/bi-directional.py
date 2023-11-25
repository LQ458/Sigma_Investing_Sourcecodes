import pandas as pd
import matplotlib.pyplot as plt

# Sample data
data = {
    'Category': ['Information Technology', 'Industrials', 'Cons_Discretionary', 'Materials', 'Financials', 'Health Care', 'Energy', 'Cons_Services'],
    'Value1': [30.23, 16.21, 15.90, 12.08, 12.82, 12.75, 0, 0],
    'Value2': [29.94, 15.25, 13.40, 12.08, 0, 0, 14.93, 13.33]
}

df = pd.DataFrame(data)

# Creating a bi-directional bar chart
fig, ax = plt.subplots(figsize=(10, 6))

# Plotting the bars for each category
for index, row in df.iterrows():
    ax.barh(row['Category'], row['Value1'], color='skyblue')
    ax.text(row['Value1'], index, f' {row["Value1"]}%', va='center', color='black', fontsize=10)

    ax.barh(row['Category'], -row['Value2'], color='salmon')
    ax.text(-row['Value2'], index, f' {row["Value2"]}%', va='center', color='black', fontsize=10)

# Adding labels and title
ax.set_xlabel('Allocation (%)')
ax.set_title('Short Term vs. Long Term Sector Allocation')
ticks = ax.get_xticks()
ax.set_xticklabels([str(abs(int(tick))) for tick in ticks])


# Adding a legend
ax.legend()

# Show the plot
plt.show()
