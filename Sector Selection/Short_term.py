import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data from the Excel file
file_path = '/[path to data].xlsx'
sector_data = pd.read_excel(file_path)

sector_data['PESTEL Analysis Score'] = sector_data['PESTEL Analysis Score'].replace('17//30', '17/30')

sector_data['PESTEL Analysis Score'] = sector_data['PESTEL Analysis Score'].apply(lambda x: float(x.split('/')[0]))
sector_data['Inverted PESTEL Score'] = sector_data['PESTEL Analysis Score'].max() / sector_data['PESTEL Analysis Score']
sector_data['Inverted P/E Ratio'] = sector_data['Regular P/E Ratio'].max() / sector_data['Regular P/E Ratio']

weights = {
    'Inverted PESTEL Score': 0.20,
    'Inverted P/E Ratio': 0.20,
    'S&P 500 5 Year Index Growth Rate (%)': 0.50,
    'S&P 500 10 Year Index Growth Rate (%)': 0.10
}

# Calculate the weighted score for each sector
sector_data['Weighted Score'] = (sector_data['Inverted PESTEL Score'] * weights['Inverted PESTEL Score'] +
                                 sector_data['Inverted P/E Ratio'] * weights['Inverted P/E Ratio'] +
                                 sector_data['S&P 500 5 Year Index Growth Rate (%)'] * weights['S&P 500 5 Year Index Growth Rate (%)'] +
                                 sector_data['S&P 500 10 Year Index Growth Rate (%)'] * weights['S&P 500 10 Year Index Growth Rate (%)'])

# Sorting the sectors based on the weighted score
ranked_sectors = sector_data.sort_values('Weighted Score', ascending=False)

top_6_sectors = ranked_sectors.head(6)
top_6_sectors[['Sectors', 'Weighted Score']]

sns.set(style="whitegrid")

plt.figure(figsize=(12, 6))
sns.barplot(x='Weighted Score', y='Sectors', data=top_6_sectors, palette='coolwarm')

plt.title('Top 6 Best Performing Sectors Based on Weighted Analysis', fontsize=16)
plt.xlabel('Weighted Score', fontsize=12)
plt.ylabel('Sectors', fontsize=12)

plt.show()

total_score = top_6_sectors['Weighted Score'].sum()

top_6_sectors['Allocation Proportion'] = top_6_sectors['Weighted Score'] / total_score

it_allocation = 0.30 
remaining_allocation = 1 - it_allocation 

top_6_sectors.loc[top_6_sectors['Sectors'] == 'Information Technology', 'Allocation Proportion'] = it_allocation

top_6_sectors['Adjusted Allocation Proportion'] = top_6_sectors.apply(
    lambda row: row['Allocation Proportion'] * remaining_allocation 
    if row['Sectors'] != 'Information Technology' else row['Allocation Proportion'],
    axis=1
)

top_6_sectors[['Sectors', 'Adjusted Allocation Proportion']]