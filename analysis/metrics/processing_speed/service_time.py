import numpy as np


def activity_duration(group, column_name):
    group[column_name] = group["time:timestamp"] - group["time:timestamp"].shift(
        periods=1).where(group["lifecycle:transition"].isin(["complete", "suspend"]), np.nan)

    group[column_name] = group[column_name].dt.total_seconds()

    return group


def compute(log, resource: str, *, column_name: str = "proc_speed"):
    log.loc[log["org:resource"].isin([resource]), column_name] = np.nan

    log.loc[log["org:resource"].isin([resource]) & log["lifecycle:transition"].isin(
        ["suspend", "complete", "start", "resume"])] = log.loc[log["org:resource"].isin([resource]) & log["lifecycle:transition"].isin(
        ["suspend", "complete", "start", "resume"])].groupby(["case:concept:name", "concept:name"]).apply(activity_duration, column_name)

    log[column_name].fillna(value=np.nan, inplace=True)

    return log
