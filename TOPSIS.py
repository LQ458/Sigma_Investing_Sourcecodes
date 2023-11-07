import numpy as np
import pandas as pd

# matrix
# Country name following by 4 indices
data = [
    ['Brazil', 8.948, 0.47, 1.78, 5.84],
    ['China', 11.7, 4.69, 4.92, 1.78],
    ['India', 2.24, 2.07, 4.14, 5.74],
    ['Japan', 37.68, 6.21, 0.12, 1.2],
    ['UK', 44.79, 0.07, 0.56, 4.42],
    ['USA', 71.114, 0.01, 1.92, 3.98],
]

# transfer to pandas DataFrame
columns = ['Country', 'GDP per Capita', 'Current Account', 'rGDP growth', 'Inflation Rate']
df = pd.DataFrame(data, columns=columns)
print(df)

# Data Normalization
df.iloc[:, 1:] = df.iloc[:, 1:].apply(lambda x: x / np.sqrt((x**2).sum()))
print('Normalized Data:')
print(df)

# weight
weights = [0.35, 0.05, 0.3, 0.3]

# weight assigned to each index
df.iloc[:, 1:] = df.iloc[:, 1:].multiply(weights, axis=1)
print('Weighted Data:')
print(df)

# calculating positive and negative ideal solutios
# The first three indicators are considered better when they are larger (positive ideal), while the fourth indicator is considered better when it is smaller (negative ideal).
positive_ideal_solution = df.iloc[:, 1:4].max(axis=0).tolist() + [df.iloc[:, 4].min()]
negative_ideal_solution = df.iloc[:, 1:4].min(axis=0).tolist() + [df.iloc[:, 4].max()]
print('Positive Ideal Solutions:', positive_ideal_solution)
print('Negative Ideal Solutions:', negative_ideal_solution)

# calculate the Euclidean distance of each country
df['d_pos'] = np.sqrt(((df.iloc[:, 1:] - positive_ideal_solution) ** 2).sum(axis=1))
df['d_neg'] = np.sqrt(((df.iloc[:, 1:] - negative_ideal_solution) ** 2).sum(axis=1))
print('The Euclidean Distance of Each Country:')
print(df[['Country', 'd_pos', 'd_neg']])

# calculate relative closeness
df['closeness'] = df['d_neg'] / (df['d_pos'] + df['d_neg'])
print('Relative Closeness:')
print(df[['Country', 'closeness']])

# rank
print('Ranked Countries:')
print(df.sort_values(by='closeness', ascending=False)[['Country', 'closeness']])
