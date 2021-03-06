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

dataset_path = os.path.join('/workspaces/data/BPIC-17',
                            'BPI_Challenge_2017.parquet')
# dataset_path = os.path.join('/workspaces/data/BPIC-12',
                            # 'BPI_Challenge_2012.parquet')
# dataset_path = os.path.join('all_wl30min_psInSecMax7200_dt.parquet')
# dataset_path = os.path.join('top20_wl30min_psInSecMax7200_dt_bpi12.parquet')

ALREADY_ANALYSED = False

log = parquet_importer.apply(dataset_path)


# print(log["concept:name"].value_counts())
# print(get_resources(log, as_dict=True))
# exit()

OUTPUT_PATH = "results/"

# Currently we have to use a multiindex due to duplicates in the timestamps (at least pandas says so)
# log.set_index('time:timestamp', inplace=True, append=True, drop=False)
# log.set_index('time:timestamp', inplace=True, verify_integrity=True, append=True, drop=False)
if not ALREADY_ANALYSED:
    log.set_index('time:timestamp', inplace=True, drop=False)
    log.sort_index(inplace=True)


    # Filter for Worklow Events only (Offer and Application do not have a duration)
    # BPIC-17
    log = log[(log["EventOrigin"] == "Workflow") & log["lifecycle:transition"].isin(
        ["suspend", "complete", "start", "resume"])]

    # BPIC-12
    # log = log[log["concept:name"].isin(['W_Completeren aanvraag', 'W_Afhandelen leads', 'W_Nabellen offertes', 'W_Beoordelen fraude', 'W_Valideren aanvraag', 'W_Nabellen incomplete dossiers', 'W_Wijzigen contractgegevens'])]
# log = log[(log["case:RequestedAmount"] <= 50000)]
#  & (log["proc_speed"] <= 2000) & (log["workload"] <= 60) & (log["proc_speed"] >= 120)

# log = log[((log["proc_speed"] >= 1000))]


######################
####### CONFIG #######
######################

execution = Configuration('Test', log=log)

# execution.resources = get_most_frequent_resources(execution.log, 20)
execution.resources = ['User_9']
# execution.resources = ['User_9', 'User_132', 'User_89', 'User_139']

# BPI 12
# execution.activities = ['W_Afhandelen leads']
# execution.activities = ['W_Nabellen offertes']
# execution.activities = ['W_Nabellen incomplete dossiers']
# execution.activities = ['W_Completeren aanvraag']
# execution.activities = ['W_Valideren aanvraag']
# execution.activities = ['W_Nabellen incomplete dossiers']

# BPI 17
# execution.activities = ['W_Validate application']
# execution.activities = ['W_Complete application']
# execution.activities = ['W_Call incomplete files']
execution.activities = ['W_Call after offers']
# execution.activities = ['W_Handle leads']
# execution.activities = ['W_Call after offers','W_Call incomplete files','W_Complete application']

# execution.input_metrics = ['Workload', 'Amount', 'Daytime']
execution.input_metrics = ['Workload', 'Daytime']
execution.output_metrics = ['Processing Speed']
execution.metric_configurations = {
    'Workload': {
        'variant': 'Eventsum',
        'configuration': {
            'time_window': '3h'
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
    },
    'Amount': {
        'column': 'case:RequestedAmount',
        'is_attribute': True
    }
}




######################
##### EXTRACTION #####
######################

if not ALREADY_ANALYSED:
    Extraction.extract_metrics(execution)
    # print(execution.log[execution.log["org:resource"].isin(execution.resources)][["time:timestamp", "case:concept:name", "concept:name", "lifecycle:transition", "org:resource", "daytime", "proc_speed", "workload"]].to_string())

# print(log[log['org:resource'].isin(execution.resources)]['concept:name'].value_counts())

######################
###### ANALYSIS ######
######################

# CORRELATION
correlation = Correlation(execution)
correlation.compute_correlation()
execution.correlation = correlation.result

# REGRESSION
regression = Regression(execution)
execution.regression = regression.linear_regression()

###########################
###### VISUALISATION ######
###########################

visualiser = Visualiser(execution)

visualiser.boxPlots()
visualiser.visualiseCorrelation()
visualiser.scatterPlots()


#################
###### SAVE #####
#################

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


