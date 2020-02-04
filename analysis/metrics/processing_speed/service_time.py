import numpy as np


def cp(x, log):
    resource = x["org:resource"]
    case = x["case:concept:name"]
    task = x["concept:name"]
    time = x.name

    corres_start = log.loc[
        (log.index <= time) &
        (log["org:resource"] == resource) &
        (log["case:concept:name"] == case) &
        (log["concept:name"] == task) &
        log["lifecycle:transition"].isin(["start", "resume"])
    ].tail(1)

    processing_time = time - corres_start.index[0]

    return processing_time


def compute(log, resource: str, *, column_name: str = "proc_speed"):
    log.loc[log["org:resource"].isin([resource]), column_name] = np.nan

    log.loc[
        log["org:resource"].isin([resource]) &
        log["lifecycle:transition"].isin(["suspend", "complete"]),
        column_name] = log.loc[log["org:resource"].isin([resource]) & log["lifecycle:transition"].isin(
            ["suspend", "complete"])].apply(cp, axis=1, log=log)

    return log
