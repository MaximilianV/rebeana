import pandas as pd


def compute(log, resource: str, *, column_name: str = "workload"):


    # row_count = log.loc[log["org:resource"].isin([resource])].count()
    # pd.Series(0, dtype="Int64")

    log.loc[log["org:resource"].isin([resource]), column_name] = 0

    # print(log.info())

    workload = []
    prev_val = 0

    for row in log.loc[log["org:resource"].isin([resource])].itertuples():
        if (row._6 in ["start", "resume"]):
            prev_val += 1
        elif (row._6 in ["complete", "suspend"]):
            prev_val -= 1
        # print(str(row._6) + "->" + str(prev_val) + "\n" )
        workload.append(prev_val)

    log.loc[log["org:resource"].isin([resource]), column_name] = workload
    # log.loc[log["org:resource"].isin([resource]), column_name] = log.loc[log["org:resource"].isin([
        # resource])].apply(lambda x: print(x.shift(-1)[column_name]), axis=1)
        # resource])].apply(lambda x: print(x.shift(1, fill_value=0, axis=0)["lifecycle:transition"]), axis=1)
        # resource])].apply(lambda x: (x.shift(1)[column_name] + 1) if x["lifecycle:transition"] in ["start", "resume"] else (x.shift(1)[column_name] - 1), axis=1)
    return log
#, log.loc[log["org:resource"].isin([resource])]
