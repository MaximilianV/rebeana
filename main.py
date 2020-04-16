import os
import sys

import timeit

from pm4py.objects.log.importer.parquet import factory as parquet_importer
from pm4py.objects.log.exporter.parquet import factory as parquet_exporter
from utils.plot import plot_attribute
from utils.resources import *
import pandas as pd
from extraction.Extraction import Extraction
from visualisation.Visualiser import Visualiser
from analysis.Correlation import Correlation
from analysis.Regression import Regression
from utils.Configuration import Configuration

# from evaluation.Prediction import Prediction

# dataset_path = os.path.join('/workspaces/data/BPIC-17',
#                             'BPI_Challenge_2017.parquet')
dataset_path = os.path.join('all_wl30min_psInSecMax7200_dt.parquet')

ALREADY_ANALYSED = True

log = parquet_importer.apply(dataset_path)

OUTPUT_PATH = "results/"

# Currently we have to use a multiindex due to duplicates in the timestamps (at least pandas says so)
# log.set_index('time:timestamp', inplace=True, append=True, drop=False)
# log.set_index('time:timestamp', inplace=True, verify_integrity=True, append=True, drop=False)
if not ALREADY_ANALYSED:
    log.set_index('time:timestamp', inplace=True, drop=False)
    log.sort_index(inplace=True)

########################################################################################################

# Filter for Worklow Events only (Offer and Application do not have a duration)
    log = log[(log["EventOrigin"] == "Workflow") & log["lifecycle:transition"].isin(
        ["suspend", "complete", "start", "resume"])]


######################
####### CONFIG #######
######################

execution = Configuration('Test', log=log)

execution.resources = get_most_frequent_resources(execution.log, 20)
# execution.resources = ['User_87']

# execution.activities = ['W_Validate application']
execution.activities = ['W_Complete application']
# execution.activities = ['W_Call incomplete files']

execution.input_metrics = ['Workload']
# execution.input_metrics = ['Workload', 'Daytime']
execution.output_metrics = ['Processing Speed']
execution.metric_configurations = {
    'Workload': {
        'variant': 'Eventsum',
        'configuration': {
            'time_window': '30min'
        }
    },
    'Daytime': {
        'variant': 'Hour'
    },
    'Processing Speed': {
        'variant': 'Service Time',
        'column': 'proc_speed',
        'configuration': {
            'max_time': 7200,
            'min_time': 1
        }
    }
}


######################
##### EXTRACTION #####
######################

if not ALREADY_ANALYSED:
    Extraction.extract_metrics(execution)
    # print(execution.log[execution.log["org:resource"].isin(execution.resources)][["time:timestamp", "case:concept:name", "concept:name", "lifecycle:transition", "org:resource", "daytime", "proc_speed", "workload"]].to_string())


######################
###### ANALYSIS ######
######################

# print(log[log['org:resource'].isin(execution.resources)]['concept:name'].value_counts())


correlation = Correlation(execution)
correlation.compute_correlation()

execution.correlation = correlation.result

regression = Regression(execution)

execution.regression = regression.linear_regression()

###########################
###### VISUALISATION ######
###########################

visualiser = Visualiser(execution)

visualiser.boxPlots()
visualiser.visualiseCorrelation()
visualiser.scatterPlots()

print("##### CURRENT ID: ", execution.id)

execution.save_configuration()





# predictor = Prediction(user_id, log=log.loc[log['org:resource'].isin([user_id])], export_path='evaluation/results/case_features/')
# predictor.evaluate(['workload'], 'proc_speed')
# predictor.plot_log(['workload'], 'proc_speed')
# predictor.evaluate(['workload', 'daytime', 'concept:name'], 'proc_speed')
# predictor.evaluate(['concept:name', 'case:RequestedAmount',
#                     'workload', 'daytime'], 'proc_speed')

# log.loc[log['org:resource'].isin(res20)].to_parquet(
#     'all_wl_ps_dt.parquet', engine='pyarrow')


# parquet_exporter.apply(log, 'datasets/' + 'tenthousend' + '.parquet')
# parquet_exporter.apply(
#    log.loc[log["org:resource"].isin([user_id])], 'datasets/' + user_id + '.parquet')


