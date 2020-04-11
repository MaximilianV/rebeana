from os.path import join
import matplotlib.pyplot as plt
from utils.Configuration import Configuration
import scipy.stats
import numpy as np
from evaluation.CorrelationResult import CorrelationResult

# plt.style.use('ggplot')

# OUT_PATH = "evaluation/results"


class Correlation:
    config: Configuration
    corr_matrix: np.ndarray
    result: CorrelationResult

    def __init__(self, config: Configuration):
        self.config = config
        self.result = CorrelationResult(len(self.config.input_metrics), len(self.config.output_metrics))

        all_columns = list(self.config.get_input_columns()) + list(self.config.get_output_columns())
        self.log = self.config.log[all_columns]
        self.log.dropna(inplace=True)

    def compute_correlation(self):
        for input, i_metric in enumerate(self.config.get_input_columns()):
            for output, o_metric in enumerate(self.config.get_output_columns()):
                self.result.add_pearson(self.compute_pearson_between(i_metric, o_metric), input, output)

    def compute_pearson_between(self, col1, col2):
        x = self.log[col1].to_numpy()
        y = self.log[col2].to_numpy()

        return scipy.stats.pearsonr(x, y)
        # return scipy.stats.spearmanr(x, y)
        # return clog[col1].corr(clog[col2], method="kendall")

    # def show_correlation(self, col1, col2, fileName=None):
    #     clog = self.log.dropna(subset=[col1, col2])

    #     x = clog[col1].to_numpy()
    #     y = clog[col2].to_numpy()

    #     slope, intercept, r, p, stderr = scipy.stats.linregress(x, y)

    #     line = f'Regression line: y={intercept:.2f}+{slope:.2f}x, r={r:.2f}'

    #     fig, ax = plt.subplots()
    #     ax.plot(x, y, linewidth=0, marker='s', label='Data points')
    #     ax.plot(x, intercept + slope * x, label=line)
    #     ax.set_xlabel(col1)
    #     ax.set_ylabel(col2)
    #     ax.legend(facecolor='white')
    #     # plt.show()
    #     if fileName:
    #         plt.savefig(join(OUTPUT_PATH, fileName + ".png"))
    #     else:
    #         plt.savefig(join(OUTPUT_PATH, "foo.png"))
