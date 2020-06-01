from pm4py.objects.log.importer.parquet import factory as parquet_importer
import questionary
import glob
import os
import sys

import timeit

from pm4py.objects.log.exporter.parquet import factory as parquet_exporter

from extraction.Extraction import Extraction
from extraction.metrics.MetricManager import MetricManager
from visualisation.Visualiser import Visualiser
from analysis.Correlation import Correlation
from analysis.Regression import Regression
from utils.Configuration import Configuration
from utils.resources import *



OUTPUT_PATH = "results/"

def print_step_separator():
    print("\n")

###############################
#### STEP 1: GET DATASETS #####
###############################
print_step_separator()

f = glob.glob("/workspaces/data/**/*.parquet")
# f = f + glob.glob("/workspaces/data/**/*.xes")
# f = f + glob.glob("/workspaces/data/**/*.xml")

dataset_path = questionary.select(
    'Please select an event log to analyse.',
    f
).ask()


print("\nLoading Log...")
log = parquet_importer.apply(dataset_path)
print("Loading finished.")

log.set_index('time:timestamp', inplace=True, drop=False)
log.sort_index(inplace=True)

if (dataset_path == "/workspaces/data/BPIC-17/BPI_Challenge_2017.parquet"):
    log = log[(log["EventOrigin"] == "Workflow") & log["lifecycle:transition"].isin(
        ["suspend", "complete", "start", "resume"])]
if (dataset_path == "/workspaces/data/BPIC-12/BPI_Challenge_2012.parquet"):
    log = log[log["concept:name"].isin(['W_Completeren aanvraag', 'W_Afhandelen leads', 'W_Nabellen offertes', 'W_Beoordelen fraude', 'W_Valideren aanvraag', 'W_Nabellen incomplete dossiers', 'W_Wijzigen contractgegevens'])]

experiment = Configuration('Test', log=log)

#################################
#### STEP 2: SELECT RESOURCE ####
#################################
print_step_separator()

single_user = questionary.confirm("Do you want to analyse a specific resource? Otherwise, the 20 most frequent are analysed.").ask()

if (single_user):
    users = [questionary.text("Enter resources to analyse:").ask()]
else:
    users = get_most_frequent_resources(log, 20)

experiment.resources = users

print("Users selected for analysis:")
print(users)

#################################
#### STEP 2: SELECT ACTIVITY ####
#################################
print_step_separator()

single_activity = questionary.confirm("Do you want to analyse a specific activities?").ask()


if (single_activity):
    df_list_of_activities = log["concept:name"].value_counts()
    list_of_activities = []
    for index, value in df_list_of_activities.items():
        list_of_activities.append(f"{index} ({value})")
    raw_activities = questionary.checkbox(
        "Select activities to analyse:",
        list_of_activities
    ).ask()

    activities = []
    for activity in raw_activities:
        activities.append(activity.split(" (")[0])

    print("Activities selected for analysis:")
    print(activities)
    experiment.activities = activities


#################################
#### STEP 3: SELECT METRICS #####
#################################
print_step_separator()

print("Loading metrics...")
metricManager = MetricManager()
print("Loading finished...")

print_step_separator()

av_env_metrics = metricManager.get_environmental_metrics()
av_beh_metrics = metricManager.get_behavioural_metrics()

env_metrics = questionary.checkbox(
    "Select the environmental metrics:",
    av_env_metrics
).ask()

experiment.input_metrics = env_metrics
print_step_separator()

beh_metrics = questionary.checkbox(
    "Select the behavioural metrics:",
    av_beh_metrics
).ask()

experiment.output_metrics = beh_metrics

print_step_separator()
print("Configure metrics:")

for metric in env_metrics + beh_metrics:
    metric_config = dict()
    metric_object = metricManager.get_metric(metric)
    av_variants = metric_object.get_variants()
    av_variant = questionary.select(
        f"Select a variant for metric \"{metric}\"",
        av_variants
    ).ask()
    metric_config["variant"] = av_variant

    configuration = metric_object.get_variant_configuration(av_variant)
    if (not configuration):
        print("There is nothing to configure for this variant.")
    else:
        metric_config["configuration"] = dict()
        for config in configuration:
            config_value = questionary.text(
                f"Provide a value for the {config['name']} (default: {config['default']}).\n{config['description']}\nLeave empty for default:"
            ).ask()
            if (config_value == ""):
                config_value = config["default"]
            metric_config["configuration"][config["key"]] = config_value
            print(f"Set {config['name']} to {config_value}.")

    experiment.metric_configurations[metric] = metric_config

    print_step_separator()

# print(experiment.metric_configurations)

######################
##### EXTRACTION #####
######################

print("Extracting metrics...")

Extraction.extract_metrics(experiment)

print("Finished extraction.")

######################
###### ANALYSIS ######
######################
print_step_separator()

# CORRELATION
print("Computing correlation...")

correlation = Correlation(experiment)
correlation.compute_correlation()
experiment.correlation = correlation.result

print("Finished correlation analysis.")


# REGRESSION
print("Computing regression...")

regression = Regression(experiment)
experiment.regression = regression.linear_regression()

print("Finished regression analysis.")

###########################
###### VISUALISATION ######
###########################
print_step_separator()

print("Starting visualisation...")

visualiser = Visualiser(experiment)

visualiser.boxPlots()
visualiser.visualiseCorrelation()
visualiser.scatterPlots()

print("Finished visualisation.")


#################
###### SAVE #####
#################
print_step_separator()

experiment.save_configuration()

print("Your experiment's results are ready!")
print("Please refer to the following experiment ID:")
print(experiment.id)
