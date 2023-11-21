import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

file_path = '/[our data directory].xlsx'
sector_data = pd.read_excel(file_path)

sector_data.loc[sector_data['Sectors'] == 'Consumer Discretionary', 'PESTEL Analysis Score'] = '17/30'

sector_data['PESTEL Analysis Score'] = sector_data['PESTEL Analysis Score'].apply(lambda x: float(x.split('/')[0]))

scaler = MinMaxScaler()

columns_to_normalize = ['PESTEL Analysis Score', 'Regular P/E Ratio', 'S&P 500 5 Year Index Growth Rate (%)', 'S&P 500 10 Year Index Growth Rate (%)']

# Applying MinMaxScaler for normalization (except for P/E Ratio which needs inversion)
sector_data_normalized = sector_data.copy()
sector_data_normalized[columns_to_normalize] = scaler.fit_transform(sector_data[columns_to_normalize])

# Invert the P/E Ratio (since lower P/E is better)
sector_data_normalized['Regular P/E Ratio'] = 1 - sector_data_normalized['Regular P/E Ratio']

weights = {
    'PESTEL Analysis Score': 0.20,
    'Regular P/E Ratio': 0.20,
    'S&P 500 5 Year Index Growth Rate (%)': 0.30,
    'S&P 500 10 Year Index Growth Rate (%)': 0.30
}

# Calculating the weighted score
sector_data_normalized['Weighted Score'] = (
    sector_data_normalized['PESTEL Analysis Score'] * weights['PESTEL Analysis Score'] + 
    sector_data_normalized['Regular P/E Ratio'] * weights['Regular P/E Ratio'] + 
    sector_data_normalized['S&P 500 5 Year Index Growth Rate (%)'] * weights['S&P 500 5 Year Index Growth Rate (%)'] + 
    sector_data_normalized['S&P 500 10 Year Index Growth Rate (%)'] * weights['S&P 500 10 Year Index Growth Rate (%)']
)

ranked_sectors = sector_data_normalized.sort_values('Weighted Score', ascending=False)

ranked_sectors[['Sectors', 'Weighted Score']]

top_6_sectors = ranked_sectors.head(6)

total_score_top_6 = top_6_sectors['Weighted Score'].sum()
top_6_sectors['Allocation (%)'] = (top_6_sectors['Weighted Score'] / total_score_top_6) * 100

# Displaying the allocation for the top 6 sectors
top_6_sectors[['Sectors', 'Allocation (%)']]

sectors = top_6_sectors['Sectors']
allocations = top_6_sectors['Allocation (%)']

# Creating the bar chart
plt.figure(figsize=(12, 6))
plt.bar(sectors, allocations, color='skyblue')
plt.xlabel('Sectors')
plt.ylabel('Allocation (%)')
plt.title('Investment Allocation Among Top 6 Sectors')
plt.xticks(rotation=45)
plt.grid(axis='y')

# Show the plot
plt.show()