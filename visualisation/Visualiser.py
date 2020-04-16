from utils.Configuration import Configuration
import seaborn as sb
import matplotlib.pyplot as plt


class Visualiser:

    @staticmethod
    def scatterPlots(configuration: Configuration):
        in_cols = list(configuration.get_input_columns())
        out_cols = list(configuration.get_output_columns())
        # scatter_map = sb.pairplot(configuration.log[all_columns])
        # mapped = scatter_map.map(plt.scatter)
        # plt.savefig('scattermap.png')
        fig, axs = plt.subplots(ncols=len(configuration.input_metrics), nrows=len(configuration.output_metrics), sharey=True, squeeze=False)
        for col, in_col in enumerate(in_cols):
            for row, out_col in enumerate(out_cols):
                sb.scatterplot(x=configuration.log[in_col], y=configuration.log[out_col], ax=axs[row, col])

        plt.savefig("results/" + configuration.id + "_scattermap.png")


    @staticmethod
    def visualiseCorrelation(configuration: Configuration):
        pearson_heatmap = sb.heatmap(configuration.correlation.pearson, vmin=-1, vmax=1, annot=True, square=True, linewidths=.5,
                                     xticklabels=configuration.output_metrics, yticklabels=configuration.input_metrics)
        plt.savefig("results/" + configuration.id + "_correlation_heatmap.png")

    @staticmethod
    def saveFigure(plot_object, path: str):
        figure = plot_object.get_figure()
        figure.savefig("results/" + path)
