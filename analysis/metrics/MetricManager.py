import os
import sys

import toml

from analysis.metrics.Metric import Metric


class MetricManager:
    metrics: dict = {}
    plugin_path = ""

    def __init__(self, plugin_dir=os.path.dirname(__file__)):
        self.plugin_path = plugin_dir
        # Add metric/plugin path to sys path to allow importing them as modules
        sys.path.append(self.plugin_path)
        self.load_metrics()

    def load_metrics(self):
        self.metrics = {}
        dir_list = next(os.walk(self.plugin_path))[1]
        for dir in dir_list:
            self._load_metric(dir)

    def _load_metric(self, dir: str):
        if (dir == "__pycache__"):
            return

        absolute_path = os.path.join(self.plugin_path, dir)
        try:
            configuration = toml.load(
                os.path.join(absolute_path, dir + ".toml"))
            self.metrics[configuration["name"]] = Metric(configuration)
        except FileNotFoundError:
            print("Directory \"" + dir +
                  "\" does not contain a configuration file for a metric! It will not be imported.")
        except toml.TomlDecodeError as msg:
            print("Configuration file for \"" + dir +
                  "\" could not be read. Please check it for syntax errors:")
            print(msg)

    def available_metrics(self):
        return self.metrics.keys()

    def get_metric(self, metric_name: str) -> Metric:
        try:
            return self.metrics[metric_name]
        except KeyError:
            print("The metric \"" + metric_name + "\" is not defined.")
            print("Maybe try reloading the metrics directory?")
            raise
