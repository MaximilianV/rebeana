from os.path import join
import matplotlib.pyplot as plt
from utils.Configuration import Configuration
import scipy.stats
import numpy as np
from analysis.CorrelationResult import CorrelationResult


class Correlation:
    config: Configuration
    corr_matrix: np.ndarray
    result: CorrelationResult

    def __init__(self, config: Configuration):
        self.config = config
        self.result = CorrelationResult(len(self.config.input_metrics), len(self.config.output_metrics))
        self.log = self.config.get_filtered_log()

    def compute_correlation(self):
        for input, in_metric in enumerate(self.config.get_input_columns()):
            for output, out_metric in enumerate(self.config.get_output_columns()):
                in_col_np = self.log[in_metric].to_numpy()
                out_col_np = self.log[out_metric].to_numpy()

                print("Computing correlation between " + in_metric + " and " + out_metric + ".")

                pearson = scipy.stats.pearsonr(in_col_np, out_col_np)
                spearman = scipy.stats.spearmanr(in_col_np, out_col_np)

                self.result.add_correlation(input, output, pearson=pearson, spearman=spearman)
