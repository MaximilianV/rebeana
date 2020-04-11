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


# resources = get_resources(log, True)
# res20 = get_most_frequent_resources(log, 20)

#####################
###### METRICS ######
#####################

metrics = MetricManager()
proc_speed = metrics.get_metric('Processing Speed')
workload = metrics.get_metric('Workload')
daytime = metrics.get_metric('Daytime')


### PROCESSING SPEED ###
# proc_speed.execute_variant('Service Time', log, user_id, max_time=7200, min_time=1)
# log["proc_speed"] = log["proc_speed"].astype("Int64")


### WORKLOAD ###
# workload.execute_variant('Running', log, user_id)
# workload.execute_variant('Eventsum', log, user_id, time_window="30min")


### DAYTIME ###
# daytime.execute_variant('Hour', log, user_id)



# for res, freq in resources.items():
#     if freq < 10000:
#         print(res + ":" + "PS...", end="")
#         proc_speed.execute_variant('Service Time', log, res, max_time=7200, min_time=1)
#         print("WL...", end="")
#         workload.execute_variant('Eventsum', log, res, time_window="30min")
#         print("DT...")
#         daytime.execute_variant('Hour', log, res)




# predictor = Prediction(user_id, log=log.loc[log['org:resource'].isin([user_id])], export_path='evaluation/results/case_features/')
# predictor.evaluate(['workload'], 'proc_speed')
# predictor.plot_log(['workload'], 'proc_speed')
# predictor.evaluate(['workload', 'daytime', 'concept:name'], 'proc_speed')
# predictor.evaluate(['concept:name', 'case:RequestedAmount',
#                     'workload', 'daytime'], 'proc_speed')

log.loc[log['org:resource'].isin(res20)].to_parquet(
    'all_wl_ps_dt.parquet', engine='pyarrow')


# parquet_exporter.apply(log, 'datasets/' + 'tenthousend' + '.parquet')
# parquet_exporter.apply(
#    log.loc[log["org:resource"].isin([user_id])], 'datasets/' + user_id + '.parquet')



# corr = Correlation(log=log.loc[log["org:resource"].isin([user_id])])
# print(corr.compute_correlation('workload', 'proc_speed'))
# corr.show_correlation('workload', 'proc_speed', "BPI17_"  + user_id)
# corr.show_correlation('daytime', 'proc_speed', "BPI17_"  + user_id)
