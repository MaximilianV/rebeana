import os
import sys

import timeit

from pm4py.objects.log.importer.parquet import factory as parquet_importer
from pm4py.objects.log.exporter.parquet import factory as parquet_exporter
from utils.plot import plot_attribute
from utils.resources import *
import pandas as pd
from analysis.metrics.MetricManager import MetricManager
from evaluation.Correlation import Correlation
from evaluation.Prediction import Prediction

dataset_path = os.path.join('/workspaces/data/BPIC-17',
                            'BPI_Challenge_2017.parquet')

log = parquet_importer.apply(dataset_path)


# Currently we have to use a multiindex due to duplicates in the timestamps (at least pandas says so)
# log.set_index('time:timestamp', inplace=True, append=True, drop=False)
# log.set_index('time:timestamp', inplace=True, verify_integrity=True, append=True, drop=False)
log.set_index('time:timestamp', inplace=True, drop=False)
log.sort_index(inplace=True)

########################################################################################################

# Filter for Worklow Events only (Offer and Application do not have a duration)
log = log[(log["EventOrigin"] == "Workflow") & log["lifecycle:transition"].isin(
    ["suspend", "complete", "start", "resume"])]
        # ["suspend", "complete", "start", "resume"]) & (log["concept:name"] == 'W_Complete application')]
    # ["suspend", "complete", "start", "resume"]) & (log["concept:name"] != 'W_Call after offers')]

# Has 2 resource change in "W_Complete Application"
# print(log[log["case:concept:name"].isin(["Application_1266995739"])][["Action", "org:resource", "concept:name", "EventOrigin", "EventID", "lifecycle:transition", "OfferID"]])

# resources = get_resources(log, True)
# res20 = get_most_frequent_resources(log, 20)

# exit()

#####################
###### METRICS ######
#####################

metrics = MetricManager()
proc_speed = metrics.get_metric('Processing Speed')
workload = metrics.get_metric('Workload')
daytime = metrics.get_metric('Daytime')

# user_id = "User_135"
# user_id = "User_5"
# user_id = "User_75"
# user_id = "User_2"


# user_id = "User_1"
# user_id = "User_87"
# user_id = "User_3"
# user_id = "User_30"
# user_id = "User_5"
# user_id = "User_100"
# user_id = "User_2"
# user_id = "User_123"
# user_id = "User_29"
# user_id = "User_49"
# user_id = "User_121"
# user_id = "User_68"
# user_id = "User_27"
# user_id = "User_116"
# user_id = "User_28"
# user_id = "User_113"
# user_id = "User_99"
# user_id = "User_41"
# user_id = "User_75"
# user_id = "User_126"

### PROCESSING SPEED ###

# proc_speed.execute_variant('Service Time', log, user_id, max_time=7200, min_time=1)

# log["proc_speed"] = log["proc_speed"].astype("Int64")

# plot_attribute(log, "proc_speed", "proc_speed_u135.png")

# print(log.loc[log["org:resource"].isin([user_id])][[
#        "case:concept:name", "concept:name", "org:resource", "lifecycle:transition", "proc_speed"]].to_string())


### WORKLOAD ###

# workload.execute_variant('Running', log, user_id)
# workload.execute_variant('Eventsum', log, user_id, time_window="30min")


### DAYTIME ###

# daytime.execute_variant('Hour', log, user_id)


# print(log.loc[log["org:resource"].isin([user_id]) & (log["proc_speed"] > 30)][["time:timestamp", "lifecycle:transition", "daytime", "proc_speed", "workload"]].to_string())

res20 = ["User_1", "User_87", "User_3", "User_30", "User_5", "User_100", "User_2", "User_123", "User_29", "User_49",
             "User_121", "User_68", "User_27", "User_116", "User_28", "User_113", "User_99", "User_41", "User_75", "User_126"]

# for res, freq in resources.items():
#     if freq < 10000:
#         print(res + ":" + "PS...", end="")
#         proc_speed.execute_variant('Service Time', log, res)
#         print("WL...", end="")
#         workload.execute_variant('Eventsum', log, res)
#         print("DT...")
#         daytime.execute_variant('Hour', log, res)

for res in res20:
    print(res + ":" + "PS...", end="")
    proc_speed.execute_variant(
        'Service Time', log, res, max_time=7200, min_time=1)
    print("WL...", end="")
    workload.execute_variant('Eventsum', log, res, time_window="30min")
    print("DT...")
    daytime.execute_variant('Hour', log, res)

#     predictor = Prediction(res, log=log.loc[log['org:resource'].isin([res])], export_path='evaluation/results/ml/autorun/')
#     predictor.evaluate(['workload', 'daytime'], 'proc_speed')



# predictor = Prediction(user_id, log=log.loc[log['org:resource'].isin([user_id])], export_path='evaluation/results/case_features/')
# predictor.evaluate(['workload'], 'proc_speed')
# predictor.plot_log(['workload'], 'proc_speed')
# predictor.evaluate(['workload', 'daytime', 'concept:name'], 'proc_speed')
# predictor.evaluate(['concept:name', 'case:RequestedAmount',
#                     'workload', 'daytime'], 'proc_speed')

log.loc[log['org:resource'].isin(res20)].to_parquet(
    'all_wl_ps_dt.parquet', engine='pyarrow')

# print(log.loc[log["org:resource"].isin([user_id])][[
#        "case:concept:name", "concept:name", "org:resource", "lifecycle:transition", "daytime"]].to_string())

# parquet_exporter.apply(log, 'datasets/' + 'tenthousend' + '.parquet')
# parquet_exporter.apply(
#    log.loc[log["org:resource"].isin([user_id])], 'datasets/' + user_id + '.parquet')



# corr = Correlation(log=log.loc[log["org:resource"].isin([user_id])])
# print(corr.compute_correlation('workload', 'proc_speed'))
# corr.show_correlation('workload', 'proc_speed', "BPI17_"  + user_id)
# corr.show_correlation('daytime', 'proc_speed', "BPI17_"  + user_id)

