from utils.Configuration import Configuration
import seaborn as sb
import matplotlib.pyplot as plt


class Visualiser:
    config: Configuration

    def __init__(self, config: Configuration):
        self.config = config
        self.log = config.get_filtered_log(include_activities=True)
        sb.set()


    def boxPlots(self):
        in_cols = self.config.get_input_columns()
        out_cols = self.config.get_output_columns()

        fig, axs = plt.subplots(ncols=max(len(in_cols), len(out_cols)), nrows=2, squeeze=False)
        for col, in_col in enumerate(in_cols):
            sb.boxplot(y=self.log[in_col], ax=axs[0, col], fliersize=.5, x=self.log["concept:name"])
            # axs[0, col].set_xticklabels(axs[0, col].get_xticklabels(), rotation=40, ha="right")
        for col, out_col in enumerate(out_cols):
            sb.boxplot(y=self.log[out_col], ax=axs[1, col], fliersize=.5, x=self.log["concept:name"])
            # axs[1, col].set_xticklabels(axs[1, col].get_xticklabels(), rotation=40, ha="right")
        self.save_figure("boxplots")
        return


    def scatterPlots(self):
        in_cols = self.config.get_input_columns()
        out_cols = self.config.get_output_columns()

        fig, axs = plt.subplots(ncols=len(in_cols), nrows=len(out_cols), sharey=True, squeeze=False)
        for col, in_col in enumerate(in_cols):
            for row, out_col in enumerate(out_cols):
                sb.scatterplot(x=self.log[in_col], y=self.log[out_col], ax=axs[row, col], hue=self.log["concept:name"])
        self.save_figure("scattermap")
        return


    def visualiseCorrelation(self):
        pearson_heatmap = sb.heatmap(self.config.correlation.pearson, vmin=-1, vmax=1, annot=True, square=True, linewidths=.5,
                                     xticklabels=self.config.output_metrics, yticklabels=self.config.input_metrics)
        self.save_figure("correlation_heatmap")
        return


    def save_figure(self, name):
        plt.title(self.config.id)
        plt.savefig("results/" + self.config.id + "_" + name + ".png")
        plt.clf()
