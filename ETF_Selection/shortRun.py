import pandas as pd
import numpy as np
from scipy.stats import entropy

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


class ETF:
    def __init__(self, ticker, name, asset_class, market_cap_focus, strategy, industry_focus, geographical_focus,
                 maturity_band, rating_class_focus, total_assets, expense_ratio, std_dev_1yr, actively_managed):
        self.ticker = ticker
        self.name = name
        self.asset_class = asset_class
        self.market_cap_focus = market_cap_focus
        self.strategy = strategy
        self.industry_focus = industry_focus
        self.geographical_focus = geographical_focus
        self.maturity_band = maturity_band
        self.rating_class_focus = rating_class_focus
        self.total_assets = total_assets
        self.expense_ratio = expense_ratio
        self.std_dev_1yr = std_dev_1yr
        self.actively_managed = actively_managed

    def calculate_defensive_score(self):
        score = 0

        # Use of expense ratio calculation scores
        expense_ratio_weight = 1 - (self.expense_ratio / 0.3)
        score += max(0, expense_ratio_weight) * 30


       # Calculating scores using standard deviation
        std_dev_weight = 1 - (self.std_dev_1yr / 30)
        score += max(0, std_dev_weight) * 30

        # Total Assets (20% weight)
        total_assets_entropy = self.calculate_entropy(["Small", "Medium", "Large"],
                                                      [0.3, 0.3, 0.4], self.categorize_total_assets())
        score += total_assets_entropy * 20

        # Rating Class Focus (20% weight)
        rating_entropy = self.calculate_entropy(["High", "Medium", "Low"],
                                                [0.6, 0.3, 0.1], self.rating_class_focus)
        score += rating_entropy * 20

        return score
    
    def categorize_total_assets(self):
        # Categorize the total assets
        if self.total_assets < 1000:  # Assuming millions
            return "Small"
        elif self.total_assets < 10000:
            return "Medium"
        else:
            return "Large"

    @staticmethod
    def calculate_entropy(labels, weights, value):
        prob_distribution = np.array([weights[labels.index(label)] if label == value else 0 for label in labels], dtype=float)

        # Avoid dividing by zero by setting sum() to a small non-zero value if it is zero
        sum_value = prob_distribution.sum()
        prob_distribution = prob_distribution / sum_value if sum_value != 0 else prob_distribution + 1e-10
        
        return entropy(prob_distribution)

def evaluate_etfs(etf_objects):
    # Calculate score for each ETF
    scores = [etf.calculate_defensive_score() for etf in etf_objects]

    # return scores
    return scores

# Read data from CSV using pandas
csv_file_path = "./ETF.csv"
df = pd.read_csv(csv_file_path)

# Converting data in a DataFrame to an ETF object
etf_objects = []
for index, row in df.iterrows():
    etf_objects.append(ETF(*row))

# Calculate ratings for all ETFs
scores = evaluate_etfs(etf_objects)

# Adding scoring results to a DataFrame
df["Score"] = scores

# Sort DataFrame in descending order of ratings
df = df.sort_values(by="Score", ascending=False)

# Print Ranking Results
print(df[["name", "asset_class", "Score"]])
