import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import seaborn as sns
import matplotlib.pyplot as plt

# Load the data
file_path = '/[path to data].xlsx'
data = pd.read_excel(file_path)

# Data cleaning and preparation
data['PESTEL Analysis Score'] = data['PESTEL Analysis Score'].str.replace('//', '/')
data['PESTEL Analysis Score'] = data['PESTEL Analysis Score'].apply(lambda x: float(x.split('/')[0])/float(x.split('/')[1]))
data['Regular P/E Ratio'] = 1 / data['Regular P/E Ratio']  # Invert P/E Ratio

# Normalize the data
scaler = MinMaxScaler()
normalized_data = pd.DataFrame(scaler.fit_transform(data.iloc[:, 1:]), columns=data.columns[1:])

new_weights = np.array([0.20, 0.20, 0.10, 0.50])

# Calculate the new weighted scores
data['New Weighted Score'] = normalized_data.dot(new_weights)

# Sort the data and select the top 6 sectors
new_top_sectors = data.sort_values(by='New Weighted Score', ascending=False).head(6)

# Calculate new investment allocations
total_new_score = new_top_sectors['New Weighted Score'].sum()
new_top_sectors['New Investment Allocation (%)'] = (new_top_sectors['New Weighted Score'] / total_new_score) * 100

# Visualization
new_visualization_data = new_top_sectors[['Sectors', 'New Investment Allocation (%)']].set_index('Sectors')

plt.figure(figsize=(10, 6))
sns.barplot(x=new_visualization_data['New Investment Allocation (%)'], y=new_visualization_data.index, palette="magma")
plt.xlabel('New Investment Allocation (%)')
plt.ylabel('Sectors')
plt.title('Top 6 Best Performing Sectors with Updated Weights and Their Investment Allocations')
plt.grid(axis='x')
plt.show()

# Display the new top sectors and their allocations
new_top_sectors[['Sectors', 'New Investment Allocation (%)']]
