import os
import sys

import timeit

from pm4py.objects.log.importer.parquet import factory as parquet_importer
from pm4py.objects.log.exporter.parquet import factory as parquet_exporter
from utils.plot import plot_attribute
from utils.resources import *
import pandas as pd
from analysis.metrics.MetricManager import MetricManager

dataset_path = os.path.join('/workspaces/data/BPIC-17',
                            'BPI_Challenge_2017.parquet')

# log = parquet_importer.apply(dataset_path)
log = parquet_importer.apply('u5_ps_wl.parquet')

# Currently we have to use a multiindex due to duplicates in the timestamps (at least pandas says so)
# log.set_index('time:timestamp', inplace=True, append=True, drop=False)
# log.set_index('time:timestamp', inplace=True, verify_integrity=True, append=True, drop=False)
# log.set_index('time:timestamp', inplace=True, drop=False)
# log.sort_index(inplace=True)


##################################################################

log.dropna(inplace=True, subset=["proc_speed", "workload"])

print(log.info())

print(log['workload'].corr(log['proc_speed']))

exit()
###################################################################

# Filter for Worklow Events only (Offer and Application do not have a duration)
log = log[log["EventOrigin"] == "Workflow"]

# Has 2 resource change in "W_Complete Application"
# print(log[log["case:concept:name"].isin(["Application_1266995739"])][["Action", "org:resource", "concept:name", "EventOrigin", "EventID", "lifecycle:transition", "OfferID"]])

metrics = MetricManager()
print(metrics.get_available_metrics())

# print(get_resources(log, True))
# print(get_most_frequent_resources(log, 5, True))

# exit()

# user_id = "User_135"
user_id = "User_5"

########################
### PROCESSING SPEED ###
########################

proc_speed = metrics.get_metric('Processing Speed')
proc_speed.execute_variant('Service Time', log, user_id)

# plot_attribute(log, "proc_speed", "proc_speed_u135.png")

# print(log.loc[log["org:resource"].isin([user_id])][[
#        "case:concept:name", "concept:name", "org:resource", "lifecycle:transition", "proc_speed"]].to_string())


################
### WORKLOAD ###
################

workload = metrics.get_metric('Workload')
workload.execute_variant('Eventsum', log, user_id)

parquet_exporter.apply(
    log.loc[log["org:resource"].isin([user_id])], 'u5_ps_wl.parquet')


