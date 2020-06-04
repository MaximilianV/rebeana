import numpy as np


def activity_duration(group, column_name):
    group[column_name] = group["time:timestamp"] - group["time:timestamp"].shift(
        periods=1).where(group["lifecycle:transition"].str.lower().isin(["complete", "suspend"]), np.nan)

    group[column_name] = round(group[column_name].dt.total_seconds())

    return group


def compute(log, resource: str, *, column_name: str = "processing_speed", max_time: int = None, min_time: int = None):
    log.loc[log["org:resource"].isin([resource]), column_name] = np.nan

    log.loc[
        log["org:resource"].isin([resource]) &
        log["lifecycle:transition"].str.lower().isin(["suspend", "complete", "start", "resume"])
        ] = log.loc[
            log["org:resource"].isin([resource]) &
            log["lifecycle:transition"].str.lower().isin(["suspend", "complete", "start", "resume"])
            ].groupby(["case:concept:name", "concept:name"]).apply(activity_duration, column_name)

    if max_time:
        log.loc[log[column_name] > int(max_time), column_name] = np.nan
    if min_time:
        log.loc[log[column_name] < int(min_time), column_name] = np.nan

    log[column_name].fillna(value=np.nan, inplace=True)

    return log
