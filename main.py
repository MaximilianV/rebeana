import os

from pm4py.objects.log.importer.parquet import factory as parquet_importer
from utils.resources import *

log = parquet_importer.apply(dataset_path)

print(get_most_frequent_resources(log, 5, True))
