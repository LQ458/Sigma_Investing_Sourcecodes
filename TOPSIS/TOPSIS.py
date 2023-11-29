import numpy as np
import pandas as pd

# matrix
data = [
    ['Brazil', 8.948, -2.6, 1.78, 5.84],
    ['China', 11.7, 1.62, 4.92, 1.78],
    ['India', 2.24, -1, 4.14, 5.74],
    ['UK', 44.79, -3, 0.56, 4.42],
    ['USA', 71.114, -3.06, 1.92, 3.98],
]

columns = ['Country', 'GDP per Capita', 'Current Account', 'rGDP growth', 'Inflation Rate']
df = pd.DataFrame(data, columns=columns)
print("Initial DataFrame:")
print(df)

df.iloc[:, 1:] = df.iloc[:, 1:].apply(lambda x: x / np.sqrt((x**2).sum()))
print("\nNormalized DataFrame:")
print(df)

weights = [0.35, 0.05, 0.3, 0.3]
df.iloc[:, 1:] = df.iloc[:, 1:].multiply(weights, axis=1)

print("\nWeighted DataFrame:")
print(df)

positive_ideal_solution = pd.Series(
    df.iloc[:, 1:4].max(axis=0).tolist() + [df.iloc[:, 4].min()],
    index=df.columns[1:],
)
negative_ideal_solution = pd.Series(
    df.iloc[:, 1:4].min(axis=0).tolist() + [df.iloc[:, 4].max()],
    index=df.columns[1:],
)

print("\nPositive Ideal Solution:")
print(positive_ideal_solution)
print("\nNegative Ideal Solution:")
print(negative_ideal_solution)

# calculate the Euclidean distance of each country
df['d_pos'] = np.sqrt(((df.iloc[:, 1:] - positive_ideal_solution) ** 2).sum(axis=1))
df['d_neg'] = np.sqrt(((df.iloc[:, 1:] - negative_ideal_solution) ** 2).sum(axis=1))
print("\nEuclidean Distance of Each Country:")
print(df[['Country', 'd_pos', 'd_neg']])

df['closeness'] = df['d_neg'] / (df['d_pos'] + df['d_neg'])
print("\nRelative Closeness:")
print(df[['Country', 'closeness']])

# rank
print('\nRanked Countries:')
print(df.sort_values(by='closeness', ascending=False)[['Country', 'closeness']])