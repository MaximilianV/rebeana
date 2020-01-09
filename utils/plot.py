def plot_attribute(log, attribute: str, filename: str):
    """Plots a given column (attribute) of the log and saves the diagram to a file.

    Arguments:
        log {DataFrame} -- Log to use for plotting
        attribute {str} -- Name of the column of log to plot
        filename {str} -- Where to store the diagram
    """
    plot = log[attribute].plot(kind="line").get_figure()
    plot.savefig(filename)
