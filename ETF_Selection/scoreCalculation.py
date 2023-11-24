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
        # 根据信息熵方法定义评分规则，权重可以根据重要性进行调整
        score = 0

        # 示例：使用信息熵计算资产类别的评分
        asset_class_entropy = self.calculate_entropy(["Equity", "Fixed Income"],
                                                     [0.55, 0.45], self.asset_class)
        score += asset_class_entropy * 10

        # 示例：使用信息熵计算市值关注点的评分
        market_cap_entropy = self.calculate_entropy(["Large-cap", "Mid-cap", "Small-cap", "Broad Market"],
                                                    [0.25, 0.2, 0.15, 0.4], self.market_cap_focus)
        score += market_cap_entropy * 10

        # 示例：使用信息熵计算策略的评分
        strategy_entropy = self.calculate_entropy(
            ["Blend", "Growth", "Value", "Aggregate", "Corporate", "Government", "Municipals", "Mortgage-Backed", "Inflation Protected"],
            [0.12, 0.12, 0.12, 0.12, 0.1, 0.1, 0.08, 0.08, 0.08],
            self.strategy
        )
        score += strategy_entropy * 10

        # 示例：使用社会实际情况调整行业关注点的评分
        industry_score = self.adjust_industry_score(self.industry_focus)
        score += industry_score * 10

        # 示例：使用信息熵计算地理关注点的评分
        geographical_entropy = self.calculate_entropy(["United States",""],
                                                      [0.7, 0.3], self.geographical_focus)
        score += geographical_entropy * 10

        # 示例：使用信息熵计算评级关注点的评分
        rating_entropy = self.calculate_entropy(["Investment Grade A or higher", "Investment Grade BBB or higher", "High Yield"],
                                                [0.35, 0.3, 0.35], self.rating_class_focus)
        score += rating_entropy * 10

        # 示例：使用信息熵计算到期期限的评分
        maturity_band_entropy = self.calculate_entropy(["Short-Term", "Intermediate", "Ultra Short"],
                                                       [0.3, 0.3, 0.4], self.maturity_band)
        score += maturity_band_entropy * 10

        # 示例：使用费用比率计算评分
        expense_ratio_weight = 1 - (self.expense_ratio / 0.3)  # 假设费用比率越低分数越高
        score += max(0, expense_ratio_weight) * 10

        # 示例：使用标准差计算评分
        std_dev_weight = 1 - (self.std_dev_1yr / 30)  # 假设标准差越低分数越高
        score += max(0, std_dev_weight) * 10

        # 示例：是否主动管理权重
        # 示例：如果是主动管理，则加分
        if self.actively_managed == "Y":
            score += 2

        return score

    @staticmethod
    def calculate_entropy(labels, weights, value):
        prob_distribution = np.array([weights[labels.index(label)] if label == value else 0 for label in labels], dtype=float)

        # 避免除以零，将 sum() 为零的情况设置为一个小的非零值
        sum_value = prob_distribution.sum()
        prob_distribution = prob_distribution / sum_value if sum_value != 0 else prob_distribution + 1e-10
        
        return entropy(prob_distribution)

    @staticmethod
    def adjust_industry_score(industry_focus):
        # 根据实际情况调整行业关注点的评分
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
    # 计算每个 ETF 的评分
    scores = [etf.calculate_score() for etf in etf_objects]

    # 返回评分结果
    return scores

# 从CSV文件读取数据
csv_file_path = "./ETF.csv"
df = pd.read_csv(csv_file_path)

# 将DataFrame中的数据转换为ETF对象
etf_objects = []
for index, row in df.iterrows():
    etf_objects.append(ETF(*row))

# 计算所有ETF的评分
scores = evaluate_etfs(etf_objects)

# 将评分结果添加到DataFrame中
df["Score"] = scores

# 对DataFrame按照评分降序排列
df = df.sort_values(by="Score", ascending=False)

# 打印排名结果
print(df[["name", "Score"]])
