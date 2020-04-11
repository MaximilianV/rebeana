def dt_classification(time):
    h = time.hour
    if h > 6 and h <= 11:
        return 1
    elif h > 11 and h <= 14:
        return 2
    elif h > 14 and h <= 18:
        return 3
    elif h > 18 and h <= 23:
        return 4
    else:
        return 5

def compute(log, resource: str, *, column_name: str = "daytime"):
    log.loc[log["org:resource"].isin([resource]), column_name] = log.loc[log["org:resource"].isin([resource]), "time:timestamp"].apply(dt_classification)

    return log
