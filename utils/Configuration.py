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
    input_metrics: List[str] = []
    output_metrics: List[str] = []
    metric_configurations: Dict = {}
    # Step 3:
    correlation: CorrelationResult
    regression: str = None

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

    def get_input_columns(self) -> List[str]:
        return list(map(self.get_column_for_metric, self.input_metrics))

    def get_output_columns(self) -> List[str]:
        return list(map(self.get_column_for_metric, self.output_metrics))

    # ACCESS METRIC CONFIGURATION
    def get_metric_configuration(self, metric) -> Dict:
        return self.metric_configurations[metric]

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
