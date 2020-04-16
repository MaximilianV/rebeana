from utils.Configuration import Configuration
import seaborn as sb
import matplotlib.pyplot as plt


class Visualiser:


    @staticmethod
    def boxPlots(configuration: Configuration):
        sb.set()

        in_cols = configuration.get_input_columns()
        out_cols = configuration.get_output_columns()

        fig, axs = plt.subplots(ncols=max(len(in_cols), len(out_cols)), nrows=2, squeeze=False)
        for col, in_col in enumerate(in_cols):
            sb.boxplot(y=configuration.log[in_col], ax=axs[0, col], fliersize=.5)
        for col, out_col in enumerate(out_cols):
            sb.boxplot(y=configuration.log[out_col], ax=axs[1, col], fliersize=.5)

        plt.savefig("results/" + configuration.id + "_boxplots.png")
        plt.clf()


    @staticmethod
    def scatterPlots(configuration: Configuration):
        sb.set()

        in_cols = configuration.get_input_columns()
        out_cols = configuration.get_output_columns()

        fig, axs = plt.subplots(ncols=len(in_cols), nrows=len(out_cols), sharey=True, squeeze=False)
        for col, in_col in enumerate(in_cols):
            for row, out_col in enumerate(out_cols):
                sb.scatterplot(x=configuration.log[in_col], y=configuration.log[out_col], ax=axs[row, col])

        plt.savefig("results/" + configuration.id + "_scattermap.png")
        plt.clf()


    @staticmethod
    def visualiseCorrelation(configuration: Configuration):
        sb.set()

        pearson_heatmap = sb.heatmap(configuration.correlation.pearson, vmin=-1, vmax=1, annot=True, square=True, linewidths=.5,
                                     xticklabels=configuration.output_metrics, yticklabels=configuration.input_metrics)
        plt.savefig("results/" + configuration.id + "_correlation_heatmap.png")
        plt.clf()


    @staticmethod
    def saveFigure(plot_object, path: str):
        figure = plot_object.get_figure()
        figure.savefig("results/" + path)
