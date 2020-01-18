from utils.resources import filter_log_by_resource_names


def compute_workload(log, resource: str, time_window: str = "12h", column_name: str = "workload"):
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
    filtered_log = filter_log_by_resource_names(log, [resource])

    filtered_log[column_name] = 0

    filtered_log[column_name] = filtered_log[column_name].rolling(
        time_window).count()

    return filtered_log
