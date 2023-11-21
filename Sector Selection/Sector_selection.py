import pandas as pd
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

# Check the normalized data
sector_data_normalized.head()
