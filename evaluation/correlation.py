from pm4py.objects.log.importer.parquet import factory as parquet_importer
from os.path import join
import matplotlib.pyplot as plt
import scipy.stats

# plt.style.use('ggplot')

OUT_PATH = "evaluation/results"

class Correlation:
    log = None

    def __init__(self, file=None, log=None):
        if (file is None and log is None) or (file is not None and log is not None):
            raise Exception("You must either provide a file to load or pass a log object.")
        if file:
            self.log = parquet_importer.apply(file)
        else:
            self.log = log


    def compute_correlation(self, col1, col2):
        clog = self.log.dropna(subset=[col1, col2])
        return clog[col1].corr(clog[col2], method="kendall")

    def show_correlation(self, col1, col2, fileName=None):
        clog = self.log.dropna(subset=[col1, col2])

        x = clog[col1].to_numpy()
        y = clog[col2].to_numpy()

        slope, intercept, r, p, stderr = scipy.stats.linregress(x, y)

        line = f'Regression line: y={intercept:.2f}+{slope:.2f}x, r={r:.2f}'

        fig, ax = plt.subplots()
        ax.plot(x, y, linewidth=0, marker='s', label='Data points')
        ax.plot(x, intercept + slope * x, label=line)
        ax.set_xlabel(col1)
        ax.set_ylabel(col2)
        ax.legend(facecolor='white')
        # plt.show()
        if fileName:
            plt.savefig(join(OUT_PATH, fileName + ".png"))
        else:
            plt.savefig(join(OUT_PATH, "foo.png"))
