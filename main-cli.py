from pm4py.objects.log.importer.parquet import factory as parquet_importer
import questionary
import glob
import os
import sys

import timeit

from pm4py.objects.log.exporter.parquet import factory as parquet_exporter

from extraction.Extraction import Extraction
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
    print("2017")
    log = log[(log["EventOrigin"] == "Workflow") & log["lifecycle:transition"].isin(
        ["suspend", "complete", "start", "resume"])]
if (dataset_path == "/workspaces/data/BPIC-12/BPI_Challenge_2012.parquet"):
    print("2012")
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



