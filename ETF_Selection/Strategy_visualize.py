import matplotlib.pyplot as plt

# Data for the pie charts
defensive_labels = ['Expense Ratio', 'Standard Deviation', 'Total Assets', 'Rating Class Focus']
defensive_weights = [30, 30, 20, 20]

aggressive_labels = ['Standard Deviation', 'Market Cap Focus', 'Asset Class', 'Actively Managed']
aggressive_weights = [30, 25, 25, 20]

# Create subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

# Pie chart for Defensive Strategy
ax1.pie(defensive_weights, labels=defensive_labels, autopct='%1.1f%%', startangle=140)
ax1.set_title('Defensive Strategy Weights')

# Pie chart for Aggressive Strategy
ax2.pie(aggressive_weights, labels=aggressive_labels, autopct='%1.1f%%', startangle=140)
ax2.set_title('Aggressive Strategy Weights')

plt.tight_layout()
plt.show()
