import pandas as pd

# Load the first file: Communication_Services.xlsx
file_path_communication_services = '/[data].xlsx'
communication_services_data = pd.read_excel(file_path_communication_services)

# Combine all data into a single DataFrame
all_data = pd.concat([
    communication_services_data.assign(Sector='Communication Services')
    #etc
])

# Normalize
porter_min, porter_max = all_data['Porter Five Forces Value'].min(), all_data['Porter Five Forces Value'].max()
all_data['Porter Five Forces Normalized'] = (all_data['Porter Five Forces Value'] - porter_min) / (porter_max - porter_min)

# Calculate the combined index
all_data['Combined Index'] = 0.5 * (all_data['Sharpe Ratio Normalized'] + all_data['Porter Five Forces Normalized'])

# Calculate the total combined index for each sector
sector_total_combined_index = all_data.groupby('Sector')['Combined Index'].sum()

# Calculate the allocation of each industry as a percentage of its sector's total
all_data['Allocation (%)'] = all_data.apply(lambda row: (row['Combined Index'] / sector_total_combined_index[row['Sector']]) * 100, axis=1)

# Sort and display the data with allocations
sorted_data_with_allocation = all_data.sort_values(by=['Sector', 'Allocation (%)'], ascending=[True, False])
sorted_data_with_allocation[['Industry Group', 'Sector', 'Allocation (%)']]
