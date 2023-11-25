import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np

file_path = '/[path to data].xlsx'
data = pd.read_excel(file_path)

data['PESTEL Analysis Score'] = data['PESTEL Analysis Score'].str.replace('//', '/')
data['PESTEL Analysis Score'] = data['PESTEL Analysis Score'].apply(lambda x: float(x.split('/')[0])/float(x.split('/')[1]))

scaler = MinMaxScaler()

# Since lower P/E ratio is better, we invert it for normalization
data['Regular P/E Ratio'] = 1 / data['Regular P/E Ratio']

normalized_data = pd.DataFrame(scaler.fit_transform(data.iloc[:, 1:]), columns=data.columns[1:])

weights = np.array([0.20, 0.20, 0.50, 0.10])  # Weights as provided
data['Weighted Score'] = normalized_data.dot(weights)

# Sort
top_sectors = data.sort_values(by='Weighted Score', ascending=False).head(6)

# Allocation
total_score = top_sectors['Weighted Score'].sum()
top_sectors['Investment Allocation (%)'] = (top_sectors['Weighted Score'] / total_score) * 100

# Displaying
top_sectors[['Sectors', 'Investment Allocation (%)']]
