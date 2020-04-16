import statsmodels.api as sm
from utils.Configuration import Configuration


class Regression:
    config: Configuration

    def __init__(self, config: Configuration):
        self.config = config
        self.log = self.config.get_filtered_log()

    def linear_regression(self):
        in_cols = self.config.get_input_columns()
        out_cols = self.config.get_output_columns()
        for out_col in out_cols:
            print("Performing linear regression for ", self.config.input_metrics, " → ", out_col)
            self.perform_regression(in_cols, out_col)

    def perform_regression(self, independent_metrics, dependent_metric):
        x = sm.add_constant(self.log[independent_metrics])
        model = sm.OLS(self.log[dependent_metric], x)
        regression = model.fit()
        print(regression.summary())
