import statsmodels.api as sm
from utils.Configuration import Configuration
from sklearn.preprocessing import PolynomialFeatures
import pandas as pd


class Regression:
    config: Configuration

    def __init__(self, config: Configuration):
        self.config = config
        self.log = self.config.get_filtered_log()

    def linear_regression(self):
        results = {}
        in_cols = self.config.get_input_columns()
        out_cols = self.config.get_output_columns()
        for out_col in out_cols:
            print("Performing linear regression for ", self.config.input_metrics, " → ", out_col)
            results[out_col] = self.perform_regression(in_cols, out_col)
        return results

    def perform_regression(self, independent_metrics, dependent_metric):
        # POLYNOMIAL REGRESSION
        # polynomial_features= PolynomialFeatures(degree=3)
        # x = polynomial_features.fit_transform(self.log[independent_metrics])
        # features = pd.DataFrame(x,
                                # index=self.log.index,
                                # columns=polynomial_features.get_feature_names(self.log[independent_metrics].columns))
        # model = sm.OLS(self.log[dependent_metric], features)

        x = sm.add_constant(self.log[independent_metrics])
        model = sm.OLS(self.log[dependent_metric], x)

        regression = model.fit()
        return regression
