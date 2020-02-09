def compute(log, resource: str, *, column_name: str = "workload", time_window: str = "12h"):
    """Filters the log by the resource, computes the workload for it and adds a new column with the result to the log.

    Arguments:
        log {DataFrame} -- Log to use for analysis
        resource {str} -- Name of resource to analyse

    Keyword Arguments:
        time_window {str} -- Timewindow that should be used to compute the workload (default: {TIMEWINDOW})
        column_name {str} -- Name of the column to store workload in (default: {"workload"})

    Returns:
        DataFrame -- Log annotated with workload metric
    """

    log.loc[log["org:resource"].isin([resource]), column_name] = 0
    log.loc[log["org:resource"].isin([resource]), column_name] = log.loc[log["org:resource"].isin([
        resource]), column_name].rolling(time_window).count()

    log.loc[log["org:resource"].isin([resource]), column_name] = log.loc[log["org:resource"].isin([resource]), column_name].shift(1, fill_value=0)

    return log
