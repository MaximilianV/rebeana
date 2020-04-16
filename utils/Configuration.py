from typing import List, Dict
from pm4py.objects.log.importer.parquet import factory as parquet_importer
import uuid
import pandas as pd
from utils.utils import name_to_module
from analysis.CorrelationResult import CorrelationResult


class Configuration:
    # Step 1:
    name: str
    log: pd.DataFrame
    # Step 2:
    resources: List[str] = []
    activities: List[str] = []
    input_metrics: List[str] = []
    output_metrics: List[str] = []
    metric_configurations: Dict = {}
    # Step 3:
    correlation: CorrelationResult
    regression: Dict = {}

    def __init__(self, name, file: str = None, log: pd.DataFrame = None):
        if (file is None and log is None) or (file is not None and log is not None):
            raise Exception(
                "You must either provide a file to load or pass a log object.")
        if file:
            self.log = parquet_importer.apply(file)
        else:
            self.log = log

        self.name: str = name
        self.id: str = str(uuid.uuid4())

    def get_all_metrics(self) -> List[str]:
        return self.input_metrics + self.output_metrics

    def __str__(self):
        return self.id

    def save_configuration(self):
        f = open("results/" + self.id + ".txt", "w")
        f.writelines([line + "\n" for line in [
            "Configuration #" + self.id,
            "",
            "Resource:\t" + str(self.resources),
            "Activities:\t" + str(self.activities),
            "",
            "Inputs:\t\t" + str(self.input_metrics),
            "Outputs:\t" + str(self.output_metrics),
            ""
        ]])
        f.write("#############################################################################\n")
        f.write("##### REGRESSION RESULTS ######\n")
        for regression in self.regression:
            f.write("###" + regression + "\n")
            f.write(str(self.regression[regression].summary()) + "\n")
        f.write("#############################################################################\n")
        f.close()


    # ACCESS METHODS FOR LOG AND COLUMN NAMES
    def get_input_columns(self) -> List[str]:
        return list(map(self.get_column_for_metric, self.input_metrics))

    def get_output_columns(self) -> List[str]:
        return list(map(self.get_column_for_metric, self.output_metrics))

    def get_filtered_log(self, include_activities=False) -> pd.DataFrame:
        metrics_columns = self.get_input_columns() + self.get_output_columns()
        filtered_log = self.log
        if len(self.activities) > 0:
            filtered_log = filtered_log[filtered_log["concept:name"].isin(self.activities)]
        if len(self.resources) > 0:
            filtered_log = filtered_log[filtered_log["org:resource"].isin(self.resources)]

        if include_activities:
            metrics_columns.append("concept:name")
        filtered_log = filtered_log[metrics_columns].copy()
        filtered_log.dropna(inplace=True)
        return filtered_log


    # ACCESS METRIC CONFIGURATION
    def get_metric_configuration(self, metric) -> Dict:
        return self.metric_configurations[metric]

    def is_metric_attribute(self, metric) -> bool:
        return ('is_attribute' in self.get_metric_configuration(metric))

    def get_column_for_metric(self, metric) -> str:
        if 'column' in self.metric_configurations[metric]:
            return self.metric_configurations[metric]['column']
        else:
            return name_to_module(metric)

    def get_variant_for_metric(self, metric) -> str:
        return self.metric_configurations[metric]['variant']

    def get_variant_configuration(self, metric) -> Dict:
        if 'configuration' in self.metric_configurations[metric]:
            return self.metric_configurations[metric]['configuration']
        return {}
