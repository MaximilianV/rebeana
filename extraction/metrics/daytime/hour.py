def compute(log, resource: str, *, column_name: str = "daytime"):
    log.loc[log["org:resource"].isin([resource]), column_name] = log.loc[log["org:resource"].isin([resource]), "time:timestamp"].dt.hour

    return log
