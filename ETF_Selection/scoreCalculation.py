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

    def calculate_score(self):
        # Use information entropy to structure the analysis
        score = 0

        # Calculate the score for asset class using information entropy
        asset_class_entropy = self.calculate_entropy(["Equity", "Fixed Income"],
                                                     [0.55, 0.45], self.asset_class)
        score += asset_class_entropy * 10

        # Calculate the score for market focus using information entropy
        market_cap_entropy = self.calculate_entropy(["Large-cap", "Mid-cap", "Small-cap", "Broad Market"],
                                                    [0.25, 0.2, 0.15, 0.4], self.market_cap_focus)
        score += market_cap_entropy * 10

        # Calculate the score for investment strategy using information entropy
        strategy_entropy = self.calculate_entropy(
            ["Blend", "Growth", "Value", "Aggregate", "Corporate", "Government", "Municipals", "Mortgage-Backed", "Inflation Protected"],
            [0.12, 0.12, 0.12, 0.12, 0.1, 0.1, 0.08, 0.08, 0.08],
            self.strategy
        )
        score += strategy_entropy * 10

        # Use of social realities to adjust scores for industry concerns
        industry_score = self.adjust_industry_score(self.industry_focus)
        score += industry_score * 10

        # Using Information Entropy to Calculate Scores for Geographic Concerns
        geographical_entropy = self.calculate_entropy(["United States",""],
                                                      [0.7, 0.3], self.geographical_focus)
        score += geographical_entropy * 10

        # Using Information Entropy to Calculate Ratings of Concerns
        rating_entropy = self.calculate_entropy(["Investment Grade A or higher", "Investment Grade BBB or higher", "High Yield"],
                                                [0.35, 0.3, 0.35], self.rating_class_focus)
        score += rating_entropy * 10

        # Using information entropy to compute scores for maturity periods
        maturity_band_entropy = self.calculate_entropy(["Short-Term", "Intermediate", "Ultra Short"],
                                                       [0.3, 0.3, 0.4], self.maturity_band)
        score += maturity_band_entropy * 10

        # Use of expense ratio calculation scores
        expense_ratio_weight = 1 - (self.expense_ratio / 0.3)
        score += max(0, expense_ratio_weight) * 10

        # Calculating scores using standard deviation
        std_dev_weight = 1 - (self.std_dev_1yr / 30)
        score += max(0, std_dev_weight) * 10

        # Weight for active management
        # Add 2 points if the ETF is actively managed
        if self.actively_managed == "Y":
            score += 2

        return score

    @staticmethod
    def calculate_entropy(labels, weights, value):
        prob_distribution = np.array([weights[labels.index(label)] if label == value else 0 for label in labels], dtype=float)

        # Avoid dividing by zero by setting sum() to a small non-zero value if it is zero
        sum_value = prob_distribution.sum()
        prob_distribution = prob_distribution / sum_value if sum_value != 0 else prob_distribution + 1e-10
        
        return entropy(prob_distribution)

    @staticmethod
    def adjust_industry_score(industry_focus):
        # Adjusting the scoring of industry concerns to the actual situation
        industry_scores = {
            "Technology": 0.15,
            "Finance": 0.12,
            "Healthcare": 0.12,
            "Energy": 0.1,
            "Real Estate": 0.1,
            "Communications": 0.08,
            "Consumer Discretionary": 0.08,
            "Industrials": 0.08,
            "Thematic": 0.07,
            "Utilities": 0.1
        }
        
        return industry_scores.get(industry_focus, 0)

def evaluate_etfs(etf_objects):
    # Calculate score for each ETF
    scores = [etf.calculate_score() for etf in etf_objects]

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
print(df[["name", "Score"]])
