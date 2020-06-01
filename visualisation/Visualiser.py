from utils.Configuration import Configuration
import seaborn as sb
import matplotlib.pyplot as plt


class Visualiser:
    config: Configuration

    def __init__(self, config: Configuration):
        self.config = config
        self.log = config.get_filtered_log(include_activities=True)
        sb.set()
        sb.set_style("darkgrid", {'font.sans-serif': ['Open Ssans', 'DejaVu Sans', 'Arial', 'sans-serif'],})
        sb.set_context("paper") # DEFAULT: notebook, can be paper, talk, and poster
        # plt.figure(figsize=(16,6))



    def boxPlots(self):
        in_cols = self.config.get_input_columns()
        out_cols = self.config.get_output_columns()

        fig, axs = plt.subplots(ncols=max(len(in_cols), len(out_cols)), nrows=2, squeeze=False)
        for col, in_col in enumerate(in_cols):
            sb.boxplot(y=in_col, ax=axs[0, col], fliersize=.5, x="concept:name", data=self.log)
            # axs[0, col].set_xticklabels(axs[0, col].get_xticklabels(), rotation=-15, ha="left", fontsize='xx-small')
            axs[0, col].set_xticklabels([])
            # axs[0, col].get_legend().remove()

        for col, out_col in enumerate(out_cols):
            if ((col + 1) == len(out_cols)):
                sb.boxplot(y=self.log[out_col], ax=axs[1, col], fliersize=.5, x="concept:name", hue="concept:name", data=self.log)
                h, l = axs[1, col].get_legend_handles_labels()
                fig.legend(h, l, loc='center left', bbox_to_anchor=(0.6, 0.3))
                axs[1, col].cla()
            sb.boxplot(y=self.log[out_col], ax=axs[1, col], fliersize=.5, x="concept:name", data=self.log)
            # axs[1, col].set_xticklabels(axs[1, col].get_xticklabels(), rotation=-15, ha="left", fontsize='xx-small')
            axs[1, col].set_xticklabels([])
            # axs[1, col].get_legend().remove()
            axs[1,1].set_visible(False)
        self.save_figure("boxplots")
        return


    def scatterPlots(self):
        in_cols = self.config.get_input_columns()
        out_cols = self.config.get_output_columns()

        fig, axs = plt.subplots(ncols=len(in_cols), nrows=len(out_cols), sharey=True, squeeze=False, figsize=(7.5,4.5))
        for col, in_col in enumerate(in_cols):
            for row, out_col in enumerate(out_cols):
                show_legend = False
                if (col + 1 + row + 1) == (len(in_cols) + len(out_cols)):
                    show_legend = 'brief'
                sb.scatterplot(x=self.log[in_col], y=self.log[out_col], ax=axs[row, col], hue=self.log["concept:name"], legend=show_legend)
        plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
        self.save_figure("scattermap")
        return


    def visualiseCorrelation(self):
        color_pal = sb.diverging_palette(h_neg=220, h_pos=20, s=99, l=55, sep=3, as_cmap=True)
        pearson_heatmap = sb.heatmap(self.config.correlation.pearson, vmin=-1, vmax=1, center=0, cmap=color_pal,
                                     annot=True, square=True, linewidths=.5,
                                     xticklabels=self.config.output_metrics, yticklabels=self.config.input_metrics)
        self.save_figure("correlation_heatmap_pearson")
        spearman_heatmap = sb.heatmap(self.config.correlation.spearman, vmin=-1, vmax=1, center=0, cmap=color_pal,
                                     annot=True, square=True, linewidths=.5,
                                     xticklabels=self.config.output_metrics, yticklabels=self.config.input_metrics)
        self.save_figure("correlation_heatmap_spearman")
        return


    def save_figure(self, name):
        plt.title(self.config.id, loc='center', pad=10.0)
        plt.tight_layout()
        # plt.figure(constrained_layout=True)
        plt.savefig("results/" + self.config.id + "_" + name + ".png", bbox_inches='tight',dpi=300)
        plt.clf()
