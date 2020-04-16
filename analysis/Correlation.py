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

        all_columns = self.config.get_input_columns() + self.config.get_output_columns()
        self.log = self.config.log[all_columns].copy()
        self.log.dropna(inplace=True)

    def compute_correlation(self):
        for input, in_metric in enumerate(self.config.get_input_columns()):
            for output, out_metric in enumerate(self.config.get_output_columns()):
                in_col_np = self.log[in_metric].to_numpy()
                out_col_np = self.log[out_metric].to_numpy()
                print("Computing correlation between " + in_metric + " and " + out_metric + ".")
                pearson = scipy.stats.pearsonr(in_col_np, out_col_np)
                spearman = scipy.stats.spearmanr(in_col_np, out_col_np)
                print("\tPearson\tp")
                print("\t", round(pearson[0], 3), "\t", round(pearson[1], 3))
                print("\tSpearman\tp")
                print("\t", round(spearman[0], 3), "\t", round(spearman[1], 3))
                self.result.add_correlation(input, output, pearson=pearson, spearman=spearman)
